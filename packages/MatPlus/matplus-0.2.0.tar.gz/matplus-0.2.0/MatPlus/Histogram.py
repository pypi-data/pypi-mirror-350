from matplotlib import pyplot as plt


class Histogram:
    """
    A class for creating histogram plots using matplotlib.

    The Histogram class provides a simplified interface for creating histogram plots
    with customizable bins, density normalization, and colors.

    Parameters
    ----------
    data : array-like
        The data to be displayed in the histogram.
    bins : int or sequence or str, optional
        Number of bins, sequence of bin edges, or binning strategy.
        Default is 10.
    density : bool, optional
        If True, the histogram is normalized to form a probability density.
        The area under the histogram will sum to 1.
        Default is False.
    color : str or tuple, optional
        Color for all the elements of the histogram. Can be a string
        specifying a color name or a RGB tuple.
        Default is None (uses matplotlib default color).

    Examples
    --------
    >>> # Basic histogram with default settings
    >>> import numpy as np
    >>> data = np.random.normal(0, 1, 1000)
    >>> hist = Histogram(data)
    >>> hist.plot()

    >>> # Custom histogram with specific bins and normalization
    >>> data = [1, 2, 2, 3, 3, 3, 4, 5, 5]
    >>> hist = Histogram(data, bins=5, density=True, color='blue')
    >>> hist.plot()

    >>> # Histogram with custom bin edges
    >>> hist = Histogram(data, bins=[0, 2, 3, 6], color='green')
    >>> hist.plot()

    """

    def __init__(
        self,
        data,
        bins=10,
        density=False,
        color=None,
        width=3,
        height=3,
        title=None,
        xlabel=None,
        ylabel=None,
    ):
        self.data = data
        self.bins = bins
        self.density = density
        self.color = color
        self.width = width
        self.height = height
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

    def plot(self):
        """
        Create and display a histogram.

        This method creates a matplotlib figure and plots the histogram
        using the data and parameters provided during initialization.
        The histogram is displayed using matplotlib's plt.show() function.

        Returns
        -------
        None
            The plot is displayed but not returned.

        """
        plt.figure(figsize=(self.width, self.height))
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.hist(self.data, bins=self.bins, density=self.density, color=self.color)
        plt.show()
