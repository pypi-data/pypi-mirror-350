from functools import wraps

import pandas as pd

try:
    from hydws.parser import BoreholeHydraulics
except ImportError:
    _hydraulics_available = False
else:
    _hydraulics_available = True
from seismostats import Catalog, GRRateGrid
from seismostats.utils import _check_required_cols
from shapely import wkt

from hermes_model.schemas import ModelInput


def validate_entrypoint(_func=None, *, induced=False):
    def decorator_entrypoint(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            # check only one argument is passed
            if len(args) != 1:
                raise ValueError("Only one argument is allowed")

            model_input = ModelInput(**args[0])

            if induced:
                if not _hydraulics_available:
                    raise ValueError(
                        "HYDWS-Client is not installed, "
                        "please install this package with [hydws] extras "
                        "to induced seismicity features.")
                # check if hydraulics are in the right format
                try:
                    if model_input.injection_observation is None:
                        raise Exception
                    for well in model_input.injection_observation:
                        if well is None:
                            raise Exception
                        BoreholeHydraulics(well)
                except BaseException:
                    raise ValueError("Invalid injection observation, "
                                     "please use valid hydjson.")

                try:
                    if model_input.injection_plan is None:
                        raise Exception
                    for ip in model_input.injection_plan:
                        BoreholeHydraulics(ip)
                except BaseException:
                    raise ValueError("Invalid injection plan, "
                                     "please use valid hydjson.")

            try:
                Catalog.from_quakeml(model_input.seismicity_observation)
            except BaseException:
                raise ValueError("Invalid format for seismic catalog, "
                                 "please use valid quakeml.")

            try:
                wkt.loads(model_input.bounding_polygon)
            except BaseException:
                raise ValueError("Invalid format for bounding polygon, "
                                 "please use valid WKT.")

            results = func(model_input, **kwargs)

            if not all(isinstance(r, GRRateGrid)
                       or isinstance(r, Catalog)
                       or isinstance(r, pd.DataFrame) for r in results):
                raise ValueError(
                    "Results need to be of type (Forecast)GRRateGrid, "
                    "(Forecast)Catalog or DataFrame.")

            if not all(
                _check_required_cols(r, ['longitude', 'latitude', 'depth',
                                         'time', 'magnitude'])
                for r in results) \
                and not all(
                    _check_required_cols(r, ['longitude_min', 'longitude_max',
                                             'latitude_min', 'latitude_max',
                                             'depth_min', 'depth_max',
                                             'a', 'b', 'mc'
                                             ])
                    for r in results):
                raise ValueError("Results are missing required columns.")

            return results
        return wrapper

    if _func is None:
        return decorator_entrypoint
    else:
        return decorator_entrypoint(_func)
