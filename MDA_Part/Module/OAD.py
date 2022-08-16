import warnings

warnings.filterwarnings(action='ignore')
import os.path as pth
import openmdao.api as om
import logging
import shutil
import fastoad.api as oad
from fastoad._utils.files import make_parent_dir
from fastoad.io.configuration import FASTOADProblemConfigurator
from typing import Union
import pandas as pd
import plotly.graph_objects as go
from fastoad.io import VariableIO
import numpy as np
import csv
import yaml
from math import isnan
from typing import Dict
import ipysheet as sh
from fastoad.io import DataFile
from fastoad.io.configuration.configuration import (
    FASTOADProblemConfigurator,
    KEY_CONSTRAINTS,
    KEY_DESIGN_VARIABLES,
    KEY_OBJECTIVE,
)
from fastoad.openmdao.variables import Variable, VariableList


pd.set_option("display.max_rows", None)



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

   #Save XML File
    def Save_File(self,file_ref,path_file,file_name):
        self.file_ref=file_ref
        self.path_file=path_file
        self.file_name=file_name+".xml"
        self.file=pth.join(self.path_file,self.file_name)
        shutil.copy(self.file_ref,self.file)

 #Save CSV File
    def Save_CSV_File(self,file_ref,path_file,file_name):
        self.csv_file_ref=file_ref
        self.csv_path_file=path_file
        self.csv_file_name=file_name+".csv"
        self.csv_file=pth.join(self.csv_path_file,self.csv_file_name)
        shutil.copy(self.csv_file_ref,self.csv_file)
        

    # View the reference aircrfat data

    def reference_view(self):
        title = widgets.HTML(value=" <b>REFERENCE AIRCRAFT DATA</b>")
        self.Title_ref = widgets.HBox(children=[title], font_size=100,
                                      layout=Layout(display='flex', flex_flow='column', align_items='center',
                                                    width='100'))
        display(self.Title_ref)
        self.ref_view = oad.variable_viewer(self.SOURCE_FILE)

        return self.ref_view
    

    def write_configuration(self,list_modules):
        self.list_modules=list_modules
        path="data"
        file="oad_sizing.yml"
        file_path=pth.join(path,file)
        with open(file_path, 'r+') as f:
            f.truncate(0)
        
        problem={'title': 'Sample OAD Process','input_file': '../workdir/oad_sizing_in.xml','output_file': '../workdir/oad_sizing_out.xml','model': {'nonlinear_solver': 'om.NonlinearBlockGS(maxiter=50, atol=1e-2, stall_limit=5)', 'linear_solver': 'om.DirectSolver()', 'geometry': {'id':'fastoad.geometry.legacy'},'weight': {'id': 'fastoad.weight.legacy', 'payload_from_npax': False}, 'mtow': {'id':'fastoad.mass_performances.compute_MTOW'},
  'aerodynamics_highspeed': {'id': 'fastoad.aerodynamics.highspeed.legacy'}, 'aerodynamics_lowspeed': {'id':'fastoad.aerodynamics.lowspeed.legacy'},'aerodynamics_takeoff': {'id': 'fastoad.aerodynamics.takeoff.legacy'}, 'aerodynamics_landing': {'id':'fastoad.aerodynamics.landing.legacy','use_xfoil': False},'performance': {'id': 'fastoad.performances.mission','propulsion_id':'fastoad.wrapper.propulsion.rubber_engine', 'mission_file_path': '../File/Mission/design_mission.yml','mission_name': 'MTOW_mission','out_file': '../workdir/oad_sizing.csv','adjust_fuel': True,'is_sizing': True},'hq_tail_sizing': {'id': 'fastoad.handling_qualities.tail_sizing'},'hq_static_margin': {'id': 'fastoad.handling_qualities.static_margin'},'wing_area': {'id': 'fastoad.loop.wing_area'}}}
        
        if ("geometry" in self.list_modules):
            problem["model"]["geometry"]={'id': 'fastoad.geometry.legacy'}
        else:
            if("geometry" in problem["model"].keys()):
                problem["model"].pop("geometry")
        
        if ("weight" in self.list_modules):
            problem["model"]["weight"]={'id': 'fastoad.weight.legacy', 'payload_from_npax': False}
        else:
            if("weight" in problem["model"].keys()):
                problem["model"].pop("weight")
        
        if ("mtow" in self.list_modules):
            problem["model"]["mtow"]={'id': 'fastoad.mass_performances.compute_MTOW'}
        else:
            if("mtow" in problem["model"].keys()):
                problem["model"].pop("mtow")
        
        if ("aerodynamics_highspeed" in self.list_modules):
            problem["model"]["aerodynamics_highspeed"]={'id': 'fastoad.aerodynamics.highspeed.legacy'}
        else:
            if("aerodynamics_highspeed" in problem["model"].keys()):
                problem["model"].pop("aerodynamics_highspeed")
                
        if ("aerodynamics_lowspeed" in self.list_modules):
            problem["model"]["aerodynamics_lowspeed"]={'id': 'fastoad.aerodynamics.lowspeed.legacy'}
        else:
            if("aerodynamics_lowspeed" in problem["model"].keys()):
                problem["model"].pop("aerodynamics_lowspeed")
                
        if ("aerodynamics_takeoff" in self.list_modules):
            problem["model"]["aerodynamics_takeoff"]={'id': 'fastoad.aerodynamics.takeoff.legacy'}
        else:
            if("aerodynamics_takeoff" in problem["model"].keys()):
                problem["model"].pop("aerodynamics_takeoff")
                
        if ("aerodynamics_landing" in self.list_modules):
            problem["model"]["aerodynamics_landing"]= {'id': 'fastoad.aerodynamics.landing.legacy','use_xfoil': False}
        else:
            if("aerodynamics_landing" in problem["model"].keys()):
                problem["model"].pop("aerodynamics_landing")
                
        if ("performance" in self.list_modules):
            problem["model"]["performance"]={'id': 'fastoad.performances.mission','propulsion_id': 'fastoad.wrapper.propulsion.rubber_engine',
   'mission_file_path': '../File/Mission/design_mission.yml','mission_name': 'MTOW_mission','out_file': '../workdir/oad_sizing.csv','adjust_fuel': True,
   'is_sizing': True}
        else:
            if("performance" in problem["model"].keys()):
                problem["model"].pop("performance")
                
        if ("hq_tail_sizing" in self.list_modules):
            problem["model"]["hq_tail_sizing"]= {'id': 'fastoad.handling_qualities.tail_sizing'}
        else:
            if("hq_tail_sizing" in problem["model"].keys()):
                problem["model"].pop("hq_tail_sizing")
            
        if ("hq_static_margin" in self.list_modules):
            problem["model"]["hq_static_margin"]= {'id': 'fastoad.handling_qualities.static_margin'}
        else:
            if("hq_static_margin" in problem["model"].keys()):
                problem["model"].pop("hq_static_margin")
        
        if ("wing_area" in self.list_modules):
            problem["model"]["wing_area"]= {'id': 'fastoad.loop.wing_area'}
        else:
            if("wing_area" in problem["model"].keys()):
                problem["model"].pop("wing_area")
                
        
        with open(file_path,"w") as f:
            yaml.dump(problem,f,sort_keys=False)
            f.close()

            
        try:

            logging.basicConfig(level=logging.INFO, format="%(levelname)-8s: %(message)s")
            self.CONFIGURATION_FILE = pth.join(path, file)
            print("MDA PROBLEM DEFINED IN THE CONFIGURATION FILE")
            print("----------------------------------------------------------------------------------------------------------------------------")
            
            
        except:
            print("MDA PROBELM NOT DEFINED. PLEASE SELECT MODULES TO DEFINE YOUR MDA ")
        
        

    # OAD instruction for the configuration file
    def Configuration_File(self,file_name):
        self.file_name=file_name
        
       

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
        return self.Input_Data
    


    
# Run OAD PROBLEM

    def RUN_OAD(self):
        
        self.problem=oad.evaluate_problem(self.CONFIGURATION_FILE,overwrite=True)
        return self.problem
    
# View AIRCRAFT OUTPUTS DATA
    def Join_File(self,path,name):
        self.path=path
        self.name=name
        self.FILE=pth.join(self.path,self.name)
        return self.FILE
    
    def View_outputs_data(self,output_file):
        
        title = widgets.HTML(value=" <b>AIRCRAFT OUTPUTS DATA</b>")
        Title_in = widgets.HBox(children=[title], font_size=100,layout=Layout(display='flex', flex_flow='column', align_items='center', width='100'))
        display(Title_in)
        self.output_file=output_file
        
        self.outputs_viewer = oad.variable_viewer(self.output_file)

        return self.outputs_viewer
    
    def Output_File(self, output_file):
        
        self.output_file = output_file
        self.output_Data = oad.DataFile(self.output_file)
        return self.output_Data

# MISSION ANALYSIS
    def MISSION_ANALYSIS(self,configuration_file,source_file,path_config,path_source):
        
        
        self.path_config=path_config
        self.path_source=path_source
        self.configuration_file=configuration_file
        self.source_file=source_file
        
        self.op_CONFIGURATION_FILE=pth.join(self.path_config,self.configuration_file)
        self.op_SOURCE_FILE=pth.join(self.path_source,self.source_file)
        self.op_input_file=oad.generate_inputs(self.op_CONFIGURATION_FILE,self.op_SOURCE_FILE,overwrite=True)
        self.list_file=[self.op_CONFIGURATION_FILE,self.op_SOURCE_FILE,self.op_input_file]
        return self.list_file
    

    def RUN_MISSION_ANALYSIS(self,problem_file):
        self.problem_file=problem_file
        self.run_op_problem=oad.evaluate_problem(self.problem_file,overwrite=True)
        return self.run_op_problem
        

        

# AIRCRAFT ANALYSIS OR POST-PROCESSING


# GEOMETRY PLOT
    def WING_GEOMETRY_PLOT(self,Geo_Design_Liste,Geo_Name_Liste):
        self.Geo_Design_Liste=Geo_Design_Liste
        self.Geo_Name_Liste=Geo_Name_Liste
        fig= oad.wing_geometry_plot(self.Geo_Design_Liste[0], name=self.Geo_Name_Liste[0])
        j=1
        while(j<len(self.Geo_Design_Liste)):
            fig = oad.wing_geometry_plot(self.Geo_Design_Liste[j],name=self.Geo_Name_Liste[j],fig=fig)
            j=j+1
        fig.show()
        
    def AIRCRAFT_GEOMETRY_PLOT(self,Geo_Design_Liste,Geo_Name_Liste):
        self.Geo_Design_Liste=Geo_Design_Liste
        self.Geo_Name_Liste=Geo_Name_Liste
        fig= oad.aircraft_geometry_plot(self.Geo_Design_Liste[0], name=self.Geo_Name_Liste[0])
        j=1
        while(j<len(self.Geo_Design_Liste)):
            fig = oad.aircraft_geometry_plot(self.Geo_Design_Liste[j],name=self.Geo_Name_Liste[j],fig=fig)
            j=j+1
        fig.show()
        
# AERODYNAMIC PLOT
    def AERODYNAMIC_PLOT(self,AERO_Design_Liste,AERO_Name_Liste):
        self.AERO_Design_Liste=AERO_Design_Liste
        self.AERO_Name_Liste=AERO_Name_Liste
        fig= oad.drag_polar_plot(self.AERO_Design_Liste[0], name=self.AERO_Name_Liste[0])
        j=1
        while(j<len(self.AERO_Design_Liste)):
            fig = oad.drag_polar_plot(self.AERO_Design_Liste[j],name=self.AERO_Name_Liste[j],fig=fig)
            j=j+1
        fig.show()


# MASS BREAK DOWN  PLOT

# MASS BAR PLOT

        
    def MASS_BAR_PLOT(self,MASS_BAR_Design_Liste,MASS_BAR_Name_Liste):
        
        self.MASS_BAR_Design_Liste=MASS_BAR_Design_Liste
        self.MASS_BAR_Name_Liste=MASS_BAR_Name_Liste
        fig= oad.mass_breakdown_bar_plot(self.MASS_BAR_Design_Liste[0], name=self.MASS_BAR_Name_Liste[0])
        j=1
        while(j<len(self.MASS_BAR_Design_Liste)):
            fig = oad.mass_breakdown_bar_plot(self.MASS_BAR_Design_Liste[j],name=self.MASS_BAR_Name_Liste[j],fig=fig)
            j=j+1
        fig.show()            
    
# MASS SUN PLOT   

    def MASS_SUN_PLOT(self,MASS_SUN_Design_Liste):
        
        self.MASS_SUN_Design_Liste=MASS_SUN_Design_Liste
        j=0
        while(j<len(self.MASS_SUN_Design_Liste)):
            fig= oad.mass_breakdown_sun_plot(self.MASS_SUN_Design_Liste[j])
            fig.show() 
            j=j+1
        
 # MISSION PLOT       





    def MISSION_PLOT(self,MISS_Design_Liste,MISS_Name_Liste):
        
        self.MISS_Design_Liste=MISS_Design_Liste
        self.MISS_Name_Liste=MISS_Name_Liste
        self.mission =MissionViewer()
        j=0
        while(j<len(self.MISS_Design_Liste)):
            self.mission.add_mission(self.MISS_Design_Liste[j],name=self.MISS_Name_Liste[j])
            j=j+1
        self.mission.display()
        return self.mission
    
   
        
        
        
        
# PLOT PAYLOAD/RANGE DIAGRAM
    
 # COMPUTE THE SFC COEFFICIENT
    def sfc(self,path):
        self.path=path 
        f = open( self.path)
        myreader = csv.reader(f, delimiter=',')
        i = 0
        j = 0
        fuel_flow = []
        thrust = []
        table = []
        list_sfc = []
        for row in myreader:
            table.append(row)
        for k in range(0, len(table[0])):
            if ('sfc [kg/N/s]' in table[0]): 
                index=table[0].index('sfc [kg/N/s]')
                for v in range (1, len(table)):
                    list_sfc.append(float(table[v][index]))
            else : 
                if table[0][k] == "Fuelflow [kg/s]":
                    i = k
                if table[0][k] == "thrust[N]":
                    j = k
                for v in range(1, len(table)):
                    fuel_flow.append(table[v][i])
                    thrust.append(table[v][j])
                for m in range(0, len(thrust)):
                    list_sfc.append(float(fuel_flow[m]) / float(thrust[m]))
        mean_sfc = sum(list_sfc) / len(list_sfc)
        return mean_sfc
    
    
    def k_ra(self,range):
        self.range=range
        k_ra = 1 - 0.895 * np.exp(-(self.range/814))
        return k_ra

 # COMPUTE THE COEFFECIENT RANGE
    def coefficient_range(self,data, path):
        self.data=data
        self.path=path
        gamma = 1.4
        r = 287
        z = np.asarray(self.data["data:mission:sizing:main_route:cruise:altitude"].value)
        t = 288 - (1 / 154) * (z / 3.28084)
        
        # a= (gamma*R*T)**(1/2) /1.61 # Mph
        a = (gamma * r * t) ** (1 / 2)  # Km.H
        M = np.asarray(data["data:TLAR:cruise_mach"].value)
        L_over_D = np.asarray(data["data:aerodynamics:aircraft:cruise:L_D_max"].value)
        mean_sfc= self.sfc(self.path)
        coefficient = a * M * L_over_D / (mean_sfc * 9.81)
        return (coefficient)
    
    def payload_range(self,Path, Perfo_csv_path, name=None, fig=None, file_formatter=None):
        self.Path=Path
        self.Perfo_csv_path=Perfo_csv_path
        ### Variable definition ###
        List_points = []
        Range = []
        Data=VariableIO(self.Path, file_formatter).read()
        MTOW = np.asarray(Data["data:weight:aircraft:MTOW"].value)
        OWE = np.asarray(Data["data:weight:aircraft:OWE"].value)
        MFW = np.asarray(Data["data:weight:aircraft:MFW"].value)
        MZFW = np.asarray(Data["data:weight:aircraft:MZFW"].value)
        Max_Payload = np.asarray(Data["data:weight:aircraft:max_payload"].value)
        
        ### Point A ###
        Point_A = Max_Payload
        Range_A = 0
        
        Range = Range + [float(Range_A)]
        List_points = List_points + [float(Point_A)]
        
        ### Point B ###
        Point_B = Point_A
        Fuel_Weight = MTOW - (OWE + Max_Payload)
        
        coefficient = self.coefficient_range(Data,self.Perfo_csv_path)
        
        #print (coefficient)
        Range_B = coefficient * np.log(1 + (Fuel_Weight / MZFW))
        Range_B = self.k_ra(Range_B) * Range_B
        #print (Range_B)
        List_points = List_points + [float(Point_B)]
        Range = Range + [float(Range_B)]
        
        
        ### Point D ###
        Point_D = Max_Payload - (MFW - Fuel_Weight)
        Range_D = coefficient * np.log(1 + (MFW / (MTOW - MFW)))
        Range_D = self.k_ra(Range_D) * Range_D

        List_points = List_points + [float(Point_D)]
        Range = Range + [float(Range_D)]
        ### Point E ###
        Point_E = 0
        Range_E = coefficient * np.log(1 + (MFW / OWE))
        Range_E = self.k_ra(Range_E) * Range_E
        List_points = List_points + [float(Point_E)]
        Range = Range + [float(Range_E)]
        Range=[i*0.539957/1000 for i in Range]  #From meter to nm
        
        ### Graphic Display ###
        if fig is None:
            fig = go.Figure()
            
        # scatter_prd= go.Scatter(x=Range, y=List_points, name="Payload-Range diagram"+name,#                         )
        scatter_prd = go.Scatter(x=Range, y=List_points, name="Payload-Range diagram")
        scatter_nominal = go.Scatter(x=(np.asarray(Data["data:TLAR:range"].value)), y=np.asarray(Data["data:weight:aircraft:payload"].value),name="Nominal working point" )
        fig.add_trace(scatter_prd)
        fig.add_trace(scatter_nominal)
        fig = go.FigureWidget(fig)
    # Set x-axes titles
        fig.update_xaxes(title_text="Range [Nm]")
 # Set y-axes titles
        fig.update_yaxes(title_text="Payload [Kg]")
        return fig
    
# WRITING OPTIMIZATION PROBLEM IN THE CONFIGURATION FILE
    def Write_Optimization_Problem(self,path,data):
        
        self.path=path
        self.data=data
        
        # Read and Get of the contents of the configuration file
        d={}
        f=open(self.path,"r",encoding="utf-8")
        d=yaml.load(f.read(),Loader=yaml.FullLoader)
        f.close()
        
        #  Check if there is a previous optimization problem and delete it
        if "optimization" in d.keys():
            d.pop("optimization")
            
        with open(self.path,"w") as f:
            yaml.dump(d,f,sort_keys=False)
            f.close()
        # Add the optimization problem to the configuration file    
        f=open(self.path,'a',encoding="utf-8")
        yaml.dump(self.data,f,sort_keys=False)
        f.close()
        
    
# GENERATION INPUTS FOR THE OPTIMIZATION PROBLEM
    def OPT_INPUTS(self,configuration,source):
        self.configuration=configuration
        self.source=source
        opt_input=oad.generate_inputs(self.configuration,self.source,overwrite=True)
        return opt_input
        

#  VIEW THE OPTIMIZATION PROBLEM
    def Optimization_View(self,configuration):
        
        self.configuration=configuration
        opt_view=oad.optimization_viewer(self.configuration)
        return opt_view
    
  # RUN THE OPTIMIZATION PROBLEM
    def Run_Optimization_Problem(self,configuration):
        
        self.configuration=configuration
        opt_problem=oad.optimize_problem(self.configuration,overwrite=True )
        return opt_problem
    
    def View_Optimization_Result(self,configuration):
        self.configuration=configuration
        opt_result=oad.optimization_viewer(self.configuration)
        return opt_result
    
        
    
 ############################################################################################################################
########################  PARAMETRIC BRANCH ################################################################################ 

# GENERATE THE REDESIGN AIRCRAFT DATA FILE
     
    def PARA_AC_FILE(self,AC_ref):
    
        self.AC_ref=AC_ref
        path="OUTPUT_FILE"
        file_path=pth.join(path,self.AC_ref)
        file_para="ID_Aircraft_File.xml"
        para_path=pth.join(path, file_para)
        shutil.copy(file_path, para_path)
    
    
    def para_k_ra(self,range):
        self.range=range
        k_ra = 1 - 0.895 * np.exp(-(self.range/814))
        return k_ra
        
    def para_sfc(self,path):
        self.path=path 
        f = open( self.path)
        myreader = csv.reader(f, delimiter=',')
        i = 0
        j = 0
        fuel_flow = []
        thrust = []
        table = []
        list_sfc = []
        for row in myreader:
            table.append(row)
        for k in range(0, len(table[0])):
            if ('sfc [kg/N/s]' in table[0]): 
                index=table[0].index('sfc [kg/N/s]')
                for v in range (1, len(table)):
                    list_sfc.append(float(table[v][index]))
            else : 
                if table[0][k] == "Fuelflow [kg/s]":
                    i = k
                if table[0][k] == "thrust[N]":
                    j = k
                for v in range(1, len(table)):
                    fuel_flow.append(table[v][i])
                    thrust.append(table[v][j])
                for m in range(0, len(thrust)):
                    list_sfc.append(float(fuel_flow[m]) / float(thrust[m]))
        mean_sfc = sum(list_sfc) / len(list_sfc)
        return mean_sfc
    # COMPUTE THE COEFFECIENT RANGE
    def para_coefficient_range(self,data,sfc):
        self.data=data
        self.sfc=sfc
        gamma = 1.4
        r = 287
        z = np.asarray(self.data["data:mission:sizing:main_route:cruise:altitude"].value)
        t = 288 - (1 / 154) * (z / 3.28084)
        
        # a= (gamma*R*T)**(1/2) /1.61 # Mph
        a = (gamma * r * t) ** (1 / 2)  # Km.H
        M = np.asarray(data["data:TLAR:cruise_mach"].value)
        L_over_D = np.asarray(data["data:aerodynamics:aircraft:cruise:L_D_max"].value)
        coefficient = a * M * L_over_D / (self.sfc * 9.81)
        return (coefficient)
    
    
    def para_payload_range(self,Path,sfc,name=None, fig=None, file_formatter=None):
        self.Path=Path
        self.sfc=sfc
        self.name=name
        ### Variable definition ###
        List_points = []
        Range = []
        Data=VariableIO(self.Path, file_formatter).read()
        MTOW = np.asarray(Data["data:weight:aircraft:MTOW"].value)
        OWE = np.asarray(Data["data:weight:aircraft:OWE"].value)
        MFW = np.asarray(Data["data:weight:aircraft:MFW"].value)
        MZFW = np.asarray(Data["data:weight:aircraft:MZFW"].value)
        Max_Payload = np.asarray(Data["data:weight:aircraft:max_payload"].value)
        
        ### Point A ###
        Point_A = Max_Payload
        Range_A = 0
        
        Range = Range + [float(Range_A)]
        List_points = List_points + [float(Point_A)]
        
        ### Point B ###
        Point_B = Point_A
        Fuel_Weight = MTOW - (OWE + Max_Payload)
        
        coefficient = self.para_coefficient_range(Data,self.sfc)
        
        #print (coefficient)
        Range_B = coefficient * np.log(1 + (Fuel_Weight / MZFW))
        Range_B = self.para_k_ra(Range_B) * Range_B
        #print (Range_B)
        List_points = List_points + [float(Point_B)]
        Range = Range + [float(Range_B)]
        
        
        ### Point D ###
        Point_D = Max_Payload - (MFW - Fuel_Weight)
        Range_D = coefficient * np.log(1 + (MFW / (MTOW - MFW)))
        Range_D = self.para_k_ra(Range_D) * Range_D

        List_points = List_points + [float(Point_D)]
        Range = Range + [float(Range_D)]
        ### Point E ###
        Point_E = 0
        Range_E = coefficient * np.log(1 + (MFW / OWE))
        Range_E = self.para_k_ra(Range_E) * Range_E
        List_points = List_points + [float(Point_E)]
        Range = Range + [float(Range_E)]
        Range=[i*0.539957/1000 for i in Range]  #From meter to nm
        
        ### Graphic Display ###
        if fig is None:
            fig = go.Figure()
            
        # scatter_prd= go.Scatter(x=Range, y=List_points, name="Payload-Range diagram"+name,#                         )
        scatter_prd = go.Scatter(x=Range, y=List_points, name=self.name)
        scatter_nominal = go.Scatter(x=(np.asarray(Data["data:TLAR:range"].value)), y=np.asarray(Data["data:weight:aircraft:payload"].value),name="Nominal working point:"+" "+ self.name )
        fig.add_trace(scatter_prd)
        fig.add_trace(scatter_nominal)
        fig = go.FigureWidget(fig)
    # Set x-axes titles
        fig.update_xaxes(title_text="Range [Nm]")
 # Set y-axes titles
        fig.update_yaxes(title_text="Payload [Kg]")
        return fig

       
 # COMPUTE THE SPECIFIC AIRCRAFT RANGE

    def mass(self,path):
        self.path=path
        f = open(self.path)
        myreader = csv.reader(f, delimiter=',')
        i = 0
        j = 0
        
        table = []
        list_mass = []
        for row in myreader:
            table.append(row)
            
        for k in range(0, len(table[0])):
            if ('mass [kg]' in table[0]):
                index = table[0].index('mass [kg]')
                for v in range(1, len(table)):
                    if table[v][-1] == "MTOW_mission:main_route:cruise" or table[v][-1]=="MTOW_mission:main_route:climb":
                        list_mass.append(float(table[v][index]))
                        
        mean_mass = sum(list_mass) / len(list_mass)
        return mean_mass
        
        
    def compute_SR(self,Path,SFC,Mass, file_formatter=None):
        self.Path=Path
        self.SFC=SFC
        self.Mass=Mass
        variables = VariableIO(self.Path, file_formatter).read()
        g = 9.81
        gamma = 1.4
        R = 287
        z = np.asarray(variables["data:mission:sizing:main_route:cruise:altitude"].value)
        z=z/3.28084 #   lenght from feet to meters 1 m = 3.28084 feets
        T = 288 - 0.0065 * z
        a = (gamma * R * T) ** (1 / 2)
        M = np.asarray(variables["data:TLAR:cruise_mach"].value)
        L_over_D = np.asarray(variables["data:aerodynamics:aircraft:cruise:L_D_max"].value)
        
        P = self.Mass * g
        SR = (a * M * L_over_D) / (self.SFC * P)
        SR= SR * 0.000539957 # from m/kg fuel to Nm/kg fuel 1 m = 0.000539957 Nm
        return (SR)
        
        
    def Npax_BF_Diagramm(self,Path,name=None, fig=None, file_formatter=None):
        self.Path=Path
        List_BF = [0]
        self.name=name
        List_Npax_BF = [0]
        Data=VariableIO(self.Path, file_formatter).read()
        MTOW= np.asarray(Data["data:weight:aircraft:MTOW"].value)
        OWE = np.asarray(Data["data:weight:aircraft:OWE"].value)
        Max_Payload = np.asarray(Data["data:weight:aircraft:max_payload"].value)
        NPAX1=np.asarray(Data["data:geometry:cabin:NPAX1"].value)
        
        BF=MTOW-OWE-Max_Payload
        Npax_BF=NPAX1/BF
        List_BF=List_BF+[float(BF)]
        List_Npax_BF=List_Npax_BF+[float(Npax_BF)]
        
        if fig is None:
            fig = go.Figure()
            
        # scatter_prd= go.Scatter(x=Range, y=List_points, name="Payload-Range diagram"+name,#                         )
        scatter_Npax_BF = go.Scatter(x=List_BF, y=List_Npax_BF, name=self.name)
        
        fig.add_trace(scatter_Npax_BF )
        
        fig = go.FigureWidget(fig)
    # Set x-axes titles
        fig.update_xaxes(title_text="BF [KG]")
 # Set y-axes titles
        fig.update_yaxes(title_text="NPAX/BF[Seat/Kg Fuel]")
        return fig
        
 # MODIFYING THE FAST MissionViewer class in order to use it with the interface user        

        
class MissionViewer:
    
    """
    A class for facilitating the post-processing of mission and trajectories
    """
    def __init__(self):
        
        # The dataframes containing each mission
        self.missions = {}

        # The figure displayed
        self._fig = None

        # The x selector
        self._x_widget = None

        # The y selector
        self._y_widget = None
        
    def add_mission(self, mission_data: Union[str, pd.DataFrame], name=None):
        
        """
        Adds the mission to the mission database (self.missions)
        :param mission_data: path of the mission file or Dataframe containing the mission data
        :param name: name to give to the mission
        """
        if (
            isinstance(mission_data, str)
            and mission_data.endswith(".csv")
            and pth.exists(mission_data)
        ):
            self.missions[name] = pd.read_csv(mission_data, index_col=0)
        elif isinstance(mission_data, pd.DataFrame):
            self.missions[name] = mission_data
        else:
            raise TypeError("Unknown type for mission data, please use .csv of DataFrame")

        # Initialize widgets when first mission is added
        if len(self.missions) == 1:
            self._initialize_widgets()
            
        
    def _initialize_widgets(self):
        
        """
        Initializes the widgets for selecting x and y
        """

        key = list(self.missions)[0]
        keys = self.missions[key].keys()

        # By default ground distance
        self._x_widget = widgets.Dropdown(value=keys[2], options=keys)
        self._x_widget.observe(self.display, "value")
        # By default altitude
        self._y_widget = widgets.Dropdown(value=keys[1], options=keys)
        self._y_widget.observe(self.display, "value")
        
    def _build_plots(self):
        
        """
        Add a plot of the mission
        """

        x_name = self._x_widget.value
        y_name = self._y_widget.value

        for name in self.missions:
            if self._fig is None:
                self._fig = go.Figure()
            # pylint: disable=invalid-name # that's a common naming
            x = self.missions[name][x_name]
            # pylint: disable=invalid-name # that's a common naming
            y = self.missions[name][y_name]

            scatter = go.Scatter(x=x, y=y, mode="lines", name=name)

            self._fig.add_trace(scatter)

            self._fig = go.FigureWidget(self._fig)

        self._fig.update_layout(
            title_text="Mission", title_x=0.5, xaxis_title=x_name, yaxis_title=y_name
        )

    # pylint: disable=unused-argument  # args has to be there for observe() to work
    
    def display(self, change=None) -> display:
        
        """
        Display the user interface
        :return the display object
        """
        self._update_plots()
        toolbar = widgets.HBox(
            [widgets.Label(value="x:"), self._x_widget, widgets.Label(value="y:"), self._y_widget]
        )
        # pylint: disable=invalid-name # that's a common naming
        ui = widgets.VBox([toolbar, self._fig])
        return display(ui)
    

    def _update_plots(self):
        """
        Update the plots
        """
        self._fig = None
        self._build_plots()




 



  


    
 