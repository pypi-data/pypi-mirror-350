import matplotlib.pyplot as plt
import numpy as np
import math


class BarPlot:
    """
    A class for creating bar plots with customizable properties.

    The BarPlot class provides a simplified interface for creating bar plots
    with customizable axis limits and bar properties such as width and line weight.

    Parameters
    ----------
    x : array-like
        The x-coordinates of the bars.
    y : array-like
        The heights of the bars.
    lowerlimx : float, optional
        Lower limit of the x-axis. Default is None (auto-determined as 90% of minimum x).
    lowerlimy : float, optional
        Lower limit of the y-axis. Default is None (auto-determined as 90% of minimum y).
    upperlimx : float, optional
        Upper limit of the x-axis. Default is None (auto-determined as 110% of maximum x).
    upperlimy : float, optional
        Upper limit of the y-axis. Default is None (auto-determined as 110% of maximum y).
    barwidth : float, optional
        The width of the bars. Default is None (uses default width of 1).
    linewidth : float, optional
        The linewidth of the bar edges. Default is None (uses default linewidth of 1).
    xlabel : str, optional
        The x-axis label. Default is None.
    ylabel : str, optional
        The y-axis label. Default is None.
    title : str, optional
        The title of the plot. Default is None.

    Examples
    --------
    >>> # Basic bar plot
    >>> x = [1, 2, 3, 4, 5]
    >>> y = [10, 15, 7, 12, 9]
    >>> bar = BarPlot(x, y)
    >>> bar.plot()

    >>> # Bar plot with custom width and axis limits
    >>> bar = BarPlot(x, y, lowerlimx=0, upperlimx=6, barwidth=0.5)
    >>> bar.plot()

    >>> # Bar plot with custom linewidth
    >>> bar = BarPlot(x, y, linewidth=2)
    >>> bar.plot()
    """

    def __init__(
        self,
        x,
        y,
        lowerlimx=None,
        lowerlimy=None,
        upperlimx=None,
        upperlimy=None,
        barwidth=None,
        linewidth=None,
        xlabel=None,
        ylabel=None,
        title=None,
        height=3,
        width=3,
    ):
        self.x = x
        self.y = y
        self.lowerlimx = lowerlimx
        self.lowerlimy = lowerlimy
        self.upperlimx = upperlimx
        self.upperlimy = upperlimy
        self.title = title
        self.ylabel = ylabel
        self.xlabel = xlabel
        self.width = width
        self.height = height

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

        self.barwidth = barwidth
        self.linewidth = linewidth

        # Set default width and linewidth if not provided
        if self.linewidth is None:
            self.linewidth = 1
        if self.barwidth is None:
            self.barwidth = 1

    def plot(self):
        """
        Create and display the bar plot.

        This method creates a matplotlib figure and plots the data
        as bars with the specified properties. It applies all configured
        settings such as bar width, linewidth, and axis limits before
        displaying the plot.

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
        ax.bar(
            self.x,
            self.y,
            width=self.barwidth,
            edgecolor="black",
            linewidth=self.linewidth,
        )
        ax.set(
            xlim=(self.lowerlimx, self.upperlimx),
            xticks=np.linspace(self.lowerlimx, self.upperlimx, min(10, len(self.x))),
            ylim=(self.lowerlimy, self.upperlimy),
            yticks=np.arange(
                self.lowerlimy + 1,
                self.upperlimy,
                1
                + round(
                    3.5
                    * (
                        math.sqrt(self.upperlimy - self.lowerlimy)
                        / (self.height * self.height)
                    )
                ),
            ),
        )
        plt.show()
