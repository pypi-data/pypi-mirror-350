import matplotlib.pyplot as plt
import numpy as np
import math


class ScatterPlot:
    """
    A class for creating scatter plots with customizable properties.

    The ScatterPlot class provides a simplified interface for creating scatter plots
    with customizable axis limits and point properties such as sizes and colors.

    Parameters
    ----------
    x : array-like
        The x-coordinates of the data points.
    y : array-like
        The y-coordinates of the data points.
    lowerlimx : float, optional
        Lower limit of the x-axis. Default is None (auto-determined as 90% of minimum x).
    lowerlimy : float, optional
        Lower limit of the y-axis. Default is None (auto-determined as 90% of minimum y).
    upperlimx : float, optional
        Upper limit of the x-axis. Default is None (auto-determined as 110% of maximum x).
    upperlimy : float, optional
        Upper limit of the y-axis. Default is None (auto-determined as 110% of maximum y).
    sizes : array-like, optional
        The sizes of the data points. Default is empty list (uses default size).
    colors : array-like, optional
        The colors of the data points. Default is empty list (uses default color).
    vmin : float, optional
        The minimum value for color scaling. Default is 0.
    vmax : float, optional
        The maximum value for color scaling. Default is 0.
    width : float, optional
        The width of the plot. Default is 1.

    Examples
    --------
    >>> # Basic scatter plot
    >>> x = [1, 2, 3, 4, 5]
    >>> y = [1, 4, 9, 16, 25]
    >>> scatter = ScatterPlot(x, y)
    >>> scatter.plot()

    >>> # Scatter plot with custom point sizes
    >>> scatter = ScatterPlot(x, y, sizes=[10, 20, 30, 40, 50])
    >>> scatter.plot()

    >>> # Scatter plot with colored points
    >>> scatter = ScatterPlot(x, y, colors=[0.1, 0.5, 0.7, 0.9, 1.0], vmin=0, vmax=1)
    >>> scatter.plot()
    """

    def __init__(
        self,
        x,
        y,
        lowerlimx=None,
        lowerlimy=None,
        upperlimx=None,
        upperlimy=None,
        sizes=[],
        colors=[],
        vmin=0,
        vmax=0,
        width=1,
    ):
        self.type = type
        self.x = x
        self.y = y
        self.lowerlimx = lowerlimx
        self.lowerlimy = lowerlimy
        self.upperlimx = upperlimx
        self.upperlimy = upperlimy
        self.sizes = sizes
        self.colors = colors
        self.vmin = vmin
        self.vmax = vmax
        self.width = width

        # Set default axis limits if not provided
        # Lower limit for x-axis/y-axis
        if self.lowerlimx is None:
            self.lowerlimx = np.min(x) * 0.9
        if self.lowerlimy is None:
            self.lowerlimy = np.min(y) * 0.9
        # Upper limit for x-axis/y-axis
        if self.upperlimx is None:
            self.upperlimx = np.max(x) * 1.1
        if self.upperlimy is None:
            self.upperlimy = np.max(y) * 1.1

    def plot(self):
        """
        Create and display the scatter plot.

        This method creates a matplotlib figure and plots the data
        points provided during initialization with the specified properties.
        It applies all configured settings such as point sizes, colors,
        and axis limits before displaying the plot.

        Returns
        -------
        None
            The plot is displayed but not returned.
        """
        # Plots the scatter plot with the given parameters
        fig, ax = plt.subplots()

        # Plot scatter plot with sizes and colors if both are provided
        if len(self.sizes) != 0 and len(self.colors) != 0:
            ax.scatter(
                self.x,
                self.y,
                s=self.sizes,
                c=self.colors,
                vmin=self.vmin,
                vmax=self.vmax,
            )

        # Plot scatter plot with sizes if only sizes are provided
        elif len(self.sizes) != 0:
            ax.scatter(self.x, self.y, s=self.sizes, vmin=self.vmin, vmax=self.vmax)
        # Plot scatter plot with default size if neither sizes nor colors are provided
        else:
            ax.scatter(self.x, self.y, s=20, vmin=self.vmin, vmax=self.vmax)
        # Set labels for the x-axis and y-axis"""
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        # Set limits and ticks for the x-axis and y-axis"""
        ax.set(
            xlim=(self.lowerlimx, self.upperlimx),
            xticks=np.arange(
                self.lowerlimx,
                self.upperlimx + 1,
                step=1
                + round(
                    1.5
                    * (
                        math.sqrt(self.upperlimx - self.lowerlimx)
                        / (self.width * self.width * 5)
                    )
                ),
            ),
            ylim=(self.lowerlimy, self.upperlimy),
            yticks=np.arange(
                self.lowerlimy,
                self.upperlimy + 1,
                step=1
                + round(
                    1.5
                    * (
                        math.sqrt(self.upperlimy - self.lowerlimy)
                        / (self.width * self.width * 5)
                    )
                ),
            ),
        )
        # Display the plot
        plt.show()
