
import ipyvuetify as v


class Snackbar(v.Snackbar):
    """
    A Snackbar to put in the app to display info messages or errors.
    """
    def __init__(self, text: str, **kwargs):
        """
        :param text: The text to put in the snackbar.
        """
        super().__init__(**kwargs)
            
        close_snackbar_button = v.Btn(
            class_="ma-0 pa-0",
            color="pink",
            text=True,
            children=["Close"],
        )
        close_snackbar_button.on_event("click", self.open_close)
        
        self.app = True
        self.v_model = False
        
        self.children = [
            v.Row(
                justify="space-between",
                align="center",
                children=[
                    v.Col(
                        children=[text],
                    ),
                    v.Col(
                        class_="pa-0",
                        cols=2,
                        children=[close_snackbar_button],
                    ),
                ],
            ),
        ]
    

    def open_close(self, widget, event, data):
        """
        Opens or closes the snackbar depending on its state.

        To be called by the "on_event" of a widget.
        """
        self.v_model = not self.v_model
   