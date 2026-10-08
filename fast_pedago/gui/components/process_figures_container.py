import webbrowser

import ipyvuetify as v


from . import Snackbar
from fast_pedago.utils import _image_from_path, PathManager


# Image files
N2_PNG = "n2.png"
N2_HTML = "n2.html"
XDSM_PNG = "xdsm.png"
XDSM_HTML = "xdsm.html"


class ProcessFiguresContainer(v.Col):
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

    def to_MDA(self):
        """
        Changes the buttons texts and the figure displayed to MDA
        """
        self._is_MDA = True

    def set_loading(self, message):
        """
        Displays a loading screen with a message instead of a figure
        or N2/XDSM.

        :param message: a message to display
        """
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
            location="bottom",
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
            location="bottom",
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

        self._display_selection_buttons = v.BtnToggle(
            v_model=0,
            mandatory=True,
            density="compact",
            children=[
                v.Btn(
                    value=0,
                    children=["N2"],
                    tooltip="Displays the N2 diagram of the sizing process",
                ),
                v.Btn(
                    value=1,
                    children=["XDSM"],
                    tooltip="Displays the XDSM diagram of the sizing process",
                ),
            ],
        )
        self._display_selection_buttons.observe(
            self._change_display,
            names="v_model",
        )

        self.mdo_end_snackbar = Snackbar("Optimization ended.")
        self.mda_success_snackbar = Snackbar("Analysis converged successfully!")
        self.mda_failure_snackbar = Snackbar(
            "Analysis did not converged. Try again with more reasonable values."
        )
        self._snackbars = [
            self.mdo_end_snackbar,
            self.mda_failure_snackbar,
            self.mda_success_snackbar,
        ]

        # This is a container to avoid resetting all of the
        # GraphVisualizationContainer children when switching between MDA/MDO
        self._display = v.Container(class_="mx-auto pa-0")
        self._display.children = [self._n2_widget]

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
        ] + self._snackbars

    def _change_display(self, change):
        """
        Changes the display to a figure, N2 or XDSM graph,
        or opens a web page with N2/XDSM graphs

        To be called with "observe" method of a widget.
        """
        data = change["new"]

        # 0: N2 1: XDSM
        if data == 0:
            self._display.children = [self._n2_widget]

        elif data == 1:
            self._display.children = [self._xdsm_widget]

    def open_snackbar(self, snackbar_to_open: Snackbar):
        """
        Opens the chosen snackbar and closes the other one that may still be open.

        :param snackbar_to_open: the snackbar to open.
        """
        for snackbar in self._snackbars:
            if snackbar == snackbar_to_open:
                snackbar.display()
            else:
                snackbar.disappear()
