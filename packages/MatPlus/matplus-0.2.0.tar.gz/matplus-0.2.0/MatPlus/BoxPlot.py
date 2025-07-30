import matplotlib.pyplot as plt
import numpy as np
import math


class BoxPlot:
    """
    A class for creating box plots with customizable properties.

    The BoxPlot class provides a simplified interface for creating box plots
    with options for notches, outlier symbols, and orientation.

    Parameters
    ----------
    data : array-like
        The data to be plotted.
    notch : bool, optional
        Whether to draw a notch to indicate the confidence interval around the median.
        Default is False.
    symbol : str, optional
        The symbol for outliers. Default is "b".
    vert : bool, optional
        Whether to draw the box plot vertically. Default is True.
    whisker_length : float, optional
        The length of the whiskers as a multiple of the interquartile range (IQR).
        Default is 1.5.
    width : float, optional
        The width of the plot. Default is 3. Effects auto ticks.
    height : float, optional
        The height of the plot. Default is 3. Effects auto ticks.
    title : str, optional
        The title of the plot. Default is None.
    xlabel : str, optional
        The x-axis label. Default is None.
    ylabel : str, optional
        The y-axis label. Default is None.

    Examples
    --------
    >>> # Basic box plot
    >>> data = [1, 2, 2, 3, 3, 3, 4, 4, 5, 6]
    >>> box = BoxPlot(data)
    >>> box.plot()

    >>> # Box plot with notches
    >>> box = BoxPlot(data, notch=True)
    >>> box.plot()

    >>> # Horizontal box plot with custom outlier symbols
    >>> box = BoxPlot(data, vert=False, symbol="r*")
    >>> box.plot()
    """

    def __init__(
        self,
        data,
        notch=False,
        symbol="b",
        vert=True,
        whisker_length=1.5,
        width=3,
        height=3,
        title=None,
        xlabel=None,
        ylabel=None,
    ):
        # Validate data type
        if not isinstance(data, (list, np.ndarray)):
            raise TypeError("Data must be a list or numpy array")

        # Validate numeric data
        try:
            numeric_data = [float(x) for x in data]
        except (ValueError, TypeError):
            raise TypeError("All elements must be numeric")

        # Validate data length
        if not data or len(data) == 0:
            raise ValueError("Data array cannot be empty")

        # Validate whisker_length parameter
        if whisker_length <= 0:
            raise ValueError("Whisker length must be positive")

        self.data = numeric_data
        self.notch = notch
        self.symbol = symbol
        self.vert = vert
        self.whisker_length = whisker_length
        self.width = width
        self.height = height
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

    # Rest of the class implementation remains the same
    def median(self):
        """
        Calculate the median of the data.

        Returns
        -------
        float
            The median value of the dataset.
        """
        return float(np.median(self.data))

    def quartiles(self):
        """
        Calculate the first and third quartiles of the data.

        Returns
        -------
        tuple
            A tuple containing (Q1, Q3) values.
        """
        q1 = float(np.percentile(self.data, 25))
        q3 = float(np.percentile(self.data, 75))
        return (q1, q3)

    def outliers(self):
        """
        Identify outliers using the whisker*IQR rule.

        Returns
        -------
        list
            A list of data points identified as outliers.
        """
        q1, q3 = self.quartiles()
        iqr = q3 - q1
        lower_bound = q1 - (self.whisker_length * iqr)
        upper_bound = q3 + (self.whisker_length * iqr)
        return [x for x in self.data if x < lower_bound or x > upper_bound]

    def plot(self):
        """
        Create and display the box plot.

        This method creates a matplotlib figure and plots the box plot
        with the specified properties. It applies settings such as orientation,
        notches, and outlier symbols as configured during initialization.

        Returns
        -------
        None
            The plot is displayed but not returned.
        """
        plt.style.use("_mpl-gallery")
        fig, ax = plt.subplots(figsize=(self.width, self.height))
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        # Set labels and ticks
        ax.set_xticks([])
        if self.vert:
            ax.set_yticks(
                np.arange(
                    min(self.data),
                    max(self.data) + 1,
                    step=1
                    + round(
                        1.5
                        * (
                            math.sqrt(max(self.data) - min(self.data))
                            / (self.height * self.height)
                        )
                    ),
                )
            )
        else:
            ax.set_xticks(
                np.arange(
                    min(self.data),
                    max(self.data) + 1,
                    step=1
                    + round(
                        3.5
                        * (
                            math.sqrt(max(self.data) - min(self.data))
                            / (self.width * self.width)
                        )
                    ),
                )
            )
        ax.boxplot(
            self.data,
            notch=self.notch,
            sym=self.symbol,
            vert=self.vert,
            whis=self.whisker_length,
        )

        # Adjust layout to prevent label clipping

        plt.show()
