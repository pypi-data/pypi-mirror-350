import numpy as np
from MatPlus.BarPlot import BarPlot


def test_barplot_initialization():
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    barplot = BarPlot(x, y)

    assert np.array_equal(barplot.x, x)
    assert np.array_equal(barplot.y, y)
    assert barplot.lowerlimx == np.min(x) * 0.9
    assert barplot.lowerlimy == np.min(y) * 0.9
    assert barplot.upperlimx == np.max(x) * 1.1
    assert barplot.upperlimy == np.max(y) * 1.1
    assert barplot.barwidth == 1
    assert barplot.linewidth == 1


def test_barplot_custom_limits():
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    barplot = BarPlot(x, y, lowerlimx=0, lowerlimy=3, upperlimx=4, upperlimy=7)

    assert barplot.lowerlimx == 0
    assert barplot.lowerlimy == 3
    assert barplot.upperlimx == 4
    assert barplot.upperlimy == 7


def test_barplot_custom_width_linewidth():
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    barplot = BarPlot(x, y, barwidth=0.5, linewidth=2)

    assert barplot.barwidth == 0.5
    assert barplot.linewidth == 2


def test_barplot_plot():
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    barplot = BarPlot(x, y)

    barplot.plot()
