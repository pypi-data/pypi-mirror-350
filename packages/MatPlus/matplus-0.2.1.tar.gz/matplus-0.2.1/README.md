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
```python
from MatPlus import Histogram
import numpy as np

data = np.random.normal(0, 1, 1000)
hist = Histogram(data)
hist.plot()
```

Stem Plot
```python
from MatPlus import StemPlot
import numpy as np

x = np.arange(0, 10)
y = np.sin(x)

stem = StemPlot(x, y)
stem.plot()
```

## Documentation
For detailed API documentation, visit our [documentation site](https://ac-i2i-engineering.github.io/MatPlus/).

## Examples
For detailed examples of MatPlus usage in jupyter notebooks, please refer to the [examples in our GitHub](https://github.com/ac-i2i-engineering/MatPlus/tree/main/examples)

## Contributing
Contributions are welcome, whether it is building new plots, fixing bugs, or writing documentation. Here's how to get started:

1. **Clone the repository:**

```bash
git clone https://github.com/ac-i2i-engineering/MatPlus.git
cd MatPlus
```

2. **Create and activate a virtual environment:**

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. **Install development dependencies:**

```bash
pip install -r requirements.txt
```

### Development Workflow
#### Pre-commit Hooks
We use pre-commit hooks to ensure code quality. Install them with:

```bash
pre-commit install
```

And run them with:

```bash
pre-commit run
```

This will automatically style your code before each commit.

#### Unit Testing
Run the test suite with pytest:

```bash
pytest
```

Our standard is 95% code coverage.

### Documentation
#### Adding Docstrings for Auto-documentation
To ensure your code is properly documented for auto-generation, follow these guidelines for adding docstrings to your MatPlus classes and methods:

#### Docstring Guidelines

To ensure consistency and support automatic documentation generation, MatPlus adheres to the NumPy-style docstring format. Contributors should follow these guidelines when writing docstrings for classes and methods:

#### General Structure

All classes and functions must have a descriptive docstring with clear sections:

- **Short Summary**: A concise one-line summary.
- **Extended Description**: (Optional) A more detailed explanation providing additional context or usage notes.
- **Parameters**: List all parameters with type annotations, optionality, defaults, and descriptions.
- **Returns**: Clearly state the type and description of the returned value(s).
- **Examples**: Include examples demonstrating common usage.

##### Example Template

```python
class ClassName:
    """
    Short summary of the class or method.

    Extended description if necessary, explaining the purpose and usage in more detail.

    Parameters
    ----------
    param1 : type
        Description of the first parameter.
    param2 : type, optional
        Description of the second parameter with default value if applicable. Default is value.

    Returns
    -------
    return_type
        Description of the return value.

    Examples
    --------
    >>> example_var = ClassName(param1, param2)
    >>> example_var.method()
    """

    def method(self, param1):
        """
        Short method summary.

        Parameters
        ----------
        param1 : type
            Description of parameter.

        Returns
        -------
        return_type
            Description of return value.

        Examples
        --------
        >>> instance = ClassName()
        >>> instance.method(param1)
        """
```

##### Additional Notes
- Use clear and direct language.
- Maintain consistency in formatting, indentation, and spacing.
- Examples should be executable and demonstrate common usage scenarios.

Following this structure ensures clarity and helps automate documentation generation effectively.

#### PR Workflow

To contribute effectively to MatPlus, follow this Pull Request (PR) workflow:

1. **Fork the Repository**:
   - Fork the MatPlus repository to your GitHub account.

2. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   Use descriptive branch names, such as `feature/bar-plot-enhancement` or `fix/scatter-plot-bug`.

3. **Make Your Changes**:
   - Implement your feature or fix.
   - Follow coding standards and ensure documentation consistency.
   - Update the [changelog](./CHANGELOG.md) describing your changes. This is only necessary for new features, not bug fixes or minor changes.

4. **Run Tests Locally**:
   ```bash
   pytest
   ```
   - Ensure your changes pass all tests and meet the minimum coverage requirement (95%).

5. **Commit and Push Your Changes**:
   ```bash
   git add .
   git commit -m "Detailed description of your changes"
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**:
   - Navigate to your forked repository on GitHub.
   - Click on "Compare & pull request".
   - Provide a clear and detailed description of the changes you've made.
   - Reference any relevant issues.

7. **Code Review**:
   - Address review comments promptly and update your PR accordingly.

8. **Merge and Clean Up**:
   - Once approved and merged, delete your feature branch.

Following this workflow helps maintain a streamlined and efficient collaboration process.

## License
This project is licensed under the MIT License - see the LICENSE file for details.