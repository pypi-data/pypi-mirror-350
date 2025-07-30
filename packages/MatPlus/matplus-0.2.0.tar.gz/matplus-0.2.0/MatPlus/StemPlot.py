import matplotlib.pyplot as plt
import numpy as np


class StemPlot:
    """
    A class for creating Stem plots with customizable properties.
    The StemPlot class provides a simplified interface for creating stem plots
    with customizable axis limits and line properties such as line format, marker format,
    and base format.

    Parameters:
    ----------
    x : array-like
        The x-values of the stem plot.
    y : array-like
        The y-values of the stem plot.
    lowerlimx : float, optional
        The lower limit of the x-axis. Default is 90% of the minimum x-value.
    lowerlimy : float, optional
        The lower limit of the y-axis. Default is 90% of the minimum y-value.
    upperlimx : float, optional
        The upper limit of the x-axis. Default is 110% of the maximum x-value.
    upperlimy : float, optional
        The upper limit of the y-axis. Default is 110% of the maximum y-value.
    linefmt : str, optional
        Format string for the vertical lines in the stem plot. Default is '-'.
    markerfmt : str, optional
        Format string for the markers at the stem heads. Default is 'o'.
    basefmt : str, optional
        Format string for the baseline. Default is ' ' (invisible).
    label : str, optional
        Label for the stem plot. Default is None.
    orientation : str, optional
        Orientation of the stem plot, either 'vertical' or 'horizontal'. Default is 'vertical'.
    """

    def __init__(
        self,
        x,
        y,
        lowerlimx=None,
        lowerlimy=None,
        upperlimx=None,
        upperlimy=None,
        linefmt="-",
        markerfmt="o",
        basefmt=" ",
        label=None,  # Keep for backward compatibility but it won't be used
        orientation="vertical",
    ):
        self.x = np.array(x)
        self.y = np.array(y)
        self.lowerlimx = lowerlimx
        self.lowerlimy = lowerlimy
        self.upperlimx = upperlimx
        self.upperlimy = upperlimy
        self.linefmt = linefmt
        self.markerfmt = markerfmt
        self.basefmt = basefmt
        self.label = label
        self.orientation = orientation

        # Set default axis limits if not provided
        # Lower limit for x-axis/y-axis
        if lowerlimx is None:
            self.lowerlimx = 0.9 * min(self.x) if self.x.size > 0 else 0
        if lowerlimy is None:
            self.lowerlimy = 0.9 * min(self.y) if self.y.size > 0 else 0
        # Upper limit for x-axis/y-axis
        if upperlimx is None:
            self.upperlimx = 1.1 * max(self.x) if self.x.size > 0 else 0
        if upperlimy is None:
            self.upperlimy = 1.1 * max(self.y) if self.y.size > 0 else 0

    def plot(self):
        """
        Constructs all the necessary attributes for the StemPlot object.
        Plot the stem plot with the given parameters.
        """
        # Plots the stem plot with the given parameters.
        fig, ax = plt.subplots()

        if self.orientation == "vertical":
            ax.stem(
                self.x,
                self.y,
                linefmt=self.linefmt,
                markerfmt=self.markerfmt,
                basefmt=self.basefmt,
                label=self.label,
            )
            ax.set_xlim(self.lowerlimx, self.upperlimx)
            ax.set_ylim(self.lowerlimy, self.upperlimy)
        elif self.orientation == "horizontal":
            ax.stem(
                self.y,
                self.x,
                linefmt=self.linefmt,
                markerfmt=self.markerfmt,
                basefmt=self.basefmt,
                label=self.label,
            )
            ax.set_ylim(self.lowerlimx, self.upperlimx)
            ax.set_xlim(self.lowerlimy, self.upperlimy)

        if self.label:
            ax.legend()
        plt.show()
