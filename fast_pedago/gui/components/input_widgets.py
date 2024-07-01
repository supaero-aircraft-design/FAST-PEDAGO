"""
Contains input widgets presets such as buttons, selection dropdowns or sliders. 
"""

import ipywidgets as widgets
import ipyvuetify as v


GITHUB_FAST_CORE = "https://github.com/fast-aircraft-design/FAST-OAD"
GITHUB_FAST_CS25 = "https://github.com/fast-aircraft-design/FAST-OAD_CS25"
GITHUB_FAST_CS23 = "https://github.com/supaero-aircraft-design/FAST-GA"


class ClearAllButton(v.Tooltip):
    """
    A button with a trash icon to clear all the input/output files
    in the work directory that are not the reference aircraft files.

    The button displays a tooltip to inform the user of the behavior
    of the button.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.button = v.Btn(
            v_on = 'tooltip.on', 
            x_large=True,
            icon = True,
            color = 'error', 
            children = [
                v.Icon(children=["fa-trash"])
            ]
        )
        
        self.bottom = True

        # The button has to be encapsulated by the tooltip 
        self.v_slots = [{
            'name': 'activator',
            'variable': 'tooltip',
            'children': self.button
        }]
        self.children = ['Press this button to clear ALL results generated by running this app.']



class GitLinksButton(v.Menu):
    """
    A github icon button that expands to show links to 
    FAST-OAD githubs.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.offset_y = True
        self.rounded = True
        self.open_on_hover = True
        self.v_slots = [{
            "name": "activator",
            "variable": "button",
            "children": v.Btn(
                v_bind="button.attrs",
                v_on="button.on",
                icon=True,
                x_large=True,
                children=[
                    v.Icon(
                        x_large=True,
                        children=["fa-github"],
                    ),
                ],
            ),   
        }]
        self.children = [
            v.List(
                class_="pa-0",
                children=[
                    _GitLinkButtonItem(GITHUB_FAST_CORE, "FAST-OAD_core"),
                    _GitLinkButtonItem(GITHUB_FAST_CS25, "FAST-OAD_cs25"),
                    _GitLinkButtonItem(GITHUB_FAST_CS23, "FAST-OAD_cs23"),
                ],
            ),
        ]


class _GitLinkButtonItem(v.ListItem):
    """
    A button that is clickable and opens the github link provided.
    It is made to be used with GitLinksButton.
    """
    def __init__(self, href, text, **kwargs):
        """
        :param href: The url to the web page to open.
        :param text: The text of the button.
        """
        super().__init__(**kwargs)

        self.class_ = "pa-0"
        self.children = [
            v.Btn(
                text=True,
                href=href,
                children=[
                    text,
                ],
            ),
        ]



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
        close_snackbar_button.on_event("click", self.open_or_close)
        
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
    
    def open_or_close(self, widget, event, data):
        """
        Opens or closes the snackbar depending on its state.

        To be called by the "on_event" of a widget.
        """
        self.v_model = not self.v_model



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
        
        self.text_field = v.TextField(
            v_model=value,
            class_="mt-0 pt-0",
            style_="width: 60px",
            variant="outlined",
            density="compact",
            hide_details=True,
            single_line=True,
        )
        
        # Slider is an instance variable to be able to get the value of
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
        widgets.jslink((self.slider,'v_model'),(self.text_field,'v_model'))
        
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
                                        children=[self.text_field],
                                    ),
                                ]
                            ),
                        ],
                    ),
                ],
            ),
        }]
        
        self.children=[
            tooltip,
        ]


    def disable(self):
        self.slider.readonly = True
        self.text_field.readonly = True

    
    def enable(self):
        self.slider.readonly = False
        self.text_field.readonly = False



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
        
        # Unfortunately it is impossible to link the v_model of the slider
        # with two v_models of text fields, as it is done for the SliderInput,
        # since it is impossible to get only a part of the list that is the
        # range slider v_model.
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
            tooltip,
        ]


    def disable(self):
        self.slider.readonly = True


    def enable(self):
        self.slider.readonly = False



class SelectOutput(v.Select):
    """
    A dropdown to select what output aircraft to plot.
    """
    def __init__(self, is_single_output=False, **kwargs):
        """
        :param is_single_output: True if the selection only authorize a
            single output file. Will change the way the dropdown works.
        """
        super().__init__(**kwargs)
        
        self.outlined = True
        self.clearable = True
        self.hide_details = True
        
        if is_single_output:
            self.label = "Select a main output file to display"
        else:
            self.label = "Select output files for comparison"
            self.multiple = True
            self.chips = True
            self.deletable_chips = True
            self.hide_selected = True