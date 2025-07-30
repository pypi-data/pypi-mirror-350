import numpy as np
import matplotlib.pyplot as plt
from MatPlus.Histogram import Histogram


def test_histogram_creation():
    data = [1, 2, 3, 4, 5]
    hist = Histogram(data)
    assert hist.data == data
    assert hist.bins == 10
    assert hist.density is False
    assert hist.color is None


def test_histogram_with_parameters():
    data = [1, 2, 3, 4, 5]
    hist = Histogram(data, bins=20, density=True, color="blue")
    assert hist.bins == 20
    assert hist.density is True
    assert hist.color == "blue"


def test_histogram_with_numpy_array():
    data = np.array([1, 2, 3, 4, 5])
    hist = Histogram(data)
    assert np.array_equal(hist.data, data)
    assert hist.bins == 10


def test_histogram_plot():
    data = [1, 2, 3, 4, 5]
    hist = Histogram(data)
    # Just verify the plot method runs without error
    hist.plot()
    plt.close()  # Clean up plot


def test_histogram_plot_with_parameters():
    data = np.random.normal(0, 1, 100)
    hist = Histogram(data, bins=20, density=True, color="red")
    hist.plot()
    plt.close()  # Clean up plot


def test_single_value_data():
    data = [5]
    hist = Histogram(data)
    hist.plot()
    plt.close()  # Should work but produce a simple plot


def test_histogram_with_large_dataset():
    data = np.random.normal(0, 1, 10000)
    hist = Histogram(data, bins=50)
    hist.plot()
    plt.close()


def test_histogram_with_string_bins():
    data = [1, 2, 3, 4, 5]
    # Test with string bin parameter like 'auto', 'fd', 'doane', etc.
    hist = Histogram(data, bins="auto")
    hist.plot()
    plt.close()


def test_histogram_with_bin_array():
    data = [1, 2, 3, 4, 5]
    bin_edges = [0, 2, 5]
    hist = Histogram(data, bins=bin_edges)
    assert hist.bins == bin_edges
    hist.plot()
    plt.close()
