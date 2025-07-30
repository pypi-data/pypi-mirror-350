# Static Map 3

Static Map 3 is a fork of [Static Map](https://github.com/komoot/staticmap), a small, python-based library for creating map images with lines and markers.\
The main purpose of this fork is to fix error handling on tile requests, to allow interrupting the execution (see [PR](https://github.com/komoot/staticmap/pull/39) on the original repository).

Changes since the fork are detailed in [CHANGELOG.md](CHANGELOG.md).

## Example
```python
from staticmap3 import StaticMap, Line

m = StaticMap(300, 400, 10)
m.add_line(Line(((13.4, 52.5), (2.3, 48.9)), 'blue', 3))
image = m.render()
image.save('map.png')
```
This will create a 300px x 400px map with a blue line drawn from Berlin to Paris.

![Map with Line from Berlin to Paris](/samples/berlin_paris.png?raw=true)


## Installation
Static Map 3 is a small library, all it takes is python and three python packages: [Pillow](https://python-pillow.github.io/), [requests](https://requests.readthedocs.io/) and [cachecontrol](https://cachecontrol.readthedocs.io/en/latest/). 

To install Static Map 3:

```bash
pip install git+https://github.com/SamR1/staticmap.git
```

To use [`Filecache`](https://cachecontrol.readthedocs.io/en/latest/storage.html#filecache) as storage backend for cache:

```bash
pip install git+https://github.com/SamR1/staticmap.git@main#egg=staticmap3[filecache]
```
The default directory for cache is `.staticmap_cache`. It can be changed by exporting the environment variable `STATICMAP_CACHE_DIR`.

## Usage
#### Create a new map instance:

```python
m = StaticMap(width, height, padding_x, padding_y, url_template, tile_size)
```

parameter           | description
------------------- | -------------
width               | width of the image in pixels
height              | height of the image in pixels
padding_x           | (optional) minimum distance in pixel between map features (lines, markers) and map border
padding_y           | (optional) minimum distance in pixel between map features (lines, markers) and map border
url_template        | (optional) the tile server URL for the map base layer, e.g. <code>https://tile.openstreetmap.org/{z}/{x}/{y}.png</code>
tile_size           | (optional) tile size in pixel, usually 256

#### Add a line:

```python
line = Line(coordinates, color, width))
m.add_line(line)
```

parameter     | description
------------- | -------------
coordinate    | a sequence of lon/lat pairs
color         | a color definition Pillow <a href="https://pillow.readthedocs.io/en/stable/reference/ImageColor.html">supports</a>
width         | the stroke width of the line in pixel
simplify      | whether to simplify coordinates, looks less shaky, default is true

#### Add a map circle marker:

```python
marker = CircleMarker(coordinate, color, width))
m.add_marker(marker)
```

parameter     | description
------------- | -------------
coordinate    | a lon/lat pair: e.g. `(120.1, 47.3)`
color         | a color definition Pillow <a href="https://pillow.readthedocs.io/en/stable/reference/ImageColor.html#color-names">supports</a>
width         | diameter of marker in pixel

#### Add a polygon:

```python
polygon = Polygon(coordinates, fill_color, outline_color, simplify)
m.add_polygon(polygon)
```

parameter     | description
------------- | -------------
coordinate    | a lon/lat pair: e.g. `[[9.628, 47.144], [9.531, 47.270], [9.468, 47.057], [9.623, 47.050], [9.628, 47.144]]`
fill_color    | a color definition Pillow <a href="https://pillow.readthedocs.io/en/stable/reference/ImageColor.html#color-names">supports</a>
outline_color | a color definition Pillow <a href="https://pillow.readthedocs.io/en/stable/reference/ImageColor.html#color-names">supports</a>
simplify      | whether to simplify coordinates, looks less shaky, default is true

## Samples
#### Show Position on Map

```python
from staticmap3 import StaticMap, CircleMarker

m = StaticMap(
    200, 200, url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png'
)

marker_outline = CircleMarker((10, 47), 'white', 18)
marker = CircleMarker((10, 47), '#0036FF', 12)

m.add_marker(marker_outline)
m.add_marker(marker)

image = m.render(zoom=5)
image.save('marker.png')
```

![Position IconMarker on a Map](/samples/marker.png?raw=true)

#### Show Ferry Connection

```python
from staticmap3 import StaticMap, Line

m = StaticMap(200, 200, 80)

coordinates = [[12.422, 45.427], [13.749, 44.885]]
line_outline = Line(coordinates, 'white', 6)
line = Line(coordinates, '#D2322D', 4)

m.add_line(line_outline)
m.add_line(line)

image = m.render()
image.save('ferry.png')
```

![Ferry Connection Shown on a Map](/samples/ferry.png?raw=true)

#### Show Icon Marker

```python
from staticmap3 import StaticMap, IconMarker

m = StaticMap(240, 240, 80)
icon_flag = IconMarker(
    (6.63204, 45.85378), './samples/icon-flag.png', 12, 32
)
icon_factory = IconMarker(
    (6.6015, 45.8485), './samples/icon-factory.png', 18, 18
)
m.add_marker(icon_flag)
m.add_marker(icon_factory)
image = m.render()
image.save('icons.png')
```

![Ferry Connection Shown on a Map](/samples/icons.png?raw=true)

### Alternatives
With [papermap](https://github.com/sgraaf/papermap) there is also a spin-off project dedicated to print maps.

### Licence
Static Map 3 is open source and licensed under Apache License, Version 2.0

The map samples on this page are made with [OSM](https://www.openstreetmap.org) data, © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors
