
import ipyvuetify as v
import ipywidgets as widgets


class SliderInput(v.Tooltip):
    """
    A slider input with a text field for more input possibilities.
    The slider has an optional tooltip to display information.
    """
    def __init__(
        self,
        min: float=0,
        max: float=100,
        step: float=10,
        label: str=None,
        tooltip: str=None,
        value: float=0,
        **kwargs,
        ):
        """
        :param min: min value of the slider
        :param max: max value of the slider
        :param step: step between two slider values 
        :pram label: label to put before the slider
        :param tooltip: tooltip to show when label, slider,
            or text field is hovered
        :param value: initial value of the slider
        """
        super().__init__(**kwargs)
        
        text_field = v.TextField(
            v_model=value,
            class_="mt-0 pt-0",
            style_="width: 60px",
            variant="outlined",
            density="compact",
            hide_details=True,
            single_line=True,
        )
        
        # slider is an instance variable to be able to get the value of
        # its v_model from outside.
        self.slider = v.Slider(
            v_model=value,
            max=max,
            min=min,
            step=step,
            hide_details=True,
            class_="align-center pe-3",
        )

        # Link the values of the slider with the associated text field.
        # Since v_slots has an known issue in ipyvuetify, this is for 
        # now the best way to do it.
        widgets.jslink((self.slider,'v_model'),(text_field,'v_model'))
        
        self.v_slots=[{
            'name': 'activator',
            'variable': 'tooltip',
            'children': v.Row(
                v_bind="tooltip.attrs",
                v_on="tooltip.on",
                justify="center",
                children=[
                    v.Col(
                        class_="ps-8 pe-0 py-1",
                        cols=4,
                        children=[
                            v.Html(
                                tag="p",
                                children=[label],
                            ),
                        ],
                    ),
                    v.Col(
                        class_="ps-3 py-1",
                        children=[
                            v.Row(
                                children=[
                                    v.Col(
                                        class_="pa-0",
                                        cols=9,
                                        children=[self.slider],
                                    ),
                                    v.Col(
                                        class_="pa-0",
                                        children=[text_field],
                                    ),
                                ]
                            ),
                        ],
                    ),
                ],
            ),
        }]
        
        self.children=[
            tooltip
        ]