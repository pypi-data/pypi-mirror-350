"""Tests for PyDaymet package."""

from __future__ import annotations

import io
import shutil
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from shapely import Polygon

import pydaymet as daymet
from pydaymet.cli import cli

GEOM = Polygon(
    [[-69.77, 45.07], [-69.31, 45.07], [-69.31, 45.45], [-69.77, 45.45], [-69.77, 45.07]]
)
DAY = ("2000-01-01", "2000-01-12")
YEAR = 2010
VAR = ["prcp", "tmin"]
DEF_CRS = 4326
ALT_CRS = 3542
COORDS = (-1431147.7928, 318483.4618)
DATES = ("2000-01-01", "2000-12-31")


def assert_close(a: float, b: float, rtol: float = 1e-3) -> None:
    assert np.isclose(a, b, rtol=rtol).all()


def test_tiles():
    tiles = daymet.daymet_tiles(GEOM)
    assert tiles.shape[0] == 1
    assert tiles[0] == "12116"


class TestByCoords:
    @pytest.mark.parametrize(
        ("method", "expected"),
        [("hargreaves_samani", 3.7651), ("priestley_taylor", 3.198), ("penman_monteith", 3.533)],
    )
    def test_pet(self, method, expected):
        clm = daymet.get_bycoords(COORDS, DATES, crs=ALT_CRS, pet=method)
        assert_close(clm["pet (mm/day)"].mean(), expected)

    def test_pet_arid(self):
        clm = daymet.get_bycoords(
            COORDS, DATES, crs=ALT_CRS, pet="priestley_taylor", pet_params={"arid_correction": True}
        )
        assert_close(clm["pet (mm/day)"].mean(), 3.113)

    @pytest.mark.jit
    def test_snow(self):
        clm = daymet.get_bycoords(COORDS, DATES, snow=True, crs=ALT_CRS)
        assert_close(clm["snow (mm/day)"].mean(), 0.000737)

    def test_daily(self):
        clm = daymet.get_bycoords(COORDS, DATES, variables=VAR, crs=ALT_CRS)
        clm_ds = daymet.get_bycoords(COORDS, DATES, variables=VAR, crs=ALT_CRS, to_xarray=True)

        expected = 1.144
        assert_close(clm["prcp (mm/day)"].mean(), expected)
        assert_close(clm_ds.prcp.mean(), expected)

    def test_monthly(self):
        clm = daymet.get_bycoords(COORDS, YEAR, variables=VAR, crs=ALT_CRS, time_scale="monthly")
        assert_close(clm["tmin (degrees C)"].mean(), 11.458)

    def test_annual(self):
        clm = daymet.get_bycoords(COORDS, YEAR, variables=VAR, crs=ALT_CRS, time_scale="annual")
        assert_close(clm["tmin (degrees C)"].mean(), 11.458)


class TestByGeom:
    @pytest.mark.parametrize(
        ("method", "expected"),
        [("hargreaves_samani", 0.4525), ("priestley_taylor", 0.119), ("penman_monteith", 0.627)],
    )
    def test_pet(self, method, expected):
        clm = daymet.get_bygeom(GEOM, DAY, pet=method)
        assert_close(clm.pet.mean().compute().item(), expected)

    def test_pet_arid(self):
        clm = daymet.get_bygeom(
            GEOM, DAY, pet="priestley_taylor", pet_params={"arid_correction": True}
        )
        assert_close(clm.pet.mean().compute().item(), 0.1066)

    @pytest.mark.jit
    def test_snow(self):
        clm = daymet.get_bygeom(GEOM, DAY, snow=True, snow_params={"t_snow": 0.5})
        assert_close(clm.snow.mean().compute().item(), 3.4999)

    def test_bounds(self):
        clm = daymet.get_bygeom(GEOM.bounds, DAY)
        assert_close(clm.prcp.mean().compute().item(), 3.4999)

    def test_daily(self):
        clm = daymet.get_bygeom(GEOM, DAY, variables=VAR)
        assert_close(clm.tmin.mean().compute().item(), -9.421)

    def test_monthly(self):
        clm = daymet.get_bygeom(GEOM, YEAR, variables=VAR, time_scale="monthly")
        assert_close(clm.tmin.mean().compute().item(), 1.311)

    def test_annual(self):
        clm = daymet.get_bygeom(GEOM, YEAR, variables=VAR, time_scale="annual")
        assert_close(clm.tmin.mean().compute().item(), 1.361)

    def test_region(self):
        hi_ext = (-160.3055, 17.9539, -154.7715, 23.5186)
        pr_ext = (-67.9927, 16.8443, -64.1195, 19.9381)
        hi = daymet.get_bygeom(hi_ext, YEAR, variables=VAR, region="hi", time_scale="annual")
        pr = daymet.get_bygeom(pr_ext, YEAR, variables=VAR, region="pr", time_scale="annual")

        assert_close(hi.prcp.mean().compute().item(), 1035.233)
        assert_close(pr.tmin.mean().compute().item(), 21.441)


class TestCLI:
    """Test the command-line interface."""

    def test_geometry(self, runner):
        params = {
            "id": "geo_test",
            "start": "2000-01-01",
            "end": "2000-05-31",
            "time_scale": "monthly",
            "snow": "false",
        }
        geo_gpkg = Path("nat_geo.gpkg")
        save_dir = "test_geometry"
        gdf = gpd.GeoDataFrame(params, geometry=[GEOM], index=[0], crs=DEF_CRS)
        gdf.to_file(geo_gpkg)
        ret = runner.invoke(
            cli,
            [
                "geometry",
                str(geo_gpkg),
                *[item for v in VAR for item in ["-v", v]],
                "-s",
                save_dir,
            ],
        )
        if geo_gpkg.is_dir():
            shutil.rmtree(geo_gpkg)
        else:
            geo_gpkg.unlink()
        shutil.rmtree(save_dir, ignore_errors=True)
        assert str(ret.exception) == "None"
        assert ret.exit_code == 0
        assert "Found 1 geometry" in ret.output

    @pytest.mark.jit
    def test_coords(self, runner):
        params = {
            "id": "coords_test",
            "lon": -69.77,
            "lat": 45.07,
            "start": DAY[0],
            "end": DAY[1],
            "pet": "hargreaves_samani",
            "snow": "TRUE",
        }
        coord_csv = "coords.csv"
        save_dir = "test_coords"
        df = pd.DataFrame(params, index=[0])
        df.to_csv(coord_csv, index=False)
        ret = runner.invoke(
            cli,
            [
                "coords",
                coord_csv,
                *[item for v in VAR for item in ["-v", v]],
                "-s",
                save_dir,
            ],
        )
        runner.invoke(
            cli,
            [
                "coords",
                coord_csv,
                *[item for v in VAR for item in ["-v", v]],
                "-s",
                save_dir,
            ],
        )
        Path(coord_csv).unlink()
        shutil.rmtree(save_dir, ignore_errors=True)
        assert str(ret.exception) == "None"
        assert ret.exit_code == 0
        assert "Found coordinates of 1 point" in ret.output


@pytest.mark.xfail(reason="This test is failing due to an issue with MS Stac.")
def test_stac():
    clm = daymet.get_bystac(
        GEOM,
        ("2010-01-01", "2010-01-02"),
        variables="prcp",
        res_km=4,
        snow=True,
        pet="hargreaves_samani",
    )
    assert_close(clm["pet"].mean().item(), 0.3157)


def test_show_versions():
    f = io.StringIO()
    daymet.show_versions(file=f)
    assert "SYS INFO" in f.getvalue()
