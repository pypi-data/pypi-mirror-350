from __future__ import annotations

import abc
from typing import Any, Callable, Sequence, cast

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import rasterio.features
import xarray as xr
from numpy.typing import DTypeLike
from odc.geo.geobox import GeoBox

from mccn._types import (
    DType_Map_T,
    Dtype_T,
    MergeMethod_Map_T,
    MergeMethod_T,
    Nodata_Map_T,
    Nodata_T,
    Number_T,
)
from mccn.loader.utils import (
    coords_from_geobox,
    query_by_key,
    query_if_null,
)


class Drawer(abc.ABC):
    def __init__(
        self,
        x_coords: np.ndarray,
        y_coords: np.ndarray,
        dtype: Dtype_T = "float64",
        nodata: Nodata_T = 0,
        **kwargs: Any,
    ) -> None:
        # Set up xarray dimensions and shape
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.shape = [len(y_coords), len(x_coords)]
        # Set up drawer parameters
        self.dtype = dtype
        self.nodata = nodata
        # Date index for quick query
        self.data: dict[Any, np.ndarray] = {}
        # Post init hooks
        self.__post_init__(kwargs)

    @property
    def nbytes(self) -> int:
        return sum([arr.nbytes for arr in self.data.values()])

    def _alloc(self, dtype: DTypeLike, fill_value: Nodata_T) -> np.ndarray:
        return np.full(shape=self.shape, fill_value=fill_value, dtype=dtype)

    def alloc(self) -> np.ndarray:
        return self._alloc(self.dtype, self.nodata)

    def __post_init__(self, kwargs: Any) -> None: ...

    def draw(self, t_value: Any, layer: np.ndarray) -> None:
        if t_value not in self.data:
            self.data[t_value] = self.alloc()
        valid_mask = self.valid_mask(layer)
        nodata_mask = self.data[t_value] == self.nodata
        self._draw(t_value, layer, valid_mask, nodata_mask)

    @abc.abstractmethod
    def _draw(
        self,
        t_value: Any,
        layer: np.ndarray,
        valid_mask: Any,
        nodata_mask: Any,
    ) -> None:
        self.data[t_value][nodata_mask & valid_mask] = layer[nodata_mask & valid_mask]

    @abc.abstractmethod
    def _draw_point(
        self, t_value: Any, y_value: int, x_value: int, value: Number_T
    ) -> None:
        raise NotImplementedError

    def draw_point(
        self, t_value: Any, y_value: int, x_value: int, value: Number_T
    ) -> None:
        if t_value not in self.data:
            self.data[t_value] = self.alloc()
        if not (0 <= y_value < self.shape[0] and 0 <= x_value < self.shape[1]):
            raise ValueError(f"Out of bound: {y_value, x_value, self.shape}")
        if value != self.nodata and not np.isnan(value):
            if self.data[t_value][y_value, x_value] == self.nodata or np.isnan(
                self.data[t_value][y_value, x_value]
            ):
                self.data[t_value][y_value, x_value] = value
            else:
                self._draw_point(t_value, y_value, x_value, value)

    def valid_mask(self, layer: np.ndarray) -> Any:
        return (layer != self.nodata) & ~(np.isnan(layer))


class SumDrawer(Drawer):
    def _draw(
        self,
        t_value: Any,
        layer: np.ndarray,
        valid_mask: Any,
        nodata_mask: Any,
    ) -> None:
        super()._draw(t_value, layer, valid_mask, nodata_mask)
        self.data[t_value][valid_mask & ~nodata_mask] += layer[
            valid_mask & ~nodata_mask
        ]

    def _draw_point(
        self, t_value: Any, y_value: int, x_value: int, value: Number_T
    ) -> None:
        self.data[t_value][y_value, x_value] += value


class MinMaxDrawer(Drawer):
    def __init__(self, is_max: bool = True, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.is_max = is_max
        self.op = np.maximum if is_max else np.minimum

    def _draw(
        self,
        t_value: Any,
        layer: np.ndarray,
        valid_mask: Any,
        nodata_mask: Any,
    ) -> None:
        super()._draw(t_value, layer, valid_mask, nodata_mask)
        data = self.data[t_value]
        data = self.op(layer, data, out=data, where=valid_mask & ~nodata_mask)
        self.data[t_value] = data

    def _draw_point(
        self, t_value: Any, y_value: int, x_value: int, value: Number_T
    ) -> None:
        self.data[t_value][y_value, x_value] = self.op(
            value, self.data[t_value][y_value, x_value]
        )


class MinDrawer(MinMaxDrawer):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(is_max=False, **kwargs)


class MaxDrawer(MinMaxDrawer):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(is_max=True, **kwargs)


class MeanDrawer(Drawer):
    def __post_init__(self, kwargs: Any) -> None:
        self.count: dict[Any, np.ndarray] = {}

    def draw(self, t_value: Any, layer: np.ndarray) -> None:
        if t_value not in self.count:
            self.count[t_value] = self._alloc(dtype="uint8", fill_value=0)
        super().draw(t_value, layer)

    def _draw(
        self,
        t_value: Any,
        layer: np.ndarray,
        valid_mask: Any,
        nodata_mask: Any,
    ) -> None:
        data = self.data[t_value]
        count = self.count[t_value]
        data[count > 0] = data[count > 0] * count[count > 0]
        data[nodata_mask & valid_mask] = layer[nodata_mask & valid_mask]
        data[~nodata_mask & valid_mask] += layer[~nodata_mask & valid_mask]
        count[valid_mask] += 1
        data[count > 0] = data[count > 0] / count[count > 0]
        self.count[t_value] = count
        self.data[t_value] = data

    def draw_point(
        self, t_value: Any, y_value: int, x_value: int, value: Number_T
    ) -> None:
        if t_value not in self.count:
            self.count[t_value] = self._alloc(dtype="uint8", fill_value=0)
        if t_value not in self.data:
            self.data[t_value] = self.alloc()
        if not (0 <= y_value < self.shape[0] and 0 <= x_value < self.shape[1]):
            raise ValueError(f"Out of bound: {y_value, x_value, self.shape}")
        if value != self.nodata and not np.isnan(value):
            if self.data[t_value][y_value, x_value] == self.nodata or np.isnan(
                self.data[t_value][y_value, x_value]
            ):
                self.count[t_value][y_value, x_value] += 1
                self.data[t_value][y_value, x_value] = value
            else:
                self._draw_point(t_value, y_value, x_value, value)

    def _draw_point(
        self, t_value: Any, y_value: int, x_value: int, value: Number_T
    ) -> None:
        count = self.count[t_value][y_value, x_value]
        data = self.data[t_value][y_value, x_value]
        self.count[t_value][y_value, x_value] += 1
        self.data[t_value][y_value, x_value] = (data * count + value) / (count + 1)


class ReplaceDrawer(Drawer):
    def _draw_point(
        self, t_value: Any, y_value: int, x_value: int, value: Number_T
    ) -> None:
        self.data[t_value][y_value, x_value] = value

    def _draw(
        self,
        t_value: Any,
        layer: np.ndarray,
        valid_mask: Any,
        nodata_mask: Any,
    ) -> None:
        self.data[t_value][valid_mask] = layer[valid_mask]


DRAWERS: dict[MergeMethod_T | str, type[Drawer]] = {
    "mean": MeanDrawer,
    "max": MaxDrawer,
    "min": MinDrawer,
    "replace": ReplaceDrawer,
    "sum": SumDrawer,
}


class Canvas:
    def __init__(
        self,
        x_coords: np.ndarray,
        y_coords: np.ndarray,
        x_dim: str = "x",
        y_dim: str = "y",
        t_dim: str = "t",
        spatial_ref: xr.DataArray | None = None,
        spatial_ref_dim: str = "spatial_ref",
        dtype: DType_Map_T = None,
        dtype_fallback: Dtype_T = "float64",
        nodata: Nodata_Map_T = 0,
        nodata_fallback: Nodata_T = 0,
        is_sorted: bool = False,
        merge: MergeMethod_Map_T = None,
        merge_fallback: MergeMethod_T = "replace",
    ) -> None:
        self.spatial_ref = spatial_ref
        self.x_coords = self._sort_coord(x_coords, is_sorted)
        self.y_coords = self._sort_coord(y_coords, is_sorted)
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.t_dim = t_dim
        self.spatial_ref_dim = spatial_ref_dim
        # Cube parameters
        self.dims = (self.t_dim, self.y_dim, self.x_dim)
        self.dtype = dtype
        self.dtype_fallback = dtype_fallback
        self.nodata = nodata
        self.nodata_fallback = nodata_fallback
        self.is_sorted = is_sorted
        self.merge = merge
        self.merge_fallback = merge_fallback
        self._drawers: dict[str, Drawer] = {}
        self._t_coords = np.array([])
        self._t_set: set[Any] = set()
        self._time_sorted: bool = False

    def get_drawer(self, band: str) -> Drawer:
        return self._drawers[band]

    @property
    def t_coords(self) -> np.ndarray:
        if not self._time_sorted:
            self._t_coords = np.array(sorted(self._t_set))
            self._time_sorted = True
        return self._t_coords

    @property
    def shape(self) -> tuple[int, int, int]:
        return (len(self.t_coords), len(self.y_coords), len(self.x_coords))

    @property
    def coords(self) -> dict[str, Any]:
        return {
            self.y_dim: self.y_coords,
            self.x_dim: self.x_coords,
            self.spatial_ref_dim: self.spatial_ref,
            self.t_dim: self.t_coords,
        }

    @property
    def nbytes(self) -> int:
        return sum([drawer.nbytes for drawer in self._drawers.values()])

    def _sort_coord(self, coords: np.ndarray, is_sorted: bool) -> np.ndarray:
        if not is_sorted:
            coords = np.sort(coords)
        return coords

    def has_band(self, band: str) -> bool:
        return band in self._drawers

    def get_method(
        self, band: str, merge: MergeMethod_T | None = None
    ) -> MergeMethod_T:
        return query_if_null(merge, band, self.merge, self.merge_fallback)

    def get_dtype(self, band: str, dtype: Dtype_T | None = None) -> Dtype_T:
        return cast(
            Dtype_T, query_if_null(dtype, band, self.dtype, self.dtype_fallback)
        )

    def get_nodata(self, band: str, nodata: Nodata_T | None = None) -> Nodata_T:
        return query_if_null(nodata, band, self.nodata, self.nodata_fallback)

    def add_band(
        self,
        band: str,
        merge: MergeMethod_T | None = None,
        dtype: Dtype_T | None = None,
        nodata: Nodata_T | None = None,
    ) -> None:
        if band not in self._drawers:
            _method = self.get_method(band, merge)
            _nodata = self.get_nodata(band, nodata)
            _dtype = self.get_dtype(band, dtype)
            handler = DRAWERS[_method]
            self._drawers[band] = handler(
                self.x_coords,
                self.y_coords,
                _dtype,
                _nodata,
            )

    def draw(self, t_value: Any, band: str, layer: np.ndarray) -> None:
        if band not in self._drawers:
            raise KeyError(f"Unallocated band: {band}")
        # Mark time columns as dirty
        if t_value not in self._t_set:
            self._t_set.add(t_value)
            self._time_sorted = False
        drawer = self._drawers[band]
        drawer.draw(t_value, layer)

    def compile_data_vars(self) -> dict[str, tuple[tuple[str, str, str], np.ndarray]]:
        data_vars: dict[str, tuple[tuple[str, str, str], np.ndarray]] = {}
        for band, drawer in self._drawers.items():
            layers = np.stack(
                [drawer.data.get(time, drawer.alloc()) for time in self.t_coords],
                axis=0,
            )
            data_vars[band] = (self.dims, layers)
        return data_vars

    def compile(self, attrs: dict[str, Any]) -> xr.Dataset:
        data_vars = self.compile_data_vars()
        return xr.Dataset(
            data_vars=data_vars,
            coords=self.coords,
            attrs=attrs,
        )

    @classmethod
    def from_geobox(
        cls,
        x_dim: str,
        y_dim: str,
        t_dim: str,
        spatial_ref_dim: str,
        geobox: GeoBox,
        dtype: DType_Map_T,
        dtype_fallback: Dtype_T,
        nodata: Nodata_Map_T,
        nodata_fallback: Nodata_T,
        merge: MergeMethod_Map_T,
        merge_fallback: MergeMethod_T,
    ) -> Canvas:
        coords = coords_from_geobox(geobox, x_dim, y_dim)
        x_coords = coords[x_dim].values
        y_coords = coords[y_dim].values
        spatial_ref = coords[spatial_ref_dim]

        return Canvas(
            x_coords,
            y_coords,
            x_dim,
            y_dim,
            t_dim,
            spatial_ref,
            spatial_ref_dim,
            dtype,
            dtype_fallback,
            nodata,
            nodata_fallback,
            True,
            merge,
            merge_fallback,
        )


class Rasteriser:
    def __init__(
        self,
        canvas: Canvas,
        **kwargs: Any,
    ) -> None:
        self.attrs: dict[str, dict[int, Any]] = {}
        self.rev_attrs: dict[str, dict[Any, int]] = {}
        self.keys: dict[str, int] = {}
        self.canvas = canvas
        self.t_dim = self.canvas.t_dim

    def encode(self, series: pd.Series, nodata: int, band: str) -> pd.Series:
        if band not in self.attrs:
            self.attrs[band] = {nodata: "nodata"}
            self.rev_attrs[band] = {"nodata": nodata}
            curr = 0 if nodata != 0 else 1
        else:
            curr = self.keys[band]
        # Update attr map and rev attrs map
        for name in series.unique():
            if curr == nodata:
                curr += 1
            if name not in self.rev_attrs[band]:
                self.attrs[band][curr] = name
                self.rev_attrs[band][name] = curr
                curr += 1
        # Set key
        self.keys[band] = curr
        # Attr dict - mapped value -> original
        series = series.map(self.rev_attrs[band])
        return series

    def handle_categorical(self, series: pd.Series, band: str) -> pd.Series:
        nodata = self.canvas.get_nodata(band)
        dtype = cast(Dtype_T, query_by_key(band, self.canvas.dtype, "int8"))
        try:
            nodata = int(nodata)
        except ValueError:
            raise ValueError(
                f"nodata value for categorical band ({band}) must be integers or int-convertible. Received: {nodata}"
            )
        series = self.encode(series, nodata, band)
        if not self.canvas.has_band(band):
            self.canvas.add_band(band, merge="replace", dtype=dtype, nodata=nodata)
        return series

    def handle_numeric(self, series: pd.Series, band: str) -> pd.Series:
        if not self.canvas.has_band(band):
            self.canvas.add_band(band)
        nodata = self.canvas.get_nodata(band)
        return series.replace(nodata, np.nan)

    def rasterise_raster(self, raster: xr.Dataset) -> None:
        for index, date in enumerate(raster[self.t_dim].values):
            for band in list(raster.data_vars.keys()):
                if not self.canvas.has_band(band):
                    self.canvas.add_band(band)
                raster_layer = raster[cast(str, band)].values[index, :, :]
                self.canvas.draw(pd.Timestamp(date), cast(str, band), raster_layer)

    @staticmethod
    def last_nodata(nodata: Nodata_T) -> Callable:
        def fn(s: pd.Series) -> Number_T:
            s = [item for item in s if item != nodata]
            return s[-1] if s else nodata

        return fn

    def get_op(self, band: str) -> Callable:
        nodata = self.canvas.get_nodata(band)
        method = self.canvas.get_method(band)
        match method:
            case "max":
                return np.nanmax
            case "min":
                return np.nanmin
            case "mean":
                return np.nanmean
            case "sum":
                return np.nansum
            case _:
                return self.last_nodata(nodata)

    def rasterise_point(self, data: pd.DataFrame, bands: set[str]) -> None:
        gy = self.canvas.y_coords
        gx = self.canvas.x_coords
        dy, dx = gy[1] - gy[0], gx[1] - gx[0]
        sx = data["grid_x"] = (data[self.canvas.x_dim] - gx[0]) // dx
        sy = data["grid_y"] = (data[self.canvas.y_dim] - gy[0]) // dy
        mask_x = (sx.isna()) | (sx < 0) | (sx >= len(gx))
        mask_y = (sy.isna()) | (sy < 0) | (sy >= len(gy))

        data["grid_x"] = data["grid_x"].where(~mask_x)
        data["grid_y"] = data["grid_y"].where(~mask_y)
        for band in bands:
            for date in data[self.t_dim].unique():
                dim_series, band_series = self.prepare_df(
                    data,
                    band,
                    date,
                    ["grid_x", "grid_y"],
                )
                try:
                    band_series = pd.to_numeric(band_series)
                    band_series = self.handle_numeric(band_series, band)
                    op = self.get_op(band)
                except ValueError:
                    band_series = self.handle_categorical(band_series, band)
                    op = self.last_nodata(self.canvas.get_nodata(band))
                dim_series[band] = band_series
                grid_data = dim_series.groupby(["grid_x", "grid_y"]).agg(op)
                grid_x = grid_data.index.get_level_values("grid_x").values.astype("int")
                grid_y = grid_data.index.get_level_values("grid_y").values.astype("int")
                raster = self.canvas.get_drawer(band).alloc()
                raster[grid_y, grid_x] = grid_data.values.reshape(-1)
                self.canvas.draw(pd.Timestamp(date), band, raster)

    def prepare_df(
        self, data: pd.DataFrame, band: str, date: str, dims: Sequence[str]
    ) -> tuple[pd.Series, pd.Series]:
        series = data.loc[data[self.t_dim] == date, [*dims, band]]
        series = series.drop_duplicates().dropna()
        dims_series = series.loc[:, dims]
        band_series = series.loc[:, band]
        return dims_series, band_series

    def rasterise_vector(
        self,
        data: gpd.GeoDataFrame,
        bands: set[str],
        geobox: GeoBox,
    ) -> None:
        for band in bands:
            for date in data[self.t_dim].unique():
                dim_series, band_series = self.prepare_df(
                    data, band, date, ["geometry"]
                )
                try:
                    band_series = pd.to_numeric(band_series)
                    band_series = self.handle_numeric(band_series, band)
                except ValueError:
                    band_series = self.handle_categorical(band_series, band)
                raster: np.ndarray = rasterio.features.rasterize(
                    (
                        (geom, value)
                        for geom, value in zip(
                            dim_series["geometry"].values,
                            band_series.values,
                        )
                    ),
                    out_shape=geobox.shape,
                    transform=geobox.transform,
                )
                self.canvas.draw(pd.Timestamp(date), band, raster)

    def compile(self) -> xr.Dataset:
        return self.canvas.compile(self.attrs)
