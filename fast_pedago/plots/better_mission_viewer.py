import plotly.graph_objects as go
from IPython.display import clear_output, display


from fastoad.gui import MissionViewer


class BetterMissionViewer(MissionViewer):
    def __init__(self):
        super().__init__()
        self.layout = {}

    def update_layout(self, layout: dict):
        """
        Modifies the figure layout.

        :param layout: a plotly layout dictionary as used in the standard plotly update_layout
            method.
        """
        self.layout = layout

    def _show_plot(self, change=None):
        """
        Updates and shows the plots
        """

        with self._output_widget:

            clear_output(wait=True)

            x_name = self._x_widget.value
            y_name = self._y_widget.value

            fig = None

            for mission_name in self.missions:

                if fig is None:
                    fig = go.Figure()
                x = self.missions[mission_name][x_name]
                y = self.missions[mission_name][y_name]

                scatter = go.Scatter(x=x, y=y, mode="lines", name=mission_name)

                fig.add_trace(scatter)

            fig.update_layout(
                title_text="Mission",
                title_x=0.5,
                xaxis_title=x_name,
                yaxis_title=y_name,
            )
            fig.update_layout(self.layout)

            fig = go.FigureWidget(fig)
            display(fig)
