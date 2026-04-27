import np
import pytest
from weather.clustering import clustering_dbscan

from weather.utils import celsius_to_fahrenheit


class TestCelsiusToFahrenheit:
    def test_freezing_point(self):
        assert celsius_to_fahrenheit(0) == 32.0

    def test_boiling_point(self):
        assert celsius_to_fahrenheit(100) == 212.0

    def test_negative_forty(self):
        assert celsius_to_fahrenheit(-40) == -40.0

    def test_decimal_value(self):
        assert celsius_to_fahrenheit(37.5) == 99.5

    def test_absolute_zero(self):
        assert celsius_to_fahrenheit(-273.15) == pytest.approx(-459.67)

    def test_invalid_type_raises_error(self):
        with pytest.raises(TypeError):
            celsius_to_fahrenheit("not a number")


class test_clustering:
    def test_dbscan_labels():
        X = np.random.rand(50, 2)

        labels = clustering_dbscan(X, eps=0.5)

        assert len(labels) == 50
