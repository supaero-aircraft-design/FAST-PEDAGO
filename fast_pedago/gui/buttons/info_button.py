# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipyvuetify as v

MAIN_MENU_TOOLTIP = (
            "Welcome to the training branch of FAST-OAD.\n This is the main menu which can lead you "
            "to the different activities to be performed. You'll also find some links to the source "
            "code of FAST-OAD and its plugins."
        )

SENSITIVITY_ANALYSIS_TOOLTIP = (
        "This is the sensitivity analysis part of the training branch.\n"
        "In this part, you'll study the influence of a few select aircraft design "
        "parameters on the mass, aerodynamics and performances of the aircraft "
    )

SINGLE_PROCESS_SELECTION_TOOLTIP = (
        "- Select a sizing process in the dropdown menu to make the corresponding display appear \n"
        '- Select "None" to clear the display'
    )

MULTIPLE_PROCESS_SELECTION_TOOLTIP = (
        "- Select a sizing process in the dropdown menu to add the corresponding aircraft to the "
        "display  \n"
        '- Select "None" to clear the display'
    )

class BaseInfoButton(v.Tooltip):
    """
    An information "button" that is not clickable but shows custom informations when hovered

    :arg tooltip: The tooltip that is displayed when the button is hovered
    """
    
    def __init__(self, tooltip, **kwargs):
        super().__init__(**kwargs)

        self.button = v.Btn(
            children = [v.Icon(children=["fa-info-circle"])],
            icon = True,
            disabled = True
        )
        
        self.top = True
        self.max_width = "50%"

        # The button has to be encapsulated by the tooltip 
        self.v_slots = [{
            'name': 'activator',
            'variable': 'tooltip',
            'children': v.Html(
                tag="div", 
                v_on = 'tooltip.on',
                class_ = "d-inline-block",
                children=[self.button]
            ),
        }]
        self.children = [tooltip]
        

class MainMenuInfoButton(BaseInfoButton):

    def __init__(self, **kwargs):
        super().__init__(MAIN_MENU_TOOLTIP, **kwargs)

class SensitivityAnalysisInfoButton(BaseInfoButton):

    def __init__(self, **kwargs):
        super().__init__(SENSITIVITY_ANALYSIS_TOOLTIP, **kwargs)

class SingleProcessSelectionInfoButton(BaseInfoButton):

    def __init__(self, **kwargs):
        super().__init__(SINGLE_PROCESS_SELECTION_TOOLTIP, **kwargs)

class MultipleProcessSelectionInfoButton(BaseInfoButton):

    def __init__(self, **kwargs):
        super().__init__(MULTIPLE_PROCESS_SELECTION_TOOLTIP, **kwargs)