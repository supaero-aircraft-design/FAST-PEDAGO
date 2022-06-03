import warnings

warnings.filterwarnings(action='ignore')
import os.path as pth
import openmdao.api as om
import logging
import shutil
import fastoad.api as oad
from fastoad._utils.files import make_parent_dir
from fastoad.io.configuration import FASTOADProblemConfigurator

DEFAULT_WOP_URL = "https://ether.onera.fr/whatsopt"
_LOGGER = logging.getLogger(__name__)
_PROBLEM_CONFIGURATOR = None

import sys

sys.path.append(pth.abspath("."))

from IPython.display import display, clear_output, IFrame
import ipywidgets as widgets
from ipywidgets import Layout
from Module.Interface import *


class MDA:

    def __init__(self):
        self.DATA_FOLDER_PATH = "data"
        self.WORK_FOLDER_PATH = "workdir"

        self.path1 = "Reference\Ref"
        self.path2 = "Reference\Configuration"

    # OAD instruction for the reference file
    def Source_File(self, path, file):
        self.path = path
        self.file = file
        try:

            logging.basicConfig(level=logging.INFO, format="%(levelname)-8s: %(message)s")
            self.SOURCE_FILE = pth.join(self.DATA_FOLDER_PATH, "Aircraft_reference_data.xml")
            shutil.copy(pth.join(self.path, self.file), self.SOURCE_FILE)

        except:
            print("The reference file not created")

    # Delete the aircraft reference file

    def Delete_File(self, path_file):
        self.path = path_file
        os.remove(path_file)

    # View the reference aircrfat data

    def reference_view(self):
        title = widgets.HTML(value=" <b>REFERENCE AIRCRAFT DATA</b>")
        self.Title_ref = widgets.HBox(children=[title], font_size=100,
                                      layout=Layout(display='flex', flex_flow='column', align_items='center',
                                                    width='100'))
        display(self.Title_ref)
        self.ref_view = oad.variable_viewer(self.SOURCE_FILE)

        return self.ref_view

    # OAD instruction for the configuration file
    def Configuration_File(self, path, file):
        self.path = path
        self.file = file
        try:

            logging.basicConfig(level=logging.INFO, format="%(levelname)-8s: %(message)s")
            self.CONFIGURATION_FILE = pth.join(self.DATA_FOLDER_PATH, "oad_sizing.yml")
            shutil.copy(pth.join(self.path, self.file), self.CONFIGURATION_FILE)

        except:
            print("Your configuration file not created")

    # OAD instruction to view the modules of the design problem case
    def liste_modules(self):
        title = widgets.HTML(value=" <b>MDA PROBLEM MODULES</b>")
        self.Title_mod = widgets.HBox(children=[title], font_size=100,
                                      layout=Layout(display='flex', flex_flow='column', align_items='center',
                                                    width='100'))
        display(self.Title_mod)

        self.modules_list = oad.list_modules(self.CONFIGURATION_FILE)
        return self.modules_list

    # OAD instruction to view the variables of the design problem case
    def liste_variables(self):
        title = widgets.HTML(value=" <b>MDA PROBLEM VARIABLES</b>")
        self.Title_mod = widgets.HBox(children=[title], font_size=100,
                                      layout=Layout(display='flex', flex_flow='column', align_items='center',
                                                    width='100'))
        display(self.Title_mod)

        self.variables_list = oad.list_variables(self.CONFIGURATION_FILE)
        return self.variables_list

    # OAD instruction for N2 Diagram Visualization

    def n2_write(self, configuration_file_path: str, n2_file_path: str = None, overwrite: bool = False):

        self.configuration_file_path = configuration_file_path
        self.n2_file_path = n2_file_path
        self.overwrite = overwrite

        """
        Write the N2 diagram of the problem in file n2.html

       :param configuration_file_path:
       :param n2_file_path: if None, will default to `n2.html`
       :param overwrite:
       :return: path of generated file.
       :raise FastPathExistsError: if overwrite==False and n2_file_path already exists
       """
        if not self.n2_file_path:
            n2_file_path = "n2.html"
        n2_file_path = pth.abspath(self.n2_file_path)

        if not overwrite and pth.exists(self.n2_file_path):
            raise FastPathExistsError(
                f"N2-diagram file {n2_file_path} not written because it already exists. ""Use overwrite=True to bypass.",
                self.n2_file_path, )

        make_parent_dir(self.n2_file_path)
        conf = FASTOADProblemConfigurator(self.configuration_file_path)
        conf._set_configuration_modifier(_PROBLEM_CONFIGURATOR)
        problem = conf.get_problem()
        problem.setup()
        problem.final_setup()

        om.n2(problem, outfile=self.n2_file_path, show_browser=False)
        _LOGGER.info("N2 diagram written in %s", pth.abspath(self.n2_file_path))
        return self.n2_file_path

    def N2_Diagramm(self):
        self.N2_FILE = pth.join(self.WORK_FOLDER_PATH, "n2.html")
        self.n2_write(self.CONFIGURATION_FILE, self.N2_FILE, overwrite=True)
        from IPython.display import IFrame
        IFrame(src=self.N2_FILE, width="100%", height="700px")

    # OAD instruction for XDSM  Diagram Visualization
    def XDSM_Diagramm(self):
        self.XDSM_FILE = pth.join(self.WORK_FOLDER_PATH, "XDSM.html")
        oad.write_xdsm(self.CONFIGURATION_FILE, self.XDSM_FILE, overwrite=True)
        self.XDSM = IFrame(src=self.XDSM_FILE, width="100%", height="500px")
        display(self.XDSM)
        return self.XDSM

    # OAD instruction for the inputs data file
    def Generate_Input_File(self):
        self.INPUT = oad.generate_inputs(self.CONFIGURATION_FILE, self.SOURCE_FILE, overwrite=True)

        return self.INPUT

    def View_inputs_data(self, input_file):
        title = widgets.HTML(value=" <b>AIRCRAFT INPUTS DATA</b>")
        Title_in = widgets.HBox(children=[title], font_size=100,
                                layout=Layout(display='flex', flex_flow='column', align_items='center', width='100'))
        display(Title_in)
        self.input_file = input_file
        self.inputs_viewer = oad.variable_viewer(self.input_file)

        return self.inputs_viewer

    def Input_File(self, input_file):
        self.input_file = input_file
        self.Input_Data = oad.DataFile(self.input_file)
        return self.Inuput_Data

