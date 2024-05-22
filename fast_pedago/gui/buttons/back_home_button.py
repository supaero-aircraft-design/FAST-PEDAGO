import ipyvuetify as v

class BackHomeButton(v.Btn):
    """
    A button with a home icon to redirect to home page

    :arg home_page: the function that changes the current children
        of the app to display the home page
    """

    def __init__(self, home_page, **kwargs):
        super().__init__(**kwargs)

        self.children = [
            v.Icon(children=["fa-home"])
        ]
        self.icon = True

        self.on_event("click", home_page)

