# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipyvuetify as v

class BaseTab(v.TabItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)