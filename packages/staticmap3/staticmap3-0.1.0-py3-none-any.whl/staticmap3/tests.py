from unittest import TestCase

from staticmap3.staticmap import _lat_to_y, _lon_to_x, _x_to_lon, _y_to_lat


class LonLatConversionTest(TestCase):
    def testLon(self) -> None:
        for lon in range(-180, 180, 20):
            for zoom in range(0, 10):
                x = _lon_to_x(lon, zoom)
                longitude = _x_to_lon(x, zoom)
                self.assertAlmostEqual(lon, longitude, places=5)

    def testLat(self) -> None:
        for lat in range(-89, 89, 2):
            for zoom in range(0, 10):
                y = _lat_to_y(lat, zoom)
                longitude = _y_to_lat(y, zoom)
                self.assertAlmostEqual(lat, longitude, places=5)
