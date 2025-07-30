from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from hermes_model.validation import validate_entrypoint


@validate_entrypoint
def dummy_forecast(model_input):
    return [pd.DataFrame({
        "longitude": [1.0],
        "latitude": [2.0],
        "depth": [3.0],
        "time": ["2020-01-01"],
        "magnitude": [4.0]
    })]


model_input = {
    'forecast_start': datetime(2020, 1, 1),
    'forecast_end': datetime(2021, 1, 1),
    'seismicity_observation': '<dummy_quakeml>',
    'bounding_polygon': 'POLYGON((0 0,1 0,1 1,0 1,0 0))'
}

model_input_hyd = {
    'forecast_start': datetime(2020, 1, 1),
    'forecast_end': datetime(2021, 1, 1),
    'seismicity_observation': '<dummy_quakeml>',
    'bounding_polygon': 'POLYGON((0 0,1 0,1 1,0 1,0 0))',
    'injection_observation': [{}],
    'injection_plan': [{}]
}


def test_validate_entrypoint_valid_input():
    with pytest.raises(ValueError, match="Invalid format for seismic catalog"):
        dummy_forecast(model_input)


def test_invalid_argument_count():
    with pytest.raises(ValueError, match="Only one argument is allowed"):
        dummy_forecast({}, {})  # too many arguments


def test_invalid_seismicity_observation():

    from hermes_model import validation

    with pytest.raises(ValueError, match="Invalid format for seismic catalog"):
        with patch.object(validation.Catalog, "from_quakeml",
                          side_effect=Exception):
            dummy_forecast(model_input)


def test_invalid_result_type():
    @validate_entrypoint
    def bad_return_forecast(model_input):
        return ["not a valid type"]

    with patch("hermes_model.validation.Catalog.from_quakeml"), \
            patch("hermes_model.validation.wkt.loads"), \
            patch("hermes_model.validation._check_required_cols",
                  return_value=True):

        with pytest.raises(ValueError, match="Results need to be of type"):
            bad_return_forecast(model_input)


def test_induced_mode_without_hydws():
    @validate_entrypoint(induced=True)
    def induced_forecast(model_input):
        return [pd.DataFrame({
            "longitude": [1.0],
            "latitude": [2.0],
            "depth": [3.0],
            "time": ["2020-01-01"],
            "magnitude": [4.0]
        })]

    with patch("hermes_model.validation._hydraulics_available", False):
        with pytest.raises(ValueError, match="HYDWS-Client is not installed"):
            induced_forecast(model_input_hyd)


def test_invalid_injection_observation():
    @validate_entrypoint(induced=True)
    def induced_forecast(model_input):
        return [pd.DataFrame({
            "longitude": [1.0],
            "latitude": [2.0],
            "depth": [3.0],
            "time": ["2020-01-01"],
            "magnitude": [4.0]
        })]

    with patch("hermes_model.validation._hydraulics_available", True), \
            patch("hermes_model.validation.BoreholeHydraulics"), \
            patch("hermes_model.validation.Catalog.from_quakeml"), \
            patch("hermes_model.validation.wkt.loads"), \
            patch("hermes_model.validation._check_required_cols",
                  return_value=True):

        with pytest.raises(ValueError, match="Invalid injection observation"):
            with patch("hermes_model.validation.BoreholeHydraulics",
                       side_effect=Exception("fail")):
                induced_forecast(model_input_hyd)


def test_invalid_injection_plan():
    @validate_entrypoint(induced=True)
    def induced_forecast(model_input):
        return [pd.DataFrame({
            "longitude": [1.0],
            "latitude": [2.0],
            "depth": [3.0],
            "time": ["2020-01-01"],
            "magnitude": [4.0]
        })]

    model_input_fail = model_input_hyd.copy()

    with patch("hermes_model.validation._hydraulics_available", True), \
            patch("hermes_model.validation.BoreholeHydraulics"), \
            patch("hermes_model.validation.Catalog.from_quakeml"), \
            patch("hermes_model.validation.wkt.loads"), \
            patch("hermes_model.validation._check_required_cols",
                  return_value=True):

        model_input_fail['injection_plan'] = None  # Invalid injection plan

        with pytest.raises(BaseException, match="Invalid injection plan"):
            induced_forecast(model_input_fail)


def test_missing_required_result_columns():
    @validate_entrypoint
    def bad_results_forecast(model_input):
        # Return a DataFrame missing all required columns
        return [pd.DataFrame({"foo": [1], "bar": [2]})]

    with patch("hermes_model.validation.Catalog.from_quakeml"), \
            patch("hermes_model.validation.wkt.loads"), \
            patch("hermes_model.validation._check_required_cols",
                  return_value=False):  # force fail

        with pytest.raises(ValueError,
                           match="Results are missing required columns."):
            bad_results_forecast(model_input)


def test_gr_grid_like_results_valid():
    @validate_entrypoint
    def grid_forecast(model_input):
        return [pd.DataFrame({
            "longitude_min": [1.0],
            "longitude_max": [1.5],
            "latitude_min": [2.0],
            "latitude_max": [2.5],
            "depth_min": [3.0],
            "depth_max": [4.0],
            "a": [1.0],
            "b": [1.0],
            "mc": [2.0]
        })]

    with patch("hermes_model.validation.Catalog.from_quakeml"), \
            patch("hermes_model.validation.wkt.loads"), \
            patch("hermes_model.validation._check_required_cols",
                  return_value=True):

        results = grid_forecast(model_input)
        assert isinstance(results, list)
        assert isinstance(results[0], pd.DataFrame)
