import itertools
import os
import time
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from logging import getLogger
from math import atan, ceil, cos, floor, log, pi, sinh, sqrt, tan
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import requests
from cachecontrol import CacheControl
from PIL import Image, ImageDraw

try:
    from cachecontrol.caches.file_cache import FileCache

    cache: Optional[FileCache] = FileCache(
        os.getenv("STATICMAP_CACHE_DIR", ".staticmap_cache")
    )
except ImportError:
    cache = None

logger = getLogger(__name__)


class Line:
    def __init__(
        self,
        coords: Sequence[Tuple[float, float]],
        color: str,
        width: int,
        simplify: bool = True,
    ) -> None:
        """
        Line that can be drawn in a static map

        :param coords: an iterable of lon-lat pairs,
               e.g. ((0.0, 0.0), (175.0, 0.0), (175.0, -85.1))
        :param color: color suitable for PIL / Pillow
        :param width: width in pixel
        :param simplify: whether to simplify coordinates, looks less shaky,
               default is true
        """
        self.coords = coords
        self.color = color
        self.width = width
        self.simplify = simplify

    @property
    def extent(self) -> Tuple[float, float, float, float]:
        """
        calculate the coordinates of the envelope / bounding box:
        (min_lon, min_lat, max_lon, max_lat)
        """
        return (
            min((c[0] for c in self.coords)),
            min((c[1] for c in self.coords)),
            max((c[0] for c in self.coords)),
            max((c[1] for c in self.coords)),
        )


class CircleMarker:
    def __init__(
        self, coord: Tuple[float, float], color: str, width: int
    ) -> None:
        """
        :param coord: a lon-lat pair, eg (175.0, 0.0)
        :param color: color suitable for PIL / Pillow
        :param width: marker width
        """
        self.coord = coord
        self.color = color
        self.width = width

    @property
    def extent_px(self) -> Tuple[int, int, int, int]:
        return (self.width,) * 4


class IconMarker:
    def __init__(
        self,
        coord: Tuple[float, float],
        file_path: str,
        offset_x: int,
        offset_y: int,
    ) -> None:
        """
        :param coord:  a lon-lat pair, eg (175.0, 0.0)
        :param file_path: path to icon
        :param offset_x: x position of the tip of the icon. relative to left
               bottom, in pixel
        :param offset_y: y position of the tip of the icon. relative to left
               bottom, in pixel
        """
        self.coord = coord
        self.img = Image.open(file_path, "r")
        self.offset = (offset_x, offset_y)

    @property
    def extent_px(self) -> Tuple[int, int, int, int]:
        w, h = self.img.size
        return (
            self.offset[0],
            h - self.offset[1],
            w - self.offset[0],
            self.offset[1],
        )


class Polygon:
    def __init__(
        self,
        coords: Sequence[Tuple[float, float]],
        fill_color: str,
        outline_color: str,
        simplify: bool = True,
    ) -> None:
        """
        Polygon that can be drawn on map

        :param coords: an iterable of lon-lat pairs,
               e.g. ((0.0, 0.0), (175.0, 0.0), (175.0, -85.1))
        :param fill_color: color suitable for PIL / Pillow, can be None
               (transparent)
        :param outline_color: color suitable for PIL / Pillow, can be None
               (transparent)
        :param simplify: whether to simplify coordinates, looks less shaky,
               default is true
        """
        self.coords = coords
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.simplify = simplify

    @property
    def extent(self) -> Tuple[float, float, float, float]:
        return (
            min((c[0] for c in self.coords)),
            min((c[1] for c in self.coords)),
            max((c[0] for c in self.coords)),
            max((c[1] for c in self.coords)),
        )


def _lon_to_x(lon: float, zoom: int) -> float:
    """
    transform longitude to tile number
    """
    if not (-180 <= lon <= 180):
        lon = (lon + 180) % 360 - 180

    return ((lon + 180.0) / 360) * pow(2, zoom)


def _lat_to_y(lat: float, zoom: int) -> float:
    """
    transform latitude to tile number
    """
    if not (-90 <= lat <= 90):
        lat = (lat + 90) % 180 - 90

    return (
        (1 - log(tan(lat * pi / 180) + 1 / cos(lat * pi / 180)) / pi)
        / 2
        * pow(2, zoom)
    )


def _y_to_lat(y: float, zoom: int) -> float:
    return atan(sinh(pi * (1 - 2 * y / pow(2, zoom)))) / pi * 180


def _x_to_lon(x: float, zoom: int) -> float:
    return x / pow(2, zoom) * 360.0 - 180.0


def _simplify(
    points: List[Tuple[int, int]], tolerance: int = 11
) -> List[Tuple[int, int]]:
    """
    :param points: list of lon-lat pairs
    :param tolerance: tolerance in pixel
    :return: list of lon-lat pairs
    """
    if not points:
        return points

    new_coords = [points[0]]

    for p in points[1:-1]:
        last = new_coords[-1]

        dist = sqrt(pow(last[0] - p[0], 2) + pow(last[1] - p[1], 2))
        if dist > tolerance:
            new_coords.append(p)

    new_coords.append(points[-1])

    return new_coords


class StaticMap:
    def __init__(
        self,
        width: int,
        height: int,
        padding_x: int = 0,
        padding_y: int = 0,
        url_template: str = "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        tile_size: int = 256,
        tile_request_timeout: Optional[float] = None,
        headers: Optional[Dict] = None,
        reverse_y: bool = False,
        background_color: str = "#fff",
        delay_between_retries: int = 0,
    ) -> None:
        """
        :param width: map width in pixel
        :param height:  map height in pixel
        :param padding_x: min distance in pixel from map features to border
               of map
        :param padding_y: min distance in pixel from map features to border
               of map
        :param url_template: tile URL
        :param tile_size: the size of the map tiles in pixel
        :param tile_request_timeout: time in seconds to wait for requesting
               map tiles
        :param headers: additional headers to add to http requests
        :param reverse_y: tile source has TMS y origin
        :param background_color: Image background color, only visible when
               tiles are transparent
        :param delay_between_retries: number of seconds to wait between retries
               of map tile requests
        """
        self.width = width
        self.height = height
        self.padding = (padding_x, padding_y)
        self.url_template = url_template
        self.headers = headers if headers else {"User-Agent": "StaticMap"}
        self.tile_size = tile_size
        self.request_timeout = tile_request_timeout
        self.reverse_y = reverse_y
        self.background_color = background_color

        # features
        self.markers: List[Union["IconMarker", "CircleMarker"]] = []
        self.lines: List["Line"] = []
        self.polygons: List["Polygon"] = []

        # fields that get set when map is rendered
        self.x_center: float = 0.0
        self.y_center: float = 0.0
        self.zoom = 0

        self.delay_between_retries = delay_between_retries

    def add_line(self, line: "Line") -> None:
        """
        :param line: line to draw
        """
        self.lines.append(line)

    def add_marker(self, marker: Union["IconMarker", "CircleMarker"]) -> None:
        """
        :param marker: marker to draw
        """
        self.markers.append(marker)

    def add_polygon(self, polygon: "Polygon") -> None:
        """
        :param polygon: polygon to be drawn
        """
        self.polygons.append(polygon)

    def render(
        self,
        zoom: Optional[int] = None,
        center: Optional[Tuple[float, float]] = None,
    ) -> "Image.Image":
        """
        render static map with all map features that were added to map before

        :param zoom: optional zoom level, will be optimized automatically if
               not given.
        :param center: optional center of map, will be set automatically from
               markers if not given.
        :return: PIL image instance
        """

        if (
            not self.lines
            and not self.markers
            and not self.polygons
            and not (center and zoom)
        ):
            raise RuntimeError(
                "cannot render empty map, add lines / markers / polygons first"
            )

        if zoom is None:
            self.zoom = self._calculate_zoom()
        else:
            self.zoom = zoom

        if center:
            self.x_center = _lon_to_x(center[0], self.zoom)
            self.y_center = _lat_to_y(center[1], self.zoom)
        else:
            # get extent of all lines
            extent = self.determine_extent(zoom=self.zoom)

            # calculate center point of map
            lon_center, lat_center = (
                (extent[0] + extent[2]) / 2,
                (extent[1] + extent[3]) / 2,
            )
            self.x_center = _lon_to_x(lon_center, self.zoom)
            self.y_center = _lat_to_y(lat_center, self.zoom)

        image = Image.new(
            "RGB", (self.width, self.height), self.background_color
        )

        self._draw_base_layer(image)
        self._draw_features(image)

        return image

    def determine_extent(
        self, zoom: Optional[int] = None
    ) -> Tuple[float, float, float, float]:
        """
        calculate common extent of all current map features

        :param zoom: optional parameter, when set extent of markers can be
               considered
        :return: extent (min_lon, min_lat, max_lon, max_lat)
        """
        extents = [line.extent for line in self.lines]

        for m in self.markers:
            e = (m.coord[0], m.coord[1])

            if zoom is None:
                extents.append(e * 2)
                continue

            # consider dimension of marker
            e_px = m.extent_px

            x = _lon_to_x(e[0], zoom)
            y = _lat_to_y(e[1], zoom)

            extents += [
                (
                    _x_to_lon(x - float(e_px[0]) / self.tile_size, zoom),
                    _y_to_lat(y + float(e_px[1]) / self.tile_size, zoom),
                    _x_to_lon(x + float(e_px[2]) / self.tile_size, zoom),
                    _y_to_lat(y - float(e_px[3]) / self.tile_size, zoom),
                )
            ]

        extents += [p.extent for p in self.polygons]

        return (
            min(e[0] for e in extents),
            min(e[1] for e in extents),
            max(e[2] for e in extents),
            max(e[3] for e in extents),
        )

    def _calculate_zoom(self) -> int:
        """
        calculate the best zoom level for given extent

        :return: lowest zoom level for which the entire extent fits in
        """

        for z in range(17, -1, -1):
            extent = self.determine_extent(zoom=z)

            width = (
                _lon_to_x(extent[2], z) - _lon_to_x(extent[0], z)
            ) * self.tile_size
            if width > (self.width - self.padding[0] * 2):
                continue

            height = (
                _lat_to_y(extent[1], z) - _lat_to_y(extent[3], z)
            ) * self.tile_size
            if height > (self.height - self.padding[1] * 2):
                continue

            # we found first zoom that can display entire extent
            return z

        # map dimension is too small to fit all features
        return 0

    def _x_to_px(self, x: float) -> int:
        """
        transform tile number to pixel on image canvas
        """
        px = (x - self.x_center) * self.tile_size + self.width / 2
        return round(px)

    def _y_to_px(self, y: float) -> int:
        """
        transform tile number to pixel on image canvas
        """
        px = (y - self.y_center) * self.tile_size + self.height / 2
        return round(px)

    def _draw_base_layer(self, image: "Image.Image") -> None:
        x_min = floor(self.x_center - (0.5 * self.width / self.tile_size))
        y_min = floor(self.y_center - (0.5 * self.height / self.tile_size))
        x_max = ceil(self.x_center + (0.5 * self.width / self.tile_size))
        y_max = ceil(self.y_center + (0.5 * self.height / self.tile_size))

        # assemble all map tiles needed for the map
        tiles = []
        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                # x and y may have crossed the date line
                max_tile = 2**self.zoom
                tile_x = (x + max_tile) % max_tile
                tile_y = (y + max_tile) % max_tile

                if self.reverse_y:
                    tile_y = ((1 << self.zoom) - tile_y) - 1

                url = self.url_template.format(z=self.zoom, x=tile_x, y=tile_y)
                tiles.append((x, y, url))

        thread_pool = ThreadPoolExecutor(4)

        for nb_retry in itertools.count():
            if not tiles:
                # no tiles left
                break

            if nb_retry > 0 and self.delay_between_retries:
                # to avoid stressing the map tile server to much, wait
                # some seconds
                time.sleep(self.delay_between_retries)

            if nb_retry >= 3:
                # maximum number of retries exceeded
                raise RuntimeError(
                    "could not download {} tiles: {}".format(len(tiles), tiles)
                )

            failed_tiles = []
            futures = [
                thread_pool.submit(
                    self.get,
                    tile[2],
                    timeout=self.request_timeout,
                    headers=self.headers,
                )
                for tile in tiles
            ]

            for tile, future in zip(tiles, futures):
                x, y, url = tile

                try:
                    response_status_code, response_content = future.result()
                except Exception:
                    response_status_code, response_content = None, None

                if response_status_code != 200:
                    logger.error(
                        f"request failed [{response_status_code}]: {url}"
                    )
                    failed_tiles.append(tile)
                    continue

                if not response_content:
                    logger.error("request failed: no content")
                    failed_tiles.append(tile)
                    continue

                tile_image = Image.open(BytesIO(response_content)).convert(
                    "RGBA"
                )
                box = (
                    self._x_to_px(x),
                    self._y_to_px(y),
                    self._x_to_px(x + 1),
                    self._y_to_px(y + 1),
                )
                image.paste(tile_image, box, tile_image)

            # put failed back into list of tiles to fetch in next try
            tiles = failed_tiles

    def get(self, url: str, **kwargs: Any) -> Tuple[int, bytes]:
        """
        returns the status code and content (in bytes) of the requested
        tile url
        """
        session = requests.session()
        cached_session = CacheControl(session, cache=cache)
        res = cached_session.get(url, **kwargs)
        return res.status_code, res.content

    def _draw_features(self, image: "Image.Image") -> None:
        # Pillow does not support anti aliasing for lines and circles
        # There is a trick to draw them on an image that is twice the size and
        # resize it at the end before it gets merged with  the base layer

        image_lines = Image.new(
            "RGBA", (self.width * 2, self.height * 2), (255, 0, 0, 0)
        )
        draw = ImageDraw.Draw(image_lines)

        for line in self.lines:
            points = [
                (
                    self._x_to_px(_lon_to_x(coord[0], self.zoom)) * 2,
                    self._y_to_px(_lat_to_y(coord[1], self.zoom)) * 2,
                )
                for coord in line.coords
            ]

            if line.simplify:
                points = _simplify(points)

            for point in points:
                # draw extra points to make the connection between lines
                # look nice
                draw.ellipse(
                    (
                        point[0] - line.width + 1,
                        point[1] - line.width + 1,
                        point[0] + line.width - 1,
                        point[1] + line.width - 1,
                    ),
                    fill=line.color,
                )

            draw.line(points, fill=line.color, width=line.width * 2)

        for circle in filter(
            lambda m: isinstance(m, CircleMarker), self.markers
        ):
            point = (
                self._x_to_px(_lon_to_x(circle.coord[0], self.zoom)) * 2,
                self._y_to_px(_lat_to_y(circle.coord[1], self.zoom)) * 2,
            )
            draw.ellipse(
                (
                    point[0] - circle.width,  # type: ignore [union-attr]
                    point[1] - circle.width,  # type: ignore [union-attr]
                    point[0] + circle.width,  # type: ignore [union-attr]
                    point[1] + circle.width,  # type: ignore [union-attr]
                ),
                fill=circle.color,  # type: ignore [union-attr]
            )

        for polygon in self.polygons:
            points = [
                (
                    self._x_to_px(_lon_to_x(coord[0], self.zoom)) * 2,
                    self._y_to_px(_lat_to_y(coord[1], self.zoom)) * 2,
                )
                for coord in polygon.coords
            ]
            if polygon.simplify:
                points = _simplify(points)

            if polygon.fill_color or polygon.outline_color:
                draw.polygon(
                    points,
                    fill=polygon.fill_color,
                    outline=polygon.outline_color,
                )

        image_lines = image_lines.resize(
            (self.width, self.height), Image.Resampling.LANCZOS
        )

        # merge lines with base image
        image.paste(image_lines, (0, 0), image_lines)

        # add icon marker
        for icon in filter(lambda m: isinstance(m, IconMarker), self.markers):
            position = (
                self._x_to_px(_lon_to_x(icon.coord[0], self.zoom))
                - icon.offset[0],  # type: ignore [union-attr]
                self._y_to_px(_lat_to_y(icon.coord[1], self.zoom))
                - icon.offset[1],  # type: ignore [union-attr]
            )
            image.paste(
                icon.img,  # type: ignore [union-attr]
                position,
                icon.img,  # type: ignore [union-attr]
            )


if __name__ == "__main__":
    static_map = StaticMap(300, 400, 10)
    line = Line([(13.4, 52.5), (2.3, 48.9)], "blue", 3)
    static_map.add_line(line)
    image = static_map.render()
    image.save("berlin_paris.png")
