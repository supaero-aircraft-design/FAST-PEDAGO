import webbrowser

import plotly.graph_objects as go
import ipyvuetify as v


from . import Snackbar
from fast_pedago.utils.functions import _image_from_path
from fast_pedago.processes import PathManager


# Image files
N2_PNG = "n2.png"
N2_HTML = "n2.html"
XDSM_PNG = "xdsm.png"
XDSM_HTML = "xdsm.html"

# This is the value of the figure next to the inputs height
# This value for the height will only work for that particular definition of
# the back image. Which means it is not generic enough. If no height is
# specified however the widget will be too big for its container which is
# not very pretty.
# FIGURE_HEIGHT = 440


class ProcessGraphContainer(v.Col):
    """
    A container to display process figures, N2 and XDSM graphs.
    """

    def __init__(self, **kwargs):
        """
        :param configuration_file_path: the path to the configuration file
        needed to generated XDSM/N2 graphs.
        """
        super().__init__(**kwargs)

        self._generate_n2_xdsm()
        self._build_layout()
        self.to_MDA()

    def to_MDO(self):
        """
        Changes the buttons texts and the figure displayed to MDO
        """
        self._is_MDA = False
        self._specific_button.children = ["Objectives"]
        self._specific_button.tooltip = "Displays a graph of the evolution "
        "of the objective reached at each function call"
        self._display.children = [self._objectives_figure]

    def to_MDA(self):
        """
        Changes the buttons texts and the figure displayed to MDA
        """
        self._is_MDA = True
        self._specific_button.children = ["Residuals"]
        self._specific_button.tooltip = "Displays a graph of the evolution "
        "of residuals with the number of iterations"
        self._display.children = [self._residuals_figure]

    def set_loading(self, message):
        """
        Displays a loading screen with a message instead of a figure
        or N2/XDSM.

        :param message: a message to display
        """
        self._display_selection_buttons.v_model = 0
        self._display.children = [
            v.Col(
                children=[
                    v.Row(
                        class_="pt-8",
                        justify="center",
                        children=[
                            v.ProgressCircular(
                                indeterminate=True,
                                size=128,
                            ),
                        ],
                    ),
                    v.Row(
                        class_="pa-8",
                        justify="center",
                        children=[
                            v.Html(tag="div", children=[message]),
                        ],
                    ),
                ],
            ),
        ]

    def plot(self, iterations, main, limit):
        """
        Plots the graphs on the active figure

        :param iterations: the x axis values
        :param main: the main graph to plot (residuals/objectives), y axis
            values.
        :param limit: a limit to plot (threshold/minimum objective), y axis
            value.
        """
        if self._is_MDA:
            active_figure = self._residuals_figure
        else:
            active_figure = self._objectives_figure

        main_graph = active_figure.data[0]
        limit_graph = active_figure.data[1]

        main_graph.x = iterations
        main_graph.y = main

        limit_graph.x = iterations
        limit_graph.y = [limit for _ in iterations]

        self._display.children = [active_figure]

    # TODO: Implement the generation of the graphs
    def _generate_n2_xdsm(self):
        """
        Generate the N2 diagram and the XDSM, located them in data folder.
        Also, since the take a lot of time to generate, before actually
        generating them, we check if they exist.
        """

        # N2 and XDSM images are wrapped in a tooltip to indicate to click on
        # them.
        # This is because it is impossible to load directly the .html into a
        # frame (bugs)
        n2_image_path = PathManager.path_to("data", N2_PNG)
        n2_file_path = PathManager.path_to("data", N2_HTML)

        n2_image = _image_from_path(n2_image_path, max_height="60vh")
        n2_image.v_on = "tooltip.on"
        n2_image.on_event(
            "click",
            lambda *args: webbrowser.open_new_tab(n2_file_path),
        )

        self._n2_widget = v.Tooltip(
            contained=True,
            bottom=True,
            v_slots=[
                {
                    "name": "activator",
                    "variable": "tooltip",
                    "children": n2_image,
                }
            ],
            children=["Click me to open interactive N2 graph"],
        )

        xdsm_image_path = PathManager.path_to("data", XDSM_PNG)
        xdsm_file_path = PathManager.path_to("data", XDSM_HTML)

        xdsm_image = _image_from_path(xdsm_image_path, max_height="60vh")
        xdsm_image.v_on = "tooltip.on"
        xdsm_image.on_event(
            "click", lambda *args: webbrowser.open_new_tab(xdsm_file_path)
        )

        self._xdsm_widget = v.Tooltip(
            contained=True,
            bottom=True,
            v_slots=[
                {
                    "name": "activator",
                    "variable": "tooltip",
                    "children": xdsm_image,
                }
            ],
            children=["Click me to open interactive XDSM graph"],
        )

    def _build_layout(self):
        """
        Builds the layout of the graph visualization container
        """
        self.class_ = "pe-0"

        # TODO: Implement tooltip
        # By defining the buttons this way it is possible to change the button
        # group between MDA/MDO
        self._specific_button = v.Btn(
            children=["Residuals"],
            tooltip=(
                "Displays a graph of the evolution of residuals with the "
                "number of iterations"
            ),
        )

        self._display_selection_buttons = v.BtnToggle(
            v_model="toggle_exclusive",
            mandatory=True,
            dense=True,
            children=[
                self._specific_button,
                v.Btn(
                    children=["N2"],
                    tooltip="Displays the N2 diagram of the sizing process",
                ),
                v.Btn(
                    children=["XDSM"],
                    tooltip="Displays the XDSM diagram of the sizing process",
                ),
            ],
        )
        self._display_selection_buttons.on_event(
            "change",
            self._change_display,
        )

        self._residuals_figure = _ProcessFigure(
            main_scatter_name="Relative error",
            limit_scatter_name="Threshold",
            title="Evolution of the residuals",
            x_axes_label="Number of iterations",
            y_axes_label="Relative value of residuals",
        )

        self._objectives_figure = _ProcessFigure(
            main_scatter_name="Objective",
            limit_scatter_name="Optimized value",
            title="Evolution of the objective",
            x_axes_label="Number of function calls",
            y_axes_label="Objective value (10-4 kg)",
            is_log=False,
        )

        self.snackbar = Snackbar("Process ended!")

        # This is a container to avoid resetting all of the
        # GraphVisualizationContainer children when switching between MDA/MDO
        self._display = v.Container(class_="mx-auto pa-0")

        self.children = [
            v.Row(
                class_="pb-4 pt-2",
                justify="center",
                children=[
                    self._display_selection_buttons,
                ],
            ),
            v.Row(
                justify="space-around",
                align="center",
                no_gutters=True,
                children=[
                    v.Col(
                        children=[
                            self._display,
                        ],
                    ),
                ],
            ),
            self.snackbar,
        ]

    def _change_display(self, widget, event, data):
        """
        Changes the display to a figure, N2 or XDSM graph,
        or opens a web page with N2/XDSM graphs

        To be called by an "on_event" of an ipyvuetify widget
        """
        # None: Residuals/Objective 1: N2 2: N2(browser)
        # 3: XDSM 4: XDSM(browser)
        if data == 1:
            self._display.children = [self._n2_widget]

        elif data == 2:
            self._display.children = [self._xdsm_widget]

        else:
            if self._is_MDA:
                self._display.children = [self._residuals_figure]

            else:
                self._display.children = [self._objectives_figure]


class _ProcessFigure(go.FigureWidget):
    """
    A widget to prepare the layout used to plot residuals and
    objectives.
    """

    def __init__(
        self,
        main_scatter_name: str,
        limit_scatter_name: str,
        title: str,
        x_axes_label: str,
        y_axes_label: str,
        is_log: bool = True,
        **kwargs,
    ):
        """
        :param main_scatter_name: label for the main plot (residuals or
            objective).
        :param limit_scatter_name: label for the relative error threshold or
            the minimum objective reached.
        :param title: title of the plot.
        :param x_axes_label: label of the x axes.
        :param y_axes_label: label of the y axes.
        :param is_log: true if y is a log axis.
        """
        super().__init__(
            data=[
                go.Scatter(x=[], y=[], name=main_scatter_name),
                go.Scatter(x=[], y=[], mode="lines", name=limit_scatter_name),
            ],
            **kwargs,
        )

        self.update_layout(
            title_text=title,
            title_x=0.5,
            autosize=True,
            margin=go.layout.Margin(
                l=0,
                r=20,
                b=0,
                t=30,
            ),
        )
        self.update_xaxes(title_text=x_axes_label)
        if is_log:
            self.update_yaxes(
                title_text=y_axes_label,
                type="log",
                range=[-7.0, 1.0],
            )
        else:
            self.update_yaxes(
                title_text=y_axes_label,
                type="log",
            )
