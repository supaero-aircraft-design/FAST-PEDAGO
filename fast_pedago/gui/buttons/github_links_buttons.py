# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipyvuetify as v

GITHUB_FAST_CORE = "https://github.com/fast-aircraft-design/FAST-OAD"
GITHUB_FAST_CS25 = "https://github.com/fast-aircraft-design/FAST-OAD_CS25"
GITHUB_FAST_CS23 = "https://github.com/supaero-aircraft-design/FAST-GA"


class BaseGitButton(v.Btn):
    """
    A button with a git icon that is clickable and opens the link provided

    :arg href: The url to the web page to open
    """
    
    def __init__(self, href, text, **kwargs):
        super().__init__(**kwargs)

        self.href = href

        self.children = [
            v.Icon(
                class_ = "me-2",
                children = ["fa-github"]
            ),
            text,
        ]

class FastOadCoreGitButton(BaseGitButton):
    def __init__(self, **kwargs):
        super().__init__(GITHUB_FAST_CORE, "FAST-OAD_core", **kwargs)

class FastOadCS25GitButton(BaseGitButton):
    def __init__(self, **kwargs):
        super().__init__(GITHUB_FAST_CS25, "FAST-OAD_cs25", **kwargs)

class FastOadCS23GitButton(BaseGitButton):
    def __init__(self, **kwargs):
        super().__init__(GITHUB_FAST_CS23, "FAST-OAD_cs23", **kwargs)