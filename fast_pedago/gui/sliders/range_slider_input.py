from typing import List

import ipyvuetify as v
import ipywidgets as widgets


# Unfortunately it is impossible to link the v_model of the slider
# with two v_models of text fields, as it is done for the SliderInput,
# since it is impossible to get only a part of the list that is the
# range slider v_model.
class RangeSliderInput(v.Tooltip):
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
        range: float=0,
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
        
        # slider is an instance variable to be able to get the value of
        # its v_model from outside.
        self.slider = v.RangeSlider(
            v_model=range,
            max=max,
            min=min,
            step=step,
            dense=True,
            thumb_label="always",
            thumb_size=24,
            hide_details=True,
            class_="align-center pe-3",
        )
        
        self.v_slots=[{
            'name': 'activator',
            'variable': 'tooltip',
            'children': v.Row(
                v_bind="tooltip.attrs",
                v_on="tooltip.on",
                class_="pt-6",
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
                        children=[self.slider],
                    ),
                ],
            ),
        }]
        
        self.children=[
            tooltip
        ]