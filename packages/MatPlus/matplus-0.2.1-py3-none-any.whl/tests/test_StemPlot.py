import numpy as np
from MatPlus.StemPlot import StemPlot


def test_stemplot_default():
    x = [1, 2, 3]
    y = [1, 2, 3]
    plot = StemPlot(x, y)
    assert plot.lowerlimx == 0.9 * np.min(x)
    assert plot.upperlimx == 1.1 * np.max(x)
    assert plot.lowerlimy == 0.9 * np.min(y)
    assert plot.upperlimy == 1.1 * np.max(y)
    assert plot.linefmt == "-"
    assert plot.markerfmt == "o"
    assert plot.basefmt == " "
    assert plot.orientation == "vertical"
    plot.plot()


def test_stemplot_with_limits():
    x = [1, 2, 3]
    y = [1, 2, 3]
    plot = StemPlot(x, y, lowerlimx=0, upperlimx=4, lowerlimy=0, upperlimy=4)
    assert plot.lowerlimx == 0
    assert plot.upperlimx == 4
    assert plot.lowerlimy == 0
    assert plot.upperlimy == 4
    plot.plot()


def test_stemplot_horizontal_orientation():
    x = [1, 2, 3]
    y = [1, 2, 3]
    plot = StemPlot(x, y, orientation="horizontal")
    assert plot.orientation == "horizontal"
    plot.plot()


def test_stemplot_vertical_orientation():
    x = [1, 2, 3]
    y = [1, 2, 3]
    plot = StemPlot(x, y, orientation="vertical")
    assert plot.orientation == "vertical"
    plot.plot()


def test_stemplot_custom_styles():
    x = [1, 2, 3]
    y = [1, 2, 3]
    plot = StemPlot(x, y, linefmt="r-", markerfmt="bs", basefmt="g-")
    assert plot.linefmt == "r-"
    assert plot.markerfmt == "bs"
    assert plot.basefmt == "g-"
    plot.plot()


def test_stemplot_empty_data():
    x = []
    y = []
    plot = StemPlot(x, y)
    assert plot.lowerlimx == 0
    assert plot.upperlimx == 0
    assert plot.lowerlimy == 0
    assert plot.upperlimy == 0


def test_stemplot_single_element():
    x = [1]
    y = [1]
    plot = StemPlot(x, y)
    assert plot.lowerlimx == 0.9
    assert plot.upperlimx == 1.1
    assert plot.lowerlimy == 0.9
    assert plot.upperlimy == 1.1
    plot.plot()


def test_stemplot_with_label():
    x = [1, 2, 3, 4]
    y = [1, 2, 3, 4]
    plot = StemPlot(x, y, label="Test Label")
    assert plot.label == "Test Label"
    plot.plot()


def test_stemplot_custom_stylesWithColors():
    x = [1, 2, 3]
    y = [1, 2, 3]
    plot = StemPlot(x, y, linefmt="g--", markerfmt="ro", basefmt="b-")
    assert plot.linefmt == "g--"  # green dashed line
    assert plot.markerfmt == "ro"  # red circle markers
    assert plot.basefmt == "b-"  # blue solid line
    plot.plot()


def test_stemplot_with_edge_cases():
    x = [0]
    y = [0]
    plot = StemPlot(x, y)
    assert plot.lowerlimx == 0
    assert plot.upperlimx == 0
    assert plot.lowerlimy == 0
    assert plot.upperlimy == 0
    plot.plot()
