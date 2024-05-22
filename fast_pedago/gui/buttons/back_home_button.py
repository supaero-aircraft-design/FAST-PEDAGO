import ipywidgets as widgets


class BackHomeButton(widgets.Button):

    def __init__(self, next_page, **kwargs):
        super().__init__(**kwargs)

        self.icon = "fa-home"
        self.layout.width = "auto"
        self.layout.height = "auto"

        self.on_click(next_page)

