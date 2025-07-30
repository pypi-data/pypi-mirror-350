import numpy as np
from MatPlus.ScatterPlot import ScatterPlot


def test_scatterplot_initialization():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    scatter = ScatterPlot(x, y)

    assert scatter.x is x
    assert scatter.y is y
    assert scatter.lowerlimx == np.min(x) * 0.9
    assert scatter.lowerlimy == np.min(y) * 0.9
    assert scatter.upperlimx == np.max(x) * 1.1
    assert scatter.upperlimy == np.max(y) * 1.1


def test_scatterplot_custom_limits():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    scatter = ScatterPlot(x, y, lowerlimx=0, lowerlimy=0, upperlimx=6, upperlimy=6)

    assert scatter.lowerlimx == 0
    assert scatter.lowerlimy == 0
    assert scatter.upperlimx == 6
    assert scatter.upperlimy == 6


def test_scatterplot_sizes_colors():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    sizes = [10, 20, 30, 40, 50]
    colors = ["r", "g", "b", "y", "m"]
    scatter = ScatterPlot(x, y, sizes=sizes, colors=colors)

    assert scatter.sizes == sizes
    assert scatter.colors == colors


def test_scatterplot_plot():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    scatter = ScatterPlot(x, y)

    scatter.plot()  # This will display the plot, but we can't assert visual output in tests


def test_scatterplot_initialization():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    scatter = ScatterPlot(x, y)

    assert scatter.x is x
    assert scatter.y is y
    assert scatter.lowerlimx == np.min(x) * 0.9
    assert scatter.lowerlimy == np.min(y) * 0.9
    assert scatter.upperlimx == np.max(x) * 1.1
    assert scatter.upperlimy == np.max(y) * 1.1


def test_scatterplot_custom_limits():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    scatter = ScatterPlot(x, y, lowerlimx=0, lowerlimy=0, upperlimx=6, upperlimy=6)

    assert scatter.lowerlimx == 0
    assert scatter.lowerlimy == 0
    assert scatter.upperlimx == 6
    assert scatter.upperlimy == 6


def test_scatterplot_sizes_colors():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    sizes = [10, 20, 30, 40, 50]
    colors = ["r", "g", "b", "y", "m"]
    scatter = ScatterPlot(x, y, sizes=sizes, colors=colors)

    assert scatter.sizes == sizes
    assert scatter.colors == colors


def test_scatterplot_plot():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    scatter = ScatterPlot(x, y)

    scatter.plot()  # This will display the plot, but we can't assert visual output in tests


def test_scatterplot_vmin_vmax():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    colors = [0.1, 0.5, 0.7, 0.9, 1.0]
    scatter = ScatterPlot(x, y, colors=colors, vmin=0, vmax=1)

    assert scatter.colors == colors
    assert scatter.vmin == 0
    assert scatter.vmax == 1


def test_scatterplot_sizes():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    size = [3, 4, 5, 2, 1]
    # Explicitly provide empty sizes list but colors
    scatter = ScatterPlot(x, y, sizes=size, colors=[], vmin=0, vmax=1)

    assert len(scatter.colors) == 0
    assert scatter.sizes == size
    scatter.plot()


# Line 123 is likely in the range of setting axis properties
# Test with edge cases for axis limits
def test_scatterplot_integer_axis_limits():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    # Set very specific limits that will trigger different axis ticks behavior
    scatter = ScatterPlot(x, y, lowerlimx=1, upperlimx=5, lowerlimy=1, upperlimy=5)

    scatter.plot()


# Also test with only one data point, which might affect axis settings
def test_scatterplot_single_point():
    x = np.array([3])
    y = np.array([3])
    scatter = ScatterPlot(x, y)

    scatter.plot()


# Test with negative values which might affect axis calculations
def test_scatterplot_negative_values():
    x = np.array([-5, -3, -1, 0, 1, 3, 5])
    y = np.array([-3, -2, -1, 0, 1, 2, 3])
    scatter = ScatterPlot(x, y)

    scatter.plot()


# Test empty axis ranges to ensure proper handling
def test_scatterplot_equal_limits():
    x = np.array([1, 1, 1, 1, 1])  # All same x value
    y = np.array([1, 2, 3, 4, 5])
    scatter = ScatterPlot(x, y)

    scatter.plot()
