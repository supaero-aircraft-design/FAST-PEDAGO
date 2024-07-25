import ipyvuetify as v

from fast_pedago.gui.resources import Slide
from fast_pedago.utils import _image_from_path, PathManager

# Image files
FAST_OAD_LOGO = "logo_fast_oad_main_menu.jpg"

INPUTS_GIF = "inputs.gif"
LAUNCH_GIF = "launch.gif"
N2_GIF = "n2.gif"
OUTPUTS_GIF = "outputs.gif"
MDA_FIGURE = "MDA.png"
MDO_FIGURE = "MDO.png"


class TutorialContainer(v.Col):
    """
    An container that contains explanations on the app and a source file
    selector to start using the app.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._load_images()
        self._build_layout()

    def _build_layout(self):
        """
        Builds the container layout : a tutorial, with the source selection
        widget at the bottom.
        """
        self.class_ = "pa-8"

        tutorial_carousel = v.Carousel(
            height="65vh",
            width="70vw",
            hide_delimiters=True,
            continuous=False,
            progress=True,
            children=[
                v.CarouselItem(
                    children=[
                        v.Row(
                            class_="mx-5",
                            justify="center",
                            align="center",
                            children=[
                                v.Html(
                                    style_="font-size: 20px; font-weight: bolder;",
                                    tag="div",
                                    children=[Slide.Introduction.WELCOME],
                                ),
                            ],
                        ),
                        v.Row(
                            class_="mx-5 mt-3",
                            justify="center",
                            children=[
                                v.Html(
                                    tag="div",
                                    children=[
                                        Slide.Introduction.EXPLANATIONS,
                                    ],
                                ),
                            ],
                        ),
                        v.Row(
                            class_="px-12",
                            justify="center",
                            align="center",
                            children=[
                                v.Html(
                                    tag="div",
                                    children=[Slide.Introduction.SELECTION],
                                ),
                            ],
                        ),
                        v.Row(
                            justify="center",
                            align="center",
                            children=[self._fast_oad_logo],
                        ),
                        v.Row(
                            class_="px-12",
                            justify="center",
                            align="center",
                            children=[
                                v.Html(
                                    tag="div",
                                    children=[Slide.Introduction.NOTA],
                                ),
                            ],
                        ),
                    ],
                ),
                v.CarouselItem(
                    children=[
                        v.Row(
                            class_="mx-3",
                            style_="font-size: 20px;",
                            justify="center",
                            children=[Slide.Process.GLOBAL],
                        ),
                        v.Row(
                            class_="pt-5",
                            children=[
                                v.Col(
                                    cols=6,
                                    children=[Slide.Process.MDA],
                                ),
                                v.Col(
                                    children=[Slide.Process.MDO],
                                ),
                            ],
                        ),
                        v.Row(
                            class_="pt-5",
                            no_gutters=True,
                            justify="center",
                            children=[
                                v.Col(
                                    cols=12,
                                    md=6,
                                    children=[self._mda_figure],
                                )
                            ],
                        ),
                    ],
                ),
                v.CarouselItem(
                    children=[
                        v.Row(
                            justify="center",
                            align="top",
                            children=[
                                v.Col(cols=2),
                                v.Col(
                                    cols=5,
                                    lg=4,
                                    children=[
                                        v.Html(
                                            class_="mb-6",
                                            style_="font-size: 20px;",
                                            tag="div",
                                            children=[
                                                Slide.Inputs.EXPLANATIONS,
                                            ],
                                        ),
                                        v.Html(
                                            tag="div",
                                            children=[Slide.Inputs.DASH_1],
                                        ),
                                        v.Html(
                                            tag="div",
                                            children=[Slide.Inputs.DASH_2],
                                        ),
                                        v.Html(
                                            tag="div",
                                            children=[Slide.Inputs.DASH_3],
                                        ),
                                        v.Html(
                                            tag="div",
                                            children=[Slide.Inputs.DASH_4],
                                        ),
                                        v.Html(
                                            class_="mt-4",
                                            style_="font-size: 14px; color: red;",
                                            tag="div",
                                            children=[Slide.Inputs.WARNING],
                                        ),
                                    ],
                                ),
                                v.Col(
                                    cols=5,
                                    lg=4,
                                    children=[self._inputs_gif],
                                ),
                                v.Col(),
                            ],
                        ),
                    ],
                ),
                v.CarouselItem(
                    children=[
                        v.Row(
                            class_="pb-5 px-12 mx-12",
                            justify="center",
                            align="center",
                            children=[Slide.Launch.EXPLANATIONS],
                        ),
                        v.Row(
                            justify="center",
                            align="center",
                            children=[self._launch_gif],
                        ),
                    ],
                ),
                v.CarouselItem(
                    children=[
                        v.Row(
                            class_="pb-5 px-12 mx-12",
                            justify="center",
                            align="center",
                            children=[Slide.Configuration.EXPLANATIONS],
                        ),
                        v.Row(
                            justify="center",
                            align="center",
                            children=[self._n2_gif],
                        ),
                    ],
                ),
                v.CarouselItem(
                    children=[
                        v.Row(
                            class_="pb-5 px-12 mx-12",
                            justify="center",
                            align="center",
                            children=[Slide.Outputs.SELECTION],
                        ),
                        v.Row(
                            justify="center",
                            align="center",
                            children=[self._outputs_gif],
                        ),
                        v.Row(
                            class_="pt-2 px-12 mx-12",
                            justify="center",
                            align="center",
                            children=[
                                v.Html(
                                    style_="font-size: 14px; color: red;",
                                    tag="div",
                                    children=[Slide.Outputs.WARNING],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

        self.children = [
            v.Row(
                justify="space-around",
                no_gutters=True,
                children=[
                    v.Col(
                        cols=12,
                        lg=8,
                        children=[tutorial_carousel],
                    ),
                ],
            ),
        ]

    def _load_images(self):
        """
        Loads tutorial images and gifs as instance variables to call them
        during the layout building.
        """
        self._fast_oad_logo = _image_from_path(
            PathManager.path_to("resources", FAST_OAD_LOGO), max_height="35vh"
        )

        self._inputs_gif = _image_from_path(
            PathManager.path_to("tutorial", INPUTS_GIF), max_height="80vh"
        )
        self._launch_gif = _image_from_path(
            PathManager.path_to("tutorial", LAUNCH_GIF), max_height="50vh"
        )
        self._n2_gif = _image_from_path(
            PathManager.path_to("tutorial", N2_GIF), max_height="50vh"
        )
        self._outputs_gif = _image_from_path(
            PathManager.path_to("tutorial", OUTPUTS_GIF), max_height="35vh"
        )
        self._mda_figure = _image_from_path(
            PathManager.path_to("tutorial", MDA_FIGURE), max_height="35vh"
        )
