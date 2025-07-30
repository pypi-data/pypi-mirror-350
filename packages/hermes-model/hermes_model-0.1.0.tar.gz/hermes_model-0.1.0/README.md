# Getting Started

## Entrypoint
All you need to in order to make your model compatible is to define an entry point, a simple function, for your model. With a predefined format for input and output from this entrypoint, hermes is then able to execute your model and store the results in the database using that funcion.

```python	
def entrypoint(input: dict) -> list:
    # Call and execute your model here.
    return output
```

## Usage
The description of the formats used for the input and output of the entrypoint can be found in the [input](#input-format) and [output](#output-format) format sections. If you want, you can stop there, without installation of this package, as hermes doesn't need anything else. If you would like to have some kind of validation of the input and output of your entrypoint, you can [install](#installation) this package and read the [validation](#validation) section.

# Input and Output Formats

The `validate_entrypoint` decorator will validate the input and output of the entrypoint, and raise an error if the input or output is not valid. The `induced` parameter is optional, and defaults to `False`. If set to `True` the input fields `injection_observation` and `injection_plan` will be validated as well.

## Input Format
The input dictionary has the following fields:
```
model_input = {
        'forecast_start': 'datetime'
        'forecast_end': 'datetime',
        'injection_observation': 'list[hydjson]',
        'injection_plan': 'hydjson',
        'bounding_polygon': 'wkt(str)',
        'depth_min': 'float',
        'depth_max': 'float'
        'seismicity_observation': 'quakeml',
        'model_parameters': 'dict'
    }
```
Following a complete description of the input fields:

```
forecast_start: datetime.datetime
```
Date and time from when on the forecast should be made.

```
forecast_end: datetime.datetime
```
Date and time until when the forecast should be made.

```
injection_observation: list[dict] # HYDJSON format
```
A list of dictionaries in the HYDJSON format, containing the history of injections into the well.

```
injection_plan: str | dict # HYDJSON format
```
A dictionary in the HYDJSON format, containing the planned injections.

```
seismicity_observation: str # QUAKEML format
```
An XML string in the QUAKEML format, containing the seismic events catalog.

```
model_parameters: dict
```
A dictionary containing the parameters for the model. The keys are the names of the parameters, and the values are the values of the parameters.

```

bounding_polygon: str # WKT format
depth_min: float
depth_max: float
```
The geometry of the area of interest. The bounding_polygon is a string in the WKT format.
It is the model's responsibility to discretize the area of interest and to calculate the forecast for each discretized volume.


## Output Format
The output of the entrypoint should be a list of forecasts, where each entry in the list represents the forecast for one timestep. The forecasts can be one of two types, either Catalogs of events, including their magnitude, location and time, or a a parametric description of the seismicity, including at least `a`, `b` and `mc` values.

Each forecast should be returned either as a `pd.DataFrame()` object, or, if using the `SeismoStats` package, as a `(Forecast)Catalog` object or a `(Forecast)GRRateGrid` object. 

In any case, they each need two attributes, `starttime` and `endtime`, which are `datetime.datetime` objects defining the timestep for which the forecast is made.
```
def entrypoint(input: dict) -> list:
    catalog = pd.DataFrame(#your data here)
    catalog.starttime = datetime.datetime(2020, 11, 24, 14, 47, 9)
    catalog.endtime = datetime.datetime(2020, 11, 24, 15, 47, 9)
    return [catalog]
```


### Catalog
If returning a Catalog of events, the returned object should have at least the following columns:

```
                          time longitude   latitude        depth  magnitude
0   2020-11-24 14:47:09.823149  8.474492  46.509983  1294.102992      -2.82
1   2020-11-24 15:28:54.648949  8.474545  46.510010  1268.102992      -2.94
2   2020-11-24 15:31:42.411869  8.474323  46.509967  1265.102992      -3.03
3   2020-11-24 15:35:01.114360  8.474359  46.509832  1260.102992      -2.95
4   2020-11-24 15:35:07.995789  8.474372  46.509814  1261.102992      -2.94
```

It is possible to return multiple realizations of catalogs for one timestep. In this case a `catalog_id` column is required, to distinguish between the different realizations:

```
                          time longitude   latitude        depth  magnitude  catalog_id
0   2020-11-24 14:47:09.823149  8.474492  46.509983  1294.102992      -2.82        0
1   2020-11-24 15:28:54.648949  8.474545  46.510010  1268.102992      -2.94        0
2   2020-11-24 15:31:42.411869  8.474323  46.509967  1265.102992      -3.03        0
3   2020-11-24 15:35:01.114360  8.474359  46.509832  1260.102992      -2.95        1
4   2020-11-24 15:35:07.995789  8.474372  46.509814  1261.102992      -2.94        1
```

### GRRateGrid
If using a grid of Gutenberg-Richter rates, the returned object should have at least the following columns:
```
 longitude_min longitude_max latitude_min latitude_max depth_min depth_max    a   b    mc
0    8.472518      8.476478    46.508451    46.511185  1121.433  1421.434 -26.1 2.1 -2.91
```

Additional columns are allowed. Currently `number_events`, `alpha` are also stored if available.

Similar to the catalog, `grid_id` can be used to return probabilistic forecast, returning multiple possible realizations of a grid per timestep:

```
 longitude_min  longitude_max  latitude_min  latitude_max depth_min depth_max a     alpha   b   mc  grid_id
0  8.472518       8.476478     46.508451     46.511185  1121.434  1421.434    -26.1 -5.3  2.1 -2.91       0
1  8.472518       8.476478     46.508451     46.511185  1121.434  1421.434    -26.1 -5.3  2.1 -2.91       1
2  8.472518       8.476478     46.508451     46.511185  1121.434  1421.434    -26.1 -5.3  2.1 -2.91       2
3  8.472518       8.476478     46.508451     46.511185  1121.434  1421.434    -26.1 -5.3  2.0 -2.91       3
```



# Validation
If you would like to have some kind of validation of the input and output of your entrypoint, you can install this package following [these instructions](#installation).

The changes to the entrypoint are minimal:

```python	
from hermes import validate_entrypoint, ModelInput

@validate_entrypoint(induced=True)
def entrypoint(model_input: ModelInput):
    # Call and execute your model here.
    return output
```

Note, that you now don't have a dict anymore inside the function, but an object, with the fields of the input format as attributes. The `validate_entrypoint` decorator will validate the input and output of the entrypoint, and raise an error if the input or output is not valid. 

The `induced` parameter is optional, and defaults to `False`. If set to `True` the input fields `injection_observation` and `injection_plan` will be validated as well. Note, that if you're using the validation for induced seismicity, you need to install the package with the extra 'hydws' dependency:

# Installation
If you want to use the validation features, you can install the package by running the following command:

```bash
# basic installation
pip install git+https://gitlab.seismo.ethz.ch/indu/hermes-model.git

# installation with hydws dependency
pip install 'hermes-model[hydws] @ git+https://gitlab.seismo.ethz.ch/indu/hermes-model.git'
```

You can reference the dependency in your requirements.txt or setup.cfg file as well:

```bash
# basic dependency
hermes-model @ git+https://gitlab.seismo.ethz.ch/indu/hermes-model.git

# dependency with hydws
hermes-model[hydws] @ git+https://gitlab.seismo.ethz.ch/indu/hermes-model.git
```

## Dependencies
The data formats we rely on are HYDJSON for the models forecasting induced seismicity, and QUAKEML for the events data. To work with those formats, we use the two packages `hydws-client` and `SeismoStats` respectively. It is not required to use them as well, but this package uses them to validate the input and output data, and they are very handy to work with quakeml and hydjson. `hydws-client` will only be installed, if you install the package with the extra 'hydws' dependency.
