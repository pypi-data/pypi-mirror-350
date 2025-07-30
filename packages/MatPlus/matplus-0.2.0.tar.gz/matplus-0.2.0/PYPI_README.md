# MatPlus

[![CI/CD](https://github.com/ac-i2i-engineering/MatPlus/actions/workflows/test.yml/badge.svg)](https://github.com/ac-i2i-engineering/MatPlus/actions/workflows/test.yml)
[![Coverage](https://coveralls.io/repos/github/ac-i2i-engineering/MatPlus/badge.svg)](https://coveralls.io/github/ac-i2i-engineering/MatPlus)
[![Docs](https://github.com/ac-i2i-engineering/MatPlus/actions/workflows/docs.yml/badge.svg)](https://github.com/ac-i2i-engineering/MatPlus/actions/workflows/docs.yml)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://ac-i2i-engineering.github.io/MatPlus/)

MatPlus is a Python package that provides easy, convenient plotting capabilities built on top of matplotlib. It simplifies the creation of common visualization types with intuitive APIs.

## Installation

Install MatPlus using pip:

```bash
pip install MatPlus
```

## Quickstart
Bar Plot
```python
import numpy as np
from MatPlus import BarPlot

x = np.array([1, 2, 3, 4, 5])
y = np.array([10, 15, 7, 12, 9])

bar = BarPlot(x, y)
bar.plot()
```

Scatter Plot
```python
from MatPlus import ScatterPlot

x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

# Basic scatter plot
scatter = ScatterPlot(x, y)
scatter.plot()

# Scatter with custom sizes and colors
sizes = [10, 20, 30, 40, 50]
colors = [0.1, 0.5, 0.7, 0.9, 1.0]
scatter = ScatterPlot(x, y, sizes=sizes, colors=colors, vmin=0, vmax=1)
scatter.plot()
```

Line Plot
```python
from MatPlus import LinePlot

# Single line plot
x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]
line_plot = LinePlot(x, y)
line_plot.plot()

# Multiple line plot
x = [[1, 2, 3], [1, 2, 3, 4]]
y = [[1, 2, 3], [4, 3, 2, 1]]
line_plot = LinePlot(x, y, lowerlimx=0, upperlimx=5)
line_plot.plot()
```

Box Plot
```python
from MatPlus import BoxPlot

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
box = BoxPlot(data)
box.plot()
```

Histogram
```
from MatPlus import Histogram
import numpy as np

data = np.random.normal(0, 1, 1000)
hist = Histogram(data)
hist.plot()
```

## Documentation
For detailed API documentation, visit our [documentation site](https://ac-i2i-engineering.github.io/MatPlus/).

## Examples
For detailed examples of MatPlus usage in jupyter notebooks, please refer to the [examples in our GitHub](https://github.com/ac-i2i-engineering/MatPlus/tree/main/examples)