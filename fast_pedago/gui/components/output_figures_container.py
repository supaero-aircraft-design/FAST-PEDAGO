import ipyvuetify as v

from .input_widgets import SelectOutput
from fast_pedago.plots import OutputGraphsPlotter, GRAPH
from fast_pedago.utils import PathManager


class OutputFiguresContainer(v.Col):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._build_layout()

    def _build_layout(self):
        """
        Builds the layout of the graph container : a selection widget and
        multiple graph sub-windows.
        """
        self.output_selection = SelectOutput()

        self._general_graph = _OutputGraph("General", is_full_screen=True)
        self._geometry_graph = _OutputGraph("Geometry")
        self._aerodynamics_graph = _OutputGraph("Aerodynamics")
        self._mass_graph = _OutputGraph("Mass")
        self._performances_graph = _OutputGraph("Performances")

        self.output_selection.on_event("click", self._browse_available_process)
        self.output_selection.on_event("change", self._update_data)
        self.hide_graphs()

        self.children = [
            v.Row(
                class_="px-4 pb-3",
                children=[self.output_selection],
            ),
            v.Row(
                class_="mb-12",
                align="top",
                children=[
                    self._geometry_graph,
                    self._mass_graph,
                    self._aerodynamics_graph,
                    self._performances_graph,
                    self._general_graph,
                ],
            ),
        ]

    def hide_graphs(self):
        """
        Hides graphs containers (for when no result file is selected).
        """
        self._general_graph.hide()
        self._geometry_graph.hide()
        self._aerodynamics_graph.hide()
        self._mass_graph.hide()
        self._performances_graph.hide()

    def show_graphs(self):
        """
        Re-displays graphs.
        """
        self._general_graph.show()
        self._geometry_graph.show()
        self._aerodynamics_graph.show()
        self._mass_graph.show()
        self._performances_graph.show()

    def _update_data(self, widget, event, data):
        """
        Updates the graphs when a new aircraft is selected or removed.
        If no aircraft is selected, hides the graphs.

        To be called with "on_event" method of a widget.
        """
        if data:
            self.show_graphs()

            self._general_graph.plotter.plot(data)
            self._geometry_graph.plotter.plot(data)
            self._aerodynamics_graph.plotter.plot(data)
            self._mass_graph.plotter.plot(data)
            self._performances_graph.plotter.plot(data)

        else:
            self.hide_graphs()

    def _browse_available_process(self, widget, event, data):
        """
        Updates the available aircraft that can be selected.

        To be called with "on_event" method of a widget.
        """
        self.output_selection.items = PathManager.list_available_process_results()


class _OutputGraph(v.Col):
    """
    A template for an output card, that can switch between figures
    of the same category.
    """

    def __init__(self, title, is_full_screen: bool = False, **kwargs):
        """
        :param title: The title of the card. Corresponds to a graph category.
        :param is_full_screen: if True, the card will take all the screen
            space.
        """
        super().__init__(**kwargs)

        # When full screen, displays by default on two columns, and only
        # one column on smaller screens.
        self.cols = 12
        if not is_full_screen:
            self.lg = 6

        self.plotter = OutputGraphsPlotter()
        select = v.Select(
            dense=True,
            hide_details=True,
            items=list(GRAPH[title]),
            v_model=list(GRAPH[title])[0],
        )
        select.on_event(
            "change",
            lambda widget, event, data: self.plotter.change_graph(title, data),
        )
        self.plotter.change_graph(title, list(GRAPH[title])[0])

        self.children = [
            v.Card(
                outlined=True,
                flat=True,
                children=[
                    v.CardTitle(
                        class_="pa-3",
                        children=[
                            v.Row(
                                no_gutters=True,
                                children=[
                                    v.Col(
                                        cols=6,
                                        children=[title],
                                    ),
                                    v.Col(
                                        children=[select],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    v.CardText(
                        class_="pa-0",
                        children=[self.plotter.output_display],
                    ),
                ],
            ),
        ]
