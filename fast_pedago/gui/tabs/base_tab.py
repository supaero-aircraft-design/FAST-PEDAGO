# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipyvuetify as v

class BaseTab(v.TabItem):
    def __init__(
        self, 
        configuration_file_path: str=None, 
        reference_input_file_path: str=None,
        working_directory_path: str=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        
        self.reference_input_file_path = reference_input_file_path
        self.configuration_file_path = configuration_file_path
        self.working_directory_path = working_directory_path