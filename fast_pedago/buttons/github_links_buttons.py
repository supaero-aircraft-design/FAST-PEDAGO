# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets

import webbrowser

GITHUB_FAST_CORE = "https://github.com/fast-aircraft-design/FAST-OAD"
GITHUB_FAST_CS25 = "https://github.com/fast-aircraft-design/FAST-OAD_CS25"
GITHUB_FAST_CS23 = "https://github.com/supaero-aircraft-design/FAST-GA"


def get_fast_oad_core_git_button():

    fast_core_git_button = widgets.Button(description="FAST-OAD_core")
    fast_core_git_button.icon = "fa-github"
    fast_core_git_button.layout.width = "auto"
    fast_core_git_button.layout.height = "auto"

    def open_github_fast_core(event):
        webbrowser.open_new_tab(GITHUB_FAST_CORE)

    fast_core_git_button.on_click(open_github_fast_core)

    return fast_core_git_button


def get_fast_oad_cs25_git_button():

    # TODO: Refactor those functions ?
    fast_cs25_git_button = widgets.Button(description="FAST-OAD_CS25")
    fast_cs25_git_button.icon = "fa-github"
    fast_cs25_git_button.layout.width = "auto"
    fast_cs25_git_button.layout.height = "auto"

    def open_github_fast_cs25(event):
        webbrowser.open_new_tab(GITHUB_FAST_CS25)

    fast_cs25_git_button.on_click(open_github_fast_cs25)

    return fast_cs25_git_button


def get_fast_oad_cs23_git_button():

    fast_cs23_git_button = widgets.Button(description="FAST-OAD_CS23")
    fast_cs23_git_button.icon = "fa-github"
    fast_cs23_git_button.layout.width = "auto"
    fast_cs23_git_button.layout.height = "auto"

    # Button to redirect to github repositories
    def open_github_fast_cs23(event):
        webbrowser.open_new_tab(GITHUB_FAST_CS23)

    fast_cs23_git_button.on_click(open_github_fast_cs23)

    return fast_cs23_git_button