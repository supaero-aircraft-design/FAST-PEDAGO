# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

import webbrowser

import ipyvuetify as v

from fast_pedago.utils.functions import _image_from_path  # noqa
from fast_pedago.utils import (
    _Figure,
    _TooltipButton,
    FIGURE_HEIGHT,
)


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
        
        self.is_MDA = True
        
        self._set_layout()
        self.to_MDA()


    def to_MDO(self):
        """
        Changes the buttons texts and the figure displayed to MDO
        """
        self.is_MDA = False
        self.specific_button.update("Objectives", 
            tooltip="Displays a graph of the evolution of the objective reached at each function call"
        )
        # Modifies the selected button to display the process figure
        self.display_selection_buttons.v_model = 0
        
        self._resize_figures()
        self.display.children = [self.objectives_figure]


    def to_MDA(self):
        """
        Changes the buttons texts and the figure displayed to MDA
        """
        self.is_MDA = True
        self.specific_button.update("Residuals", 
            tooltip="Displays a graph of the evolution of residuals with the number of iterations"
        )
        self.display_selection_buttons.v_model = 0
        
        self._resize_figures()
        self.display.children = [self.residuals_figure]


    def set_loading(self, message):
        """
        Displays a loading screen with a message instead of a figure 
        or N2/XDSM.

        :param message: a message to display
        """
        self.display_selection_buttons.v_model = 0
        self.display.children = [
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
                            v.Html(
                                tag="div",
                                children=[message]
                            ),
                        ],
                    ),
                ],
            ),
        ]


    def plot(self, iterations, main, limit):
        """
        Plots the graphs on the active figure

        :param iterations: the x axis values
        :param main: the main graph to plot (residuals/objectives), y axis values
        :param limit: a limit to plot (threshold/minimum objective), y axis value
        """
        if self.is_MDA:
            active_figure = self.residuals_figure
        else:
            active_figure = self.objectives_figure
        
        main_graph = (active_figure.data[0])
        limit_graph = (active_figure.data[1])
        
        main_graph.x = iterations
        main_graph.y = main
        
        limit_graph.x = iterations
        limit_graph.y = [limit for _ in iterations]
        
        self.display.children = [active_figure]

    
    # TODO
    # Implement the generation of the graphs
    def generate_n2_xdsm(self, configuration_file_path: str):
        """
        Generate the N2 diagram and the XDSM, located them near the configuration file
        as in this case there are more data than actual results. 
        Also, since the take a lot of time to generate, before actually generating them, 
        we check if they exist
        
        :param configuration_file_path: path to the chosen configuration file 
        """
        configuration_file_name = pth.basename(configuration_file_path)
        
        self.n2_image_path = configuration_file_path.replace(
            configuration_file_name, "n2.png"
        )
        self.n2_file_path = configuration_file_path.replace(
            configuration_file_name, "n2.html"
        )
        self.n2_visualization_widget = _image_from_path(
            self.n2_image_path , max_height="70vh"
        )
        
        self.xdsm_image_path = configuration_file_path.replace(
            configuration_file_name, "xdsm.png"
        )
        self.xdsm_file_path = configuration_file_path.replace(
            configuration_file_name, "xdsm.html"
        )
        self.xdsm_visualization_widget = _image_from_path(
            self.xdsm_image_path, max_height="70vh"
        )
        
        
    def _set_layout(self):
        """
        Sets the layout of the graph visualization container
        """
        
        # By defining the buttons this way it is possible to change the button group between MDA/MDO
        self.specific_button = _TooltipButton("Residuals", 
            tooltip="Displays a graph of the evolution of residuals with the number of iterations"
        )
        
        self.display_selection_buttons = v.BtnToggle(
            v_model="toggle_exclusive",
            mandatory=True,
            children=[
                self.specific_button,
                _TooltipButton("N2", tooltip="Displays the N2 diagram of the sizing process"),
                _TooltipButton("N2 (browser)", tooltip="Displays the N2 diagram of the sizing process in a new browser tab"),
                _TooltipButton("XDSM", tooltip="Displays the XDSM diagram of the sizing process"),
                _TooltipButton("XDSM (browser)", tooltip="Displays the XDSM diagram of the sizing process in a new browser tab"),
            ]
        )
        self.display_selection_buttons.on_event("change", self._change_display)
        
        self.residuals_figure = _Figure(
            main_scatter_name="Relative error",
            limit_scatter_name="Threshold",
            title="Evolution of the residuals",
            x_axes_label="Number of iterations",
            y_axes_label="Relative value of residuals",
        )
        
        self.objectives_figure = _Figure(
            main_scatter_name="Objective",
            limit_scatter_name="Optimized value",
            title="Evolution of the objective",
            x_axes_label="Number of function calls",
            y_axes_label="Objective value",
            is_log=False,
        )
        
        # This is a container to avoid resetting all of the GraphVisualizationContainer
        # children when switching between MDA/MDO
        self.display = v.Row(
            justify="center",
        )
        
        self.children = [
            v.Row(
                class_="pb-4 pt-2",
                justify="center",
                children=[
                    self.display_selection_buttons,
                ],
            ),
            self.display,
        ]
    

    def _change_display(self, widget, event, data):
        """
        Changes the display to a figure, N2 or XDSM graph,
        or opens a web page with N2/XDSM graphs

        To be called by an "on_event" of an ipyvuetify widget
        """
        # None: Residuals/Objective 1: N2 2: N2(browser) 3: XDSM 4: XDSM(browser)
        if data == 1:
            self.display.children = [self.n2_visualization_widget]

        elif data == 2:
            webbrowser.open_new_tab(self.n2_file_path)

        elif data == 3:
            self.display.children = [self.xdsm_visualization_widget]

        elif data == 4:
            webbrowser.open_new_tab(self.xdsm_file_path)
        
        else:
            self._resize_figures()
            if self.is_MDA:
                self.display.children = [self.residuals_figure]
 
            else :
                self.display.children = [self.objectives_figure]


    def _resize_figures(self):
        """
        Resizes the figures to defined height in case it has been
        autosized.
        """
        # It looks like the fact that we switch back and forth between image
        # automatically resizes this FigureWidget so we'll ensure that the layout remains
        # consistent. Additionally, we have to resize before displaying or else,
        # for some reasons, the figure is suddenly too big every other time ...
        self.residuals_figure.update_layout(
            dict(height=FIGURE_HEIGHT, autosize=None)
        )
        self.objectives_figure.update_layout(
            dict(height=FIGURE_HEIGHT, autosize=None)
        )
