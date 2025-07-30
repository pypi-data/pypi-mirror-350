# Maidenhead &lt;-&gt; Lat/Lon

[![DOI](https://zenodo.org/badge/132653071.svg)](https://zenodo.org/badge/latestdoi/132653071)
[![ci](https://github.com/space-physics/maidenhead/actions/workflows/ci.yml/badge.svg)](https://github.com/space-physics/maidenhead/actions/workflows/ci.yml)
[![pypi versions](https://img.shields.io/pypi/pyversions/maidenhead.svg)](https://pypi.python.org/pypi/maidenhead)
[![PyPi Download stats](http://pepy.tech/badge/maidenhead)](http://pepy.tech/project/maidenhead)

`maidenhead` provides a simple, yet effective location hashing algorithm.
Maidenhead allows global location precision down to 750m

Maidenhead provides 4 levels of increasing accuracy

  Level |  Precision
--------|------------
  1     |  World
  2     |  Regional
  3     |  Metropolis
  4     |  City
  5     |  Street
  6     |  1m precision

```sh
pip install maidenhead
```

or for development version

```sh
git clone https://github.com/space-physics/maidenhead

pip install -e maidenhead
```

Examples assume first doing

```python
import maidenhead as mh
```

Lat, lon to Maidenhead locator:

```python
mh.to_maiden(lat, lon, level)
```

returns a char (len = lvl*2)

Maidenhead locator to lat lon:

```python
mh.to_location('AB01cd')
```

takes Maidenhead location string and returns top-left lat, lon of Maidenhead grid square.

The `center=True` option outputs lat lon of the center of provided maidenhead grid square, instead of the default southwest corner.


Maidenhead locator to [geoJSON](https://geojson.org/) ([RFC 7946](https://tools.ietf.org/html/rfc7946))

```python
geo_obj = mh.to_geoJSONObject('AB01cd', center=True, nosquare=False)
geoJSON = json.dumps(geo_obj, indent=2)
```


## Command Line

The command line interface takes either decimal degrees for "latitude longitude" or the Maidenhead locator string:

```sh
python -m maidenhead 65.0 -148.0
```

> BP65aa

```sh
python -m maidenhead BP65aa12
```

> 65.0083 -147.9917

The "python -m" CLI is also available:

```sh
python -m maidenhead 65.0 -148.0
```

The `--center` option outputs lat lon of the center of provided maidenhead grid square, instead of the default southwest corner.


```sh
python -m maidenhead --center --geojson EN35ld
```

> {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"QTHLocator_Centerpoint": "EN35ld"}, "geometry": {"type": "Point", "coordinates": [-93.04166666666667, 45.145833333333336]}}, {"type": "Feature", "properties": {"QTHLocator": "EN35ld"}, "geometry": {"type": "Polygon", "coordinates": [[[-93.08333333333333, 45.125], [-93.08333333333333, 45.166666666666664], [-93.0, 45.166666666666664], [-93.0, 45.125], [-93.08333333333333, 45.125]]]}}]}

The `--center` option enables adding center point of the grid square as Point feature.

The `--nosquare` option  disables  adding Polygon feature for the requested grid square


## Alternatives

Open Location Codes a.k.a Plus Codes are in
[Python code by Google](https://github.com/google/open-location-code/tree/master/python).

Web convertor [Earth Point - Tools for Google Earth](https://www.earthpoint.us/Convert.aspx).
