# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets

from IPython.display import display, clear_output, HTML

from fast_pedago.buttons.github_links_buttons import (
    get_fast_oad_core_git_button,
    get_fast_oad_cs25_git_button,
    get_fast_oad_cs23_git_button,
)


class SensitivityAnalysisInterface:
    def __init__(self):

        self.main_menu = None

    def init_main_menu(self):

        title = widgets.HTML(
            value="<h1 style='text-align:center;font-weight:bold;font-family:Arial, "
            "sans-serif;font-size:28px;color:#003399;text-decoration:underline;'>FAST "
            "Overall Aircraft Design</h1> "
        )
        layout_title = widgets.Layout(
            align_items="center", justify_content="center", width="65%", height="50%"
        )

        image_path = "../BlockImage/Images/Wing.jpg"
        custom_css = f"""
                        .vbox-with-background {{
                            background-image: url("{image_path}");
                            background-size: cover;
                            background-position: center;
                            background-repeat: no-repeat;
                            width: 100%;
                            height: 100%;
                        }}
                        """

        # Creating and instantiating an info button
        info_button = widgets.Button(description="")
        info_button.icon = "fa-info-circle"
        info_button.layout.width = "auto"
        info_button.layout.height = "auto"

        output = widgets.Output()

        # Define what happens when you click on the info button
        def info_message(event):

            with output:

                clear_output(wait=True)

                print(
                    "Welcome to the training branch of FAST-OAD.\n"
                    "This is the main menu which can lead you to the different activities to be performed. You'll also "
                    "find some links to the source code of FAST-OAD and its plugins."
                )

        info_button.on_click(info_message)

        fast_core_git_button = get_fast_oad_core_git_button()
        fast_cs25_git_button = get_fast_oad_cs25_git_button()
        fast_cs23_git_button = get_fast_oad_cs23_git_button()

        box_buttons_git = widgets.HBox(
            children=[fast_core_git_button, fast_cs25_git_button, fast_cs23_git_button],
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                justify_content="center",
                align_items="center",
                width="100%",
                height="10%",
            ),
        )

        box1 = widgets.HBox(children=[title], layout=layout_title)
        box4 = widgets.Box(
            children=[info_button, output],
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                align_items="center",
                width="100",
                height="12%",
            ),
        )

        display(
            widgets.HTML(
                """
        <style>
        .custom-vbox {
            background-color: white;
        }
        </style>
        """
            )
        )

        self.main_menu = widgets.VBox(
            children=[box1, box_buttons_git, box4],
            layout=widgets.Layout(
                border="6px solid black",
                margin="100 20 50 100px",
                padding="10px",
                align_items="center",
                width="940px",
                height="665px",
                justify_content="center",
            ),
        )
        self.main_menu.add_class("vbox-with-background")

        display(HTML(f"<style>{custom_css}</style>"))

        # Returning the menu make it appear on the screen, else nothing happens
        return self.main_menu
