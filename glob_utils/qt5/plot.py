from abc import ABC, abstractmethod
import logging
from typing import Any, Callable
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
import matplotlib.pyplot
from PyQt5.QtWidgets import QVBoxLayout
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


class Plotter(ABC):

    _allowed_data_type: tuple = ()
    _plotting_func: Callable = None

    def __init__(self) -> None:
        """Create a plotter which plot defined type of data using predefined
        plotting function
        """
        super().__init__()
        self._allowed_data_type = ()
        self._post_init_()

    @abstractmethod
    def _post_init_(self):
        """Initialization of each custom Plotter
        here should _allowed_data_type and _plotting_func be defined"""

    def build(self, fig: Figure, data: Any, labels:Any= None):
        """Build the layout of the figure with the data

        Args:
            fig (matplotlib.pyplot.Figure): figure were to plot
            data (Data2Plot): data to plot
        """

        if not isinstance(fig, Figure):
            return

        if not isinstance(data, self._allowed_data_type):
            return

        fig.clear()  # clear figure

        self._build(fig, data, labels)

    @abstractmethod
    def _build(self, fig: Figure, data: Any, labels: dict= None):
        """Custom layout build of each custom Plotter"""

class CanvasLayout(object):

    _figure = None
    _canvas = None
    _toolbar = None
    _plotter: Plotter = None
    _visible: bool = True
    _gui = None
    _last_data: Any = None

    def __init__(self, gui, layout: QVBoxLayout, plotter: Plotter) -> None:
        """Create a CanvasLayout object with predefined plotter,
        which build a prefdined gaph layout

        Args:
            gui (_type_): obj in whcoh the layout is defined
            layout (QVBoxLayout): layout where the plotter
            should plot
            plotter(Plotter): predefined layout plotter

        Raises:
            TypeError: is raised if layout is not "QVBoxLayout",
            or if layout_type is not "CustomLayout"
        """

        if not isinstance(layout, QVBoxLayout):
            raise TypeError("wrong layout type")

        if not issubclass(plotter, Plotter):
            raise TypeError(f"wrong plot type {plotter}")

        self._gui = gui
        self._layout = layout
        self._plotter = plotter()
        self._init_layout()

    def _init_layout(self, **kwargs):
        """"""
        dpi = kwargs.pop("dpi", 100)
        self._figure = matplotlib.pyplot.figure(dpi=dpi)
        self._canvas = FigureCanvasQTAgg(self._figure)
        self._toolbar = NavigationToolbar2QT(self._canvas, self._gui)
        self._layout.addWidget(self._toolbar)
        self._layout.addWidget(self._canvas)
        self.clear_canvas()

    def set_options(self, **kwargs):
        """Set some plotting options
        valid kwargs:
        dpi= val"""
        if dpi := kwargs.pop("dpi", None):
            self._layout.removeWidget(self._toolbar)
            self._layout.removeWidget(self._canvas)
            self._init_layout(dpi=dpi)

        if self._last_data:
            self.plot(self._last_data)

    def set_visible(self, visible: bool = True):
        """Make the Canvas visible or insisible"""
        self._visible = visible
        if not self._visible:
            self.clear_canvas()

    def clear_canvas(self):
        """Make the Canvas visible or insisible"""
        self._figure.clear()
        self._canvas.draw()

    def plot(self, data: Any, labels:Any= None):
        """Plot the data"""
        if not self._visible:
            self.clear_canvas()
            return
        
        self._plotter.build(self._figure, data, labels)
        self._last_data = data
        self._canvas.draw()



if __name__ == "__main__":
    """"""
