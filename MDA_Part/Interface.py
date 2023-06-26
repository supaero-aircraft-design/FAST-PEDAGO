from IPython.display import display,clear_output, HTML
import os.path as pth
import os
import fastoad.api as oad
import openmdao.api as om
import ipywidgets as widgets
from ipywidgets import Layout
from OAD import MDA
from fastoad.io import VariableIO
import csv
import yaml
import statistics
import plotly.graph_objects as go
import json
import xmltodict
import os
import subprocess
import numpy
import math
import shutil
import subprocess
import threading
import progressbar
import time
import webbrowser
class Interface:


    def __init__(self):
        self.path1="File\Reference"
        self.path2="File\Configuration"
        self.path3 = "OUTPUT_FILE"
        self.OAD= MDA()



# Function to read csv file

    def csv_to_table(self,path_to_target):
        self.path_to_target=path_to_target
        table = []
        f = open(self.path_to_target)
        myreader = csv.reader(f, delimiter=';')
        headings = next(myreader)
        for row in myreader:
            table.append(row[0])
        return table

    def HomeInterface(self,event):
        clear_output()
        image_path="Images/Wing.jpg"
        custom_css = f'''
        .vbox-with-background {{
            background-image: url("{image_path}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            width: 100%;
            height: 100%;
        }}
        '''
        display(HTML(f'<style>{custom_css}</style>'),self.menu)


    #The principal FAST-OAD ANALYSIS INTERFACE
    def Menu(self):

        table=["REFERENCE","CONFIGURATION","AIRCRAFT DATA","MDA","ANALYSIS","OPTIMIZATION","INCREMENTAL DEVELOPMENT"]
        title = widgets.HTML(
            value=" <h1 style='text-align:center;font-weight:bold;font-family:Arial, sans-serif;font-size:28px;color:#003399;text-decoration:underline;'>FAST OVERALL AIRCRAFT DESIGN</h1>")
        layout_button=Layout(width='17%', height='80px', border='4px solid black')
        layout_box = Layout(width='100%',height='40%',align_items='center',justify_content='center')
        layout_title= widgets.Layout(align_items='center',justify_content='center',width='65%',height='50%')
        self.Button_M0 = widgets.Button(description='DEMO', layout=layout_button, style=dict(button_color="#00d600"))
        self.Button_M1=widgets.Button(description=table[0], layout=layout_button, style=dict(button_color="#ebebeb"))
        self.Button_M2=widgets.Button(description=table[1], layout=layout_button,disabled=True, style=dict(button_color='#ebebeb'))
        self.Button_M3=widgets.Button(description=table[2], layout=layout_button,disabled=True, style=dict(button_color='#ebebeb'))
        self.Button_M4=widgets.Button(description=table[3], layout=layout_button, style=dict(button_color='#ebebeb'))
        self.Button_M5=widgets.Button(description=table[4], layout=layout_button, style=dict(button_color='#ebebeb'))
        self.Button_M6=widgets.Button(description=table[5], layout=layout_button, style=dict(button_color='#ebebeb'))
        self.Button_M7 = widgets.Button(description=table[6], layout=layout_button, style=dict(button_color='#ebebeb'))

        self.Button_M0.icon = 'fa-leanpub'
        self.Button_M1.icon = 'fa-plane'
        self.Button_M2.icon = 'fa-cogs'
        self.Button_M3.icon = 'fa-table'
        self.Button_M4.icon = 'fa-play'
        self.Button_M5.icon = 'fa-bar-chart'
        self.Button_M6.icon = 'fa-flask'

        self.Button_M0.on_click(self.menu_to_demo)
        self.Button_M1.on_click(self.menu_to_reference)
        self.Button_M2.on_click(self.configuration_file)
        self.Button_M3.on_click(self.menu_to_input)
        self.Button_M4.on_click(self.MDA_UI)
        self.Button_M5.on_click(self.POST_PROCESSING_UI)
        self.Button_M6.on_click(self.OPT_DESIGN)
        self.Button_M7.on_click(self. PARAMETRIC_UI1)

        Line_1=[self.Button_M0,self.Button_M1,self.Button_M2,self.Button_M3]
        Line_2 = [ self.Button_M4, self.Button_M5,self.Button_M6, self.Button_M7]

        image_path="Images/Wing.jpg"
        custom_css = f'''
        .vbox-with-background {{
            background-image: url("{image_path}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            width: 100%;
            height: 100%;
        }}
        '''

        buttonINFO = widgets.Button(description='')
        buttonINFO.icon = 'fa-info-circle'
        buttonINFO.layout.width = 'auto'
        buttonINFO.layout.height = 'auto'
        output = widgets.Output()

        def info_message(event):
            with output:
                output.clear_output()
                if len(output.outputs) > 0:
                    output.clear_output()

                else:
                    print('Welcome to FAST-OAD Training Branch.\n'
                          'This is the main menu, with different phases. Follow the order from left to right.\n'
                          'If a button is not enabled, it means that a previous step has to be fulfilled.')

        buttonINFO.on_click(info_message)


        button_git_FAST = widgets.Button(description="FAST-OAD")
        button_git_FAST.icon ="fa-github"
        button_git_FAST.layout.width = 'auto'
        button_git_FAST.layout.height = 'auto'
        def open_github_FAST(event):
            webbrowser.open_new_tab("https://github.com/fast-aircraft-design/FAST-OAD")
        button_git_FAST.on_click(open_github_FAST)

        button_git_CS25 = widgets.Button(description="CS25")
        button_git_CS25.icon ="fa-github"
        button_git_CS25.layout.width = 'auto'
        button_git_CS25.layout.height = 'auto'
        def open_github_CS25(event):
            webbrowser.open_new_tab("https://github.com/fast-aircraft-design/FAST-OAD_CS25")
        button_git_CS25.on_click(open_github_CS25)

        button_git_GA = widgets.Button(description="GA")
        button_git_GA.icon ="fa-github"
        button_git_GA.layout.width = 'auto'
        button_git_GA.layout.height = 'auto'
        def open_github_GA(event):
            webbrowser.open_new_tab("https://github.com/supaero-aircraft-design/FAST-GA")
        button_git_GA.on_click(open_github_GA)

        box_buttons_git = widgets.HBox(children=[button_git_FAST,button_git_CS25,button_git_GA],
                                       layout=Layout(border='0px solid black',margin='0 0 0 0px', padding='0px',
                                        justify_content='center', align_items='center', width='100%',height='10%'))

        box1 = widgets.HBox(children=[title],layout=layout_title)
        box2=widgets.HBox(children=Line_1,layout=layout_box)
        box3 = widgets.HBox(children=Line_2, layout=layout_box)
        box4 = widgets.Box(children=[buttonINFO, output],layout=Layout(border='0px solid black',
                                         margin='0 0 0 0px', padding='0px', align_items='center', width='100',height='12%'))
        box4.add_class('custom-vbox')
        display(widgets.HTML("""
        <style>
        .custom-vbox {
            background-color: white;
        }
        </style>
        """))
        self.menu=widgets.VBox(children=[box1,box_buttons_git,box2,box3,box4],layout=Layout(border='6px solid black'
                               ,margin='100 20 50 100px', padding='10px', align_items='center', width='940px',height='665px',
                               justify_content='center'))
        self.menu.add_class('vbox-with-background')

        display(HTML(f'<style>{custom_css}</style>'))

        return self.menu

    ## .................................................................................................................
    ## DEMO PHASE ......................................................................................................
    ## .................................................................................................................
    ## .................................................................................................................
    ## .................................................................................................................
    def menu_to_demo(self,event):
        clear_output()
        self.demo = self.demo_models()
        print("DEMO PHASE")
        print(
            "--------------------------------------------------------------------------------------------------------")
        return self.demo

    #User interface for the
    #reference aircraft choice step
    def demo_models(self):
        clear_output()
        title = widgets.HTML(value=" <b>Learning Environment </b>")
        layout_button = Layout(width='30%', height='40px', border='4px solid black')
        layout_box = Layout(width='100%', padding='10px')
        layout_title = widgets.Layout(display='flex', flex_flow='column', align_items='center', width='50%')
        # ---------------------------------------------------------------------------------------------------------------
        buttonHOME = widgets.Button(description='')
        buttonHOME.icon = 'fa-home'
        buttonHOME.layout.width = 'auto'
        buttonHOME.layout.height = 'auto'
        buttonHOME.on_click(self.HomeInterface)
        # ---------------------------------------------------------------------------------------------------------------
        box1 = widgets.HBox(children=[title],
                            layout=Layout(display='flex', flex_flow='column', align_items='center', width='70%'))

        # ---------------------------------------------------------------------------------------------------------------
        buttonINFO = widgets.Button(description='')
        buttonINFO.icon = 'fa-info-circle'
        buttonINFO.layout.width = 'auto'
        buttonINFO.layout.height = 'auto'
        output = widgets.Output()

        def info_message(event):
            with output:
                output.clear_output()
                if len(output.outputs) > 0:
                    output.clear_output()
                else:
                    print('Welcome to the Learning Environment DEMO.\n'
                          'This section aims to provide a better understanding of the sizing process using FAST-OAD\n')

        buttonINFO.on_click(info_message)
        box3 = widgets.Box(children=[buttonINFO, output], layout=Layout(border='0px solid black',
                                                                        margin='50 0 50 0px', padding='5px',
                                                                        align_items='center', width='100'))
        # ---------------------------------------------------------------------------------------------------------------
        box4 = widgets.Box(children=[buttonHOME, box3], layout=Layout(border='0px solid black',
                                                                      margin='50 0 50 0px', padding='0.5px',
                                                                      align_items='center', width='100'))
        Button_demo=widgets.Button(description='Inspect Modules', layout=layout_button, style=dict(button_color='#ebebeb'))
        Button_demo.on_click(self.demo_modules)

        Button_basis=widgets.Button(description='Performance Basis', layout=layout_button, style=dict(button_color='#ebebeb'))
        Button_basis.on_click(self.demo_basis)

        Button_Exo=widgets.Button(description='Impact Variables', layout=layout_button, style=dict(button_color='#ebebeb'))
        Button_Exo.on_click(self.demo_exo)

        self.BOX_INPUT = widgets.VBox(children=[box1, box4,Button_demo,Button_basis,Button_Exo],
                                      layout=Layout(border='6px solid black', padding='10px', align_items='center',
                                                    width='100%'))
        display(self.BOX_INPUT)


        return self.BOX_INPUT

        # Display the Principal UI _inputs



    def demo_modules(self, event=None):
        clear_output()
        display(self.BOX_INPUT)

        # Layout widget
        layout = widgets.Layout(width="75%", height='50px', justify_content='space-between')
        style = style = {'description_width': 'initial'}
        layout_button = widgets.Layout(width='30%', height='50px', border='4px solid black')
        layout_box = widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')

        ###############################GEOMETRY UI###############################
        # COMPUTE FUSELAGE UI
        with open("BlockImage/Geometry/Fuselage/Fuselage_IN.csv", 'r') as file:
            csvreader = csv.reader(file, delimiter=',')
            Data_Fuselage_IN=[]
            for row in csvreader:
                for value in row:
                    Data_Fuselage_IN.append(float(value))


        self.C_value1 = Data_Fuselage_IN[0]
        self.C_value2 = Data_Fuselage_IN[1]
        self.C_value3 = Data_Fuselage_IN[2]
        self.C_value4 = Data_Fuselage_IN[3]
        self.C_value5 = Data_Fuselage_IN[4]
        self.C_value6 = Data_Fuselage_IN[5]
        self.C_value7 = Data_Fuselage_IN[6]

        self.CAB_1 = widgets.BoundedFloatText(min=0,max=1000,step=0.1, value=self.C_value1,
                                              description="seats:width [m]", description_tooltip='Economical width', style=style,
                                              layout=layout)
        self.CAB_2 = widgets.BoundedFloatText(min=0,max=1000,step=0.1, value=self.C_value2,
                                              description="seats:length [m]", description_tooltip='Economical width', style=style,
                                              layout=layout)
        self.CAB_3 = widgets.BoundedFloatText(min=0,max=1000,step=1, value=self.C_value3,
                                              description="seats:by_row [-]", description_tooltip='Number of seats per row', style=style,
                                              layout=layout)
        self.CAB_4 = widgets.BoundedFloatText(min=0,max=1000,step=0.1, value=self.C_value4,
                                              description="cabin:aisle_width [m]", description_tooltip='Width of the aisle', style=style,
                                              layout=layout)
        self.CAB_5 = widgets.BoundedFloatText(min=0,max=1000,step=0.1, value=self.C_value5,
                                              description="cabin:exit_width [m]", description_tooltip='Cabins exit width', style=style,
                                              layout=layout)
        self.CAB_6 = widgets.BoundedFloatText(min=0,max=1000,step=1, value=self.C_value6,
                                              description="NPAX [-]", description_tooltip='Number of passanger from TLARS', style=style,
                                              layout=layout)
        self.CAB_7 = widgets.BoundedFloatText(min=0,max=1000,step=1, value=self.C_value7,
                                              description="engine:count [-]", description_tooltip='Number of engines', style=style,
                                              layout=layout)



        self.CAB_1_OUT = widgets.BoundedFloatText(min=0,max=1000,value=0,disabled=True,description="cabin:NPAX1",
                                                  description_tooltip='Updated number of Pax', style=style,layout=layout,width='150px')

        self.CAB_2_OUT  = widgets.BoundedFloatText(min=0,max=1000,value=0,disabled=True,
                                              description="flight_kit:CG:x [m]", description_tooltip='CG of flight kit', style=style,
                                              layout=layout,width='150px')
        self.CAB_3_OUT  = widgets.BoundedFloatText(min=0,max=1000,value=0,disabled=True,
                                              description="pax_seats:CG:x [m]", description_tooltip='CG of passenger seat', style=style,
                                              layout=layout)
        self.CAB_4_OUT  = widgets.BoundedFloatText(min=0,max=1000,value=0,disabled=True,
                                              description="fuselage:length [m]", description_tooltip='', style=style,
                                              layout=layout)
        self.CAB_5_OUT  = widgets.BoundedFloatText(min=0,max=1000,value=0,disabled=True,
                                              description="fuselage:max_width [m]", description_tooltip='', style=style,
                                              layout=layout)
        self.CAB_6_OUT  = widgets.BoundedFloatText(min=0,max=1000,value=0,disabled=True,
                                              description="fuselage:max_height [m]", description_tooltip='', style=style,
                                              layout=layout)
        self.CAB_7_OUT  = widgets.BoundedFloatText(min=0,max=1000,value=0,disabled=True,
                                              description="fuselage:front_length [m]", description_tooltip='', style=style,
                                              layout=layout)
        self.CAB_8_OUT  = widgets.BoundedFloatText(min=0,max=1000,value=0,disabled=True,
                                              description="fuselage:rear_length [m]", description_tooltip='', style=style,
                                              layout=layout)
        self.CAB_9_OUT  = widgets.BoundedFloatText(min=0,max=1000,value=0,disabled=True,
                                              description="fuselage:PAX_length [m]", description_tooltip='', style=style,
                                              layout=layout)
        self.CAB_10_OUT  = widgets.BoundedFloatText(min=0,max=1000,value=0,disabled=True,
                                              description="cabin:length [m]", description_tooltip='', style=style,
                                              layout=layout)
        self.CAB_11_OUT  = widgets.BoundedFloatText(min=0,max=1000,value=0,disabled=True,
                                              description="crew_count:commercial [-]", description_tooltip='', style=style,
                                              layout=layout)
        self.CAB_12_OUT  = widgets.BoundedFloatText(min=0,max=1000,value=0,disabled=True,
                                              description="fuselage:wetted_area [m^2]", description_tooltip='', style=style,
                                              layout=layout,width='150px')

        def update_fus(event):
            front_seat_number_eco = self.CAB_3.value  # inputs["data:geometry:cabin:seats:economical:count_by_row"]
            ws_eco = self.CAB_1.value  # inputs["data:geometry:cabin:seats:economical:width"]
            ls_eco = self.CAB_2.value  # inputs["data:geometry:cabin:seats:economical:length"]
            w_aisle = self.CAB_4.value  # inputs["data:geometry:cabin:aisle_width"]
            w_exit = self.CAB_5.value  # inputs["data:geometry:cabin:exit_width"]
            npax = self.CAB_6.value  # inputs["data:TLAR:NPAX"]
            n_engines = self.CAB_7.value  # inputs["data:geometry:propulsion:engine:count"]

            # Cabin width = N * seat width + Aisle width + (N+2)*2"+2 * 1"
            wcabin = (front_seat_number_eco * ws_eco + w_aisle + (front_seat_number_eco + 2) * 0.051 + 0.05)
            # Number of rows = Npax / N
            npax_1 = int(1.05 * npax)
            n_rows = int(npax_1 / front_seat_number_eco)
            pnc = int((npax + 17) / 35)
            # Length of pax cabin = Length of seat area + Width of 1 Emergency
            # exits
            lpax = (n_rows * ls_eco) + 1 * w_exit
            l_cyl = lpax - (2 * front_seat_number_eco - 4) * ls_eco
            r_i = wcabin / 2
            radius = 1.06 * r_i
            # Cylindrical fuselage
            b_f = 2 * radius
            # 0.14m is the distance between both lobe centers of the fuselage
            h_f = b_f + 0.14
            lav = 1.7 * h_f

            if n_engines == 3.0:
                lar = 3.0 * h_f
            else:
                lar = 3.60 * h_f

            fus_length = lav + lar + l_cyl
            cabin_length = 0.81 * fus_length
            x_cg_c6 = lav - (front_seat_number_eco - 4) * ls_eco + lpax * 0.1
            x_cg_d2 = lav - (front_seat_number_eco - 4) * ls_eco + lpax / 2

            # Equivalent diameter of the fuselage
            fus_dia = math.sqrt(b_f * h_f)
            wet_area_nose = 2.45 * fus_dia * lav
            wet_area_cyl = 3.1416 * fus_dia * l_cyl
            wet_area_tail = 2.3 * fus_dia * lar
            wet_area_fus = wet_area_nose + wet_area_cyl + wet_area_tail

            self.CAB_1_OUT.value = round(npax_1,3)
            self.CAB_2_OUT.value = round(x_cg_c6,3)
            self.CAB_3_OUT.value = round(x_cg_d2,3)
            self.CAB_4_OUT.value = round(fus_length,3)
            self.CAB_5_OUT.value = round(b_f,3)
            self.CAB_6_OUT.value = round(h_f,3)
            self.CAB_7_OUT.value = round(lav,3)
            self.CAB_8_OUT.value = round(lar,3)
            self.CAB_9_OUT.value = round(lpax,3)
            self.CAB_10_OUT.value = round(cabin_length,3)
            self.CAB_11_OUT.value = round(pnc,3)
            self.CAB_12_OUT.value = round(wet_area_fus,3)

            Data_Fuselage_IN[0] = self.CAB_1.value
            Data_Fuselage_IN[1] = self.CAB_2.value
            Data_Fuselage_IN[2] = self.CAB_3.value
            Data_Fuselage_IN[3] = self.CAB_4.value
            Data_Fuselage_IN[4] = self.CAB_5.value
            Data_Fuselage_IN[5] = self.CAB_6.value
            Data_Fuselage_IN[6] = self.CAB_7.value

            # Open the CSV file in write mode
            with open("BlockImage/Geometry/Fuselage/Fuselage_IN.csv", 'w') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(Data_Fuselage_IN)

        button_Update_FUS = widgets.Button(description='Update DATA')
        button_Update_FUS.icon = 'fa-check'
        button_Update_FUS.layout.width = 'auto'
        button_Update_FUS.layout.height = 'auto'
        button_Update_FUS.on_click(update_fus)

        C_file = open("Images/cabin.PNG", "rb")
        C_image = C_file.read()
        C_img = widgets.Image(value=C_image, format="PNG", width="45%", height="100%")

        C_box_C = widgets.VBox(
            children=[self.CAB_1, self.CAB_2, self.CAB_3, self.CAB_4, self.CAB_5, self.CAB_6, self.CAB_7],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))
        C_box_Out = widgets.VBox(
            children=[self.CAB_1_OUT, self.CAB_2_OUT, self.CAB_3_OUT, self.CAB_4_OUT, self.CAB_5_OUT, self.CAB_6_OUT,
                      self.CAB_7_OUT,self.CAB_8_OUT,self.CAB_9_OUT,self.CAB_10_OUT,self.CAB_11_OUT,self.CAB_12_OUT],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))

        C_input = widgets.HTML(value=" <b>INPUTS-- </b>")
        C_output = widgets.HTML(value=" <b>--OUTPUTS </b>")

        C_inout_inter = widgets.HBox(children=[C_input, C_output],align_items='space-between')
        C_box_inter = widgets.HBox(children=[C_box_C, C_box_Out], layout=layout_box)

        C_file1 = open("BlockImage/Geometry/Fuselage/1.PNG", "rb")
        C_file2 = open("BlockImage/Geometry/Fuselage/2.PNG", "rb")
        C_file3 = open("BlockImage/Geometry/Fuselage/3.PNG", "rb")
        C_image1 = C_file1.read()
        C_image2 = C_file2.read()
        C_image3 = C_file3.read()
        C_img1 = widgets.Image(value=C_image1, format="PNG", width="100%", height="100%")
        C_img2 = widgets.Image(value=C_image2, format="PNG", width="100%", height="100%")
        C_img3 = widgets.Image(value=C_image3, format="PNG", width="100%", height="100%")


        # GEOMETRY MODULES BY COMPUTED BLOCKS
        self.tab_GEO_Block = widgets.Tab(children=[C_img1,C_img2,C_img3])
        self.tab_GEO_Block.set_title(0, 'Miscellaneous')
        self.tab_GEO_Block.set_title(1, 'Lengths')
        self.tab_GEO_Block.set_title(2, 'Surfaces')
        self.C_box = widgets.VBox(children=[button_Update_FUS,C_inout_inter, C_box_inter, self.tab_GEO_Block, C_img],
                                  layout=layout_box)





        # GEOMETRY MENU TABS
        self.tab_GEO = widgets.Tab(children=[self.C_box,self.C_box,self.C_box,self.C_box,self.C_box,self.C_box])
        self.tab_GEO.set_title(0, 'FUSELAGE')
        self.tab_GEO.set_title(1, 'WING')
        self.tab_GEO.set_title(2, 'HT')
        self.tab_GEO.set_title(3, 'VT')
        self.tab_GEO.set_title(4, 'Nacelle Pylons')
        self.tab_GEO.set_title(5, 'Wetted Area')


        # GENERAL INPUTS MENU
        self.tab_IN = widgets.Tab(children=[self.tab_GEO,self.tab_GEO,self.tab_GEO,self.tab_GEO,self.tab_GEO,self.tab_GEO])
        self.tab_IN.set_title(0, 'GEOMETRY')
        self.tab_IN.set_title(1, 'WEIGHT')
        self.tab_IN.set_title(2, 'AERODYNAMICS')
        self.tab_IN.set_title(3, 'LOADS')
        self.tab_IN.set_title(4, 'MISSION')
        self.tab_IN.set_title(5, 'PROPULSION')
        display(self.tab_IN)
        return self.tab_IN



    def demo_basis(self, event=None):
        clear_output()
        display(self.BOX_INPUT)

        # Layout widget
        layout = widgets.Layout(width="75%", height='50px', justify_content='space-between')
        style = style = {'description_width': 'initial'}
        layout_button = widgets.Layout(width='30%', height='50px', border='4px solid black')
        layout_box = widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')

        # BREGUET ------------------------------------------------------------------------------------------------------
        with open("BlockImage/Basis/Breguet/Breguet_Range.csv", 'r') as file:
            csvreader = csv.reader(file, delimiter=',')
            Data_Breguet_Range_IN=[]
            for row in csvreader:
                for value in row:
                    Data_Breguet_Range_IN.append(float(value))


        self.Breguet_value1 = Data_Breguet_Range_IN[0] # finesse
        self.Breguet_value2 = Data_Breguet_Range_IN[1] # velocity
        self.Breguet_value3 = Data_Breguet_Range_IN[2] # sfc
        self.Breguet_value4 = Data_Breguet_Range_IN[3] # initial weight
        self.Breguet_value5 = Data_Breguet_Range_IN[4] # final weight
        self.Breguet_value6 = Data_Breguet_Range_IN[5] # owe/mtow
        self.Breguet_value7 = Data_Breguet_Range_IN[6] # reserve/mlw
        self.Breguet_value8 = Data_Breguet_Range_IN[7] # payload
        self.Breguet_value9 = Data_Breguet_Range_IN[8] # desired range


        self.Breguet_1 = widgets.BoundedFloatText(min=0,max=1000,step=0.1, value=self.Breguet_value1,
                                              description="Finesse L/D", description_tooltip='Mean Lift/Drag ratio', style=style,
                                              layout=layout)
        self.Breguet_2 = widgets.BoundedFloatText(min=0,max=1000,step=0.1, value=self.Breguet_value2,
                                              description="Velocity [km/h]", description_tooltip='Aircraft True Airspeed', style=style,
                                              layout=layout)
        self.Breguet_3 = widgets.BoundedFloatText(min=0,max=1000,step=1, value=self.Breguet_value3,
                                              description="SFC [kg/N/h]", description_tooltip='Specific Fuel Consumption (Flue flow per unit of thrust)', style=style,
                                              layout=layout)
        self.Breguet_4 = widgets.BoundedFloatText(min=0,max=900000,step=10, value=self.Breguet_value4,
                                              description="Initial Weight (TOW) [kg]", description_tooltip='Initial aircraft weight', style=style,
                                              layout=layout)
        self.Breguet_5 = widgets.BoundedFloatText(min=0,max=900000,step=10, value=self.Breguet_value5,
                                              description="Final Weight (LW) [kg]", description_tooltip='Final aircraft weight', style=style,
                                              layout=layout)
        self.Breguet_6 = widgets.BoundedFloatText(min=0, max=900000, step=10, value=self.Breguet_value6,description="OWE/MTOW",
                                                  description_tooltip='OWE and MTOW ratio', style=style,layout=layout)
        self.Breguet_7 = widgets.BoundedFloatText(min=0, max=900000, step=10, value=self.Breguet_value7,description="Reserve/MLW",
                                                  description_tooltip='Fuel Reserve and Max Landing Weight ratio', style=style,layout=layout)
        self.Breguet_8 = widgets.BoundedFloatText(min=0, max=900000, step=10, value=self.Breguet_value8,description="Payload [kg]",
                                                  description_tooltip='Aircraft payload', style=style,layout=layout)
        self.Breguet_9 = widgets.BoundedFloatText(min=0, max=900000, step=10, value=self.Breguet_value9,
                                                  description="Range [km]",description_tooltip='Desired range', style=style, layout=layout)


        self.Breguet_Range_1_OUT = widgets.BoundedFloatText(min=0,max=20000,value=0,disabled=True,description="Aircraft Range [km]",
                                                  description_tooltip='Aircraft range in km', style=style,layout=layout,width='150px')
        self.Breguet_Range_2_OUT = widgets.BoundedFloatText(min=0,max=20000,value=0,disabled=True,description="Aircraft Range [NM]",
                                                  description_tooltip='Aircraft range in Nautical miles', style=style,layout=layout,width='150px')

        self.Breguet_Masses_1_OUT = widgets.BoundedFloatText(min=0,max=900000,value=0,disabled=True,description="Take off Weight [kg]",
                                                  description_tooltip='Maximum or Take off weight', style=style,layout=layout,width='150px')
        self.Breguet_Masses_2_OUT = widgets.BoundedFloatText(min=0,max=900000,value=0,disabled=True,description="Fuel Weight [kg]",
                                                  description_tooltip='Fuel weight including reserve fuel', style=style,layout=layout,width='150px')
        self.Breguet_Masses_3_OUT = widgets.BoundedFloatText(min=0,max=900000,value=0,disabled=True,description="Reserve Fuel Weight [kg]",
                                                  description_tooltip='Reserve of fuel weight', style=style,layout=layout,width='150px')
        self.Breguet_Masses_4_OUT = widgets.BoundedFloatText(min=0,max=900000,value=0,disabled=True,description="OWE [kg]",
                                                  description_tooltip='Operational Weight Empty', style=style,layout=layout,width='150px')
        self.Breguet_Masses_5_OUT = widgets.BoundedFloatText(min=0,max=900000,value=0,disabled=True,description="LW [kg]",
                                                  description_tooltip='Maximum or Landing Weight', style=style,layout=layout,width='150px')
        self.Breguet_Masses_6_OUT = widgets.BoundedFloatText(min=0,max=900000,value=0,disabled=True,description="MF/MTOW [kg]",
                                                  description_tooltip='Ratio between Mass fuel and Take off weight', style=style,layout=layout,width='150px')



        def update_breguet(event):
            finesse = self.Breguet_1.value
            V = self.Breguet_2.value #velocity km/h
            SFC= self.Breguet_3.value #kg/N/h
            Wi = self.Breguet_4.value #kg
            Wf = self.Breguet_5.value #kg
            g= 9.8066 #m/s^2
            range = V*finesse*math.log(Wi/Wf) /(g*SFC) # km

            OWE_MTOW = self.Breguet_6.value #
            RESERVE_MLW = self.Breguet_7.value #
            Payload = self.Breguet_8.value #kg
            Range_2 = self.Breguet_9.value #km

            ratio_Weight_i_f = math.exp( (Range_2*g*SFC) / (V*finesse) )

            MLW = Payload / ( 1 -RESERVE_MLW -ratio_Weight_i_f*OWE_MTOW )
            MTOW = MLW * ratio_Weight_i_f
            OWE= MTOW*OWE_MTOW
            Reserve_Fuel = MLW*RESERVE_MLW
            #MTOW= OWE + PL + RESERVE + FUEL
            Fuel = MTOW- OWE -Payload

            self.Breguet_Range_1_OUT.value = round(range,3)
            self.Breguet_Range_2_OUT.value = round(range*0.5395680,3) #km to Nautical miles

            self.Breguet_Masses_1_OUT.value = round(MTOW,3)
            self.Breguet_Masses_2_OUT.value = round(Fuel,3)
            self.Breguet_Masses_3_OUT.value = round(Reserve_Fuel,3)
            self.Breguet_Masses_4_OUT.value = round(OWE,3)
            self.Breguet_Masses_5_OUT.value = round(MLW,3)
            self.Breguet_Masses_6_OUT.value = round(Fuel/MTOW,3)

            Data_Breguet_Range_IN[0] = self.Breguet_1.value
            Data_Breguet_Range_IN[1] = self.Breguet_2.value
            Data_Breguet_Range_IN[2] = self.Breguet_3.value
            Data_Breguet_Range_IN[3] = self.Breguet_4.value
            Data_Breguet_Range_IN[4] = self.Breguet_5.value
            Data_Breguet_Range_IN[5] = self.Breguet_6.value
            Data_Breguet_Range_IN[6] = self.Breguet_7.value
            Data_Breguet_Range_IN[7] = self.Breguet_8.value
            Data_Breguet_Range_IN[8] = self.Breguet_9.value

            # Open the CSV file in write modea

            with open("BlockImage/Basis/Breguet/Breguet_Range.csv", 'w') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(Data_Breguet_Range_IN)


        button_Update_Breguet = widgets.Button(description='Update DATA')
        button_Update_Breguet.icon = 'fa-check'
        button_Update_Breguet.layout.width = 'auto'
        button_Update_Breguet.layout.height = 'auto'
        button_Update_Breguet.on_click(update_breguet)

        C_box_C = widgets.VBox(
            children=[self.Breguet_1, self.Breguet_2, self.Breguet_3, self.Breguet_4, self.Breguet_5],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))
        C_box_Out = widgets.VBox(
            children=[self.Breguet_Range_1_OUT,self.Breguet_Range_2_OUT],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))

        C_box2_C = widgets.VBox(
            children=[self.Breguet_1, self.Breguet_2, self.Breguet_3, self.Breguet_6, self.Breguet_7,self.Breguet_8,self.Breguet_9],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))
        C_box2_Out = widgets.VBox(children=[self.Breguet_Masses_1_OUT,self.Breguet_Masses_2_OUT,self.Breguet_Masses_3_OUT,
                                            self.Breguet_Masses_4_OUT,self.Breguet_Masses_5_OUT,self.Breguet_Masses_6_OUT],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))


        C_input = widgets.HTML(value=" <b>INPUTS----  </b>")
        C_output = widgets.HTML(value=" <b>  ----OUTPUTS </b>")

        C_inout_inter = widgets.HBox(children=[C_input, C_output],align_items='space-between')
        C_box_inter = widgets.HBox(children=[C_box_C, C_box_Out], layout=layout_box)
        C_box2_inter = widgets.HBox(children=[C_box2_C, C_box2_Out], layout=layout_box)

        C_file1 = open("BlockImage/Basis/Breguet/1.PNG", "rb")
        C_image1 = C_file1.read()
        C_img1 = widgets.Image(value=C_image1, format="PNG", width="100%", height="50%")

        Breguets_2nd_Title = widgets.HTML(value=" <b>  Breguet's Formulation with range as input </b>")


        # GEOMETRY MODULES BY COMPUTED BLOCKS
        #self.tab_Basis_Block = widgets.Tab(children=[C_img1])
        #self.tab_Basis_Block.set_title(0, 'Miscellaneous')
        #self.tab_Basis_Block.set_title(1, 'Lengths')
        #self.tab_Basis_Block.set_title(2, 'Surfaces')
        self.C_basis_box = widgets.VBox(children=[button_Update_Breguet,C_img1,C_inout_inter, C_box_inter,Breguets_2nd_Title,C_inout_inter, C_box2_inter],layout=layout_box)

        # END OF BREGUET IMPLEMENTATION --------------------------------------------------------------------------------

        # MASS LOOP-----------------------------------------------------------------------------------------------------
        with open("BlockImage/Basis/MassLoop/Massloop.csv", 'r') as file:
            csvreader = csv.reader(file, delimiter=',')
            Data_Mass_Loop_IN = []
            for row in csvreader:
                for value in row:
                    Data_Mass_Loop_IN.append(float(value))

        self.MassLoop_value1_min = Data_Mass_Loop_IN[0]  # MTOW min
        self.MassLoop_value2_min = Data_Mass_Loop_IN[1]  # span in m
        self.MassLoop_value3_min = Data_Mass_Loop_IN[2]  # area in m^2
        self.MassLoop_value4_min = Data_Mass_Loop_IN[3]  # t/c relative thickness
        self.MassLoop_value5_min = Data_Mass_Loop_IN[4]  # quarter chord sweep
        self.MassLoop_value6_min = Data_Mass_Loop_IN[5]  # engine weight
        self.MassLoop_value7_min = Data_Mass_Loop_IN[6]  # Npax
        self.MassLoop_value1_max = Data_Mass_Loop_IN[7]   # MTOW max
        self.MassLoop_value_NpaxKg = Data_Mass_Loop_IN[8]  # kg/pax



        self.MassLoop_1_min = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.MassLoop_value1_min,
                                                   description="MTOW- MIN [kg]", description_tooltip='Maximum take off weight',
                                                  style=style,layout=layout)
        self.MassLoop_2_min = widgets.BoundedFloatText(min=0, max=1000, step=0.1, value=self.MassLoop_value2_min,
                                                  description="Span [m]",
                                                  description_tooltip='The span of the wing', style=style,layout=layout)

        self.MassLoop_3_min = widgets.BoundedFloatText(min=0, max=5000, step=1, value=self.MassLoop_value3_min,
                                                  description="Wing Area [m^2]",
                                                  description_tooltip='Area of the wing in square meters',
                                                  style=style,layout=layout)
        self.MassLoop_4_min = widgets.BoundedFloatText(min=0, max=900000, step=10, value=self.MassLoop_value4_min,
                                                  description="t/c",
                                                  description_tooltip='Relative thickness', style=style,layout=layout)
        self.MassLoop_5_min = widgets.BoundedFloatText(min=0, max=900000, step=10, value=self.MassLoop_value5_min,
                                                  description="Quarter chord sweep [º]",
                                                  description_tooltip='Quarter chord sweep at 25% of MAC', style=style,layout=layout)
        self.MassLoop_6_min = widgets.BoundedFloatText(min=0, max=900000, step=10, value=self.MassLoop_value6_min,
                                                  description="Engine weight x2 [kg]",
                                                  description_tooltip='Weight of the engines', style=style, layout=layout)

        self.MassLoop_7_min = widgets.BoundedFloatText(min=0, max=900000, step=10, value=self.MassLoop_value7_min,
                                                  description="Npax",
                                                  description_tooltip='Number of passenger', style=style, layout=layout)



        self.MassLoop_1_max = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.MassLoop_value1_max,
                                                   description="MTOW- MAX [kg]", description_tooltip='Maximum takee off weight',
                                                  style=style,layout=layout)


        self.MassLoop_1_OUT_min = widgets.BoundedFloatText(min=0, max=900000, value=0, disabled=True,
                                                            description="OWE [kg]",
                                                            description_tooltip='Operational Weight Empty for Min MTOW', style=style,
                                                            layout=layout, width='150px')
        self.MassLoop_2_OUT_min = widgets.BoundedFloatText(min=0, max=900000, value=0, disabled=True,
                                                            description="Operator items [kg]",
                                                            description_tooltip='Weight of the operational items', style=style,
                                                            layout=layout, width='150px')
        self.MassLoop_3_OUT_min = widgets.BoundedFloatText(min=0, max=900000, value=0, disabled=True,
                                                            description="Wing weight [kg]",
                                                            description_tooltip='Weight of the wing', style=style,
                                                            layout=layout, width='150px')
        self.MassLoop_4_OUT_min = widgets.BoundedFloatText(min=0, max=900000, value=0, disabled=True,
                                                            description="Fuselage weight [kg]",
                                                            description_tooltip='Weight of the fuselage', style=style,
                                                            layout=layout, width='150px')
        self.MassLoop_5_OUT_min = widgets.BoundedFloatText(min=0, max=900000, value=0, disabled=True,
                                                            description="Powerplant weight [kg]",
                                                            description_tooltip='Weight of the engines', style=style,
                                                            layout=layout, width='150px')
        self.MassLoop_6_OUT_min = widgets.BoundedFloatText(min=0, max=900000, value=0, disabled=True,
                                                            description="Landing gear weight [kg]",
                                                            description_tooltip='Weight of the landing gear', style=style,
                                                            layout=layout, width='150px')



        self.MassLoop_1_OUT_max = widgets.BoundedFloatText(min=0, max=900000, value=0, disabled=True,
                                                            description="OWE [kg]",
                                                            description_tooltip='Operational Weight Empty for Max MTOW',
                                                            style=style, layout=layout, width='150px')
        self.MassLoop_2_OUT_max = widgets.BoundedFloatText(min=0, max=900000, value=0, disabled=True,
                                                            description="Operator items [kg]",
                                                            description_tooltip='Weight of the operational items', style=style,
                                                            layout=layout, width='150px')
        self.MassLoop_3_OUT_max = widgets.BoundedFloatText(min=0, max=900000, value=0, disabled=True,
                                                            description="Wing weight [kg]",
                                                            description_tooltip='Weight of the wing', style=style,
                                                            layout=layout, width='150px')
        self.MassLoop_4_OUT_max = widgets.BoundedFloatText(min=0, max=900000, value=0, disabled=True,
                                                            description="Fuselage weight [kg]",
                                                            description_tooltip='Weight of the fuselage', style=style,
                                                            layout=layout, width='150px')
        self.MassLoop_5_OUT_max = widgets.BoundedFloatText(min=0, max=900000, value=0, disabled=True,
                                                            description="Powerplant weight [kg]",
                                                            description_tooltip='Weight of the engines', style=style,
                                                            layout=layout, width='150px')
        self.MassLoop_6_OUT_max = widgets.BoundedFloatText(min=0, max=900000, value=0, disabled=True,
                                                            description="Landing gear weight [kg]",
                                                            description_tooltip='Weight of the landing gear', style=style,
                                                            layout=layout, width='150px')

        self.MissionLoop_1 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.MassLoop_value1_min,disabled=True,
                                                   description="MTOW- MIN [kg]", description_tooltip='Maximum take off weight',
                                                  style=style,layout=layout)
        self.MissionLoop_2 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.MassLoop_value1_max,disabled=True,
                                                   description="MTOW- MAX [kg]", description_tooltip='Maximum take off weight',
                                                  style=style,layout=layout)
        self.MissionLoop_3 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value= self.Breguet_value1,disabled=True,
                                                      description="L/D",description_tooltip='Finesse',
                                                      style=style, layout=layout)
        self.MissionLoop_4 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value= self.Breguet_value2,disabled=True,
                                                      description="Velocity [km/h]",description_tooltip='Aircrafts true airspeed',
                                                      style=style, layout=layout)
        self.MissionLoop_5 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value= self.Breguet_value3,disabled=True,
                                                      description="SFC [kg/N/h]",description_tooltip='Specific fuel consumption',
                                                      style=style, layout=layout)
        self.MissionLoop_6 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value= self.Breguet_value7,disabled=True,
                                                      description="Reserve / ZFW ",description_tooltip='Fuel reserve ratio',
                                                      style=style, layout=layout)
        self.MissionLoop_7 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value= self.Breguet_value9,disabled=True,
                                                      description="Range [km]",description_tooltip='Aircrafts range',
                                                      style=style, layout=layout)
        self.MissionLoop_8 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value= self.MassLoop_value_NpaxKg,
                                                      description="Payload units [kg/pax]",description_tooltip='Aircrafts range',
                                                      style=style, layout=layout)

        self.MissionLoop_1_OUT_min = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=0,disabled=True,
                                                   description="OWE- MIN [kg]", description_tooltip='Operational Weight Empty',
                                                  style=style,layout=layout)
        self.MissionLoop_2_OUT_min = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=0,disabled=True,
                                                   description="LW- MIN [kg]", description_tooltip='Landing Weight',
                                                  style=style,layout=layout)
        self.MissionLoop_3_OUT_min = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=0,disabled=True,
                                                   description="ZFW- MIN [kg]", description_tooltip='Zero Fuel Weight',
                                                  style=style,layout=layout)

        self.MissionLoop_1_OUT_max = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=0,disabled=True,
                                                   description="OWE- MAX [kg]", description_tooltip='Operational Weight Empty',
                                                  style=style,layout=layout)
        self.MissionLoop_2_OUT_max = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=0,disabled=True,
                                                   description="LW- MAX [kg]", description_tooltip='Landing Weight',
                                                  style=style,layout=layout)
        self.MissionLoop_3_OUT_max = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=0,disabled=True,
                                                   description="ZFW- MAX [kg]", description_tooltip='Zero Fuel Weight',
                                                  style=style,layout=layout)


        # ----Creating the plot for MASS MISSION LOOP
        self.fig = go.Figure()
        # ----Initializing data points plot for MASS MISSION LOOP
        self.x = [self.MassLoop_1_min.value, self.MassLoop_1_max.value]
        self.y = [self.MassLoop_1_OUT_min.value, self.MassLoop_1_OUT_max.value]

        self.x_mission = [self.MassLoop_1_min.value, self.MassLoop_1_max.value]
        self.y_mission = [self.MissionLoop_1_OUT_min.value, self.MissionLoop_1_OUT_max.value]

        self.fig.add_trace(go.Scatter(name='Mass', x=self.x, y=self.y, mode='lines+markers'))
        self.fig.add_trace(go.Scatter(name='Mission', x=self.x_mission, y=self.y_mission, mode='lines+markers'))
        # set axis labels
        self.fig.update_layout(xaxis_title='MTOW [kg]', yaxis_title='OWE [kg]')
        self.MassMission = go.FigureWidget(self.fig)
        # ----
        self.MTOW_opt = 0 #initializing MTOW optimal value
        def update_massloop(event):
            #this computes the aircrafts structure mass
            a= 0.0191*self.MassLoop_1_min.value**(0.8)
            b= self.MassLoop_2_min.value**(1.2)
            c= self.MassLoop_3_min.value**(-0.2)
            d= self.MassLoop_4_min.value**(-0.2)
            e= math.cos(self.MassLoop_5_min.value*3.1416/180)**(-1)
            wing_weight_min = a*b*c*d*e
            fuselage_weight_min = 0.1*self.MassLoop_1_min.value
            engine_weight_min = self.MassLoop_6_min.value
            landing_gear_weight_min = 0.05*self.MassLoop_1_min.value
            operator_min = 40*self.MassLoop_7_min.value

            OWE_min = (wing_weight_min+fuselage_weight_min+engine_weight_min+landing_gear_weight_min+operator_min)*1.333

            wing_weight_max = 0.019 * math.pow(self.MassLoop_1_max.value, 0.8) * math.pow(self.MassLoop_2_min.value,1.2) *math.pow(self.MassLoop_3_min.value, -0.2) * math.pow(self.MassLoop_4_min.value, -0.2) * math.pow(math.cos(self.MassLoop_5_min.value * math.pi / 180), -1)
            fuselage_weight_max = 0.1 * self.MassLoop_1_max.value
            engine_weight_max = self.MassLoop_6_min.value
            landing_gear_weight_max = 0.05 * self.MassLoop_1_max.value
            operator_max = 40 * self.MassLoop_7_min.value

            OWE_max = (wing_weight_max + fuselage_weight_max + engine_weight_max + landing_gear_weight_max + operator_max) * 1.333

            # this computes the aircrafts mass to complete the mission

            exponent = math.exp((self.Breguet_9.value * 9.8066 * self.Breguet_3.value) / (self.Breguet_2.value * self.Breguet_1.value))
            LandingWeight_min = self.MassLoop_1_min.value / exponent
            LandingWeight_max = self.MassLoop_1_max.value / exponent

            PL = self.MissionLoop_8.value*self.MassLoop_7_min.value

            ZFW_min = LandingWeight_min / (1+ self.MissionLoop_6.value)
            ZFW_max = LandingWeight_max / (1+ self.MissionLoop_6.value)

            OWE_mission_min = ZFW_min - PL
            OWE_mission_max = ZFW_max - PL

            self.MassLoop_1_OUT_min.value = round(OWE_min,3)
            self.MassLoop_1_OUT_max.value = round(OWE_max,3)
            self.MassLoop_2_OUT_min.value = round(operator_min,3)
            self.MassLoop_2_OUT_max.value = round(operator_max,3)
            self.MassLoop_3_OUT_min.value = round(wing_weight_min,3)
            self.MassLoop_3_OUT_max.value = round(wing_weight_max,3)
            self.MassLoop_4_OUT_min.value = round(fuselage_weight_min,3)
            self.MassLoop_4_OUT_max.value = round(fuselage_weight_max,3)
            self.MassLoop_5_OUT_min.value = round(engine_weight_min,3)
            self.MassLoop_5_OUT_max.value = round(engine_weight_max,3)
            self.MassLoop_6_OUT_min.value = round(landing_gear_weight_min,3)
            self.MassLoop_6_OUT_max.value = round(landing_gear_weight_max,3)

            self.MissionLoop_1_OUT_min.value = round(OWE_mission_min,3)
            self.MissionLoop_2_OUT_min.value = round(LandingWeight_min,3)
            self.MissionLoop_3_OUT_min.value = round(ZFW_min,3)
            self.MissionLoop_1_OUT_max.value = round(OWE_mission_max,3)
            self.MissionLoop_2_OUT_max.value = round(LandingWeight_max,3)
            self.MissionLoop_3_OUT_max.value = round(ZFW_max,3)

            Data_Mass_Loop_IN[0] = self.MassLoop_1_min.value # MTOW
            Data_Mass_Loop_IN[1] = self.MassLoop_2_min.value # span in m
            Data_Mass_Loop_IN[2] = self.MassLoop_3_min.value # area in m^2
            Data_Mass_Loop_IN[3] = self.MassLoop_4_min.value # t/c relative thickness
            Data_Mass_Loop_IN[4] = self.MassLoop_5_min.value # quarter chord sweep
            Data_Mass_Loop_IN[5] = self.MassLoop_6_min.value # engine weight
            Data_Mass_Loop_IN[6] = self.MassLoop_7_min.value # Npax
            Data_Mass_Loop_IN[7] = self.MassLoop_1_max.value # MTOW
            Data_Mass_Loop_IN[8] = self.MissionLoop_8.value # kg/pax

            # calculate converged aircraft owe mtow point
            m1 = (self.MassLoop_1_OUT_max.value - self.MassLoop_1_OUT_min .value) /( self.MassLoop_1_max.value - self.MassLoop_1_min.value )
            m2 = (self.MissionLoop_1_OUT_max.value - self.MissionLoop_1_OUT_min.value) / (self.MassLoop_1_max.value - self.MassLoop_1_min.value)

            n1 = self.MassLoop_1_OUT_min.value - m1*self.MassLoop_1_min.value
            n2 = self.MissionLoop_1_OUT_max.value - m2 * self.MassLoop_1_max.value

            X_converged = (n2-n1) /(m1-m2)
            Y_converged = m1*X_converged +n1
            # here finishes the convergence point searching
            self.MTOW_opt = X_converged

            print('The convergence point is: ' + ' MTOW= '+str(round(X_converged,3)) +' kg '+' OWE= '+str(round(Y_converged,3))+' kg' )





            # Open the CSV file in write mode

            with open("BlockImage/Basis/MassLoop/Massloop.csv", 'w') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(Data_Mass_Loop_IN)

            # ----Creating the plot for MASS MISSION LOOP
            self.fig = go.Figure()
            # ----Initializing data points plot for MASS MISSION LOOP
            self.x = [self.MassLoop_1_min.value, self.MassLoop_1_max.value]
            self.y = [self.MassLoop_1_OUT_min.value, self.MassLoop_1_OUT_max.value]

            self.x_mission = [self.MassLoop_1_min.value,self.MassLoop_1_max.value]
            self.y_mission = [self.MissionLoop_1_OUT_min.value,self.MissionLoop_1_OUT_max.value]

            self.fig.add_trace(go.Scatter(name='Mass',x=self.x, y=self.y, mode='lines+markers'))
            self.fig.add_trace(go.Scatter(name='Mission',x=self.x_mission, y=self.y_mission, mode='lines+markers'))
            # set axis labels
            self.fig.update_layout(xaxis_title='MTOW [kg]', yaxis_title='OWE [kg]')
            self.MassMission = go.FigureWidget(self.fig)
            self.MassMission.show()
            # ----

        button_Update_Massloop = widgets.Button(description='Update DATA')
        button_Update_Massloop.icon = 'fa-check'
        button_Update_Massloop.layout.width = 'auto'
        button_Update_Massloop.layout.height = 'auto'
        button_Update_Massloop.on_click(update_massloop)

        C_box_massloop_Min = widgets.VBox(
            children=[self.MassLoop_1_min, self.MassLoop_2_min, self.MassLoop_3_min, self.MassLoop_4_min, self.MassLoop_5_min,self.MassLoop_6_min,
                      self.MassLoop_7_min],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))
        C_box_massloop_Out_Min = widgets.VBox(
            children=[self.MassLoop_1_OUT_min,self.MassLoop_2_OUT_min,self.MassLoop_3_OUT_min,self.MassLoop_4_OUT_min,self.MassLoop_5_OUT_min,self.MassLoop_6_OUT_min],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))

        C_box_massloop_Max = widgets.VBox(
            children=[self.MassLoop_1_max, self.MassLoop_2_min, self.MassLoop_3_min, self.MassLoop_4_min, self.MassLoop_5_min,self.MassLoop_6_min,
                      self.MassLoop_7_min],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))
        C_box_massloop_Out_Max = widgets.VBox(
            children=[self.MassLoop_1_OUT_max,self.MassLoop_2_OUT_max,self.MassLoop_3_OUT_max,self.MassLoop_4_OUT_max,self.MassLoop_5_OUT_max,self.MassLoop_6_OUT_max],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))

        C_box_inter_massloop_min = widgets.HBox(children=[C_box_massloop_Min, C_box_massloop_Out_Min], layout=layout_box)
        C_box_inter_massloop_max = widgets.HBox(children=[C_box_massloop_Max, C_box_massloop_Out_Max], layout=layout_box)


        C_box_missionloop = widgets.VBox(
            children=[self.MissionLoop_1,self.MissionLoop_2,self.MissionLoop_3,self.MissionLoop_4,self.MissionLoop_5,self.MissionLoop_6,self.MissionLoop_7,self.MissionLoop_8],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))
        C_box_missionloop_Out = widgets.VBox(
            children=[self.MissionLoop_1_OUT_min,self.MissionLoop_2_OUT_min,self.MissionLoop_3_OUT_min,self.MissionLoop_1_OUT_max,
                      self.MissionLoop_2_OUT_max,self.MissionLoop_3_OUT_max],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))



        C_box_inter_missionloop = widgets.HBox(children=[C_box_missionloop, C_box_missionloop_Out],
                                                layout=layout_box)


        # Titles in MassMissionLoop
        C_massloop1 = widgets.HTML(value=" <b>Aircraft Mass Loop</b>")
        C_massloop2 = widgets.HTML(value=" <b>Aircraft Mission Loop</b>")
        C_massloop3 = widgets.HTML(value=" <b>Mass Mission Performance Loop</b>")


        self.C_basis_massloop_box = widgets.VBox(children=[button_Update_Massloop,C_massloop1,C_box_inter_massloop_min,
                                 C_box_inter_massloop_max,C_massloop2,C_box_inter_missionloop, C_massloop3],layout=layout_box)



        # Constraint Diagram-----------------------------------------------------------------------------------------------------
        with open("BlockImage/Basis/Constraint/Constraint.csv", 'r') as file:
            csvreader = csv.reader(file, delimiter=',')
            Data_Constraint_IN = []
            for row in csvreader:
                for value in row:
                    Data_Constraint_IN.append(float(value))

        #Vstall data

        self.Constraint_density_at_stall = Data_Constraint_IN[0]  # kg/m^3
        self.Constraint_Clmax = Data_Constraint_IN[1]  # Cl max

        #Take off data
        self.Constraint_TOP = Data_Constraint_IN[2]  # Take off Parameter
        self.Constraint_density_to = Data_Constraint_IN[3]  # kg/m^3
        self.Constraint_density_sl = Data_Constraint_IN[4]  # kg/m^3
        self.Constraint_CL_TO = Data_Constraint_IN[5]  # Cl take off

        #Straight Level Flight
        self.Constraint_Cd0 = Data_Constraint_IN[6]  # Cd0
        self.Constraint_e = Data_Constraint_IN[7]  # Oswalt
        self.Constraint_density_fl = Data_Constraint_IN[8]  # kg/m^3

        # Climb
        self.Constraint_climb_rate = Data_Constraint_IN[9]  # m/s
        self.Constraint_climbing_vel = Data_Constraint_IN[10]  # m/s
        self.Constraint_density_climbing = Data_Constraint_IN[11]  # kg/m^s
        self.Constraint_n = Data_Constraint_IN[12]  # n load factor n=1 if





        self.Constraint_1_Density = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Constraint_density_at_stall,
                                                   description="Density [kg/m^3]", description_tooltip='Density at desired altitude',
                                                  style=style,layout=layout)
        self.Constraint_2_Clmax = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Constraint_Clmax,
                                                   description="Cl max", description_tooltip='Max lift coefficient',
                                                  style=style,layout=layout)
        self.Constraint_3_TOP = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Constraint_TOP,
                                                   description="TOP", description_tooltip='Take Off Parameter',
                                                  style=style,layout=layout)
        self.Constraint_4_Density_TO = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Constraint_density_to,
                                                   description="Density TO [kg/m^3]", description_tooltip='Density at take off',
                                                  style=style,layout=layout)
        self.Constraint_5_Density_SL = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Constraint_density_sl,
                                                   description="Density SL[kg/m^3]", description_tooltip='Density at sea level',
                                                  style=style,layout=layout)
        self.Constraint_6_CL_TO = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Constraint_CL_TO,
                                                   description="Cl Take off", description_tooltip='Lift Coefficient at Take off',
                                                  style=style,layout=layout)

        self.Constraint_7_Cd0 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Constraint_Cd0,
                                                   description="Drag Cd0", description_tooltip='Cd0 coefficient',
                                                  style=style,layout=layout)
        self.Constraint_8_e = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Constraint_e,
                                                   description="Oswalt factor", description_tooltip='Drag lift correction facotr for 3d wings',
                                                  style=style,layout=layout)
        self.Constraint_9_density_FL = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Constraint_density_fl,
                                                   description="Density FL [kg/m^3]", description_tooltip='Density at cruise altitude',
                                                  style=style,layout=layout)
        self.Constraint_10_climb_rate = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Constraint_climb_rate,
                                                   description="dh/dt [m/s]", description_tooltip='Climbing rate',
                                                  style=style,layout=layout)
        self.Constraint_11_climb_velocity = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Constraint_climbing_vel,
                                                   description="V climb [m/S]", description_tooltip='Climb phase velocity',
                                                  style=style,layout=layout)
        self.Constraint_12_density_CL = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Constraint_density_climbing,
                                                   description="Density Climbing [kg/m^3]", description_tooltip='Density at cruise altitude',
                                                  style=style,layout=layout)
        self.Constraint_13_n = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Constraint_n,
                                                   description="Load factor n", description_tooltip='Load factor',
                                                  style=style,layout=layout)

        # ----Creating the plot for MASS MISSION LOOP



        def update_constraint(event):
            #create vector Wing loading
            W_S =numpy.linspace(1000, 7000, num=100)
            #this computes the aircrafts Vstall
            Vstall = math.sqrt(2*self.MTOW_opt*9.8066/(self.Constraint_1_Density.value*self.Constraint_2_Clmax.value*self.MassLoop_3_min.value))
            WingLoading_Stall = 0.5*self.Constraint_1_Density.value*self.Constraint_2_Clmax.value*Vstall**2

            # this computes the take off curve
            density_ratio_sigma = self.Constraint_4_Density_TO.value / self.Constraint_5_Density_SL.value

            T_W_TakeOff = W_S / (self.Constraint_3_TOP.value * density_ratio_sigma * self.Constraint_6_CL_TO.value  )

            # this computes the straight level flight curve
            q = 0.5*self.Constraint_9_density_FL.value*self.Breguet_2.value**2 #dynamic pressure
            AR= (self.MassLoop_2_min.value**2)/(self.MassLoop_3_min.value)
            K = 1/(math.pi*AR*self.Constraint_8_e.value)

            T_W_LevelFlight = q*self.Constraint_7_Cd0.value/W_S + (K/q)*W_S

            # this computes the climbing curve
            q = 0.5*self.Constraint_12_density_CL.value*self.Constraint_11_climb_velocity.value**2

            T_W_Climbing = q*self.Constraint_7_Cd0.value/W_S + (K*self.Constraint_13_n.value**2 /q)*W_S + (1/self.Constraint_11_climb_velocity.value)*self.Constraint_10_climb_rate.value

            Data_Constraint_IN[0] = self.Constraint_1_Density.value  # kg/m^3
            Data_Constraint_IN[1] = self.Constraint_2_Clmax.value  # Cl max
            Data_Constraint_IN[2] = self.Constraint_3_TOP.value  # Cl max
            Data_Constraint_IN[3] = self.Constraint_4_Density_TO.value  # Cl max
            Data_Constraint_IN[4] = self.Constraint_5_Density_SL.value  # Cl max
            Data_Constraint_IN[5] = self.Constraint_6_CL_TO.value  # Cl max
            Data_Constraint_IN[6] = self.Constraint_7_Cd0.value  # Cl max
            Data_Constraint_IN[7] = self.Constraint_8_e.value  # Cl max
            Data_Constraint_IN[8] = self.Constraint_9_density_FL.value  # Cl max
            Data_Constraint_IN[9] = self.Constraint_10_climb_rate.value  # m/s
            Data_Constraint_IN[10] = self.Constraint_11_climb_velocity.value  # m/S
            Data_Constraint_IN[11] = self.Constraint_12_density_CL.value  # kg/m^3
            Data_Constraint_IN[12] = self.Constraint_13_n.value  # load factor



            # Open the CSV file in write mode

            with open("BlockImage/Basis/Constraint/Constraint.csv", 'w') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(Data_Constraint_IN)

            # ----Creating the plot for MASS MISSION LOOP
            fig = go.Figure()
            # ----Initializing data points plot for MASS MISSION LOOP
            x_stall = [WingLoading_Stall, WingLoading_Stall]
            y_stall = [0, 20]

            x_takeoff = W_S
            y_takeoff = T_W_TakeOff

            x_level = W_S
            y_level = T_W_LevelFlight

            x_climbing = W_S
            y_climbing = T_W_Climbing

            fig.add_trace(go.Scatter(name='V stall', x=x_stall, y=y_stall, mode='lines+markers'))
            fig.add_trace(go.Scatter(name='Take Off', x=x_takeoff, y=y_takeoff, mode='lines+markers'))
            fig.add_trace(go.Scatter(name='Straight level flight', x=x_level, y=y_level, mode='lines+markers'))
            fig.add_trace(go.Scatter(name='Climbing', x=x_climbing, y=y_climbing, mode='lines+markers'))

            # set axis labels
            fig.update_layout(xaxis_title='W/S [N/m^2]', yaxis_title='T/W')
            ConstraintGraph = go.FigureWidget(fig)
            ConstraintGraph.show()
            # ----

        button_Update_Constraint = widgets.Button(description='Update DATA')
        button_Update_Constraint.icon = 'fa-check'
        button_Update_Constraint.layout.width = 'auto'
        button_Update_Constraint.layout.height = 'auto'
        button_Update_Constraint.on_click(update_constraint)




        C_box_constraint_stall = widgets.VBox(children=[self.Constraint_1_Density,self.Constraint_2_Clmax],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))

        C_box_constraint_takeoff = widgets.VBox(children=[self.Constraint_3_TOP,self.Constraint_4_Density_TO,
                                                        self.Constraint_5_Density_SL,self.Constraint_6_CL_TO],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))

        C_box_constraint_level = widgets.VBox(children=[self.Constraint_7_Cd0,self.Constraint_8_e,self.Constraint_9_density_FL],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))
        C_box_constraint_climb = widgets.VBox(children=[self.Constraint_10_climb_rate,self.Constraint_11_climb_velocity,
                                                        self.Constraint_12_density_CL,self.Constraint_13_n],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))

        # Titles in MassMissionLoop
        C_constraint1 = widgets.HTML(value=" <b>V stall inputs</b>")
        C_constraint2 = widgets.HTML(value=" <b>Take Off</b>")
        C_constraint3 = widgets.HTML(value=" <b>Landing</b>")
        C_constraint4 = widgets.HTML(value=" <b>Climb</b>")
        C_constraint5 = widgets.HTML(value=" <b>Straight Level Flight</b>")

        self.C_basis_constraint_box = widgets.VBox(children=[button_Update_Constraint,C_constraint1,C_box_constraint_stall,
                                                             C_constraint2,C_box_constraint_takeoff,C_constraint3,
                                                             C_constraint4,C_box_constraint_climb,C_constraint5,C_box_constraint_level],layout=layout_box)




        # GENERAL INPUTS MENU for BASIS LEARNING FEATURE
        self.tab_Basis_IN = widgets.Tab(children=[self.C_basis_box,self.C_basis_massloop_box,self.C_basis_constraint_box])
        self.tab_Basis_IN.set_title(0, 'Breguet')
        self.tab_Basis_IN.set_title(1, 'Mass Loop Performance')
        self.tab_Basis_IN.set_title(2, 'Constraint Diagram')
        display(self.tab_Basis_IN)
        return self.tab_Basis_IN


    def demo_exo(self, event=None):
        clear_output()
        display(self.BOX_INPUT)

        # Layout widget
        layout = widgets.Layout(width="75%", height='50px', justify_content='space-between')
        style = style = {'description_width': 'initial'}
        self.INPUT_FILE_EXO = self.OAD.Generate_Input_File_Exo()
        #here we have input file + configuration already created

        self.INPUT_EXO = self.OAD.Input_File(self.INPUT_FILE_EXO)
        #here we can access the values of our input file

        List_StudyName = []

        self.Variable_Exo_1 = self.INPUT_EXO["data:TLAR:NPAX"].value[0]
        self.Variable_Exo_2 = self.INPUT_EXO["data:TLAR:approach_speed"].value[0]
        self.Variable_Exo_3 = self.INPUT_EXO["data:TLAR:cruise_mach"].value[0]
        self.Variable_Exo_4 = self.INPUT_EXO["data:TLAR:range"].value[0]
        self.Variable_Exo_5 = self.INPUT_EXO["data:weight:aircraft:max_payload"].value[0]
        self.Variable_Exo_6 = self.INPUT_EXO["data:weight:aircraft:payload"].value[0]
        self.Variable_Exo_7 = self.INPUT_EXO["data:geometry:wing:aspect_ratio"].value[0]
        self.Variable_Exo_8 = self.INPUT_EXO["data:propulsion:rubber_engine:bypass_ratio"].value[0]
        #herer we have each varaible of interest stored

        self.In_Variable_Exo_1 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Variable_Exo_1,
                                                   description="Npax", description_tooltip='Number of Passengers',
                                                  style=style,layout=layout)
        self.In_Variable_Exo_2 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Variable_Exo_2,
                                                   description="Vapp ", description_tooltip='Approach speed [m/s]',
                                                  style=style,layout=layout)
        self.In_Variable_Exo_3 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Variable_Exo_3,
                                                   description="Mcr", description_tooltip='Cruise mach',
                                                  style=style,layout=layout)
        self.In_Variable_Exo_4 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Variable_Exo_4,
                                                   description="Range", description_tooltip='Aircraft range  [NM]',
                                                  style=style,layout=layout)
        self.In_Variable_Exo_5 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Variable_Exo_5,
                                                   description="Max PL ", description_tooltip='Maximum payload [kg]',
                                                  style=style,layout=layout)
        self.In_Variable_Exo_6 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Variable_Exo_6,
                                                   description="PL ", description_tooltip='Payload [kg]',
                                                  style=style,layout=layout)
        self.In_Variable_Exo_7 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Variable_Exo_7,
                                                   description="AR", description_tooltip='Aspect ratio',
                                                  style=style,layout=layout)
        self.In_Variable_Exo_8 = widgets.BoundedFloatText(min=0, max=900000, step=0.1, value=self.Variable_Exo_8,
                                                   description="BPR", description_tooltip='Bypass ratio of the engine',
                                                  style=style,layout=layout)
        self.StudyName = widgets.Text(description="NAME",placeholder='Write a name for you modification',style=style,layout=layout)

        def save_variable_interests(event):

            self.INPUT_EXO["data:TLAR:NPAX"].value = self.In_Variable_Exo_1.value
            self.INPUT_EXO["data:TLAR:approach_speed"].value = self.In_Variable_Exo_2.value
            self.INPUT_EXO["data:TLAR:cruise_mach"].value = self.In_Variable_Exo_3.value
            self.INPUT_EXO["data:TLAR:range"].value = self.In_Variable_Exo_4.value
            self.INPUT_EXO["data:weight:aircraft:max_payload"].value = self.In_Variable_Exo_5.value
            self.INPUT_EXO["data:weight:aircraft:payload"].value = self.In_Variable_Exo_6.value
            self.INPUT_EXO["data:geometry:wing:aspect_ratio"].value = self.In_Variable_Exo_7.value
            self.INPUT_EXO["data:propulsion:rubber_engine:bypass_ratio"].value = self.In_Variable_Exo_8.value

            self.INPUT_EXO.save()
            List_StudyName.append(self.StudyName)
            print('The variables have been updated')

        self.button_Update_Variables = widgets.Button(description='Update VoI',description_tooltip='Update Variables of Interest')
        self.button_Update_Variables.icon = "fa-check"
        self.button_Update_Variables.layout.width = 'auto'
        self.button_Update_Variables.layout.height = 'auto'
        self.button_Update_Variables.on_click(save_variable_interests)

        # here, after this save function, the new values modifies by the user are changed in the input file
        def RUN_MDA_EXO_Function():
            MDA_problem_exo = self.OAD.RUN_OAD_EXO() # This runs the MDA problem
            self.OAD.Save_File(MDA_problem_exo.output_file_path, "OUTPUT_EXO", str(self.StudyName.value))
            self.OAD.Save_CSV_File("workdir\oad_sizing.csv", "OUTPUT_EXO", str(self.StudyName.value))
            return MDA_problem_exo
        # Function to update the progress bar
        def update_progress_bar():
            total_iterations = 100
            custom_widget = [
                'Progress: ',progressbar.Bar(marker='█', left='', right='|'),
                ' ',progressbar.Percentage()]
            with progressbar.ProgressBar(widgets=custom_widget,max_value=total_iterations) as bar:
                for i in range(total_iterations):
                    # Update progress bar
                    time.sleep(0.02)  # Simulate time for updating progress
                    bar.update(i + 1)
        def RUN_MDA_EXO(event):
            # Create a thread for the simulation
            simulation_thread = threading.Thread(target=RUN_MDA_EXO_Function)
            print('The problem is being solved: ☕... ')
            # Start the simulation thread
            simulation_thread.start()
            # Start the progress bar thread
            update_progress_bar()
            # Wait for the simulation thread to complete
            simulation_thread.join()
            print('Problem solved.')
            time.sleep(2)  # Simulate time for updating progress
            clear_output()
            display(self.BOX_INPUT)

            button_plots = widgets.Button(description='Update Plots')
            button_plots.icon = 'fa-check'
            button_plots.layout.width = 'auto'
            button_plots.layout.height = 'auto'
            button_plots.on_click(self.UpdatePlots)

            path_to_target = "OUTPUT_EXO"
            path_to_file_list_xml = []
            temp = os.listdir(path_to_target)
            for i in range(0, len(temp)):
                if temp[i][-3:] == 'xml':
                    path_to_file_list_xml.append(temp[i])

            self.output_list_exo_xml = widgets.SelectMultiple(options=path_to_file_list_xml,
                                                              description='Select an Aircraft:', disabled=False,
                                                              style={'description_width': 'initial'},
                                                              layout=widgets.Layout(width="300px", height="150 px"),
                                                              rows=len(path_to_file_list_xml))
            self.C_select = widgets.HBox(children=[self.output_list_exo_xml,button_plots],
                                                  layout=widgets.Layout(border='2px solid black', align_items='center',
                                                                        justify_content='space-around',
                                                                        padding='5px', width='100%'))
            display(self.C_select)

        #Function to run the problem with Performance Module
        def RUN_MDA_EXO_Function_Perfo():
            MDA_problem_exo = self.OAD.RUN_OAD_EXO_PERFO() # This runs the MDA problem
            self.OAD.Save_File(MDA_problem_exo.output_file_path, "OUTPUT_EXO", str(self.StudyName.value))
            self.OAD.Save_CSV_File("workdir\oad_sizing.csv", "OUTPUT_EXO", str(self.StudyName.value))
            return MDA_problem_exo
        # Function to update the progress bar
        def update_progress_bar2():
            total_iterations = 100
            custom_widget = [
                'Progress: ',progressbar.Bar(marker='█', left='', right='|'),
                ' ',progressbar.Percentage()]
            with progressbar.ProgressBar(widgets=custom_widget,max_value=total_iterations) as bar:
                for i in range(total_iterations):
                    # Update progress bar
                    time.sleep(1.7)  # Simulate time for updating progress
                    bar.update(i + 1)

        def RUN_MDA_EXO_PERFO(event):
            # Create a thread for the simulation
            simulation_thread = threading.Thread(target=RUN_MDA_EXO_Function_Perfo)
            print('The problem is being solved (PERFORMANCE MODULE USED): ☕... ')
            # Start the simulation thread
            simulation_thread.start()
            # Start the progress bar thread
            update_progress_bar2()
            # Wait for the simulation thread to complete
            simulation_thread.join()
            print('Problem solved.')
            time.sleep(2)  # Simulate time for updating progress
            clear_output()
            display(self.BOX_INPUT)

            button_plots = widgets.Button(description='Update Plots')
            button_plots.icon = 'fa-check'
            button_plots.layout.width = 'auto'
            button_plots.layout.height = 'auto'
            button_plots.on_click(self.UpdatePlots)

            path_to_target = "OUTPUT_EXO"
            path_to_file_list_xml = []
            temp = os.listdir(path_to_target)
            for i in range(0, len(temp)):
                if temp[i][-3:] == 'xml':
                    path_to_file_list_xml.append(temp[i])

            self.output_list_exo_xml = widgets.SelectMultiple(options=path_to_file_list_xml,
                                                              description='Select an Aircraft:', disabled=False,
                                                              style={'description_width': 'initial'},
                                                              layout=widgets.Layout(width="300px", height="150 px"),
                                                              rows=len(path_to_file_list_xml))
            self.C_select = widgets.HBox(children=[self.output_list_exo_xml, button_plots],
                                         layout=widgets.Layout(border='2px solid black', align_items='center',
                                                               justify_content='space-around',
                                                               padding='5px', width='100%'))
            display(self.C_select)


        #here we run the EXO problem
        self.button_Run_Exo = widgets.Button(description='LAUNCH')
        self.button_Run_Exo.icon = 'fa-rocket'
        self.button_Run_Exo.layout.width = 'auto'
        self.button_Run_Exo.layout.height = 'auto'
        self.button_Run_Exo.on_click(RUN_MDA_EXO)
        #here we run the EXO problem
        self.button_Run_Exo_Perfo = widgets.Button(description='LAUNCH Performance')
        self.button_Run_Exo_Perfo.icon = 'fa-rocket'
        self.button_Run_Exo_Perfo.layout.width = 'auto'
        self.button_Run_Exo_Perfo.layout.height = 'auto'
        self.button_Run_Exo_Perfo.on_click(RUN_MDA_EXO_PERFO)

        self.fig1 = oad.wing_geometry_plot("workdir/oad_sizing_out_exo.xml")
        self.fig2 = oad.aircraft_geometry_plot("workdir/oad_sizing_out_exo.xml")
        self.fig3 = oad.drag_polar_plot("workdir/oad_sizing_out_exo.xml")
        self.fig4 = self.OAD.payload_range("workdir/oad_sizing_out_exo.xml", "workdir/oad_sizing_exo.csv",name='oad_sizing_exo')
        self.fig5 = oad.mass_breakdown_bar_plot("workdir/oad_sizing_out_exo.xml", name='oad_sizing_exo')
        self.fig6 = oad.mass_breakdown_sun_plot("workdir/oad_sizing_out_exo.xml")
        self.output_fig5 = widgets.Output()
        with self.output_fig5:
            display(self.fig5)
        self.output_fig5 = go.FigureWidget(self.fig5)

        self.output_fig6 = widgets.Output()
        with self.output_fig6:
            display(self.fig6)
        self.output_fig6 = go.FigureWidget(self.fig6)
        self.output_fig7 = widgets.Output()
        Mission = [pth.join('workdir', 'oad_sizing_exo.csv')]
        name = ['oad_sizing_exo']
        with self.output_fig7:
            self.fig7 = self.OAD.MISSION_PLOT(Mission,name)


        self.tab_Analysis_Exo_1 = widgets.Tab(children=[self.fig1,self.fig2,self.fig3,self.output_fig5,
                                                        self.output_fig6,self.fig4,self.output_fig7])
        self.tab_Analysis_Exo_1.set_title(0, 'Wing Geometry')
        self.tab_Analysis_Exo_1.set_title(1, 'Aircraft Geometry')
        self.tab_Analysis_Exo_1.set_title(2, 'Drag polar')
        self.tab_Analysis_Exo_1.set_title(3, 'Bar Mass breakdown')
        self.tab_Analysis_Exo_1.set_title(4, 'SUN Mass Breakdown')
        self.tab_Analysis_Exo_1.set_title(5, 'Payload-Range')
        self.tab_Analysis_Exo_1.set_title(6, 'Mission')




        C_exo1 = widgets.HTML(value=" <b><u>Variables of Interest</u></b>")
        C_exo1_1 = widgets.HTML(value=" <u>TLARS</u>")
        C_exo1_2 = widgets.HTML(value=" <u>Weight</u>")
        C_exo1_3 = widgets.HTML(value=" <u>Wing Geo</u>")
        C_exo1_4 = widgets.HTML(value=" <u>Propulsion</u>")
        C_exo2 = widgets.HTML(value=" <b><u>Analysis Tool Side</u></b>")

        #here we have the inputs as varaibles of interest + the update button
        C_Vertical_box1 = widgets.VBox(children=[C_exo1,C_exo1_1,self.In_Variable_Exo_1,self.In_Variable_Exo_2,self.In_Variable_Exo_3,
            self.In_Variable_Exo_4,C_exo1_2,self.In_Variable_Exo_5,self.In_Variable_Exo_6,C_exo1_3,self.In_Variable_Exo_7,C_exo1_4,
            self.In_Variable_Exo_8,self.StudyName,self.button_Update_Variables],
                  layout=widgets.Layout(border='2px solid black', align_items='center', padding='2px', width='40%'))


        C_Vertical_box2 = widgets.VBox(children=[C_exo2,self.tab_Analysis_Exo_1],
            layout=widgets.Layout(border='2px solid black', align_items='center', padding='5px', width='200%'))


        self.C_Horizontal_box1 = widgets.HBox(children=[self.button_Run_Exo,self.button_Run_Exo_Perfo],
            layout=widgets.Layout(border='2px solid black', align_items='center',justify_content='space-around',
                                  padding='5px', width='100%'))

        self.C_Horizontal_box2 = widgets.HBox(children=[C_Vertical_box1,C_Vertical_box2],
            layout=widgets.Layout(border='2px solid black', align_items='center', padding='5px', width='100%'))


        self.Vertical_box3 = widgets.VBox(children=[self.C_Horizontal_box1,self.C_Horizontal_box2],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='5px', width='100%'))

        return display(self.Vertical_box3)

    def UpdatePlots(self,event):
        clear_output()
        display(self.BOX_INPUT)
        display(self.C_select)

        liste_exo_xml = self.output_list_exo_xml.value
        path = "OUTPUT_EXO"
        XML_Liste_Design = []
        XML_Liste_Name = []
        CSV_Liste_Design = []
        CSV_Liste_Name = []
        i = 0
        while (i < len(liste_exo_xml)):
            OUTPUT = pth.join(path, liste_exo_xml[i])
            XML_Liste_Design.append(OUTPUT)
            OUTPUT= OUTPUT[:-3]
            OUTPUT += "csv"
            CSV_Liste_Design.append(OUTPUT)
            name = os.path.splitext(os.path.split(liste_exo_xml[i])[1])[0]
            XML_Liste_Name.append(name)
            CSV_Liste_Name.append(name)
            i = i + 1

        # here we have different plots
        self.fig1 = oad.wing_geometry_plot(XML_Liste_Design[0], XML_Liste_Name[0])
        self.fig2 = oad.aircraft_geometry_plot(XML_Liste_Design[0], XML_Liste_Name[0])
        self.fig3 = oad.drag_polar_plot(XML_Liste_Design[0], XML_Liste_Name[0])
        self.fig4 = self.OAD.payload_range(XML_Liste_Design[0], CSV_Liste_Design[0],name=XML_Liste_Name[0])
        self.fig5 = oad.mass_breakdown_bar_plot(XML_Liste_Design[0], name=XML_Liste_Name[0])
        self.fig6 = oad.mass_breakdown_sun_plot(XML_Liste_Design[0])
        i = 1
        while (i < len(liste_exo_xml)):
            self.fig1 = oad.wing_geometry_plot(XML_Liste_Design[i],XML_Liste_Name[i],fig=self.fig1)
            self.fig2 = oad.aircraft_geometry_plot(XML_Liste_Design[i],XML_Liste_Name[i],fig=self.fig2)
            self.fig3 = oad.drag_polar_plot(XML_Liste_Design[i],XML_Liste_Name[i],fig=self.fig3)
            self.fig4 = self.OAD.payload_range(XML_Liste_Design[i], CSV_Liste_Design[i],name=XML_Liste_Name[i],fig=self.fig4)
            self.fig5 = oad.mass_breakdown_bar_plot(XML_Liste_Design[i], name=XML_Liste_Name[i],fig=self.fig5)
            self.fig6 = oad.mass_breakdown_sun_plot(XML_Liste_Design[i])
            i = i + 1


        self.output_fig5 = go.FigureWidget(self.fig5)
        self.output_fig6 = go.FigureWidget(self.fig6)
        self.output_fig7 = widgets.Output()
        with self.output_fig7:
            self.fig7 = self.OAD.MISSION_PLOT(CSV_Liste_Design, CSV_Liste_Name)

        self.tab_Analysis_Exo_1 = widgets.Tab(children=[self.fig1, self.fig2, self.fig3, self.output_fig5,
                                                        self.output_fig6,self.fig4, self.output_fig7])
        self.tab_Analysis_Exo_1.set_title(0, 'Wing Geometry')
        self.tab_Analysis_Exo_1.set_title(1, 'Aircraft Geometry')
        self.tab_Analysis_Exo_1.set_title(2, 'Drag polar')
        self.tab_Analysis_Exo_1.set_title(3, 'Bar Mass breakdown')
        self.tab_Analysis_Exo_1.set_title(4, 'SUN Mass Breakdown')
        self.tab_Analysis_Exo_1.set_title(5, 'Payload-Range')
        self.tab_Analysis_Exo_1.set_title(6, 'Mission')

        #here we have the luanch button
        C_exo1 = widgets.HTML(value=" <b><u>Variables of Interest</u></b>")
        C_exo1_1 = widgets.HTML(value=" <u>TLARS</u>")
        C_exo1_2 = widgets.HTML(value=" <u>Weight</u>")
        C_exo1_3 = widgets.HTML(value=" <u>Wing Geo</u>")
        C_exo1_4 = widgets.HTML(value=" <u>Propulsion</u>")
        C_exo2 = widgets.HTML(value=" <b><u>Analysis Tool Side</u></b>")

        #here we have the inputs as varaibles of interest + the update button
        C_Vertical_box1 = widgets.VBox(children=[C_exo1,C_exo1_1,self.In_Variable_Exo_1,self.In_Variable_Exo_2,self.In_Variable_Exo_3,
            self.In_Variable_Exo_4,C_exo1_2,self.In_Variable_Exo_5,self.In_Variable_Exo_6,C_exo1_3,self.In_Variable_Exo_7,C_exo1_4,
            self.In_Variable_Exo_8,self.StudyName,self.button_Update_Variables],
                  layout=widgets.Layout(border='2px solid black', align_items='center', padding='2px', width='40%'))
        C_Vertical_box2 = widgets.VBox(children=[C_exo2,self.tab_Analysis_Exo_1],
            layout=widgets.Layout(border='2px solid black', align_items='center', padding='5px', width='200%'))
        self.C_Horizontal_box1 = widgets.HBox(children=[self.button_Run_Exo,self.button_Run_Exo_Perfo],
            layout=widgets.Layout(border='2px solid black', align_items='center',justify_content='space-around',
                                  padding='5px', width='100%'))
        self.C_Horizontal_box2 = widgets.HBox(children=[C_Vertical_box1,C_Vertical_box2],
            layout=widgets.Layout(border='2px solid black', align_items='center', padding='5px', width='100%'))
        self.Vertical_box3 = widgets.VBox(children=[self.C_Horizontal_box1,self.C_Horizontal_box2],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='5px', width='100%'))

        print('Plots have been updated.')
        return display(self.Vertical_box3)





#function to move from the principal
# menu to the aircraft_reference interface
    def menu_to_reference(self,event):
        clear_output()
        self.ref = self.reference_aircraft(self.path1)
        print("REFERENCE AIRCRAFT PHASE")
        print(
            "-----------------------------------------------------------------------------------------------------------")
        print(
            "-----------------------------------------------------------------------------------------------------------")
        return self.ref

    def menu_to_input(self, event):
        clear_output()
        input_ui = self.inputs_ui()
        self.INPUT_FILE = self.OAD.Generate_Input_File()

        # AIRCRAFT INPUTS DATA PHASE TO CONFIGURATION PHASE

    def input_to_configuration(self, event):
        clear_output()
        display(self.BOX_CONFIG)

        # AIRCRAFT INPUTS DATA PHASE TO RUN MDA ANALYSIS PHASE

    def input_to_mda(self, event):
        clear_output()
        self.Button_M3.style.button_color = "#ebebeb"
        self.Button_M4.style.button_color = "#00d600"
        image_path="Images/Wing.jpg"
        custom_css = f'''
        .vbox-with-background {{
            background-image: url("{image_path}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            width: 100%;
            height: 100%;
        }}
        '''
        display(HTML(f'<style>{custom_css}</style>'),self.menu)
        print("MDA ANALYSIS PHASE")
        print(
            "-------------------------------------------------------------------------------------------------------------------------------")
        print(
            "-------------------------------------------------------------------------------------------------------------------------------")

        # INTERFACE FOR THE AIRCRAFT INPUT DATA


#The Interface for choosing the reference aircraft file


    def dropdown_reference(self,change):

        ref=self.OAD.Source_File(self.path1,change.new)

        self.Button_S3.disabled = False
        self.Button_S1.disabled = False
        # This button is from Aircraft Reference GUI, when this function is called,
        # it means a reference aircraft has been selected and the user is now prep to go to the next phase. Hence the
        # NEXT button = Button_S3 is enabled and so the Data Viewer Button = Button_S1

        print("Your choose  "+ str(change.new) + " as your reference aircraft file.")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        return ref


   # function for viewing the reference aircraft data

    def view_source(self,event):
        clear_output()
        display(self.REF_BOX)
        self.ref_view=self.OAD.reference_view()


    #function for deliting the choosen aircrafte reference data

    def delete_reference(self,event):
        clear_output()
        display(self.REF_BOX)
        self.delete_ref=self.OAD.Delete_File('data\Aircraft_reference_data.xml')
        print("Your referene aircraft data file suppressed")

        print("Choose your reference file")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        return self.delete_ref

  # The next step after choosing the reference aircraft file
    def reference_to_configuration (self,event):
        clear_output()
        self.Button_M1.style.button_color='#ebebeb'
        self.Button_M2.style.button_color="#00d600"
        self.Button_M2.disabled=False
        image_path="Images/Wing.jpg"
        custom_css = f'''
        .vbox-with-background {{
            background-image: url("{image_path}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            width: 100%;
            height: 100%;
        }}
        '''
        display(HTML(f'<style>{custom_css}</style>'),self.menu)
        print("CONFIGRATION PHASE")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------------------------")


    #User interface for the
    #reference aircrfat choice step
    def reference_aircraft(self,path_to_target):
        self.state_next_ref = False

        self.path_to_target=path_to_target
        self.path_to_file_list = []
        temp=os.listdir(self.path_to_target)
        for i in range(0, len(temp)):
            if temp[i][-3:] =='xml':
                self.path_to_file_list.append(temp[i])
        x="Click and select" # It is used to appear as default name at the dropdown list
        self.path_to_file_list.append(x)
        self.path_to_file_list.reverse()
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        title=widgets.HTML(value=" <b>Choose your reference aircraft file</b>")
        box1 = widgets.HBox(children=[title],layout=layout_title)
        datafile_name = widgets.Dropdown(options=self.path_to_file_list,description='Choose your file:',disabled=False,style={'description_width': 'initial'})
        datafile_name.observe(self.dropdown_reference,names="value")
        box2=widgets.HBox(children=[datafile_name])

       # Display the data of your reference aircraft
        self.Button_S1=widgets.Button(description="Reference data",layout=Layout(width='20%', height='50px', border='4px solid black'),disabled=True, style=dict(button_color='#adadad'))
        self.Button_S1.on_click(self.view_source)
        self.Button_S1.icon = 'fa-table'

        # Delete the reference aircraft file already chosen
        Button_S2=widgets.Button(description="Delete",layout=Layout(width='20%', height='50px', border='4px solid black'),style=dict(button_color='#ff5252'))
        Button_S2.on_click(self.delete_reference)
        Button_S2.icon = 'fa-trash-o'
        # Show the principal interface user for   the configuration step
        self.Button_S3=widgets.Button(description="Next",layout=Layout(width='20%', height='50px', border='4px solid black'),disabled=True, style=dict(button_color='#77db5c'))
        self.Button_S3.on_click (self.reference_to_configuration)
        self.Button_S3.icon='fa-angle-right'
        box3=widgets.HBox(children=[self.Button_S1,Button_S2,self.Button_S3],layout=Layout(justify_content='space-between',width='100%'))

        #---------------------------------------------------------------------------------------------------------------
        buttonINFO = widgets.Button(description='')
        buttonINFO.icon = 'fa-info-circle'
        buttonINFO.layout.width = 'auto'
        buttonINFO.layout.height = 'auto'
        output = widgets.Output()
        def info_message(event):
            with output:
                output.clear_output()
                if len(output.outputs) > 0:
                    output.clear_output()

                else:
                    print('This is the reference Aircraft Phase. The user is expected to select an aircraft from the list.\n'
                          'When it is selected it is stored as the reference.\n'
                          'The user can visualize the data by clicking the button Reference Data,\n'
                          'erase the stored referenced aircraft with  Delete or go to the next step with Next, but only once an aircraft is selected.\n')

        buttonINFO.on_click(info_message)
        #---------------------------------------------------------------------------------------------------------------
        buttonHOME = widgets.Button(description='')
        buttonHOME.icon = 'fa-home'
        buttonHOME.layout.width = 'auto'
        buttonHOME.layout.height = 'auto'
        buttonHOME.on_click(self.HomeInterface)
        #---------------------------------------------------------------------------------------------------------------
        box4 = widgets.Box(children=[buttonINFO, output,buttonHOME], layout=Layout(border='1px solid black',
                           margin='50 0 50 0px', padding='0.5px', align_items='center', width='100'))
        self.REF_BOX=widgets.VBox(children=[box1,box2,box3,box4],layout=Layout(border='6px solid black', padding='10px', align_items='center', width='100%'))

        display(self.REF_BOX)

        return datafile_name


# CONFIGURATION
    def configuration_file(self,event):
        clear_output()
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        title=widgets.HTML(value=" <b>Choose MDA PROBLEM</b>")
        box1 = widgets.HBox(children=[title],layout=layout_title)

        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        liste=["geometry","weight","mtow","aerodynamics_highspeed","aerodynamics_lowspeed","aerodynamics_takeoff","aerodynamics_landing","performance","hq_tail_sizing","hq_static_margin","wing_area"]
        self.module = widgets.SelectMultiple(options=liste,description='SELECT FAST-OAD MODULES:',disabled=False,style={'description_width': 'initial'},layout=widgets.Layout(width="800px", height="150 px"),rows=len(liste))
        button=widgets.Button(description="SAVE",tooltip="SAVE MDA PROBLEM",layout=layout_button,style=dict(button_color="#33ffcc"))
        button.on_click(self.Write_Configuration_File)
        button.icon = 'fa-floppy-o'
        self.Button_F1=widgets.Button(description="Modules list",layout=Layout(width='20%', height='50px', border='4px solid black'),disabled=True, style=dict(button_color='#ebebeb'))
        self.Button_F1.on_click(self.view_modules)
        self.Button_F1.icon = 'fa-list'

        self.Button_F2=widgets.Button(description="Variables list",layout=Layout(width='20%', height='50px', border='4px solid black'),disabled=True, style=dict(button_color='#ebebeb'))
        self.Button_F2.on_click(self.view_variables)
        self.Button_F2.icon = 'fa-list'

        self.Button_F3=widgets.Button(description="N2 Diagramm",layout=Layout(width='20%', height='50px', border='4px solid black'),disabled=True, style=dict(button_color='#ebebeb'))
        self.Button_F3.on_click(self.n2_diagramm)

        self.Button_F4=widgets.Button(description="XDSM Diagramm",layout=Layout(width='20%', height='50px', border='4px solid black'),disabled=True, style=dict(button_color='#ebebeb'))
        self.Button_F4.on_click(self.xdsm_diagramm)

        box2=widgets.HBox(children=[self.Button_F1,self.Button_F2,self.Button_F3,self.Button_F4],layout=Layout(justify_content='space-between',width='100%'))

        Button_F5=widgets.Button(description="BACK",layout=Layout(width='20%', height='45px', border='4px solid black'),style=dict(button_color='#3785d8'))
        Button_F5.on_click(self.configuration_to_reference)
        Button_F5.icon = 'fa-angle-left'

        self.Button_F6=widgets.Button(description="NEXT",layout=Layout(width='20%', height='45px', border='4px solid black'),disabled=True, style=dict(button_color='#77db5c'))
        self.Button_F6.on_click(self.configuration_to_input)
        self.Button_F6.icon = 'fa-angle-right'

        #---------------------------------------------------------------------------------------------------------------
        buttonINFO = widgets.Button(description='')
        buttonINFO.icon = 'fa-info-circle'
        buttonINFO.layout.width = 'auto'
        buttonINFO.layout.height = 'auto'
        output = widgets.Output()
        def info_message(event):
            with output:
                output.clear_output()
                if len(output.outputs) > 0:
                    output.clear_output()
                else:
                    print('Welcome to the Configuration Phase.\n'
                          'Please, select one or more modules that you would like to add and click SAVE.\n'
                          'Then, different features will be enabled, and you will be allowed to proceed.  \n')

        buttonINFO.on_click(info_message)
        box4 = widgets.Box(children=[buttonINFO, output],layout=Layout(border='1px solid black',
                                         margin='50 0 50 0px', padding='5px', align_items='center', width='100'))
        #---------------------------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------------------------
        buttonHOME = widgets.Button(description='')
        buttonHOME.icon = 'fa-home'
        buttonHOME.layout.width = 'auto'
        buttonHOME.layout.height = 'auto'
        buttonHOME.on_click(self.HomeInterface)
        #---------------------------------------------------------------------------------------------------------------
        box3 = widgets.HBox(children=[Button_F5,buttonHOME, self.Button_F6],layout=Layout(justify_content='space-between', width='100%'))
        self.BOX_CONFIG=widgets.VBox(children=[box1,self.module,button, box2,box3,box4],layout=Layout(border='6px solid black', padding='10px', align_items='center', width='100%'))
        display(self.BOX_CONFIG)


 #WRITE THE CHOSEN MODULES IN THE CONFIGURATION FILE
    def Write_Configuration_File(self,event):
        clear_output()
        display(self.BOX_CONFIG)
        modules=self.module.value
        self.OAD.write_configuration(modules)
        file_name="oad_sizing.yml"

        self.OAD.Configuration_File(file_name)

        self.Button_F1.disabled = False
        self.Button_F2.disabled = False
        self.Button_F3.disabled = False
        self.Button_F4.disabled = False
        self.Button_F6.disabled = False
        # These are the buttons from phase 2 GUI (config), when this function is called,
        # it means the modules has been selected and saved and the user is now prep to go to the next phase. Hence the
        # NEXT button = Button_F63  and the rest features are enabled.


    # Function back to the aircrft reference file user
    def configuration_to_reference(self,event):
        clear_output()
        #self.reference_aircraft(self.path1)
        display(self.REF_BOX)

    # Configuration step to inputs data step

    def configuration_to_input (self,event):
        clear_output()
        self.Button_M2.style.button_color='#ebebeb'
        self.Button_M3.style.button_color="#00d600"
        self.Button_M3.disabled=False
        image_path="Images/Wing.jpg"
        custom_css = f'''
        .vbox-with-background {{
            background-image: url("{image_path}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            width: 100%;
            height: 100%;
        }}
        '''
        display(HTML(f'<style>{custom_css}</style>'),self.menu)
        print("AIRCRAFT INPUTS DATA PHASE")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------------------------")

    #View modules by the modules list button

    def view_modules(self,event):
        clear_output()
        display(self.BOX_CONFIG)
        self.list_mod=self.OAD.liste_modules()
        return self.list_mod

    #View modules by the variable list button

    def view_variables(self,event):
        clear_output()
        display(self.BOX_CONFIG)
        self.list_var=self.OAD.liste_variables()
        return self.list_var

     # Display the N2 Diagramm of the design case
    def n2_diagramm(self,event):
        clear_output()
        display(self.BOX_CONFIG)
        self.n2=self.OAD.N2_Diagramm()
        return self.n2



    # Display the XSDM Diagramm of the design case
    def xdsm_diagramm(self,event):
        clear_output()
        display(self.BOX_CONFIG)
        self.xdsm=self.OAD.XDSM_Diagramm()
        return self.xdsm


    def view_input_data(self,event):
        clear_output()
        display(self.BOX_INPUT)
        self.input_view_data=self.OAD.View_inputs_data(self.INPUT_FILE)
        return self.input_view_data


# User interfaces for the inputs phases

# Principal inputs UI

    def inputs_ui(self):
        clear_output()
        table1=["VIEW AIRCRAFT DATA","EDIT AIRCRAFT INPUT DATA","SAVE AIRCRAFT  INPUT FILE"]
        table2=["BACK", "DELETE INPUT FILE", "NEXT"]
        title=widgets.HTML(value=" <b>AIRCRFAT INPUTS DATA </b>")
        layout_button=Layout(width='30%', height='40px', border='4px solid black')
        layout_box = Layout(width='100%',padding='10px')
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        Button_I1=widgets.Button(description=table1[0], layout=layout_button, style=dict(button_color='#ebebeb'))
        Button_I1.on_click(self.view_input_data)
        Button_I1.icon='fa-table'

        Button_I2=widgets.Button(description=table1[1], layout=layout_button, style=dict(button_color='#ebebeb'))
        Button_I2.on_click(self.Inputs_Edit_Ui)
        Button_I2.icon= 'fa-pencil-square-o'

        Button_I3=widgets.Button(description=table1[2], layout=layout_button, style=dict(button_color='#ebebeb'))
        Button_I3.on_click(self.Save_In_F_UI)
        Button_I3.icon = 'fa-floppy-o'

        Button_I4=widgets.Button(description=table2[0], layout=Layout(width='30%', height='40px', border='4px solid #3785d8'), style=dict(button_color='#3785d8'))
        Button_I4.on_click(self.input_to_configuration)
        Button_I4.icon='fa-angle-left'

        Button_I5=widgets.Button(description=table2[1], layout=Layout(width='30%', height='40px', border='4px solid  #ff5252'), style=dict(button_color='#ff5252'))
        Button_I5.on_click(self.input_aircraft_file)
        Button_I5.icon = 'fa-trash-o'


        Button_I6=widgets.Button(description=table2[2], layout=Layout(width='30%', height='40px', border='4px solid  #77db5c'), style=dict(button_color='#77db5c'))
        Button_I6.on_click(self.input_to_mda)
        Button_I6.icon = 'fa-angle-right'
        #---------------------------------------------------------------------------------------------------------------
        buttonHOME = widgets.Button(description='')
        buttonHOME.icon = 'fa-home'
        buttonHOME.layout.width = 'auto'
        buttonHOME.layout.height = 'auto'
        buttonHOME.on_click(self.HomeInterface)
        #---------------------------------------------------------------------------------------------------------------
        box1 = widgets.HBox(children=[title],layout=Layout(display='flex',flex_flow='column',align_items='center',width='70%'))
        box2=widgets.HBox(children=[Button_I1,Button_I2,Button_I3],layout=Layout(justify_content='space-between',width='100%'))
        box3=widgets.HBox(children=[Button_I4,Button_I5,Button_I6],layout=Layout(justify_content='space-between',width='100%'))
        box4 = widgets.Box(children=[buttonHOME], layout=Layout(border='0px solid black',
                           margin='50 0 50 0px', padding='0.5px', align_items='center', width='100'))

        #---------------------------------------------------------------------------------------------------------------
        buttonINFO = widgets.Button(description='')
        buttonINFO.icon = 'fa-info-circle'
        buttonINFO.layout.width = 'auto'
        buttonINFO.layout.height = 'auto'
        output = widgets.Output()
        def info_message(event):
            with output:
                output.clear_output()
                if len(output.outputs) > 0:
                    output.clear_output()
                else:
                    print('Welcome to the Aircraft Data Phase.\n'
                          'At this point, with the Reference Aircraft and the Configuration files, the input file is generated.\n'
                          'Feel free to visualize its data or to edit it, then save it with a different name.\n')

        buttonINFO.on_click(info_message)
        box4 = widgets.Box(children=[buttonINFO, output],layout=Layout(border='1px solid black',
                                         margin='50 0 50 0px', padding='5px', align_items='center', width='100'))
        #---------------------------------------------------------------------------------------------------------------
        box5 = widgets.Box(children=[buttonHOME,box4], layout=Layout(border='0px solid black',
                           margin='50 0 50 0px', padding='0.5px', align_items='center', width='100'))
        self.BOX_INPUT=widgets.VBox(children=[box1,box2,box3,box5],layout=Layout(border='6px solid black', padding='10px', align_items='center', width='100%'))
        display(self.BOX_INPUT)
        return self.BOX_INPUT

 # Display the Principal UI _inputs
    def menu_to_input(self,event):
        clear_output()
        input_ui=self.inputs_ui()
        self.INPUT_FILE=self.OAD.Generate_Input_File()

# AIRCRAFT INPUTS DATA PHASE TO CONFIGURATION PHASE
    def input_to_configuration (self,event):
        clear_output()
        display(self.BOX_CONFIG)

# AIRCRAFT INPUTS DATA PHASE TO RUN MDA ANALYSIS PHASE
    def input_to_mda (self,event):
        clear_output()
        self.Button_M3.style.button_color="#ebebeb"
        self.Button_M4.style.button_color="#00d600"
        image_path="Images/Wing.jpg"
        custom_css = f'''
        .vbox-with-background {{
            background-image: url("{image_path}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            width: 100%;
            height: 100%;
        }}
        '''
        display(HTML(f'<style>{custom_css}</style>'),self.menu)
        print("MDA ANALYSIS PHASE")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------------------------")


#INTERFCE FOR THE AIRCRAFT INPUT DATA

    def Inputs_Edit_Ui(self,event=None):
        clear_output()
        display(self.BOX_INPUT)
        self.INPUT=self.OAD.Input_File(self.INPUT_FILE)

        #Layout widget
        layout=widgets.Layout(width="50%", height='50px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        layout_button=widgets.Layout(width='30%', height='50px', border='4px solid black')
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')

        #TLARS UI
        try:
            self.T_value1=self.INPUT["data:TLAR:NPAX"].value[0]
            status_T_value1 = False
        except:
            status_T_value1=True
            self.T_value1 = "NaN"

        try:
            self.T_value2=self.INPUT["data:TLAR:approach_speed"].value[0]
            status_T_value2=False
        except:
            status_T_value2=True
            self.T_value2 = "NaN"
        try:
            self.T_value3 = self.INPUT["data:TLAR:cruise_mach"].value[0]
            status_T_value3 = False
        except:
            status_T_value3 = True
            self.T_value3 = "NaN"

        try:
            self.T_value4 = self.INPUT["data:TLAR:range"].value[0]
            status_T_value4 = False
        except:
            status_T_value4 = True
            self.T_value4 = "NaN"


        T_path1="Table/TLARS_name.csv"
        T_path2="Table/TLARS_unit.csv"
        T_path3="Table/TLARS_des.csv"
        T_Table1=self.csv_to_table(T_path1)
        T_Table2=self.csv_to_table(T_path2)
        T_Table3=self.csv_to_table(T_path3)
        T_Table4=[T_Table1[i]+T_Table2[i] for i in range(len(T_Table1))]
        T_title=widgets.HTML(value=" <b>Top Level Aircraft Requirements</b>")
        T_Button=widgets.Button(description="Save",layout=layout_button,style=dict(button_color="#33ffcc"))
        T_Button.on_click(self.Save_TLARS)

        self.TLAR_1=widgets.BoundedFloatText(min=100,max=400,step=1,value=self.T_value1, disabled=status_T_value1,description=T_Table4[0],description_tooltip=T_Table3[0],style=style,layout=layout)
        self.TLAR_2=widgets.BoundedFloatText(min=10,max=100,step=0.01,value=self.T_value2,disabled=status_T_value2,description=T_Table4[1],description_tooltip=T_Table3[1],style=style,layout=layout)
        self.TLAR_3=widgets.BoundedFloatText(min=0,max=1,step=0.01,value=self.T_value3,disabled=status_T_value3,description=T_Table4[2],description_tooltip=T_Table3[2],style=style,layout=layout)
        self.TLAR_4=widgets.BoundedFloatText(min=500,max=5000,step=1,value=self.T_value4,disabled=status_T_value4,description=T_Table4[3],description_tooltip=T_Table3[3],style=style,layout=layout)

        T_box_T=widgets.VBox(children=[ self.TLAR_1,self.TLAR_2,self.TLAR_3,self.TLAR_4], layout=widgets.Layout(border='3px solid black',align_items='center', padding='10px', width='100%'))
        self.T_box=widgets.VBox(children=[T_title,T_box_T,T_Button],layout=layout_box)

        ###############################GEOMETRY UI###############################

        # FUSELAGE UI
        try:
            self.C_value1 = self.INPUT["data:geometry:cabin:aisle_width"].value[0]
            status_C_value1 = False
        except:
            self.C_value1 = "NaN"
            status_C_value1 = True
        try:
            self.C_value2 = self.INPUT["data:geometry:cabin:exit_width"].value[0]
            status_C_value2 = False
        except:
            self.C_value2 = "NaN"
            status_C_value2 = True
        try:
            self.C_value3 = self.INPUT["data:geometry:cabin:containers:count_by_row"].value[0]
            status_C_value3 = False
        except:
            self.C_value3 = "NaN"
            status_C_value3 = True
        try:
            self.C_value4 = self.INPUT["data:geometry:cabin:crew_count:technical"].value[0]
            status_C_value4 = False
        except:
            self.C_value4 = "NaN"
            status_C_value4 = True
        try:
            self.C_value5 = self.INPUT["data:geometry:cabin:seats:economical:count_by_row"].value[0]
            status_C_value5 = False
        except:
            self.C_value5 = "NaN"
            status_C_value5 = True
        try:
            self.C_value6 = self.INPUT["data:geometry:cabin:seats:economical:length"].value[0]
            status_C_value6 = False
        except:
            self.C_value6 = "NaN"
            status_C_value6 = True
        try:
            self.C_value7 = self.INPUT["data:geometry:cabin:seats:economical:width"].value[0]
            status_C_value7 = False
        except:
            self.C_value7 = "NaN"
            status_C_value7 = True


        C_path1 = "Table/cab_name.csv"
        C_path2 = "Table/cab_unit.csv"
        C_path3 = "Table/cab_des.csv"
        C_Table1 = self.csv_to_table(C_path1)
        C_Table2 = self.csv_to_table(C_path2)
        C_Table3 = self.csv_to_table(C_path3)
        C_Table4 = [C_Table1[i] + C_Table2[i] for i in range(len(C_Table1))]
        C_title = widgets.HTML(value=" <b>FUSELAGE </b>")
        C_Button = widgets.Button(description="Save", layout=layout_button, style=dict(button_color="#33ffcc"))
        C_Button.on_click(self.Save_FUSELAGE)

        self.CAB_1 = widgets.BoundedFloatText(min=0, max=2, step=0.001, value=self.C_value1, disabled=status_C_value1,
                                              description=C_Table4[0], description_tooltip=C_Table3[0], style=style,
                                              layout=layout)
        self.CAB_2 = widgets.BoundedFloatText(min=0, max=2, step=0.001, value=self.C_value2, disabled=status_C_value2,
                                              description=C_Table4[1], description_tooltip=C_Table3[1], style=style,
                                              layout=layout)
        self.CAB_3 = widgets.BoundedFloatText(min=0, max=4, step=1, value=self.C_value3, disabled=status_C_value3,
                                              description=C_Table4[2], description_tooltip=C_Table3[2], style=style,
                                              layout=layout)
        self.CAB_4 = widgets.BoundedFloatText(min=1, max=4, step=1, value=self.C_value4, disabled=status_C_value4,
                                              description=C_Table4[3], description_tooltip=C_Table3[3], style=style,
                                              layout=layout)
        self.CAB_5 = widgets.BoundedFloatText(min=1, max=10, step=1, value=self.C_value5, disabled=status_C_value5,
                                              description=C_Table4[4], description_tooltip=C_Table3[4], style=style,
                                              layout=layout)
        self.CAB_6 = widgets.BoundedFloatText(min=0, max=2, step=0.001, value=self.C_value6, disabled=status_C_value6,
                                              description=C_Table4[5], description_tooltip=C_Table3[5], style=style,
                                              layout=layout)
        self.CAB_7 = widgets.BoundedFloatText(min=0, max=2, step=0.001, value=self.C_value7, disabled=status_C_value7,
                                              description=C_Table4[6], description_tooltip=C_Table3[6], style=style,
                                              layout=layout)

        C_file = open("Images/cabin.PNG", "rb")
        C_image = C_file.read()
        C_img = widgets.Image(value=C_image, format="PNG", width="45%", height="100%")
        C_box_C = widgets.VBox(
            children=[self.CAB_1, self.CAB_2, self.CAB_3, self.CAB_4, self.CAB_5, self.CAB_6, self.CAB_7],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))
        self.C_box = widgets.VBox(children=[C_title, C_box_C, C_img, C_Button], layout=layout_box)


        # WING UI
        try:
            self.W_value1 = self.INPUT["data:geometry:wing:aspect_ratio"].value[0]
            status_W_value1 = False
        except:
            self.W_value1 = "NaN"
            status_W_value1 = True
        try:
            self.W_value2 = self.INPUT["data:geometry:wing:sweep_25"].value[0]
            status_W_value2 = False
        except:
            self.W_value2 = "NaN"
            status_W_value2 = True
        try:
            self.W_value3 = self.INPUT["data:geometry:wing:virtual_taper_ratio"].value[0]
            status_W_value3 = False
        except:
            self.W_value3 = "NaN"
            status_W_value3 = True
        try:
            self.W_value4 = self.INPUT["data:geometry:wing:kink:span_ratio"].value[0]
            status_W_value4 = False
        except:
            self.W_value4 = "NaN"
            status_W_value4 = True
        try:
            self.W_value5 = self.INPUT["data:geometry:wing:spar_ratio:front:kink"].value[0]
            status_W_value5 = False
        except:
            self.W_value5 = "NaN"
            status_W_value5 = True
        try:
            self.W_value6 = self.INPUT["data:geometry:wing:spar_ratio:front:root"].value[0]
            status_W_value6 = False
        except:
            self.W_value6 = "NaN"
            status_W_value6 = True
        try:
            self.W_value7 = self.INPUT["data:geometry:wing:spar_ratio:front:tip"].value[0]
            status_W_value7 = False
        except:
            self.W_value7 = "NaN"
            status_W_value7 = True
        try:
            self.W_value8 = self.INPUT["data:geometry:wing:spar_ratio:rear:kink"].value[0]
            status_W_value8 = False
        except:
            self.W_value8 = "NaN"
            status_W_value8 = True
        try:
            self.W_value9 = self.INPUT["data:geometry:wing:spar_ratio:rear:root"].value[0]
            status_W_value9 = False
        except:
            self.W_value9 = "NaN"
            status_W_value9 = True
        try:
            self.W_value10 = self.INPUT["data:geometry:wing:spar_ratio:rear:tip"].value[0]
            status_W_value10 = False
        except:
            self.W_value10 = "NaN"
            status_W_value10 = True


        W_path1 = "Table/wing_name.csv"
        W_path2 = "Table/wing_unit.csv"
        W_path3 = "Table/wing_des.csv"
        W_Table1 = self.csv_to_table(W_path1)
        W_Table2 = self.csv_to_table(W_path2)
        W_Table3 = self.csv_to_table(W_path3)
        W_Table4 = [W_Table1[i] + W_Table2[i] for i in range(len(W_Table1))]
        W_title = widgets.HTML(value=" <b> WING GEOMETRY </b>")

        W_Button = widgets.Button(description="Save", tooltip="Save data to the aircraft inputs file",
                                  layout=layout_button, style=dict(button_color="#33ffcc"))
        W_Button.on_click(self.Save_WING)

        self.WING_1 = widgets.BoundedFloatText(min=4, max=20, step=0.01, value=self.W_value1, disabled=status_W_value1,
                                               description=W_Table4[0], description_tooltip=W_Table3[0], style=style,
                                               layout=layout)
        self.WING_2 = widgets.BoundedFloatText(min=15, max=60, step=0.001, value=self.W_value2, disabled=status_W_value2,
                                               description=W_Table4[1], description_tooltip=W_Table3[1], style=style,
                                               layout=layout)
        self.WING_3 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.W_value3, disabled=status_W_value3,
                                               description=W_Table4[2], description_tooltip=W_Table3[2], style=style,
                                               layout=layout)
        self.WING_4 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.W_value4, disabled=status_W_value4,
                                               description=W_Table4[3], description_tooltip=W_Table3[3], style=style,
                                               layout=layout)
        self.WING_5 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.W_value5, disabled=status_W_value5,
                                               description=W_Table4[4], description_tooltip=W_Table3[4], style=style,
                                               layout=layout)
        self.WING_6 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.W_value6, disabled=status_W_value6,
                                               description=W_Table4[5], description_tooltip=W_Table3[5], style=style,
                                               layout=layout)
        self.WING_7 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.W_value7, disabled=status_W_value7,
                                               description=W_Table4[6], description_tooltip=W_Table3[6], style=style,
                                               layout=layout)
        self.WING_8 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.W_value8, disabled=status_W_value8,
                                               description=W_Table4[7], description_tooltip=W_Table3[7], style=style,
                                               layout=layout)
        self.WING_9 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.W_value9, disabled=status_W_value9,
                                               description=W_Table4[8], description_tooltip=W_Table3[8], style=style,
                                               layout=layout)
        self.WING_10 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.W_value10, disabled=status_W_value10,
                                                description=W_Table4[9], description_tooltip=W_Table3[9], style=style,
                                                layout=layout)
        W_box_W = widgets.VBox(
            children=[self.WING_1, self.WING_2, self.WING_3, self.WING_4, self.WING_5, self.WING_6, self.WING_7,
                      self.WING_8, self.WING_9, self.WING_10],
            layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px', width='100%'))
        W_file = open("Images/Wing.PNG", "rb")
        W_image = W_file.read()
        W_img = widgets.Image(value=W_image, format="PNG", width="100%", height="50%")
        self.W_box = widgets.VBox(children=[W_title, W_box_W, W_img, W_Button], layout=layout_box)

        # FLAPS UI
        try:
            self.F_value1 = self.INPUT["data:geometry:flap:chord_ratio"].value[0]
            status_F_value1 = False
        except:
            self.F_value1 = "NaN"
            status_F_value1 = True
        try:
            self.F_value2 = self.INPUT["data:geometry:flap:span_ratio"].value[0]
            status_F_value2 = False
        except:
            self.F_value2 = "NaN"
            status_F_value2 = True



        F_path1 = "Table/flap_name.csv"
        F_path2 = "Table/flap_unit.csv"
        F_path3 = "Table/flap_des.csv"
        F_Table1 = self.csv_to_table(F_path1)
        F_Table2 = self.csv_to_table(F_path2)
        F_Table3 = self.csv_to_table(F_path3)
        F_Table4 = [F_Table1[i] + F_Table2[i] for i in range(len(F_Table1))]
        F_title = widgets.HTML(value=" <b> FLAPS </b>")
        F_Button = widgets.Button(description="Save", tooltip="Save data to the aircraft inputs file",
                                  layout=layout_button, style=dict(button_color="#33ffcc"))
        F_Button.on_click(self.Save_FLAPS)

        self.FLAP_1 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.F_value1, disabled=status_F_value1,
                                               description=F_Table4[0], description_tooltip=F_Table3[0], style=style,
                                               layout=layout)
        self.FLAP_2 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.F_value2, disabled=status_F_value2,
                                               description=F_Table4[1], description_tooltip=F_Table3[1], style=style,
                                               layout=layout)

        F_box_F = widgets.VBox(children=[self.FLAP_1, self.FLAP_2],
                               layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px',
                                                     width='100%'))
        F_file = open("Images/flaps.PNG", "rb")
        F_image = F_file.read()
        F_img = widgets.Image(value=F_image, format="PNG", width="70%", height="100%")
        self.F_box = widgets.VBox(children=[F_title, F_box_F, F_img, F_Button], layout=layout_box)

        # SLATS UI
        try:
            self.S_value1 = self.INPUT["data:geometry:slat:chord_ratio"].value[0]
            status_S_value1 = False
        except:
            self.S_value1 = "NaN"
            status_S_value1 = True
        try:
            self.S_value2 = self.INPUT["data:geometry:slat:span_ratio"].value[0]
            status_S_value2 = False
        except:
            self.S_value2 = "NaN"
            status_S_value2 = True



        S_path1 = "Table/slat_name.csv"
        S_path2 = "Table/slat_unit.csv"
        S_path3 = "Table/slat_des.csv"
        S_Table1 = self.csv_to_table(S_path1)
        S_Table2 = self.csv_to_table(S_path2)
        S_Table3 = self.csv_to_table(S_path3)
        S_Table4 = [S_Table1[i] + S_Table2[i] for i in range(len(S_Table1))]
        S_title = widgets.HTML(value=" <b> SLATS </b>")
        S_Button = widgets.Button(description="Save", tooltip="Save data to the aircraft inputs file",
                                  layout=layout_button, style=dict(button_color="#33ffcc"))
        S_Button.on_click(self.Save_SLATS)

        self.SLAT_1 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.S_value1, disabled=status_S_value1,
                                               description=S_Table4[0], description_tooltip=S_Table3[0], style=style,
                                               layout=layout)
        self.SLAT_2 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.S_value2, disabled=status_S_value2,
                                               description=S_Table4[1], description_tooltip=S_Table3[1], style=style,
                                               layout=layout)

        S_box_S = widgets.VBox(children=[self.SLAT_1, self.SLAT_2],
                               layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px',
                                                     width='100%'))
        S_file = open("Images/SLATS.PNG", "rb")
        S_image = S_file.read()
        S_img = widgets.Image(value=S_image, format="PNG", width="70%", height="100%")
        self.S_box = widgets.VBox(children=[S_title, S_box_S, S_img, S_Button], layout=layout_box)

        # HORIZONTAL TAIL UI
        try:
            self.H_value1 = self.INPUT["data:geometry:horizontal_tail:aspect_ratio"].value[0]
            status_H_value1 = False
        except:
            self.H_value1 = "NaN"
            status_H_value1 = True
        try:
            self.H_value2 = self.INPUT["data:geometry:horizontal_tail:sweep_25"].value[0]
            status_H_value2 = False
        except:
            self.H_value2 = "NaN"
            status_H_value2 = True
        try:
            self.H_value3 = self.INPUT["data:geometry:horizontal_tail:taper_ratio"].value[0]
            status_H_value3 = False
        except:
            self.H_value3 = "NaN"
            status_H_value3 = True
        try:
            self.H_value4 = self.INPUT["data:geometry:horizontal_tail:thickness_ratio"].value[0]
            status_H_value4 = False
        except:
            self.H_value4 = "NaN"
            status_H_value4 = True





        H_path1 = "Table/ht_name.csv"
        H_path2 = "Table/ht_unit.csv"
        H_path3 = "Table/ht_des.csv"
        H_Table1 = self.csv_to_table(H_path1)
        H_Table2 = self.csv_to_table(H_path2)
        H_Table3 = self.csv_to_table(H_path3)
        H_Table4 = [H_Table1[i] + H_Table2[i] for i in range(len(H_Table1))]
        H_title = widgets.HTML(value=" <b> HORIZONTAL TAIL </b>")
        H_Button = widgets.Button(description="Save", tooltip="Save data to the aircraft inputs file",
                                  layout=layout_button, style=dict(button_color="#33ffcc"))
        H_Button.on_click(self.Save_HT)

        self.HT_1 = widgets.BoundedFloatText(min=1, max=10, step=0.001, value=self.H_value1, disabled=status_H_value1,
                                             description=H_Table4[0], description_tooltip=H_Table3[0], style=style,
                                             layout=layout)
        self.HT_2 = widgets.BoundedFloatText(min=10, max=50, step=0.1, value=self.H_value2, disabled=status_H_value2,
                                             description=H_Table4[1], description_tooltip=H_Table3[1], style=style,
                                             layout=layout)
        self.HT_3 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.H_value3, disabled=status_H_value3,
                                             description=H_Table4[2], description_tooltip=H_Table3[2], style=style,
                                             layout=layout)
        self.HT_4 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.H_value4, disabled=status_H_value4,
                                             description=H_Table4[3], description_tooltip=H_Table3[3], style=style,
                                             layout=layout)

        H_box_H = widgets.VBox(children=[self.HT_1, self.HT_2, self.HT_3, self.HT_4],
                               layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px',
                                                     width='100%'))
        H_file = open("Images/HT.PNG", "rb")
        H_image = H_file.read()
        H_img = widgets.Image(value=H_image, format="PNG", width="70%", height="100%")
        self.H_box = widgets.VBox(children=[H_title, H_box_H, H_img, H_Button], layout=layout_box)

        # VERTICAL TAIL UI
        try:
            self.V_value1 = self.INPUT["data:geometry:vertical_tail:aspect_ratio"].value[0]
            status_V_value1 = False
        except:
            self.V_value1 = "NaN"
            status_V_value1 = True
        try:
            self.V_value2 = self.INPUT["data:geometry:vertical_tail:sweep_25"].value[0]
            status_V_value2 = False
        except:
            self.V_value2 = "NaN"
            status_V_value2 = True
        try:
            self.V_value3 = self.INPUT["data:geometry:vertical_tail:taper_ratio"].value[0]
            status_V_value3 = False
        except:
            self.V_value3 = "NaN"
            status_V_value3 = True
        try:
            self.V_value4 = self.INPUT["data:geometry:vertical_tail:thickness_ratio"].value[0]
            status_V_value4 = False
        except:
            self.V_value4 = "NaN"
            status_V_value4 = True


        V_path1 = "Table/vt_name.csv"
        V_path2 = "Table/vt_unit.csv"
        V_path3 = "Table/vt_des.csv"
        V_Table1 = self.csv_to_table(V_path1)
        V_Table2 = self.csv_to_table(V_path2)
        V_Table3 = self.csv_to_table(V_path3)
        V_Table4 = [V_Table1[i] + V_Table2[i] for i in range(len(V_Table1))]
        V_title = widgets.HTML(value=" <b> VERTICAL TAIL </b>")
        V_Button = widgets.Button(description="Save", tooltip="Save data to the aircraft inputs file",
                                  layout=layout_button, style=dict(button_color="#33ffcc"))
        V_Button.on_click(self.Save_VT)

        self.VT_1 = widgets.BoundedFloatText(min=1, max=10, step=0.001, value=self.V_value1, disabled=status_V_value1,
                                             description=V_Table4[0], description_tooltip=V_Table3[0], style=style,
                                             layout=layout)
        self.VT_2 = widgets.BoundedFloatText(min=10, max=50, step=0.1, value=self.V_value2, disabled=status_V_value2,
                                             description=V_Table4[1], description_tooltip=V_Table3[1], style=style,
                                             layout=layout)
        self.VT_3 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.V_value3, disabled=status_V_value3,
                                             description=V_Table4[2], description_tooltip=V_Table3[2], style=style,
                                             layout=layout)
        self.VT_4 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.V_value4, disabled=status_V_value4,
                                             description=V_Table4[3], description_tooltip=V_Table3[3], style=style,
                                             layout=layout)

        V_box_V = widgets.VBox(children=[self.VT_1, self.VT_2, self.VT_3, self.VT_4],
                               layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px',
                                                     width='100%'))
        V_file = open("Images/HT.PNG", "rb")
        V_image = V_file.read()
        V_img = widgets.Image(value=V_image, format="PNG", width="70%", height="100%")
        self.V_box = widgets.VBox(children=[V_title, V_box_V, V_img, V_Button], layout=layout_box)

        # PROPULSION UI
        try:
            self.P_value1 = self.INPUT["data:geometry:propulsion:layout"].value[0]
            status_P_value1 = False
        except:
            self.P_value1 = "NaN"
            status_P_value1 = True
        try:
            self.P_value2 = self.INPUT["data:geometry:propulsion:engine:count"].value[0]
            status_P_value2 = False
        except:
            self.P_value2 = "NaN"
            status_P_value2 = True
        try:
            self.P_value3 = self.INPUT["data:geometry:propulsion:engine:y_ratio"].value[0]
            status_P_value3 = False
        except:
            self.P_value3 = "NaN"
            status_P_value3 = True



        P_path1 = "Table/prop_name.csv"
        P_path2 = "Table/prop_unit.csv"
        P_path3 = "Table/prop_des.csv"
        P_Table1 = self.csv_to_table(P_path1)
        P_Table2 = self.csv_to_table(P_path2)
        P_Table3 = self.csv_to_table(P_path3)
        P_Table4 = [P_Table1[i] + P_Table2[i] for i in range(len(P_Table1))]
        P_title = widgets.HTML(value=" <b> PROPULSION GEOMETRY </b>")
        P_Button = widgets.Button(description="Save", tooltip="Save data to the aircraft inputs file",
                                  layout=layout_button, style=dict(button_color="#33ffcc"))
        P_Button.on_click(self.Save_P)

        self.PROP_1 = widgets.BoundedFloatText(min=1, max=2, step=1, value=self.P_value1, disabled=status_P_value1,
                                               description=P_Table4[0], description_tooltip=P_Table3[0], style=style,
                                               layout=layout)
        self.PROP_2 = widgets.BoundedFloatText(min=1, max=10, step=1, value=self.P_value2, disabled=status_P_value2,
                                               description=P_Table4[1], description_tooltip=P_Table3[1], style=style,
                                               layout=layout)
        self.PROP_3 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.P_value3, disabled=status_P_value3,
                                               description=P_Table4[2], description_tooltip=P_Table3[2], style=style,
                                               layout=layout)

        P_box_P = widgets.VBox(children=[self.PROP_1, self.PROP_2, self.PROP_3],
                               layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px',
                                                     width='100%'))
        P_file = open("Images/Engine.PNG", "rb")
        P_image = P_file.read()
        P_img = widgets.Image(value=P_image, format="PNG", width="100%", height="100%")
        self.P_box = widgets.VBox(children=[P_title, P_box_P, P_img, P_Button], layout=layout_box)

        # GEOMETRY MENU
        self.tab_GEO = widgets.Tab(
            children=[self.C_box, self.W_box, self.F_box, self.S_box, self.H_box, self.V_box, self.P_box])
        self.tab_GEO.set_title(0, 'FUSELAGE')
        self.tab_GEO.set_title(1, 'WING')
        self.tab_GEO.set_title(2, 'FLAPS')
        self.tab_GEO.set_title(3, 'SLATS')
        self.tab_GEO.set_title(4, 'HORIZONTAL TAIL')
        self.tab_GEO.set_title(5, 'VERTICAL TAIL')
        self.tab_GEO.set_title(6, 'PROPULSION')

        # WEIGHT UI
        try:
            self.We_value1 = self.INPUT["data:weight:aircraft:max_payload"].value[0]
            status_We_value1 = False
        except:
            self.We_value1 = "NaN"
            status_We_value1 = True
        try:
            self.We_value2 = self.INPUT["data:weight:aircraft:payload"].value[0]
            status_We_value2 = False
        except:
            self.We_value2 = "NaN"
            status_We_value2 = True



        We_path1 = "Table/We_name.csv"
        We_path2 = "Table/We_unit.csv"
        We_path3 = "Table/We_des.csv"
        We_Table1 = self.csv_to_table(We_path1)
        We_Table2 = self.csv_to_table(We_path2)
        We_Table3 = self.csv_to_table(We_path3)
        We_Table4 = [We_Table1[i] + We_Table2[i] for i in range(len(We_Table1))]
        We_title = widgets.HTML(value=" <b>WEIGHT</b>")
        We_Button = widgets.Button(description="Save", layout=layout_button, style=dict(button_color="#33ffcc"))
        We_Button.on_click(self.Save_WEIGHT)
        self.We_1 = widgets.BoundedFloatText(min=10000, max=60000, step=1, value=self.We_value1, disabled=status_We_value1,
                                             description=We_Table4[0], description_tooltip=We_Table3[0], style=style,
                                             layout=layout)
        self.We_2 = widgets.BoundedFloatText(min=10000, max=60000, step=1, value=self.We_value2, disabled=status_We_value2,
                                             description=We_Table4[1], description_tooltip=We_Table3[1], style=style,
                                             layout=layout)
        We_box_We = widgets.VBox(children=[self.We_1, self.We_2],
                                 layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px',
                                                       width='100%'))
        We_file = open("Images/WE.PNG", "rb")
        We_image = We_file.read()
        We_img = widgets.Image(value=We_image, format="PNG", width="100%", height="50%")
        self.We_box = widgets.VBox(children=[We_title, We_box_We, We_img, We_Button], layout=layout_box)

        # AERODYNAMICS UI
        try:
            self.A_value1 = self.INPUT["data:aerodynamics:aircraft:landing:CL_max_clean_2D"].value[0]
            status_A_value1 = False
        except:
            self.A_value1 = "NaN"
            status_A_value1 = True
        try:
            self.A_value2 = self.INPUT["data:aerodynamics:aircraft:takeoff:mach"].value[0]
            status_A_value2 = False
        except:
            self.A_value2 = "NaN"
            status_A_value2 = True



        A_path1 = "Table/aero_name.csv"
        A_path2 = "Table/aero_unit.csv"
        A_path3 = "Table/aero_des.csv"
        A_Table1 = self.csv_to_table(A_path1)
        A_Table2 = self.csv_to_table(A_path2)
        A_Table3 = self.csv_to_table(A_path3)
        A_Table4 = [A_Table1[i] + A_Table2[i] for i in range(len(A_Table1))]

        A_title = widgets.HTML(value=" <b> AERODYNAMICS </b>")
        A_Button = widgets.Button(description="Save", tooltip="Save data to the aircraft inputs file",
                                  layout=layout_button, style=dict(button_color="#33ffcc"))
        A_Button.on_click(self.Save_AERO)

        self.AERO_1 = widgets.BoundedFloatText(min=0.5, max=3, step=0.01, value=self.A_value1, disabled=status_A_value1,
                                               description=A_Table4[0], description_tooltip=A_Table3[0], style=style,
                                               layout=layout)
        self.AERO_2 = widgets.BoundedFloatText(min=0, max=1, step=0.001, value=self.A_value2, disabled=status_A_value2,
                                               description=A_Table4[1], description_tooltip=A_Table3[1], style=style,
                                               layout=layout)

        A_box_A = widgets.VBox(children=[self.AERO_1, self.AERO_2],
                               layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px',
                                                     width='100%'))
        A_file = open("Images/aero.PNG", "rb")
        A_image = A_file.read()
        A_img = widgets.Image(value=A_image, format="PNG", width="100%", height="50%")
        self.A_box = widgets.VBox(children=[A_title, A_box_A, A_img, A_Button], layout=layout_box)

        # LOADS UI
        try:
            self.L_value1 = self.INPUT["data:load_case:lc1:U_gust"].value[0]
            status_L_value1 = False
        except:
            self.L_value1 = "NaN"
            status_L_value1 = True
        try:
            self.L_value2 = self.INPUT["data:load_case:lc1:Vc_EAS"].value[0]
            status_L_value2 = False
        except:
            self.L_value2 = "NaN"
            status_L_value2 = True
        try:
            self.L_value3 = self.INPUT["data:load_case:lc1:altitude"].value[0]
            status_L_value3 = False
        except:
            self.L_value3 = "NaN"
            status_L_value3 = True
        try:
            self.L_value4 = self.INPUT["data:load_case:lc2:U_gust"].value[0]
            status_L_value4 = False
        except:
            self.L_value4 = "NaN"
            status_L_value4 = True
        try:
            self.L_value5 = self.INPUT["data:load_case:lc2:Vc_EAS"].value[0]
            status_L_value5 = False
        except:
            self.L_value5 = "NaN"
            status_L_value5 = True
        try:
            self.L_value6 = self.INPUT["data:load_case:lc2:altitude"].value[0]
            status_L_value6 = False
        except:
            self.L_value6 = "NaN"
            status_L_value6 = True





        L_path1 = "Table/load_name.csv"
        L_path2 = "Table/load_unit.csv"
        L_path3 = "Table/load_des.csv"
        L_Table1 = self.csv_to_table(L_path1)
        L_Table2 = self.csv_to_table(L_path2)
        L_Table3 = self.csv_to_table(L_path3)
        L_Table4 = [L_Table1[i] + L_Table2[i] for i in range(len(L_Table1))]

        L_title = widgets.HTML(value=" <b> LOADS CASE </b>")
        L_Button = widgets.Button(description="Save", tooltip="Save data to the aircraft inputs file",
                                  layout=layout_button, style=dict(button_color="#33ffcc"))
        L_Button.on_click(self.Save_LOAD)

        self.LOAD_1 = widgets.BoundedFloatText(min=5, max=50, step=0.01, value=self.L_value1, disabled=status_L_value1,
                                               description=L_Table4[0], description_tooltip=L_Table3[0], style=style,
                                               layout=layout)
        self.LOAD_2 = widgets.BoundedFloatText(min=100, max=1000, step=0.1, value=self.L_value2, disabled=status_L_value2,
                                               description=L_Table4[1], description_tooltip=L_Table3[1], style=style,
                                               layout=layout)
        self.LOAD_3 = widgets.BoundedFloatText(min=1000, max=100000, step=1, value=self.L_value3, disabled=status_L_value3,
                                               description=L_Table4[2], description_tooltip=L_Table3[2], style=style,
                                               layout=layout)
        self.LOAD_4 = widgets.BoundedFloatText(min=5, max=50, step=0.01, value=self.L_value4, disabled=status_L_value4,
                                               description=L_Table4[3], description_tooltip=L_Table3[3], style=style,
                                               layout=layout)
        self.LOAD_5 = widgets.BoundedFloatText(min=100, max=1000, step=0.001, value=self.L_value5, disabled=status_L_value5,
                                               description=L_Table4[4], description_tooltip=L_Table3[4], style=style,
                                               layout=layout)
        self.LOAD_6 = widgets.BoundedFloatText(min=1000, max=100000, step=1, value=self.L_value6, disabled=status_L_value6,
                                               description=L_Table4[5], description_tooltip=L_Table3[5], style=style,
                                               layout=layout)

        L_box_L = widgets.VBox(children=[self.LOAD_1, self.LOAD_2, self.LOAD_3, self.LOAD_4, self.LOAD_5, self.LOAD_6],
                               layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px',
                                                     width='100%'))
        L_file = open("Images/load.PNG", "rb")
        L_image = L_file.read()
        L_img = widgets.Image(value=L_image, format="PNG", width="100%", height="50%")
        self.L_box = widgets.VBox(children=[L_title, L_box_L, L_img, L_Button], layout=layout_box)

        # MISSION UI

        # MTOW MISSION
        try:
            self.MTOW_value1 = self.INPUT["data:mission:MTOW_mission:diversion:distance"].value[0]
            status_MTOW_value1 = False
        except:
            self.MTOW_value1 = "NaN"
            status_MTOW_value1 = True
        try:
            self.MTOW_value2 = self.INPUT["data:mission:MTOW_mission:holding:duration"].value[0]
            status_MTOW_value2 = False
        except:
            self.MTOW_value2= "NaN"
            status_MTOW_value2 = True
        try:
            self.MTOW_value3 = self.INPUT["data:mission:MTOW_mission:main_route:range"].value[0]
            status_MTOW_value3 = False
        except:
            self.MTOW_value3 = "NaN"
            status_MTOW_value3 = True
        try:
            self.MTOW_value4 = self.INPUT["data:mission:MTOW_mission:takeoff:V2"].value[0]
            status_MTOW_value4 = False
        except:
            self.MTOW_value4 = "NaN"
            status_MTOW_value4 = True
        try:
            self.MTOW_value5 = self.INPUT["data:mission:MTOW_mission:takeoff:fuel"].value[0]
            status_MTOW_value5 = False
        except:
            self.MTOW_value5 = "NaN"
            status_MTOW_value5 = True


        MTOW_path1 = "Table/MTOW_name.csv"
        MTOW_path2 = "Table/MTOW_unit.csv"
        MTOW_path3 = "Table/MTOW_des.csv"
        MTOW_Table1 = self.csv_to_table(MTOW_path1)
        MTOW_Table2 = self.csv_to_table(MTOW_path2)
        MTOW_Table3 = self.csv_to_table(MTOW_path3)
        MTOW_Table4 = [MTOW_Table1[i] + MTOW_Table2[i] for i in range(len(MTOW_Table1))]
        MTOW_title = widgets.HTML(value=" <b>MTOW MISSION </b>")
        MTOW_Button = widgets.Button(description="Save", layout=layout_button, style=dict(button_color="#33ffcc"))
        MTOW_Button.on_click(self.Save_MTOW)

        self.MTOW_1 = widgets.BoundedFloatText(min=50, max=500, step=1, value=self.MTOW_value1, disabled=status_MTOW_value1,
                                               description=MTOW_Table4[0], description_tooltip=MTOW_Table3[0],
                                               style=style, layout=layout)
        self.MTOW_2 = widgets.BoundedFloatText(min=10, max=100, step=1, value=self.MTOW_value2, disabled=status_MTOW_value2,
                                               description=MTOW_Table4[1], description_tooltip=MTOW_Table3[1],
                                               style=style, layout=layout)
        self.MTOW_3 = widgets.BoundedFloatText(min=1000, max=10000, step=1, value=self.MTOW_value3, disabled=status_MTOW_value3,
                                               description=MTOW_Table4[2], description_tooltip=MTOW_Table3[2],
                                               style=style, layout=layout)
        self.MTOW_4 = widgets.BoundedFloatText(min=10, max=200, step=0.1, value=self.MTOW_value4, disabled=status_MTOW_value4,
                                               description=MTOW_Table4[3], description_tooltip=MTOW_Table3[3],
                                               style=style, layout=layout)
        self.MTOW_5 = widgets.BoundedFloatText(min=10, max=200, step=0.1, value=self.MTOW_value5, disabled=status_MTOW_value5,
                                               description=MTOW_Table4[4], description_tooltip=MTOW_Table3[4],
                                               style=style, layout=layout)

        MTOW_box_MTOW = widgets.VBox(children=[self.MTOW_1, self.MTOW_2, self.MTOW_3, self.MTOW_4, self.MTOW_5],
                                     layout=widgets.Layout(border='3px solid black', align_items='center',
                                                           padding='10px', width='100%'))
        MTOW_file = open("Images/Mission.PNG", "rb")
        MTOW_image = MTOW_file.read()
        MTOW_img = widgets.Image(value=MTOW_image, format="PNG", width="100%", height="50%")
        self.MTOW_box = widgets.VBox(children=[MTOW_title, MTOW_box_MTOW, MTOW_img, MTOW_Button], layout=layout_box)

        # SIZING MISSION
        try:
            self.Size_value1 = self.INPUT["data:mission:sizing:landing:flap_angle"].value[0]
            status_Size_value1 = False
        except:
            self.Size_value1 = "NaN"
            status_Size_value1 = True
        try:
            self.Size_value2 = self.INPUT["data:mission:sizing:landing:slat_angle"].value[0]
            status_Size_value2 = False
        except:
            self.Size_value2= "NaN"
            status_Size_value2 = True
        try:
            self.Size_value3 = self.INPUT["data:mission:sizing:takeoff:flap_angle"].value[0]
            status_Size_value3 = False
        except:
            self.Size_value3 = "NaN"
            status_Size_value3 = True
        try:
            self.Size_value4 = self.INPUT["data:mission:sizing:takeoff:slat_angle"].value[0]
            status_Size_value4 = False
        except:
            self.Size_value4 = "NaN"
            status_Size_value4 = True
        try:
            self.Size_value5 = self.INPUT["data:mission:sizing:main_route:cruise:altitude"].value[0]
            status_Size_value5 = False
        except:
            self.Size_value5 = "NaN"
            status_Size_value5 = True


        Size_path1 = "Table/Size_name.csv"
        Size_path2 = "Table/Size_unit.csv"
        Size_path3 = "Table/Size_des.csv"
        Size_Table1 = self.csv_to_table(Size_path1)
        Size_Table2 = self.csv_to_table(Size_path2)
        Size_Table3 = self.csv_to_table(Size_path3)
        Size_Table4 = [Size_Table1[i] + Size_Table2[i] for i in range(len(Size_Table1))]
        Size_title = widgets.HTML(value=" <b>SIZING MISSION </b>")
        Size_Button = widgets.Button(description="Save", layout=layout_button, style=dict(button_color="#33ffcc"))
        Size_Button.on_click(self.Save_SIZE)
        self.Size_1 = widgets.BoundedFloatText(min=10, max=60, step=0.1, value=self.Size_value1, disabled=status_Size_value1,
                                               description=Size_Table4[0], description_tooltip=Size_Table3[0],
                                               style=style, layout=layout)
        self.Size_2 = widgets.BoundedFloatText(min=10, max=60, step=0.1, value=self.Size_value2, disabled=status_Size_value2,
                                               description=Size_Table4[1], description_tooltip=Size_Table3[1],
                                               style=style, layout=layout)
        self.Size_3 = widgets.BoundedFloatText(min=10, max=60, step=0.1, value=self.Size_value3, disabled=status_Size_value3,
                                               description=Size_Table4[2], description_tooltip=Size_Table3[2],
                                               style=style, layout=layout)
        self.Size_4 = widgets.BoundedFloatText(min=10, max=60, step=0.1, value=self.Size_value4, disabled=status_Size_value4,
                                               description=Size_Table4[3], description_tooltip=Size_Table3[3],
                                               style=style, layout=layout)
        self.Size_5 = widgets.BoundedFloatText(min=10000, max=60000, step=100, value=self.Size_value5, disabled=status_Size_value5,
                                               description=Size_Table4[4], description_tooltip=Size_Table3[4],
                                               style=style, layout=layout)
        Size_box_Size = widgets.VBox(children=[self.Size_1, self.Size_2, self.Size_3, self.Size_4, self.Size_5],
                                     layout=widgets.Layout(border='3px solid black', align_items='center',
                                                           padding='10px', width='100%'))
        Size_file = open("Images/Mission.PNG", "rb")
        Size_image = Size_file.read()
        Size_img = widgets.Image(value=Size_image, format="PNG", width="100%", height="50%")
        self.Size_box = widgets.VBox(children=[Size_title, Size_box_Size, Size_img, Size_Button], layout=layout_box)

        # MISSION MENU
        self.tab_MISS = widgets.Tab(children=[self.MTOW_box, self.Size_box])
        self.tab_MISS.set_title(0, 'MTOW MISSION')
        self.tab_MISS.set_title(1, 'SIZING MISSION')

        # PROPULSION UI
        try:
            self.PR_value1 = self.INPUT["data:propulsion:MTO_thrust"].value[0]
            status_PR_value1 = False
        except:
            self.PR_value1 = "NaN"
            status_PR_value1 = True
        try:
            self.PR_value2 = self.INPUT["data:propulsion:rubber_engine:bypass_ratio"].value[0]
            status_PR_value2 = False
        except:
            self.PR_value2 = "NaN"
            status_PR_value2 = True
        try:
            self.PR_value3 = self.INPUT["data:propulsion:rubber_engine:design_altitude"].value[0]
            status_PR_value3 = False
        except:
            self.PR_value3 = "NaN"
            status_PR_value3 = True
        try:
            self.PR_value4 = self.INPUT["data:propulsion:rubber_engine:maximum_mach"].value[0]
            status_PR_value4 = False
        except:
            self.PR_value4 = "NaN"
            status_PR_value4 = True
        try:
            self.PR_value5 = self.INPUT["data:propulsion:rubber_engine:overall_pressure_ratio"].value[0]
            status_PR_value5 = False
        except:
            self.PR_value5 = "NaN"
            status_PR_value5 = True
        try:
            self.PR_value6 = self.INPUT["data:propulsion:rubber_engine:turbine_inlet_temperature"].value[0]
            status_PR_value6 = False
        except:
            self.PR_value6 = "NaN"
            status_PR_value6 = True


        PR_path1 = "Table/pro_name.csv"
        PR_path2 = "Table/pro_unit.csv"
        PR_path3 = "Table/pro_des.csv"
        PR_Table1 = self.csv_to_table(PR_path1)
        PR_Table2 = self.csv_to_table(PR_path2)
        PR_Table3 = self.csv_to_table(PR_path3)
        PR_Table4 = [PR_Table1[i] + PR_Table2[i] for i in range(len(PR_Table1))]
        PR_title = widgets.HTML(value=" <b>PROPULSION  </b>")
        PR_Button = widgets.Button(description="Save", tooltip="Save data to the aircraft inputs file",
                                   layout=layout_button, style=dict(button_color="#33ffcc"))
        PR_Button.on_click(self.Save_PR)

        self.PR_1 = widgets.BoundedFloatText(min=5000, max=500000, step=1, value=self.PR_value1, disabled=status_PR_value1,
                                             description=PR_Table4[0], description_tooltip=PR_Table3[0], style=style,
                                             layout=layout)
        self.PR_2 = widgets.BoundedFloatText(min=1, max=20, step=1, value=self.PR_value2, disabled=status_PR_value2,
                                             description=PR_Table4[1], description_tooltip=PR_Table3[1], style=style,
                                             layout=layout)
        self.PR_3 = widgets.BoundedFloatText(min=1000, max=20000, step=0.1, value=self.PR_value3, disabled=status_PR_value3,
                                             description=PR_Table4[2], description_tooltip=PR_Table3[2], style=style,
                                             layout=layout)
        self.PR_4 = widgets.BoundedFloatText(min=0, max=1, step=0.1, value=self.PR_value4, disabled=status_PR_value4,
                                             description=PR_Table4[3], description_tooltip=PR_Table3[3], style=style,
                                             layout=layout)
        self.PR_5 = widgets.BoundedFloatText(min=1, max=100, step=0.1, value=self.PR_value5, disabled=status_PR_value5,
                                             description=PR_Table4[4], description_tooltip=PR_Table3[4], style=style,
                                             layout=layout)
        self.PR_6 = widgets.BoundedFloatText(min=500, max=3000, step=1, value=self.PR_value6, disabled=status_PR_value6,
                                             description=PR_Table4[5], description_tooltip=PR_Table3[5], style=style,
                                             layout=layout)
        PR_box_PR = widgets.VBox(children=[self.PR_1, self.PR_2, self.PR_3, self.PR_4, self.PR_5, self.PR_6],
                                 layout=widgets.Layout(border='3px solid black', align_items='center', padding='10px',
                                                       width='100%'))
        PR_file = open("Images/Engine.PNG", "rb")
        PR_image = PR_file.read()
        PR_img = widgets.Image(value=PR_image, format="PNG", width="100%", height="50%")
        self.PR_box = widgets.VBox(children=[PR_title, PR_box_PR, PR_img, PR_Button], layout=layout_box)

        # GENERAL INPUTS MENU
        self.tab_IN = widgets.Tab(
            children=[self.T_box, self.tab_GEO, self.We_box, self.A_box, self.L_box, self.tab_MISS, self.PR_box])
        self.tab_IN.set_title(0, 'TLARS')
        self.tab_IN.set_title(1, 'GEOMETRY')
        self.tab_IN.set_title(2, 'WEIGHT')
        self.tab_IN.set_title(3, 'AERODYNAMICS')
        self.tab_IN.set_title(4, 'LOADS')
        self.tab_IN.set_title(5, 'MISSION')
        self.tab_IN.set_title(6, 'PROPULSION')
        display(self.tab_IN)
        return self.tab_IN

#SAVE TLARS DATA
    def Save_TLARS(self,event):
        try:
            self.INPUT["data:TLAR:NPAX"].value = self.TLAR_1.value
        except:
            pass
        try:
            self.INPUT["data:TLAR:approach_speed"].value=self.TLAR_2.value
        except:
            pass
        try:
            self.INPUT["data:TLAR:cruise_mach"].value=self.TLAR_3.value
        except:
            pass
        try:
            self.INPUT["data:TLAR:range"].value=self.TLAR_4.value
        except:
            pass
        self.INPUT.save()

#SAVE GEOMETRY DATA

#SAVE THE FUSELAGE DATA
    def Save_FUSELAGE(self,event):
        try:
            self.INPUT["data:geometry:cabin:aisle_width"].value = self.CAB_1.value
        except:
            pass
        try:
            self.INPUT["data:geometry:cabin:exit_width"].value = self.CAB_2.value
        except:
            pass
        try:
            self.INPUT["data:geometry:cabin:containers:count_by_row"].value = self.CAB_3.value
        except:
            pass
        try:
            self.INPUT["data:geometry:cabin:crew_count:technical"].value = self.CAB_4.value
        except:
            pass
        try:
            self.INPUT["data:geometry:cabin:seats:economical:count_by_row"].value = self.CAB_5.value
        except:
            pass
        try:
            self.INPUT["data:geometry:cabin:seats:economical:length"].value = self.CAB_6.value
        except:
            pass
        try:
            self.INPUT["data:geometry:cabin:seats:economical:width"].value = self.CAB_7.value
        except:
            pass
        self.INPUT.save()



#SAVE WING DATA

    def Save_WING(self,event):
        try:
            self.INPUT["data:geometry:wing:aspect_ratio"].value=self.WING_1.value
        except:
            pass
        try:
            self.INPUT["data:geometry:wing:sweep_25"].value=self.WING_2.value
        except:
            pass
        try:
            self.INPUT["data:geometry:wing:virtual_taper_ratio"].value=1.5*self.WING_3.value
        except:
            pass
        try:
            self.INPUT["data:geometry:wing:kink:span_ratio"].value=self.WING_4.value
        except:
            pass
        try:
            self.INPUT["data:geometry:wing:spar_ratio:front:kink"].value=self.WING_5.value
        except:
            pass
        try:
            self.INPUT["data:geometry:wing:spar_ratio:front:root"].value=self.WING_6.value
        except:
            pass
        try:
            self.INPUT["data:geometry:wing:spar_ratio:front:tip"].value=self.WING_7.value
        except:
            pass
        try:
            self.INPUT["data:geometry:wing:spar_ratio:rear:kink"].value=self.WING_8.value
        except:
            pass
        try:
            self.INPUT["data:geometry:wing:spar_ratio:rear:root"].value=self.WING_9.value
        except:
            pass
        try:
            self.INPUT["data:geometry:wing:spar_ratio:rear:tip"].value=self.WING_10.value
        except:
            pass

        self.INPUT.save()


#SAVE FLAPS DATA
    def Save_FLAPS(self,event):
        try:
            self.INPUT["data:geometry:flap:chord_ratio"].value=self.FLAP_1.value
        except:
            pass
        try:
            self.INPUT["data:geometry:flap:span_ratio"].valuevalue=self.FLAP_2.value
        except:
            pass


        self.INPUT.save()

#SAVE SLATS DATA
    def Save_SLATS(self,event):
        try:
            self.INPUT["data:geometry:slat:chord_ratio"].value=self.SLAT_1.value
        except:
            pass
        try:
            self.INPUT["data:geometry:slat:span_ratio"].valuevalue=self.SLAT_2.value
        except:
            pass

        self.INPUT.save()

#SAVE HORIZONTAL TAIL  DATA
    def Save_HT(self,event):
        try:
            self.INPUT["data:geometry:horizontal_tail:aspect_ratio"].value= self.HT_1.value
        except:
            pass
        try:
            self.INPUT["data:geometry:horizontal_tail:sweep_25"].value=self.HT_2.value
        except:
            pass
        try:
            self.INPUT["data:geometry:horizontal_tail:taper_ratio"].value=self.HT_3.value
        except:
            pass
        try:
            self.INPUT["data:geometry:horizontal_tail:thickness_ratio"].value= self.HT_4.value
        except:
            pass

        self.INPUT.save()



#SAVE VERITICAL TAIL  DATA
    def Save_VT(self,event):
        try:
            self.INPUT["data:geometry:vertical_tail:aspect_ratio"].value= self.VT_1.value
        except:
            pass
        try:
            self.INPUT["data:geometry:vertical_tail:sweep_25"].value=self.VT_2.value
        except:
            pass
        try:
            self.INPUT["data:geometry:vertical_tail:taper_ratio"].value=self.VT_3.value
        except:
            pass
        try:
            self.INPUT["data:geometry:vertical_tail:thickness_ratio"].value= self.VT_4.value
        except:
            pass

        self.INPUT.save()


#SAVE PROPULSION GEOMETRY DATA
    def Save_P(self,event):
        try:
            self.INPUT["data:geometry:propulsion:layout"].value= self.PROP_1.value
        except:
            pass
        try:
            self.INPUT["data:geometry:propulsion:engine:count"].value= self.PROP_2.value
        except:
            pass
        try:
            self.INPUT["data:geometry:propulsion:engine:y_ratio"].value= self.PROP_3.value
        except:
            pass

        self.INPUT.save()

#SAVE WEIGHT DATA
    def Save_WEIGHT(self,event):
        try:
            self.INPUT["data:weight:aircraft:max_payload"].value=self.We_1.value
        except:
            pass
        try:
            self.INPUT["data:weight:aircraft:payload"].value=self.We_2.value
        except:
            pass

        self.INPUT.save()


#SAVE AERODYNAMICS DATA
    def Save_AERO(self,event):
        try:
            self.INPUT["data:aerodynamics:aircraft:landing:CL_max_clean_2D"].value=self.AERO_1.value
        except:
            pass
        try:
            self.INPUT["data:aerodynamics:aircraft:takeoff:mach"].value=self.AERO_2.value
        except:
            pass

        self.INPUT.save()

#SAVE LOADS DATA
    def Save_LOAD(self,event):
        try:
            self.INPUT["data:load_case:lc1:U_gust"].value=self.LOAD_1.value
        except:
            pass
        try:
            self.INPUT["data:load_case:lc1:Vc_EAS"].value=self.LOAD_2.value
        except:
            pass
        try:
            self.INPUT["data:load_case:lc1:altitude"].value=self.LOAD_3.value
        except:
            pass
        try:
            self.INPUT["data:load_case:lc2:U_gust"].value=self.LOAD_4.value
        except:
            pass
        try:
            self.INPUT["data:load_case:lc2:Vc_EAS"].value=self.LOAD_5.value
        except:
            pass
        try:
            self.INPUT["data:load_case:lc2:altitude"].value=self.LOAD_6.value
        except:
            pass

        self.INPUT.save()

#SAVE MISSION DATA

#SAVE THE MTOW MISSION DATA
    def Save_MTOW(self,event):
        try:
            self.INPUT["data:mission:MTOW_mission:diversion:distance"].value=self.MTOW_1.value
        except:
            pass
        try:
            self.INPUT["data:mission:MTOW_mission:holding:duration"].value=self.MTOW_2.value
        except:
            pass
        try:
            self.INPUT["data:mission:MTOW_mission:main_route:range"].value=self.MTOW_3.value
        except:
            pass
        try:
            self.INPUT["data:mission:MTOW_mission:takeoff:V2"].value=self.MTOW_4.value
        except:
            pass
        try:
            self.INPUT["data:mission:MTOW_mission:takeoff:fuel"].value=self.MTOW_5.value
        except:
            pass

        self.INPUT.save()


#SAVE THE SIZING MISSION

    def Save_SIZE(self,event):
        try:
            self.INPUT["data:mission:sizing:landing:flap_angle"].value=self.Size_1.value
        except:
            pass
        try:
            self.INPUT["data:mission:sizing:landing:slat_angle"].value=self.Size_2.value
        except:
            pass
        try:
            self.INPUT["data:mission:sizing:takeoff:flap_angle"].value=self.Size_3.value
        except:
            pass
        try:
            self.INPUT["data:mission:sizing:takeoff:slat_angle"].value=self.Size_4.value
        except:
            pass
        try:
            self.INPUT["data:mission:sizing:main_route:cruise:altitude"].value=self.Size_5.value
        except:
            pass

        self.INPUT.save()




#SAVE THE ENGINE DATA
    def Save_PR(self,event):
        try:
            self.INPUT["data:propulsion:MTO_thrust"].value=self.PR_1.value
        except:
            pass
        try:
            self.INPUT["data:propulsion:rubber_engine:bypass_ratio"].value=self.PR_2.value
        except:
            pass
        try:
            self.INPUT["data:propulsion:rubber_engine:design_altitude"].value=self.PR_3.value
        except:
            pass
        try:
            self.INPUT["data:propulsion:rubber_engine:maximum_mach"].value=self.PR_4.value
        except:
            pass
        try:
            self.INPUT["data:propulsion:rubber_engine:overall_pressure_ratio"].value=self.PR_5.value
        except:
            pass
        try:
            self.INPUT["data:propulsion:rubber_engine:turbine_inlet_temperature"].value=self.PR_6.value
        except:
            pass

        self.INPUT["tuning:propulsion:rubber_engine:SFC:k_cr"].value = 1.0
        self.INPUT.save()


# SAVE THE INPUT FILE IN A FOLDER WITH ANOTHER NAME
    def Save_In_F_UI(self,event):

        clear_output()
        display(self.BOX_INPUT)
        layout=widgets.Layout(width="50%", height='40px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        layout_button=widgets.Layout(width='30%', height='50px', border='4px solid black')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')
        self.IN_NAME=widgets.Text(placeholder='Type the file name',description='INPUT FILE NAME:',value="",style=style,layout=layout,disabled=False)
        SI_Title=widgets.HTML(value=" <b> SAVING INPUT FILE </b>")
        SI_Button=widgets.Button(description="SAVE",tooltip="Save the  input file",layout=layout_button,style=dict(button_color="#33ffcc"))
        SI_Button.on_click(self.Save_INPUT_FILE)

        SI_box_SI=widgets.VBox(children=[self.IN_NAME], layout=widgets.Layout(border='3px solid black',align_items='center', padding='10px', width='100%'))
        self.SI_box=widgets.VBox(children=[SI_Title,self.IN_NAME,SI_Button],layout=layout_box)
        display(self.SI_box)


    def Save_INPUT_FILE(self,event):
        self.in_name=self.IN_NAME.value
        self.path_in="INPUT_FILE"
        self.OAD.Save_File(self.INPUT_FILE,self.path_in,self.in_name)
        print(str(self.IN_NAME.value)+" input file saved")
        print("-------------------------------------------")


# Delete INPUT FILE

    def input_aircraft_file(self,event):
        clear_output()
        display(self.BOX_INPUT)
        self.path_to_target="INPUT_FILE"
        self.path_to_file_list = []
        temp=os.listdir(self.path_to_target)
        for i in range(0, len(temp)):
            if temp[i][-3:] =='xml':
                self.path_to_file_list.append(temp[i])
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        title=widgets.HTML(value=" <b>Choose the input file data to delete</b>")
        box1 = widgets.HBox(children=[title],layout=layout_title)
        self.input_file_name = widgets.Dropdown(options=self.path_to_file_list,description='Choose your file:',disabled=False,style={'description_width': 'initial'})
        self.input_file_name.observe(self.delete_input_file,names="value")
        box2=widgets.HBox(children=[self.input_file_name])

        self.DI_BOX=widgets.VBox(children=[box1,box2],layout=Layout(border='6px solid black', padding='10px', align_items='center', width='100%'))
        display(self.DI_BOX)
        return self.input_file_name

    def delete_input_file(self,change):
        path_del_in="INPUT_FILE/" +str(change.new)
        self.OAD.Delete_File(path_del_in)

        print("You have deleted the"+" "+str(change.new)+ " "+ "file")
        print("------------------------------------------------")






# MDA INTERFACE PHASE

# Principal interface
    def MDA_UI(self,event):
        clear_output()

        table1=["RUN MDA","MISSION ANALYSIS","PARAMETRIC BRANCH/ID"]
        table2=["MDA OUTPUTS ", "SAVE AIRCRAFT DATA", "DELETE AIRCRAFT DATA"]
        table3=["BACK","NEXT"]

        layout_button1=widgets.Layout(width='30%', height='60px', border='4px solid black')
        layout_button2=widgets.Layout(width='30%', height='40px', border='4px solid black')
        layout_box1=widgets.Layout(justify_content='space-between',width='100%')
        layout_box2=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')

        title=widgets.HTML(value=" <b>MDA ANALYSIS </b>")

        Button_MD11=widgets.Button(description=table1[0],tooltip="Run the MDA Design Problem", layout=layout_button1, style=dict(button_color='#ebebeb'))
        Button_MD11.on_click(self.RUN_MDA)

        self.Button_MD12=widgets.Button(description=table1[1], layout=layout_button1,disabled=True, style=dict(button_color='#ebebeb'))
        self.Button_MD12.on_click(self. Mission_Analysis_UI)


        Button_MD13=widgets.Button(description=table1[2], layout=layout_button1, style=dict(button_color='#ebebeb'))
        Button_MD13.on_click(self. PARAMETRIC_UI1)

        box1=widgets.HBox(children=[Button_MD11,self.Button_MD12,Button_MD13],layout=layout_box1)

        self.Button_MD21=widgets.Button(description=table2[0],tooltip="view the outputs of the mda design problem",disabled=True, layout=layout_button2, style=dict(button_color='#ffccb3'))
        self.Button_MD21.on_click(self.View_Ouput_Data)
        self.Button_MD21.icon = 'fa-table'

        self.Button_MD22=widgets.Button(description=table2[1], layout=layout_button2,disabled=True, style=dict(button_color='#00ffbf'))
        self.Button_MD22.on_click(self.Save_OUT_F_UI)
        self.Button_MD22.icon= 'fa-floppy-o'

        Button_MD23=widgets.Button(description=table2[2], layout=layout_button2, style=dict(button_color='#ff5252'))
        Button_MD23.on_click(self.Output_aircraft_file)
        Button_MD23.icon= 'fa-trash-o'

        box2=widgets.HBox(children=[self.Button_MD21,self.Button_MD22,Button_MD23],layout=layout_box1)

        self.Button_MD31=widgets.Button(description=table3[0], layout=layout_button2,disabled=True, style=dict(button_color='#3785d8'))
        self.Button_MD31.on_click(self.mda_to_input)
        self.Button_MD31.icon = 'fa-angle-left'

        Button_MD32=widgets.Button(description=table3[1], layout=layout_button2, style=dict(button_color='#77db5c'))
        Button_MD32.on_click(self.mda_to_analysis)
        Button_MD32.icon = 'fa-angle-right'

        buttonHOME = widgets.Button(description='')
        buttonHOME.icon = 'fa-home'
        buttonHOME.layout.width = 'auto'
        buttonHOME.layout.height = 'auto'
        buttonHOME.on_click(self.HomeInterface)

        box3=widgets.HBox(children=[self.Button_MD31,buttonHOME,Button_MD32],layout=layout_box1)

        #---------------------------------------------------------------------------------------------------------------
        buttonINFO = widgets.Button(description='')
        buttonINFO.icon = 'fa-info-circle'
        buttonINFO.layout.width = 'auto'
        buttonINFO.layout.height = 'auto'
        output = widgets.Output()
        def info_message(event):
            with output:
                output.clear_output()
                if len(output.outputs) > 0:
                    output.clear_output()
                else:
                    print('Welcome to the MDA Phase.\n'
                          'If the -Performance- module was not selected, then the Mission Analysis is to be disabled\n'
                          'The rest of the button shall be activated one the RUN MDA is clicked.\n'
                          'From this screen, the user can go to the Parametric Branch\n')

        buttonINFO.on_click(info_message)
        box4 = widgets.Box(children=[buttonINFO, output],layout=Layout(border='1px solid black',
                                         margin='50 0 50 0px', padding='5px', align_items='center', width='100'))
        #---------------------------------------------------------------------------------------------------------------
        self.BOX_MDA=widgets.VBox(children=[title,box1,box2,box3,box4],layout=layout_box2)
        display(self.BOX_MDA)
        return self.BOX_MDA




# RUN THE MDA ANALYSIS
    def RUN_MDA(self,event):

        # These are the buttons from phase 4 GUI (MDA), when this function is called,it means the analysis is being run.
        # If the modules list contain the module PERFORMANCE then the MISSION ANALYSIS  button is enabled, if not, it remains disabled.
        #Also the button MDA OUTPUTS is only enabled afte the analysis is run, otherwise there is no file to show.
        #Also the button SAVE AIRCRAFT DATA is only enabled after the analysis is run, otherwise there is no file to log
        if "performance" in self.module.value:
            self.Button_MD12.disabled = False

        self.Button_MD21.disabled = False
        self.Button_MD22.disabled = False
        self.Button_MD31.disabled = False

        self.MDA_problem=self.OAD.RUN_OAD() # This runs the MDA problem
        return self.MDA_problem


# VIEW THE OUTPUTS OF THE MDA PROBLEM

    def View_Ouput_Data(self,event):
        clear_output()
        display(self.BOX_MDA)
        path="workdir"
        file=self.MDA_problem.output_file_path
        self.OUTPUT_FILE=self.OAD.Join_File(path,file)
        self.output_data=self.OAD.View_outputs_data(self.OUTPUT_FILE)
        return self.output_data

# SAVE THE OUTPUTS OF THE AIRCRAFT AND THE MISSION FILE
    def Save_OUT_F_UI(self,event):
        clear_output()
        display(self.BOX_MDA)
        layout=widgets.Layout(width="50%", height='40px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        layout_button=widgets.Layout(width='30%', height='50px', border='4px solid black')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')
        self.OUT_NAME=widgets.Text(placeholder='Type the files name',description='OUTPUTS FILE NAME:',value="",style=style,layout=layout,disabled=False)
        SO_Title=widgets.HTML(value=" <b> SAVING OUTPUT FILE </b>")
        SO_Button=widgets.Button(description="SAVE",tooltip="SAVE THE OUTPUTS",layout=layout_button,style=dict(button_color="#33ffcc"))
        SO_Button.on_click(self.Save_OUTPUT_FILE)
        SO_box_SI=widgets.VBox(children=[self.OUT_NAME], layout=widgets.Layout(border='3px solid black',align_items='center', padding='10px', width='100%'))
        self.SO_box=widgets.VBox(children=[SO_Title,self.OUT_NAME,SO_Button],layout=layout_box)
        display(self.SO_box)


    def Save_OUTPUT_FILE(self,event):
        self.out_name=self.OUT_NAME.value
        self.path_out="OUTPUT_FILE"
        self.path_miss="MISSION_FILE"
        self.path_mission_ref="workdir\oad_sizing.csv"
        self.OAD.Save_File(self.MDA_problem.output_file_path,self.path_out,self.out_name)
        self.OAD.Save_CSV_File(self.path_mission_ref,self.path_miss,self.out_name)

        #the following lines are meant to copy th output file into BaseFile folder (geo 3d modeler)
        self.path_out = "Base Files"
        self.OAD.Save_File(self.MDA_problem.output_file_path, self.path_out, self.out_name)
        print(str(self.OUT_NAME.value)+" OUTPUTS AND MISSION FILES SAVED ")
        print("-------------------------------------------")

# MISSION ANALYSIS INTERFACE
    def Mission_Analysis_UI(self,event):
        clear_output()
        display(self.BOX_MDA)
        path="workdir"
        file=self.MDA_problem.output_file_path
        self.OUTPUT_FILE=self.OAD.Join_File(path,file)

        self.OUTPUT_DATA =self.OAD.Output_File(self.OUTPUT_FILE)


        self.OPM_value1=self.OUTPUT_DATA["data:weight:aircraft:payload"].value[0]
        self.OPM_value2=self.OUTPUT_DATA["data:mission:MTOW_mission:diversion:distance"].value[0]
        self.OPM_value3=self.OUTPUT_DATA["data:mission:MTOW_mission:holding:duration"].value[0]
        self.OPM_value4=self.OUTPUT_DATA["data:mission:MTOW_mission:main_route:range"].value[0]
        self.OPM_value5=self.OUTPUT_DATA["data:mission:MTOW_mission:takeoff:V2"].value[0]
        #self.OPM_value6=self.OUTPUT_DATA["data:mission:MTOW_mission:takeoff:altitude"].value[0]
        #ATTENTION: review, conversion * 0.3048
        self.OPM_value6=self.OUTPUT_DATA["data:mission:MTOW_mission:takeoff:safety_altitude"].value[0]*0.3048
        self.OPM_value7=self.OUTPUT_DATA["data:mission:MTOW_mission:takeoff:fuel"].value[0]
        self.OPM_value8=self.OUTPUT_DATA["data:mission:MTOW_mission:taxi_in:duration"].value[0]
        self.OPM_value9=self.OUTPUT_DATA["data:mission:MTOW_mission:taxi_out:duration"].value[0]
        self.OPM_value10=self.OUTPUT_DATA["data:mission:MTOW_mission:taxi_out:thrust_rate"].value[0]



        layout=widgets.Layout(width="50%", height='50px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        layout_button=widgets.Layout(width='30%', height='50px', border='4px solid black')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')
        layout_box1=widgets.Layout(justify_content='space-between',width='100%')

        OPM_path1="Table/opm_name.csv"
        OPM_path2="Table/opm_unit.csv"
        OPM_path3="Table/opm_des.csv"
        OPM_Table1=self.csv_to_table(OPM_path1)
        OPM_Table2=self.csv_to_table(OPM_path2)
        OPM_Table3=self.csv_to_table(OPM_path3)
        OPM_Table4=[OPM_Table1[i]+OPM_Table2[i] for i in range(len(OPM_Table1))]

        OPM_title=widgets.HTML(value=" <b>MISSION ANALYSIS </b>")

        OPM_Button1=widgets.Button(description="RUN ANALYSIS",layout=layout_button,style=dict(button_color='#ebebeb'))

        OPM_Button1.on_click(self.Run_Mission_Aanlysis)

        OPM_Button2=widgets.Button(description="OUTPUTS DATA",layout=layout_button,style=dict(button_color='#ffccb3'))
        OPM_Button2.on_click(self.View_OP_Ouput_Data)

        OPM_Button3=widgets.Button(description="SAVE DATA ",layout=layout_button,style=dict(button_color="#33ffcc"))
        OPM_Button3.on_click(self.Save_OP_OUT_F_UI)

        self.OPM_1=widgets.BoundedFloatText(min=10000,max=30000,step=1,value=self.OPM_value1,disabled=False,description=OPM_Table4[0],description_tooltip=OPM_Table3[0],style=style,layout=layout)
        self.OPM_2=widgets.BoundedFloatText(min=100,max=400,step=1,value=self.OPM_value2,disabled=False,description=OPM_Table4[1],description_tooltip=OPM_Table3[1],style=style,layout=layout)

        self.OPM_3=widgets.BoundedFloatText(min=10,max=100,step=1,value=self.OPM_value3,disabled=False,description=OPM_Table4[2],description_tooltip=OPM_Table3[1],style=style,layout=layout)
        self.OPM_4=widgets.BoundedFloatText(min=1000,max=7000,step=1,value=self.OPM_value4,disabled=False,description=OPM_Table4[3],description_tooltip=OPM_Table3[3],style=style,layout=layout)
        self.OPM_5=widgets.BoundedFloatText(min=10,max=200,step=0.1,value=self.OPM_value5,disabled=False,description=OPM_Table4[4],description_tooltip=OPM_Table3[4],style=style,layout=layout)
        self.OPM_6=widgets.BoundedFloatText(min=0,max=20,step=1,value=self.OPM_value6,disabled=False,description=OPM_Table4[5],description_tooltip=OPM_Table3[5],style=style,layout=layout)
        self.OPM_7=widgets.BoundedFloatText(min=10,max=200,step=0.1,value=self.OPM_value7,disabled=False,description=OPM_Table4[6],description_tooltip=OPM_Table3[6],style=style,layout=layout)
        self.OPM_8=widgets.BoundedFloatText(min=0,max=1000,step=1,value=self.OPM_value8,disabled=False,description=OPM_Table4[7],description_tooltip=OPM_Table3[7],style=style,layout=layout)
        self.OPM_9=widgets.BoundedFloatText(min=0,max=1000,step=1,value=self.OPM_value9,disabled=False,description=OPM_Table4[8],description_tooltip=OPM_Table3[8],style=style,layout=layout)
        self.OPM_10=widgets.BoundedFloatText(min=0,max=1,step=0.01,value=self.OPM_value10,disabled=False,description=OPM_Table4[9],description_tooltip=OPM_Table3[9],style=style,layout=layout)
        OPM_box1=widgets.VBox(children=[self.OPM_1,self.OPM_2,self.OPM_3,self.OPM_4,self.OPM_5,self.OPM_6,self.OPM_7,self.OPM_8,self.OPM_9,self.OPM_10],layout=widgets.Layout(border='3px solid black',align_items='center',padding='10px', width='100%'))
        OPM_box2=widgets.HBox(children=[OPM_Button1,OPM_Button2,OPM_Button3],layout=layout_box1)
        self.OPM_box=widgets.VBox(children=[OPM_title,OPM_box1,OPM_box2],layout=layout_box)
        display(self.OPM_box)
        return self.OPM_box


# RUN THE MISSION ANALYSIS PROBLEM
    def Run_Mission_Aanlysis(self,event):

        path_config="data"
        path_source="workdir"
        config_file_name="operational_mission_conf.yml"
        source_file_name="oad_sizing_out.xml"

        self.Liste_File=self.OAD.MISSION_ANALYSIS(config_file_name,source_file_name,path_config,path_source)

        self.OP_CONFIGURATION_FILE=self.Liste_File[0]
        self.OP_INPUT_FILE=self.Liste_File[2]
        print("-----------------------------------------------------------------------")
        print("OPERATIONAL INPUT FILE GENERATED")
        print("-----------------------------------------------------------------------")

        self.OP_INPUT_DATA=self.OAD.Input_File(self.OP_INPUT_FILE)

        self.OP_INPUT_DATA["data:mission:op_mission:payload"].value=self.OPM_1.value
        self.OP_INPUT_DATA["data:mission:op_mission:diversion:distance"].value=1852*self.OPM_2.value
        self.OP_INPUT_DATA["data:mission:op_mission:holding:duration"].value=self.OPM_3.value
        self.OP_INPUT_DATA["data:mission:op_mission:main_route:range"].value=1852*self.OPM_4.value
        self.OP_INPUT_DATA["data:mission:op_mission:takeoff:V2"].value=self.OPM_5.value
        #self.OP_INPUT_DATA["data:mission:op_mission:takeoff:altitude"].value = self.OPM_6.value
        self.OP_INPUT_DATA["data:mission:op_mission:takeoff:safety_altitude"].value=self.OPM_6.value
        self.OP_INPUT_DATA["data:mission:op_mission:takeoff:fuel"].value=self.OPM_7.value
        self.OP_INPUT_DATA["data:mission:op_mission:taxi_in:duration"].value=self.OPM_8.value
        self.OP_INPUT_DATA["data:mission:op_mission:taxi_out:duration"].value=self.OPM_9.value
        self.OP_INPUT_DATA["data:mission:op_mission:taxi_out:thrust_rate"].value=self.OPM_10.value

        self.OP_INPUT_DATA.save()
        print("-----------------------------------------------------------------------")
        print("MISSION DATA SAVED IN THE OPERATIONAL INPUT FILE")
        print("-----------------------------------------------------------------------")

        self.OP_PROBLEM=self.OAD.RUN_MISSION_ANALYSIS(self.OP_CONFIGURATION_FILE)
        return self.OP_PROBLEM

# VIEW THE MISSION ANALYSIS RESULTS DATA

    def View_OP_Ouput_Data(self,event):
        clear_output()
        display(self.BOX_MDA)
        display(self.OPM_box)
        path="workdir"
        file=self.OP_PROBLEM.output_file_path
        self.OP_OUTPUT_FILE=self.OAD.Join_File(path,file)
        self.OP_output_data=self.OAD.View_outputs_data(self.OP_OUTPUT_FILE)
        return self.OP_output_data

 # SAVE THE MISSION ANALYSIS RESULTS DATA
    def Save_OP_OUT_F_UI(self,event):
        clear_output()
        display(self.BOX_MDA)
        display(self.OPM_box)
        layout=widgets.Layout(width="50%", height='40px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        layout_button=widgets.Layout(width='30%', height='50px', border='4px solid black')
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')
        self.OP_OUT_NAME=widgets.Text(placeholder='Type the files name',description='OUTPUTS FILE NAME:',value="",style=style,layout=layout,disabled=False)
        OP_Title=widgets.HTML(value=" <b> SAVING OUTPUT FILE </b>")
        OP_Button=widgets.Button(description="SAVE",tooltip="SAVE THE OUTPUTS",layout=layout_button,style=dict(button_color="#33ffcc"))
        OP_Button.on_click(self.Save_OP_OUTPUT_FILE)
        OP_box_OP=widgets.VBox(children=[self.OP_OUT_NAME], layout=widgets.Layout(border='3px solid black',align_items='center', padding='10px', width='100%'))
        self.OP_box=widgets.VBox(children=[OP_Title,OP_box_OP,OP_Button],layout=layout_box)
        display(self.OP_box)


    def Save_OP_OUTPUT_FILE(self,event):

        self.OP_out_name=self.OP_OUT_NAME.value
        self.OP_path_miss="MISSION_FILE"
        self.OP_path_mission_ref="workdir\operational_mission_study.csv"
        self.OAD.Save_CSV_File(self.OP_path_mission_ref,self.OP_path_miss,self.OP_out_name)
        print(str(self.OP_OUT_NAME.value)+" OPERATIONAL  MISSION FILES SAVED IN THE MISSION_FILE FOLDER ")
        print("-------------------------------------------")



# RUN MDA PHASE TO AIRCRAFT ANALYSIS PHASE
    def mda_to_analysis(self,event):
        clear_output()
        self.Button_M4.style.button_color="#ebebeb"
        self.Button_M5.style.button_color="#00d600"
        image_path="Images/Wing.jpg"
        custom_css = f'''
        .vbox-with-background {{
            background-image: url("{image_path}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            width: 100%;
            height: 100%;
        }}
        '''
        display(HTML(f'<style>{custom_css}</style>'),self.menu)
        print("AIRCRAFT ANALYSIS PHASE")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------------------------")

# RUN MDA TO AIRCRAFT  PHASE
    def mda_to_input(self,event):
        clear_output()
        self.Button_M5.style.button_color="#ebebeb"
        self.Button_M4.style.button_color="#00d600"
        display(self.BOX_INPUT)
        print("AIRCRAFT INPUT  PHASE")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------------------------")

# Delete INPUT FILE

    def Output_aircraft_file(self,event):
        clear_output()
        display(self.BOX_INPUT)
        path_to_target="OUTPUT_FILE"
        path_to_file_list = []
        temp=os.listdir(path_to_target)
        for i in range(0, len(temp)):
            if temp[i][-3:] =='xml':
                path_to_file_list.append(temp[i])
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        title=widgets.HTML(value=" <b>Choose the output file data to delete</b>")
        box1 = widgets.HBox(children=[title],layout=layout_title)
        self.output_file_name = widgets.Dropdown(options=path_to_file_list,description='Choose your file:',disabled=False,style={'description_width': 'initial'})
        self.output_file_name.observe(self.delete_output_file,names="value")
        box2=widgets.HBox(children=[self.output_file_name])

        self.DO_BOX=widgets.VBox(children=[box1,box2],layout=Layout(border='6px solid black', padding='10px', align_items='center', width='100%'))
        display(self.DO_BOX)
        return self.output_file_name

    def delete_output_file(self,change):
        path_del_in="OUTPUT_FILE/" +str(change.new)
        self.OAD.Delete_File(path_del_in)

        print("You have deleted the"+" "+str(change.new)+ " "+ "file from th OUTPUT_FILE FOLD")
        print("------------------------------------------------")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # AIRCRAFT ANALYSIS PHASE# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# THE PRINCIPAL AIRCRAFT ANAYSLIS USER INTERFACE

    def POST_PROCESSING_UI(self,event):
        clear_output()
        layout=widgets.Layout(width="60%", height='40px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        layout_button=widgets.Layout(width='30%', height='50px', border='4px solid black')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%',justify_content='space-between')
        layout_H=widgets.Layout( padding='10px', align_items='center', width='100%',justify_content='space-between')
        title=widgets.HTML(value=" <b>POST-PROCESSING </b>")
        RES_options=["GEOMETRY","MASS BREAKDOWN","AERODYNAMIC","PAYLOAD/RANGE","MISSION","3DMODEL"]
        self.RES_choice=widgets.Dropdown(description="CHOOSE THE ANALYSIS TOOL", options=RES_options,style=style,layout=layout)
        RES_Button1=widgets.Button(description="SAVE",tooltip=" CONFIRM THE  CHOOSEN ANALYSIS TOOL",layout=layout_button,style=dict(button_color="#33ffcc"))
        RES_Button1.on_click(self.PLOT_UI)
        RES_Button1.icon='fa-floppy-o'

        RES_Button2=widgets.Button(description="BACK",layout=layout_button,style=dict(button_color='#3785d8'))
        RES_Button3=widgets.Button(description="NEXT",layout=layout_button,style=dict(button_color='#77db5c'))

        RES_Button2.icon='fa-angle-left'
        RES_Button3.icon = 'fa-angle-right'

        RES_Button2.on_click(self.analysis_to_mda)
        RES_Button3.on_click(self.analysis_to_optimization)

        buttonHOME = widgets.Button(description='')
        buttonHOME.icon = 'fa-home'
        buttonHOME.layout.width = 'auto'
        buttonHOME.layout.height = 'auto'
        buttonHOME.on_click(self.HomeInterface)
        box5 = widgets.Box(children=[buttonHOME], layout=Layout(border='0px solid black',
                           margin='50 0 50 0px', padding='0.5px', align_items='center', width='100'))
        #---------------------------------------------------------------------------------------------------------------
        buttonINFO = widgets.Button(description='')
        buttonINFO.icon = 'fa-info-circle'
        buttonINFO.layout.width = 'auto'
        buttonINFO.layout.height = 'auto'
        output = widgets.Output()
        def info_message(event):
            with output:
                output.clear_output()
                if len(output.outputs) > 0:
                    output.clear_output()
                else:
                    print('Welcome to the Analysis Phase.\n'
                          'Different tools are at your disposal. \n'
                          'At your discretion, choose which type of plot or data it is needed.\n')

        buttonINFO.on_click(info_message)
        box4 = widgets.Box(children=[buttonINFO, output],layout=Layout(border='1px solid black',
                                         margin='50 0 50 0px', padding='5px', align_items='center', width='100'))
        #---------------------------------------------------------------------------------------------------------------
        box=widgets.HBox(children=[RES_Button2,RES_Button1,RES_Button3,box5],layout=widgets.Layout(justify_content='space-between',width='100%',padding='10 px'))
        self.RES_box=widgets.VBox(children=[title,self.RES_choice,box,box4],layout=layout_box)
        display(self.RES_box)


# FUNCTION: FROM THE ANAYSIS PHASE TO OPTIMIZATION PHASE

    def analysis_to_optimization (self,event):
        clear_output()
        self.Button_M5.style.button_color='#ebebeb'
        self.Button_M6.style.button_color="#00d600"
        image_path="Images/Wing.jpg"
        custom_css = f'''
        .vbox-with-background {{
            background-image: url("{image_path}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            width: 100%;
            height: 100%;
        }}
        '''
        display(HTML(f'<style>{custom_css}</style>'),self.menu)
# FUNCTION: FROM THE ANAYSIS PHASE TO MDA  PHASE
    def analysis_to_mda (self,event):
        clear_output()
        display(self.BOX_MDA)

# PLOT UI

    def PLOT_UI(self,event):

        # GEOMETRY UI
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')

        path_to_target="OUTPUT_FILE"
        path_to_file_list = []
        temp=os.listdir(path_to_target)
        for i in range(0, len(temp)):
            if temp[i][-3:] =='xml':
                path_to_file_list.append(temp[i])

        GEO_title=widgets.HTML(value=" <b>GEOMETRY ANALYSIS</b>")
        GEO_box1 = widgets.HBox(children=[GEO_title],layout=layout_title)
        self.output_file_geo = widgets.SelectMultiple(options=path_to_file_list,description='CHOOSE THE AIRCRAFT FILES:',disabled=False,style={'description_width': 'initial'},layout=widgets.Layout(width="500px", height="150 px"),rows=len(path_to_file_list))
        GEO_box2=widgets.HBox(children=[self.output_file_geo])
        PLOT_OPTION=["AIRCRAFT","WING"]
        self.geo_plot_choice=widgets.Select(options=PLOT_OPTION,description='CHOOSE WHICH GEOMETRY TO PLOT:',disabled=False,style={'description_width': 'initial'},layout=widgets.Layout(width="500px", height="150 px"),rows=len(PLOT_OPTION))
        GEO_Button=widgets.Button(description="PLOT",tooltip="PLOT THE GEOMETRY OF THE SELECTED AIRCRAFTS",layout=layout_button,style=dict(button_color="#33ffcc"))
        GEO_Button.on_click(self.Geometry_Plot)
        self.GEO_UI_BOX=widgets.VBox(children=[GEO_box1,GEO_box2,self.geo_plot_choice,GEO_Button],layout=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%'))

# AERODYNAMIC  UI

        AERO_title=widgets.HTML(value=" <b>AERODYNAMIC ANALYSIS</b>")
        AERO_box1 = widgets.HBox(children=[AERO_title],layout=layout_title)
        self.output_file_aero = widgets.SelectMultiple(options=path_to_file_list,description='CHOOSE THE AIRCRAFTS TO ANALYZE:',disabled=False,style={'description_width': 'initial'},layout=widgets.Layout(width="500px", height="150 px"),rows=len(path_to_file_list))
        AERO_box2=widgets.HBox(children=[self.output_file_aero])
        AERO_Button=widgets.Button(description="PLOT",tooltip="PLOT THE DRAG POLAR OF THE SELECTED AIRCRAFTS",layout=layout_button,style=dict(button_color="#33ffcc"))
        AERO_Button.on_click(self.Aerodynamic_Plot)
        self.AERO_UI_BOX=widgets.VBox(children=[AERO_box1,AERO_box2,AERO_Button],layout=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%'))


 # MASS BREAK DOWN UI
        path_to_target="OUTPUT_FILE"
        path_to_file_list = []
        temp=os.listdir(path_to_target)
        for i in range(0, len(temp)):
            if temp[i][-3:] =='xml':
                path_to_file_list.append(temp[i])
        MASS_title=widgets.HTML(value=" <b>MASS BREAKDOWN ANALYSIS</b>")
        MASS_box1 = widgets.HBox(children=[MASS_title],layout=layout_title)
        self.output_file_mass = widgets.SelectMultiple(options=path_to_file_list,description='CHOOSE THE AIRCRAFTS TO ANALYZE:',disabled=False,style={'description_width': 'initial'},layout=widgets.Layout(width="500px", height="150 px"),rows=len(path_to_file_list))
        Strategy_Option=["BAR","SUN"]
        self.mass_plot_choice=widgets.Select(options=Strategy_Option,description='CHOOSE THE PLOT STRATEGY:',disabled=False,style={'description_width': 'initial'},layout=widgets.Layout(width="500px", height="150 px"),rows=len(Strategy_Option))
        MASS_box2=widgets.HBox(children=[self.output_file_mass])
        MASS_box3=widgets.HBox(children=[self.mass_plot_choice])
        MASS_Button=widgets.Button(description="PLOT",tooltip="PLOT THE MASS BREAKDOWN THE SELECTED AIRCRAFTS",layout=layout_button,style=dict(button_color="#33ffcc"))
        MASS_Button.on_click(self.Mass_Plot)

        self.MASS_UI_BOX=widgets.VBox(children=[MASS_box1,MASS_box2,MASS_box3,MASS_Button],layout=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%'))



 # MISSION UI


        path_to_target="MISSION_FILE"
        path_to_file_list = []
        temp=os.listdir(path_to_target)
        for i in range(0, len(temp)):
            if temp[i][-3:] =='csv':
                path_to_file_list.append(temp[i])
        MISS_title=widgets.HTML(value=" <b>MISSION ANALYSIS</b>")
        MISS_box1 = widgets.HBox(children=[MISS_title],layout=layout_title)
        self.output_file_miss = widgets.SelectMultiple(options=path_to_file_list,description='CHOOSE THE MISSION TO ANALYZE:',disabled=False,style={'description_width': 'initial'},layout=widgets.Layout(width="500px", height="150 px"),rows=len(path_to_file_list))
        MISS_box2=widgets.HBox(children=[self.output_file_miss])
        MISS_Button=widgets.Button(description="PLOT",tooltip="PLOT THE MISSION  OF THE SELECTED AIRCRAFTS",layout=layout_button,style=dict(button_color="#33ffcc"))
        MISS_Button.on_click(self.Mission_Plot)

        self.MISS_UI_BOX=widgets.VBox(children=[MISS_box1,MISS_box2,MISS_Button],layout=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%'))

 # PAYLOAD RANGE UI

        path_to_target="OUTPUT_FILE"
        path_to_file_list = []
        temp=os.listdir(path_to_target)
        for i in range(0, len(temp)):
            if temp[i][-3:] =='xml':
                path_to_file_list.append(temp[i])
        PAY_title=widgets.HTML(value=" <b>PAYLOAD/RANGE DIAGRAMM </b>")

        PAY_box1 = widgets.HBox(children=[PAY_title],layout=layout_title)
        self.output_file_pay = widgets.SelectMultiple(options=path_to_file_list,description='CHOOSE THE AIRCRAFTS TO ANALYZE:',disabled=False,style={'description_width': 'initial'},layout=widgets.Layout(width="500px", height="150 px"),rows=len(path_to_file_list))
        PAY_box2=widgets.HBox(children=[self.output_file_pay])
        PAY_Button=widgets.Button(description="PLOT",tooltip="PLOT THE DRAG POLAR OF THE SELECTED AIRCRAFTS",layout=layout_button,style=dict(button_color="#33ffcc"))
        PAY_Button.on_click(self.PAYLOAD_RANGE_PLOT)

        self.PAY_UI_BOX=widgets.VBox(children=[PAY_box1,PAY_box2,PAY_Button],layout=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%'))

# 3D MODELER
        path_to_target = "OUTPUT_FILE"
        path_to_file_list = []
        temp = os.listdir(path_to_target)
        for i in range(0, len(temp)):
            if temp[i][-3:] == 'xml':
                path_to_file_list.append(temp[i])
            MODEL3D_title = widgets.HTML(value=" <b>ESP 3D MODEL </b>")

        MODEL3D_box1 = widgets.HBox(children=[MODEL3D_title], layout=layout_title)
        self.output_file_MODEL3D = widgets.SelectMultiple(options=path_to_file_list,
                                                      description='CHOOSE THE AIRCRAFT TO ANALYZE (only ONE):', disabled=False,
                                                      style={'description_width': 'initial'},
                                                      layout=widgets.Layout(width="500px", height="150 px"),
                                                      rows=len(path_to_file_list))
        MODEL3D_box2 = widgets.HBox(children=[self.output_file_MODEL3D])
        MODEL3D_Button = widgets.Button(description="PLOT", tooltip="PLOT the 3d model of the aircraft",
                                    layout=layout_button, style=dict(button_color="#33ffcc"))
        MODEL3D_Button.on_click(self.Model3d_Plot)

        self.MODEL3D_UI_BOX = widgets.VBox(children=[MODEL3D_box1, MODEL3D_box2, MODEL3D_Button],
                                       layout=widgets.Layout(border='6px solid black', padding='10px',
                                                             align_items='center', width='100%'))


        # SHOW THE GEOMETRY PLOT UI

        if (self.RES_choice.value=="GEOMETRY"):

            clear_output()
            display(self.RES_box)
            display(self.GEO_UI_BOX)


        # SHOW THE MASS BREAKDOWN PLOT UI

        elif (self.RES_choice.value=="MASS BREAKDOWN"):
            clear_output()
            display(self.RES_box)
            display(self.MASS_UI_BOX)


         # SHOW THE AERODYNAMIC  PLOT UI

        elif (self.RES_choice.value=="AERODYNAMIC"):
            clear_output()
            display(self.RES_box)
            display(self.AERO_UI_BOX)

         # SHOW THE MISSION PLOT  UI

        elif (self.RES_choice.value=="MISSION"):
            clear_output()
            display(self.RES_box)
            display(self.MISS_UI_BOX)

        # SHOW THE PAYLOAD RANGE DIAGRAMM PLOT  UI
        elif (self.RES_choice.value=="PAYLOAD/RANGE"):
            clear_output()
            display(self.RES_box)
            display(self.PAY_UI_BOX)
        elif (self.RES_choice.value == "3DMODEL"):
            clear_output()
            display(self.RES_box)
            display(self.MODEL3D_UI_BOX)

    def Model3d_Plot(self,event):
        clear_output()
        display(self.RES_box)
        display(self.MODEL3D_UI_BOX)
        MODEL3D_liste_design = self.output_file_MODEL3D.value
        path = "OUTPUT_FILE"
        MODEL3D_Liste_Design = []
        MODEL3D_Liste_Name = []
        i = 0
        while (i < len(MODEL3D_liste_design)):
            OUTPUT = pth.join(path, MODEL3D_liste_design[i])
            MODEL3D_Liste_Design.append(OUTPUT)
            name = os.path.splitext(os.path.split(MODEL3D_liste_design[i])[1])[0]
            MODEL3D_Liste_Name.append(name)
            i = i + 1

        self.GEO3D(MODEL3D_liste_design)
        #MODEL3D_PLOT = self.OAD.MASS_BAR_PLOT(MODEL3D_Liste_Design, MODEL3D_Liste_Name)


 # GEOMETRY PLOT

    def Geometry_Plot(self,event):
        clear_output()
        display(self.RES_box)
        display(self.GEO_UI_BOX)
        geo_liste_design=self.output_file_geo.value
        path="OUTPUT_FILE"
        Geo_Liste_Design=[]
        Geo_Liste_Name=[]
        i=0
        while (i<len(geo_liste_design)):
            OUTPUT=pth.join(path,geo_liste_design[i])
            Geo_Liste_Design.append(OUTPUT)
            name=os.path.splitext(os.path.split(geo_liste_design[i])[1])[0]
            Geo_Liste_Name.append(name)

            i=i+1

        if (self.geo_plot_choice.value=="WING"):
            GEO_PLOT=self.OAD.WING_GEOMETRY_PLOT(Geo_Liste_Design,Geo_Liste_Name)

        elif (self.geo_plot_choice.value=="AIRCRAFT"):
            GEO_PLOT=self.OAD.AIRCRAFT_GEOMETRY_PLOT(Geo_Liste_Design,Geo_Liste_Name)
        else:
            print("Please choose the Geometry to plot")

 # AERODYNAMIC PLOT

    def Aerodynamic_Plot(self,event):
        clear_output()
        display(self.RES_box)
        display(self.AERO_UI_BOX)
        aero_liste_design=self.output_file_aero.value
        path="OUTPUT_FILE"
        Aero_Liste_Design=[]
        Aero_Liste_Name=[]
        i=0
        while (i<len(aero_liste_design)):
            OUTPUT=pth.join(path,aero_liste_design[i])
            Aero_Liste_Design.append(OUTPUT)
            name=os.path.splitext(os.path.split(aero_liste_design[i])[1])[0]
            Aero_Liste_Name.append(name)

            i=i+1

        AERO_PLOT=self.OAD.AERODYNAMIC_PLOT(Aero_Liste_Design,Aero_Liste_Name)

 # MASS BREAKDOWN PLOT

    def Mass_Plot(self,event):
        clear_output()
        display(self.RES_box)
        display(self.MASS_UI_BOX)
        mass_liste_design=self.output_file_mass.value
        path="OUTPUT_FILE"
        Mass_Liste_Design=[]
        Mass_Liste_Name=[]
        i=0
        while (i<len(mass_liste_design)):
            OUTPUT=pth.join(path,mass_liste_design[i])
            Mass_Liste_Design.append(OUTPUT)
            name=os.path.splitext(os.path.split(mass_liste_design[i])[1])[0]
            Mass_Liste_Name.append(name)
            i=i+1

        if (self.mass_plot_choice.value=="BAR"):
            MASS_PLOT=self.OAD.MASS_BAR_PLOT(Mass_Liste_Design,Mass_Liste_Name)
        elif (self.mass_plot_choice.value=="SUN"):
            MASS_PLOT=self.OAD.MASS_SUN_PLOT(Mass_Liste_Design)
        else:
            print(" Choose a Plot Strategy Please")


 # MISSION PLOT

    def Mission_Plot(self,event):
        clear_output()
        display(self.RES_box)
        display(self.MISS_UI_BOX)
        miss_liste_design=self.output_file_miss.value
        path="MISSION_FILE"
        MISS_Liste_Design=[]
        MISS_Liste_Name=[]
        i=0
        while (i<len(miss_liste_design)):
            OUTPUT=pth.join(path,miss_liste_design[i])
            MISS_Liste_Design.append(OUTPUT)
            name=os.path.splitext(os.path.split(miss_liste_design[i])[1])[0]
            MISS_Liste_Name.append(name)
            i=i+1

        self.MISS_PLOT=self.OAD.MISSION_PLOT(MISS_Liste_Design,MISS_Liste_Name)




 # PAYLOAD RANGE DIAGRAMM PLOT

    def PAYLOAD_RANGE_PLOT(self,event):
        clear_output()
        display(self.RES_box)
        display(self.PAY_UI_BOX)
        file_name=self.output_file_pay.value
        mission_name=[]
        i=0
        while (i<len(file_name)):
            name=os.path.splitext(os.path.split(file_name[i])[1])[0]+".csv"
            mission_name.append(name)
            i=i+1

        Path1="OUTPUT_FILE"
        Path2="MISSION_FILE"
        FILE_PATH=[]
        MISSION_PATH=[]
        j=0
        while (j<len(file_name)):
            OUTPUT=pth.join(Path1,file_name[j])
            FILE_PATH.append(OUTPUT)
            MISSION=pth.join(Path2,mission_name[j])
            MISSION_PATH.append(MISSION)
            j=j+1


        fig=self.OAD.payload_range(FILE_PATH[0],MISSION_PATH[0],name=mission_name[0])
        k=1
        while (k<len(FILE_PATH)):
            fig=self.OAD.payload_range(FILE_PATH[k],MISSION_PATH[k],name=mission_name[k],fig=fig)
            k=k+1

        fig.show()





 # # # # # #  # # # # # # # # # # # # #   OPTIMIZATION   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

 # OPTIMIZATION PROBLEM UI
    def OPT_DESIGN(self,event):
        clear_output()
        path_to_target="OUTPUT_FILE"
        path_to_file_list = []
        temp=os.listdir(path_to_target)
        for i in range(0, len(temp)):
            if temp[i][-3:] =='xml':
                path_to_file_list.append(temp[i])
                layout_title=widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')
        title=widgets.HTML(value=" <b>OPTMIZATION</b>")
        self.AC_Opt = widgets.Select(options=path_to_file_list,description='CHOOSE THE AIRCRAFT TO OPTIMIZE:',disabled=False,style={'description_width':'initial'},layout=widgets.Layout(width="500px", height="150 px"),rows=len(path_to_file_list))
        AC_Button=widgets.Button(description="SAVE THE CHOICE",tooltip="SAVE THE CHOSEN AIRCRAFT ",layout=layout_button,style=dict(button_color="#33ffcc"))
        AC_Button.on_click(self.OPT_PROBLEM_UI)
        AC_Button.icon= 'fa-floppy-o'
        box1=widgets.HBox(children=[self.AC_Opt])

        buttonHOME = widgets.Button(description='')
        buttonHOME.icon = 'fa-home'
        buttonHOME.layout.width = 'auto'
        buttonHOME.layout.height = 'auto'
        buttonHOME.on_click(self.HomeInterface)
        box5 = widgets.Box(children=[buttonHOME], layout=Layout(border='0px solid black',
                           margin='50 0 50 0px', padding='0.5px', align_items='center', width='100'))
        #---------------------------------------------------------------------------------------------------------------
        buttonINFO = widgets.Button(description='')
        buttonINFO.icon = 'fa-info-circle'
        buttonINFO.layout.width = 'auto'
        buttonINFO.layout.height = 'auto'
        output = widgets.Output()
        def info_message(event):
            with output:
                output.clear_output()
                if len(output.outputs) > 0:
                    output.clear_output()
                else:
                    print('Welcome to the Optimization Phase.\n'
                          'Choose the Aircraft file to be optimized. \n')

        buttonINFO.on_click(info_message)
        box4 = widgets.Box(children=[buttonINFO, output],layout=Layout(border='1px solid black',
                                         margin='50 0 50 0px', padding='5px', align_items='center', width='100'))
        #---------------------------------------------------------------------------------------------------------------
        self.AC_BOX=widgets.VBox(children=[title,self.AC_Opt,AC_Button,box5,box4],layout=layout_box)
        display(self.AC_BOX)



    def OPT_PROBLEM_UI(self,event):
        # PATH OF THE ARICRAFT TO OPTIMIZE
        path_source="OUTPUT_FILE"
        AC_file=self.AC_Opt.value
        self.OPT_Source=pth.join(path_source,AC_file)

        clear_output()

        # LIST OF INPUT VARIABLE NAMES
        path="workdir"
        file_in="oad_sizing_in.xml"
        File_In=pth.join(path, file_in)
        datafile_in =self.OAD.Input_File(File_In)
        self.liste_in=datafile_in.names()

        # TLARS INPUTS VARIABLE NAMES
        self.liste_in_TL=[]
        for i in range(0, len(self.liste_in)):
            if self.liste_in[i][5:7] =='TL':
                self.liste_in_TL.append(self.liste_in[i])

        # GEOMETRY INPUTS VARIABLE NAMES
        self.liste_in_GEO=[]
        for i in range(0, len(self.liste_in)):
            if self.liste_in[i][5:7] =='ge':
                self.liste_in_GEO.append(self.liste_in[i])

        # WEIGHT INPUTS VARIABLE NAMES
        self.liste_in_WE=[]
        for i in range(0, len(self.liste_in)):
            if self.liste_in[i][5:7] =='we':
                self.liste_in_WE.append(self.liste_in[i])

        # AERODYNAMIC INPUTS VARIABLE NAMES
        self.liste_in_AERO=[]
        for i in range(0, len(self.liste_in)):
            if self.liste_in[i][5:7] =='ae':
                self.liste_in_AERO.append(self.liste_in[i])

        # PROPULSION INPUTS VARIABLE NAMES
        self.liste_in_PR=[]
        for i in range(0, len(self.liste_in)):
            if self.liste_in[i][5:7] =='pr':
                self.liste_in_PR.append(self.liste_in[i])

        # MISSION INPUTS VARIABLE NAMES
        self.liste_in_MISS=[]
        for i in range(0, len(self.liste_in)):
            if self.liste_in[i][5:7] =='mi':
                self.liste_in_MISS.append(self.liste_in[i])

        # LIST OF OUTPUT VARIABLE NAME
        path="workdir"
        file_out="oad_sizing_out.xml"
        File_Out=pth.join(path, file_out)
        datafile_out =self.OAD.Input_File(File_Out)
        self.liste_out=datafile_out.names()
         # TLARS OUTPUTS  VARIABLE NAMES
        self.liste_out_TL=[]
        for i in range(0, len(self.liste_out)):
            if self.liste_out[i][5:7] =='TL':
                self.liste_out_TL.append(self.liste_out[i])

        # GEOMETRY OUTPUTS VARIABLE NAMES
        self.liste_out_GEO=[]
        for i in range(0, len(self.liste_out)):
            if self.liste_out[i][5:7] =='ge':
                self.liste_out_GEO.append(self.liste_out[i])

        # WEIGHT OUTPUTS  VARIABLE NAMES
        self.liste_out_WE=[]
        for i in range(0, len(self.liste_out)):
            if self.liste_out[i][5:7] =='we':
                self.liste_out_WE.append(self.liste_out[i])


        # AERODYNAMIC OUTPUTS VARIABLE NAMES
        self.liste_out_AERO=[]
        for i in range(0, len(self.liste_out)):
            if self.liste_out[i][5:7] =='ae':
                self.liste_out_AERO.append(self.liste_out[i])

        # PROPULSION OUTPUTS VARIABLE NAMES
        self.liste_out_PR=[]
        for i in range(0, len(self.liste_out)):
            if self.liste_out[i][5:7] =='pr':
                self.liste_out_PR.append(self.liste_out[i])

        # MISSION OUTPUTS VARIABLE NAMES
        self.liste_out_MISS=[]
        for i in range(0, len(self.liste_out)):
            if self.liste_out[i][5:7] =='mi':
                self.liste_out_MISS.append(self.liste_out[i])


        # HANDLING OUTPUTS VARIABLE NAMES
        self.liste_out_HA=[]
        for i in range(0, len(self.liste_out)):
            if self.liste_out[i][5:7] =='ha':
                self.liste_out_HA.append(self.liste_out[i])


        layout=widgets.Layout(width="30%", height='40px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        layout_button=widgets.Layout(width='30%', height='50px', border='4px solid black')
        layout_V=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')
        layout_H=widgets.Layout( padding='10px', align_items='center', width='100%',justify_content='space-between')

         # DESIGN VARIABLE INTERFACE
        DES_Title=widgets.HTML(value=" <b> DESIGN VARIABLE</b>")
        DES_option1=["TLARS","GEOMETRY","WEIGHT","AERODYNAMIC","PROPULSION","MISSION"]
        self.DES_W1=widgets.Dropdown(options=DES_option1,value=DES_option1[0],description='VARIABLE TYPE:',disabled=False,style=style)
        self.DES_W1.observe(self.OPT_DES_CHANGE,names="value")

        self.DES_W2=widgets.Dropdown(options=self.liste_in,value=self.liste_in[0],description='DESIGN VARIABLE:',disabled=False,style=style)
        self.DES_LOWER=widgets.BoundedFloatText(min=0,max=10000000,step=0.001,value=0,disabled=False,description="MINIMUM VALUE",description_tooltip="ENTER THE MINIMUM VALUE OF THE DESIGN VARIABLE",style=style,layout=layout)
        self.DES_UPPER=widgets.BoundedFloatText(min=0,max=10000000,step=0.001,value=0,disabled=False,description="MAXIMUM VALUE",description_tooltip="ENTER THE MAXIMUM VALUE OF THE DESIGN VARIABLE",style=style,layout=layout)
        DES_box1=widgets.HBox(children=[self.DES_W1,self.DES_W2],layout=layout_H)
        DES_box2=widgets.HBox(children=[self.DES_LOWER,self.DES_UPPER],layout=layout_H)
        DES_BOX=widgets.VBox(children=[DES_Title,DES_box1,DES_box2],layout=layout_V)

        # CONSTRAINT VARIABLE INTERFACE
        CONS_Title=widgets.HTML(value=" <b> CONSTRAINT VARIABLE</b>")
        CONS_option1=["TLARS","GEOMETRY","WEIGHT","AERODYNAMIC","HANDLING QUALITES","PROPULSION","MISSION"]
        self.CONS_W1=widgets.Dropdown(options=CONS_option1,value=CONS_option1[0],description='VARIABLE TYPE:',disabled=False,style=style)
        self.CONS_W1.observe(self.OPT_CONS_CHANGE,names="value")
        self.CONS_W2=widgets.Dropdown(options=self.liste_out,value=self.liste_out[0],description='CONSTRAINT VARIABLE:',disabled=False,style=style)
        self.CONS_VAL=widgets.BoundedFloatText(min=0,max=10000000,step=0.001,value=0,disabled=False,description=" VALUE",description_tooltip="ENTER THE CONSTRAINT VALUE",style=style,layout=layout)
        self.CONS_LU=widgets.Dropdown(options=["lower","upper"],value="lower",description='LOWER/UPPER CONSTRAINT:',disabled=False,style=style)
        CONS_box1=widgets.HBox(children=[self.CONS_W1,self.CONS_W2],layout=layout_H)
        CONS_box2=widgets.HBox(children=[self.CONS_LU,self.CONS_VAL],layout=layout_H)
        CONS_BOX=widgets.VBox(children=[CONS_Title,CONS_box1,CONS_box2],layout=layout_V)

        # OBJECTIVE VARIABLE INTERFACE
        OBJ_Title=widgets.HTML(value=" <b> OBJECTIVE</b>")
        OBJ_option1=["TLARS","GEOMETRY","WEIGHT","AERODYNAMIC","HANDLING QUALITES","PROPULSION","MISSION"]
        self.OBJ_W1=widgets.Dropdown(options=OBJ_option1,value=OBJ_option1[0],description='VARIABLE TYPE:',disabled=False,style=style)
        self.OBJ_W1.observe(self.OPT_OBJ_CHANGE,names="value")
        self.OBJ_W2=widgets.Dropdown(options=self.liste_out,value=self.liste_out[0],description='OBJECTIVE VARIABLE:',disabled=False,style=style)
        OBJ_box1=widgets.HBox(children=[self.OBJ_W1,self.OBJ_W2],layout=layout_H)
        OBJ_BOX=widgets.VBox(children=[OBJ_Title,OBJ_box1],layout=layout_V)


        # GENERAL OPTIMIZATION INTERFACE
        OPT_Title=widgets.HTML(value=" <b> OPTIMIZATION PROBLEM </b>")
        OPT_Button=widgets.Button(description="SAVE",tooltip="SAVE THE OPTIMIZATION PROBLEM",layout=layout_button,style=dict(button_color="#33ffcc"))
        OPT_Button.on_click(self.Opt_Problem)
        buttonHOME = widgets.Button(description='')
        buttonHOME.icon = 'fa-home'
        buttonHOME.layout.width = 'auto'
        buttonHOME.layout.height = 'auto'
        buttonHOME.on_click(self.HomeInterface)
        box5 = widgets.Box(children=[buttonHOME], layout=Layout(border='0px solid black',
                           margin='50 0 50 0px', padding='0.5px', align_items='center', width='100'))
        #---------------------------------------------------------------------------------------------------------------
        buttonINFO = widgets.Button(description='')
        buttonINFO.icon = 'fa-info-circle'
        buttonINFO.layout.width = 'auto'
        buttonINFO.layout.height = 'auto'
        output = widgets.Output()
        def info_message(event):
            with output:
                output.clear_output()
                if len(output.outputs) > 0:
                    output.clear_output()
                else:
                    print('Define your optimization problem\n'
                          'Choose and give a value to the Design and Constraint Variables and finally define the Objective \n')

        buttonINFO.on_click(info_message)
        box4 = widgets.Box(children=[buttonINFO, output],layout=Layout(border='1px solid black',
                                         margin='50 0 50 0px', padding='5px', align_items='center', width='100'))
        #---------------------------------------------------------------------------------------------------------------
        self.OPT_BOX=widgets.VBox(children=[OPT_Title,DES_BOX,CONS_BOX,OBJ_BOX,OPT_Button,box5,box4],layout=layout_box)
        display(self.OPT_BOX)

    def OPT_DES_CHANGE(self,change):

        if (change.new=="TLARS"):
            self.DES_W2.options=self.liste_in_TL

        elif (change.new=="GEOMETRY"):
            self.DES_W2.options=self.liste_in_GEO

        elif (change.new=="WEIGHT"):
            self.DES_W2.options=self.liste_in_WE

        elif (change.new=="AERODYNAMIC"):
            self.DES_W2.options=self.liste_in_AERO

        elif (change.new=="PROPULSION"):
            self.DES_W2.options=self.liste_in_PR

        else:
            self.DES_W2.options=self.liste_in_MISS


    def OPT_CONS_CHANGE(self,change):

        if (change.new=="TLARS"):
            self.CONS_W2.options=self.liste_out_TL

        elif (change.new=="GEOMETRY"):
            self.CONS_W2.options=self.liste_out_GEO

        elif (change.new=="WEIGHT"):
            self.CONS_W2.options=self.liste_out_WE

        elif (change.new=="AERODYNAMIC"):
            self.CONS_W2.options=self.liste_out_AERO

        elif (change.new=="PROPULSION"):
            self.CONS_W2.options=self.liste_out_PR

        elif (change.new=="MISSION"):
            self.CONS_W2.options=self.liste_out_MISS

        else:
            self.DES_W2.options=self.liste_out_HA

    def OPT_OBJ_CHANGE(self,change):

        if (change.new=="TLARS"):
            self.OBJ_W2.options=self.liste_out_TL

        elif (change.new=="GEOMETRY"):
            self.OBJ_W2.options=self.liste_out_GEO

        elif (change.new=="WEIGHT"):
            self.OBJ_W2.options=self.liste_out_WE

        elif (change.new=="AERODYNAMIC"):
            self.OBJ_W2.options=self.liste_out_AERO

        elif (change.new=="PROPULSION"):
            self.OBJ_W2.options=self.liste_out_PR

        elif (change.new=="MISSION"):
            self.OBJ_W2.options=self.liste_out_MISS

        else:
            self.OBJ_W2.options=self.liste_out_HA

    # Defining optimization problem
    def Opt_Problem(self,event):
        # Getting the inputs optimization problem from the user interface
        des_name=self.DES_W2.value
        des_low=self.DES_LOWER.value
        des_up=self.DES_UPPER.value
        cons_name=self.CONS_W2.value
        cons_up_low=self.CONS_LU.value
        cons_val=self.CONS_VAL.value
        obj_name=self.OBJ_W2.value

         # Optimization problem dictionnary
        data={'optimization': {'design_variables': [{'name': des_name,'lower': des_low,'upper': des_up}],'constraints': [{'name': cons_name, cons_up_low: cons_val}],'objective': [{'name':obj_name,'scaler': 0.0001}]}}

        # The configuration file path
        file_name="oad_sizing.yml"
        path="data"
        file_path=pth.join(path,file_name)

         # Optimization problem definiton
        self.OAD.Write_Optimization_Problem(file_path,data)

        # NEXT OPTIMIZATION USER INETERFACE
        clear_output()
        #print("OPTIMIZATION PROBLEM SAVED")
        #print("------------------------------------------------------------------------------------------------")
        layout=widgets.Layout(width="30%", height='40px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        layout_button=widgets.Layout(width='30%', height='50px', border='4px solid black')
        layout_V=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')
        layout_H=widgets.Layout( padding='10px', align_items='center', width='100%',justify_content='space-between')

        title=widgets.HTML(value=" <b>AIRCRAFT OPTIMIZATION</b>")
        OPT_Button1=widgets.Button(description="OPTIMIZATION PROBLEM",tooltip="VIEW THE OPTIMIZATION PROBLEM",layout=layout_button,style=dict(button_color='#ebebeb'))
        OPT_Button1.on_click(self.OPt_View)

        OPT_Button2=widgets.Button(description="RUN OPTIMIZATION",tooltip="RUN THE OPTIMIZATION PROBLEM",layout=layout_button,style=dict(button_color='#ebebeb'))
        OPT_Button2.on_click(self.Run_Opt_Problem)

        OPT_Button3=widgets.Button(description="OPTIMIZATION RESULTS",tooltip="VIEW THE OPTIMIZATION RESULTS",layout=layout_button,style=dict(button_color='#ebebeb'))
        OPT_Button3.on_click(self.Opt_Result)

        OPT_Button4=widgets.Button(description="OPTIMIZED AIRCRAFT",tooltip="VIEW ALL THE OPTIMIZED AIRCRAFT DATA",layout=layout_button,style=dict(button_color='#ebebeb'))
        OPT_Button4.on_click(self.View_Opt_Ouput_Data)

        OPT_Button5=widgets.Button(description="SAVE THE AIRCRAFT DATA ",tooltip="SAVE THE DATA OF THE OPTIMIZED AIRCRFAT",layout=layout_button,style=dict(button_color='#ebebeb'))
        OPT_Button5.on_click(self.Save_OPT_F_UI)
        OPT_Button6=widgets.Button(description="AIRCRAFT ANALYSIS",tooltip="ANALYSE THE OPTIMIZED AIRCRAFT ",layout=layout_button,style=dict(button_color='#ebebeb'))
        OPT_Button6.on_click(self.Opt_Analysis)
        OPT_Button7=widgets.Button(description="CLOSE",tooltip="CLOSE THE OPTIMIZATION WINDOW",layout=layout_button,style=dict(button_color='#FF0800'))
        OPT_Button7.on_click(self.close_optimization )
        box1=widgets.HBox(children=[OPT_Button1,OPT_Button2],layout=layout_H)
        box2=widgets.HBox(children=[OPT_Button3,OPT_Button4],layout=layout_H)
        box3=widgets.HBox(children=[OPT_Button5,OPT_Button6],layout=layout_H)

        buttonHOME = widgets.Button(description='')
        buttonHOME.icon = 'fa-home'
        buttonHOME.layout.width = 'auto'
        buttonHOME.layout.height = 'auto'
        buttonHOME.on_click(self.HomeInterface)
        box5 = widgets.Box(children=[buttonHOME])
        #---------------------------------------------------------------------------------------------------------------
        buttonINFO = widgets.Button(description='')
        buttonINFO.icon = 'fa-info-circle'
        buttonINFO.layout.width = 'auto'
        buttonINFO.layout.height = 'auto'
        output = widgets.Output()
        def info_message(event):
            with output:
                output.clear_output()
                if len(output.outputs) > 0:
                    output.clear_output()
                else:
                    print('Follow the buttons order of activation.\n')

        buttonINFO.on_click(info_message)
        box4 = widgets.Box(children=[buttonINFO, output],layout=Layout(border='1px solid black',
                                         margin='50 0 50 0px', padding='5px', align_items='center', width='100'))
        #---------------------------------------------------------------------------------------------------------------
        self.OPT_BOX=widgets.VBox(children=[title,box1,box2,box3,OPT_Button7,box5,box4],layout=layout_box)
        display(self.OPT_BOX)




#  VIEW THE OPTIMIZATION PROBLEM
    def OPt_View(self,event):
        clear_output()
        display(self.OPT_BOX)
        configuration_name="oad_sizing.yml"
        path_configuration="data"
        self.configuration=pth.join(path_configuration,configuration_name)
        # INPUT FILE FOR THE OPTIMIZATION PROBLEM
        self.OAD.OPT_INPUTS(self.configuration,self.OPT_Source)

        # VIEW THE OPTIMIZATION DATA

        self.OAD.Optimization_View(self.configuration)
        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        layout_box=widgets.Layout( padding='10px', align_items='center', width='100%')
        OPTV_Button=widgets.Button(description="CLOSE",layout=layout_button,style=dict(button_color='#FF0800'))
        OPTV_Button.on_click(self.Close_Opt_View)
        OPTV_box=widgets.VBox(children=[OPTV_Button],layout=layout_box)
        display(OPTV_box)


    def Close_Opt_View(self,event):
        clear_output()
        display(self.OPT_BOX)


#  RUN THE OPTIMIZATION PROBLEM
    def Run_Opt_Problem(self,event):
        clear_output()
        display(self.OPT_BOX)
        print("OPTIMIZATION PROBLEM RUN WILL TAKE ABOUT 3 MIN ...")
        print("-------------------------------------------------------------------------------------------------------------------------------------------")
        self.OPT_problem=self.OAD.Run_Optimization_Problem(self.configuration)
        print("OPTIMIZATION PROBLEM RUN SUCCESSFULLY")

    def Opt_Result(self,event):

        self.OAD.View_Optimization_Result(self.configuration)

        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        layout_box=widgets.Layout( padding='10px', align_items='center', width='100%')
        OPTR_Button=widgets.Button(description="CLOSE",layout=layout_button,style=dict(button_color='#FF0800'))
        OPTR_Button.on_click(self.Close_Opt_View)
        OPTR_box=widgets.VBox(children=[OPTR_Button],layout=layout_box)
        display(OPTR_box)

    def View_Opt_Ouput_Data(self,event):
        clear_output()
        display(self.OPT_BOX)
        path="workdir"
        file=self.OPT_problem.output_file_path
        self.OPT_OUTPUT_FILE=self.OAD.Join_File(path,file)
        self.opt_output_data=self.OAD.View_outputs_data(self.OPT_OUTPUT_FILE)
        return self.opt_output_data



# SAVE THE OUTPUTS OF THE AIRCRAFT AND THE MISSION FILE
    def Save_OPT_F_UI(self,event):
        clear_output()
        display(self.OPT_BOX)
        layout=widgets.Layout(width="50%", height='40px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        layout_button=widgets.Layout(width='30%', height='50px', border='4px solid black')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')
        self.OPT_NAME=widgets.Text(placeholder='Type the files name',description=' FILE NAME:',value="",style=style,layout=layout,disabled=False)
        SOPT_Title=widgets.HTML(value=" <b> SAVING OUTPUT FILE </b>")
        SOPT_Button=widgets.Button(description="SAVE",tooltip="SAVE THE OUTPUTS",layout=layout_button,style=dict(button_color="#33ffcc"))
        SOPT_Button.on_click(self.Save_OPT_FILE)

        self.SOPT_box=widgets.VBox(children=[SOPT_Title,self.OPT_NAME,SOPT_Button],layout=layout_box)
        display(self.SOPT_box)


    def Save_OPT_FILE(self,event):
        opt_name=self.OPT_NAME.value
        path_out="OUTPUT_FILE"
        path_miss="MISSION_FILE"
        path_mission_ref="workdir\oad_sizing.csv"
        self.OAD.Save_File(self.OPT_problem.output_file_path,path_out,opt_name)
        self.OAD.Save_CSV_File(path_mission_ref,path_miss,opt_name)
        path_out = "Final python and .csm files\Base Files"
        self.OAD.Save_File(self.OPT_problem.output_file_path, path_out, opt_name)
        print(str(opt_name)+" OPTMIZATION OUTPUTS AND MISSION RESULTS SAVED ")
        print("-------------------------------------------")

# DISPLAY THE AIRCRAFT ANALYSIS USER INTERFACE TO ANALYZE THE OPTIMIZED AIRCRAFT
    def Opt_Analysis(self,event):

        clear_output()
        display(self.OPT_BOX)
        display(self.RES_box)

# FUNCTION: OPTIMIZATION PHASE TO THE PRINCIPAL MENUE
    def close_optimization (self,event):
        clear_output()
        self.Button_M5.style.button_color='#ebebeb'
        self.Button_M6.style.button_color='#ebebeb'
        image_path="Images/Wing.jpg"
        custom_css = f'''
        .vbox-with-background {{
            background-image: url("{image_path}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            width: 100%;
            height: 100%;
        }}
        '''
        display(HTML(f'<style>{custom_css}</style>'),self.menu)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # PARAMETRIC BRANCH # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def PARAMETRIC_UI1(self,event):
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')
        self.List_SFC=[]
        self.List_OWE=[]
        self.List_MTOW = []
        self.List_BF=[]
        self.List_SR=[]
        self.List_CD=[]
        self.List_finesse=[]

        path_to_target="OUTPUT_FILE"
        path_to_file_list = []
        temp=os.listdir(path_to_target)
        for i in range(0, len(temp)):
            if temp[i][-3:] =='xml':
                path_to_file_list.append(temp[i])

        title=widgets.HTML(value=" <b>INCREMENTAL DEVELOPEMENT </b>")
        self.AC=widgets.Select(options=path_to_file_list,description='AIRCRFAT SELECTION:',disabled=False,style={'description_width': 'initial'},layout=widgets.Layout(width="500px", height="150 px"),rows=len(path_to_file_list))
        Button=widgets.Button(description="SAVE",tooltip="SAVE THE SELECTED AIRCRAFT",layout=layout_button,style=dict(button_color="#33ffcc"))
        Button.on_click(self.PARAMETRIC_UI2)

        buttonHOME = widgets.Button(description='')
        buttonHOME.icon = 'fa-home'
        buttonHOME.layout.width = 'auto'
        buttonHOME.layout.height = 'auto'
        buttonHOME.on_click(self.HomeInterface)

        self.ID1_box=widgets.VBox(children=[title,self.AC,Button,buttonHOME],layout=layout_box)
        display(self.ID1_box)


    def PARAMETRIC_UI2(self,event):
        clear_output()
        self.ID_Type = []
        aircraft=self.AC.value
        path="OUTPUT_FILE"
        self.AC_ref=pth.join(path,aircraft)
        mission_name=os.path.splitext(os.path.split(aircraft)[1])[0]+".CSV"
        path_miss="MISSION_FILE"
        try:
            self.mission_ref=pth.join(path_miss,mission_name)
            SFC=self.OAD.para_sfc(self.mission_ref)
            self.List_SFC.append(SFC)
        except:
            print("------------NO MISSION FILE CORRESPONDING TO THE SELECTED AIRCRAFT-------------")

        self.OAD.PARA_AC_FILE(aircraft) #to copy selected ac to "IncrementalDevelopment_Aircraft_File.xml"



        print("THE REFERENCE ARICRAFT SAVED")
        print("-----------------------------------------------------------------------------------------------------")

        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        layout_H=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%')
        layout_H2 = widgets.Layout(border='4px solid black', padding='10px', justify_content='space-between',align_items='center', width='100%')
        layout_H3 = widgets.Layout(border='4px solid black', padding='10px', justify_content='space-around',align_items='center', width='100%')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')
        title1=widgets.HTML(value=" <b>INCREMENTAL DEVELOPMENT TYPE 1 </b>")
        title1_2 = widgets.HTML(value=" <b>INCREMENTAL DEVELOPMENT TYPE 1.5 </b>")
        title2 = widgets.HTML(value=" <b>STEP 2 INCREMENTAL DEVELOPMENT </b>")
        Button1=widgets.Button(description="WEIGHT SAVING",tooltip="MODIFY THE AIRCRAFT OWE",layout=layout_button,style=dict(button_color='#ebebeb'))
        Button1.on_click(self.Weight_Saving_UI)
        Button2=widgets.Button(description="SFC",tooltip="MODIFY THE AIRCRAFT Specific Fuel Consumption",layout=layout_button,style=dict(button_color='#ebebeb'))
        Button2.on_click(self.SFC_UI)
        Button3=widgets.Button(description="DRAG SAVING",tooltip="MODIFY THE AIRCRAFT DRAG",layout=layout_button,style=dict(button_color='#ebebeb'))
        Button3.on_click(self.Drag_Saving_UI)
        Button4=widgets.Button(description="MTOW INCREASE",tooltip="MODIFY THE AIRCRAFT MTOW",layout=layout_button,style=dict(button_color='#ebebeb'))
        Button4.on_click(self.MTOW_Increase_UI)

        Button5=widgets.Button(description="FUSELAGE SIMPLE STRETCH ",tooltip="MODIFY THE FUSELAGE GEOMETRY",layout=layout_button,style=dict(button_color='#ebebeb'))
        Button5.on_click(self.Fuselage_Stretch_UI)
        Button6=widgets.Button(description="NEO (no redesign)",tooltip="NEW ENGINE OPTION",layout=layout_button,style=dict(button_color='#ebebeb'))
        Button6.on_click(self.NEO_UI_1)

        Button7=widgets.Button(description="NEO (loop)",tooltip="NEW ENGINE OPTION",layout=layout_button,style=dict(button_color='#ebebeb'))
        Button7.on_click(self.NEO_UI_2)


        box_H=widgets.HBox(children=[Button1,Button2,Button3,Button4],layout=layout_H)
        box_H2 = widgets.HBox(children=[Button5, Button6], layout=layout_H2)
        box_H3 = widgets.HBox(children=[Button7], layout=layout_H2)


        Button1=widgets.Button(description="RUN - STEP 1 ",tooltip="Launch the ID analysis of level STEP 1",layout=layout_button,style=dict(button_color="#33ffcc"))
        Button1.on_click(self.INCREMENTAL_DEVELOPEMENT_STEP1)

        Button2=widgets.Button(description="RUN - STEP 2",tooltip="Launch the ID analysis of level STEP 2",layout=layout_button,style=dict(button_color="#33ffcc"))
        Button2.on_click(self.INCREMENTAL_DEVELOPEMENT_STEP2_OWE)



        box_H_Button_Run = widgets.HBox(children=[Button1, Button2], layout=layout_H3)
        # ---------------------------------------------------------------------------------------------------------------
        buttonHOME = widgets.Button(description='')
        buttonHOME.icon = 'fa-home'
        buttonHOME.layout.width = 'auto'
        buttonHOME.layout.height = 'auto'
        buttonHOME.on_click(self.HomeInterface)
        # ---------------------------------------------------------------------------------------------------------------
        self.var_owe = None
        self.var_mtow = None

        C_file1 = open("BlockImage/Parametric/STEP1.PNG", "rb")
        C_file2 = open("BlockImage/Parametric/STEP1_5.PNG", "rb")
        C_file3 = open("BlockImage/Parametric/STEP2.PNG", "rb")
        C_image1 = C_file1.read()
        C_image2 = C_file2.read()
        C_image3 = C_file3.read()
        C_img1 = widgets.Image(value=C_image1, format="PNG", width="100%", height="100%")
        C_img2 = widgets.Image(value=C_image2, format="PNG", width="100%", height="100%")
        C_img3 = widgets.Image(value=C_image3, format="PNG", width="100%", height="100%")


        # GEOMETRY MODULES BY COMPUTED BLOCKS
        accordion1 = widgets.Accordion(children=[C_img1], selected_index=None)
        accordion2 = widgets.Accordion(children=[C_img2], selected_index=None)
        accordion3 = widgets.Accordion(children=[C_img3], selected_index=None)
        accordion1.set_title(0, 'STEP 1')
        accordion2.set_title(0, 'STEP 1.5')
        accordion3.set_title(0, 'STEP 2')
        accordion_box = widgets.HBox(children=[accordion1,accordion2,accordion3], layout=widgets.Layout(width='100%'))
        self.ID2_box=widgets.VBox(children=[accordion_box,title1,box_H,title1_2,box_H2,box_H_Button_Run,buttonHOME],layout=layout_box)
        display(self.ID2_box)


    def Weight_Saving_UI(self,event):
        path="OUTPUT_FILE"
        file_name="IncrementalDevelopment_Aircraft_File.xml"
        para_path=pth.join(path,file_name)
        self.Para_Data1=self.OAD.Input_File(para_path)
        self.OWE_REF=self.Para_Data1["data:weight:aircraft:OWE"].value[0]
        self.List_OWE.append(self.OWE_REF)

        self.MTOW=self.Para_Data1["data:weight:aircraft:MTOW"].value[0]
        self.Max_Payload=self.Para_Data1["data:weight:aircraft:max_payload"].value[0]
        self.BF_REF=self.MTOW-(self.OWE_REF+self.Max_Payload)
        self.List_BF.append(self.BF_REF)

        clear_output()
        display(self.ID2_box)
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        layout_H=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')
        layout=widgets.Layout(width="50%", height='50px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        title=widgets.HTML(value=" <b>WEIGHT SAVING </b>")
        self.OWES_1=widgets.BoundedFloatText(min=0,max=1000000,step=0.001,value=self.OWE_REF,disabled=True,description="OWE (Kg) ",description_tooltip="OWE OF THE REFERENCE AICRAFT",style=style,layout=layout)
        self.OWES_2=widgets.BoundedFloatText(min=-100000,max=0,step=0.001,value=0,disabled=False,description=" ∆(OWE)",description_tooltip="THE DELTA OWE SAVING",style=style,layout=layout)
        self.OWES_2.observe(self.delta_OWE_percent,names="value")

        self.OWES_3=widgets.BoundedFloatText(min=-100,max=0,step=0.001,value=0,disabled=False,description="%∆(OWE)",description_tooltip="THE % OF DELTA OWE SAVING",style=style,layout=layout)
        self.OWES_3.observe(self.percent_OWE_delta,names="value")

        Button=widgets.Button(description="SAVE",tooltip="SAVE THE OWE MODIFICATIONS",layout=layout_button,style=dict(button_color="#33ffcc"))
        Button.on_click(self.Weight_Saving)
        self.OWES_box=widgets.VBox(children=[title,self.OWES_1,self.OWES_2,self.OWES_3,Button],layout=layout_box)

        display(self.OWES_box)


    def delta_OWE_percent(self,change):
        delta=self.OWES_2.value
        percent=(delta/self.OWES_1.value)*100
        self.OWES_3.value=percent

    def percent_OWE_delta(self,change):
        percent=self.OWES_3.value
        delta=(percent*self.OWES_1.value)/100
        self.OWES_2.value=delta

    def Weight_Saving(self,event):
        self.ID_Type= self.ID_Type + ["Weight Saving"]
        delta_OWE=self.OWES_2.value
        OWE_New=self.OWE_REF+delta_OWE
        self.var_owe = OWE_New-self.OWE_REF
        self.Para_Data1["data:weight:aircraft:OWE"].value=OWE_New
        self.Para_Data1.save()
        clear_output()
        print("---------------------------------------------------OWE MODIFCATION SAVED-------------------------------------")
        display( self.ID2_box)


    def SFC_UI(self,event):
        clear_output()
        display(self.ID2_box)

        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        layout_H=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')
        layout=widgets.Layout(width="50%", height='50px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        title=widgets.HTML(value=" <b>MODIFY SFC </b>")
        self.SFC_1=widgets.BoundedFloatText(min=0,max=100,step=0.001,value=self.List_SFC[0],disabled=True,description="ENGINE SFC (kg/N/s)",description_tooltip="THE SFC OF THE AIRCRAFT ENGINE",style=style,layout=layout)
        self.SFC_2=widgets.BoundedFloatText(min=-100,max=100,step=0.001,value=0,disabled=False,description=" ∆(SFC)",description_tooltip="THE DELTA SFC",style=style,layout=layout)
        self.SFC_2.observe(self.delta_SFC_percent,names="value")
        self.SFC_3=widgets.BoundedFloatText(min=-100,max=100,step=0.001,value=0,disabled=False,description="%∆(SFC)",description_tooltip="THE % OF DELTA SFC",style=style,layout=layout)
        self.SFC_3.observe(self.percent_SFC_delta,names="value")
        Button=widgets.Button(description="SAVE",tooltip="SAVE THE SFC MODIFICATION",layout=layout_button,style=dict(button_color="#33ffcc"))
        Button.on_click(self.SFC)
        self.SFC_box=widgets.VBox(children=[title,self.SFC_1,self.SFC_2,self.SFC_3,Button],layout=layout_box)
        display(self.SFC_box)


    def delta_SFC_percent(self,change):
        delta=self.SFC_2.value
        percent=(delta/self.SFC_1.value)*100
        self.SFC_3.value=percent

    def percent_SFC_delta(self,change):
        percent=self.SFC_3.value
        delta=(percent*self.SFC_1.value)/100
        self.SFC_2.value=delta
    def SFC(self,event):
        self.ID_Type = self.ID_Type + ["SFC"]
        SFC_NEW=self.List_SFC[0]+self.SFC_2.value
        self.List_SFC.append(SFC_NEW)
        clear_output()
        print("--------------------SFC MODIFICATIONS SAVED---------------------")
        display( self.ID2_box)





    def NEO_UI_1(self,event):
        clear_output()
        display(self.ID2_box)

        path="OUTPUT_FILE"
        file_name="IncrementalDevelopment_Aircraft_File.xml"
        para_path=pth.join(path,file_name)
        self.Para_DataNEO=self.OAD.Input_File(para_path)
        self.EngineMass=self.Para_DataNEO["data:weight:propulsion:engine:mass"].value[0]
        self.NacelleWetArea = self.Para_DataNEO["data:geometry:propulsion:nacelle:wetted_area"].value[0]
        self.OWE_REF = self.Para_DataNEO["data:weight:aircraft:OWE"].value[0]
        #self.NacelleDiameter = self.Para_DataNEO["data:propulsion:MTO_thrust"].value[0]



        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        layout_H=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')
        layout=widgets.Layout(width="100%", height='50px',justify_content='space-around')
        style=style={'description_width': 'initial'}

        title = widgets.HTML(value=" <b>MODIFY NEO </b>")

        self.NEO_1 = widgets.BoundedFloatText(min=0, max=1000000, step=0.001, value=round(self.List_SFC[0],10),disabled=True,description="Engine SFC (kg/N/s)",description_tooltip="THE SFC OF THE AIRCRAFT ENGINE",style=style,layout=layout)
        self.NEO_2 = widgets.BoundedFloatText(min=0, max=1000000, step=1, value=round(self.EngineMass,5),disabled=True,description="Engine Mass [kg]",description_tooltip="Engine mass",style=style,layout=layout)
        self.NEO_3 = widgets.BoundedFloatText(min=0, max=1000000, step=1, value=round(self.NacelleWetArea,5),disabled=True,description="Nacelle Wetted Area[m^2]",description_tooltip="Engine nacelle diameter",style=style,layout=layout)

        self.NEO_11 = widgets.BoundedFloatText(min=0, max=1000000, step=0.001, value=0,disabled=True,description="NEW Engine SFC (kg/N/s)",description_tooltip="The NEW SFC of the aircraft",style=style,layout=layout)
        self.NEO_22 = widgets.BoundedFloatText(min=0, max=1000000, step=1, value=0,disabled=True,description="NEW Engine Mass [kg]",description_tooltip="New Engine mass",style=style,layout=layout)
        self.NEO_33 = widgets.BoundedFloatText(min=0, max=1000000, step=1, value=0,disabled=True,description="NEW Nacelle Wetted Area[m^2]",description_tooltip="New Engine nacelle diameter",style=style,layout=layout)

        self.NEO_1a = widgets.BoundedFloatText(min=-10000, max=100000, step=1,value=0,disabled=True,description="∆(SFC)",description_tooltip="Delta SFC",style=style,layout=layout)
        self.NEO_1b = widgets.BoundedFloatText(min=-10000, max=100000, step=1, value=0, disabled=False, description="∆%(SFC)",description_tooltip="% SFC", style=style, layout=layout)

        self.NEO_2a = widgets.BoundedFloatText(min=-100000,max=100000,step=1,value=0,disabled=True,description="∆(Engine Mass)",description_tooltip="Delta Engine Mass",style=style,layout=layout)
        self.NEO_2b = widgets.BoundedFloatText(min=-100000, max=100000, step=1, value=0, disabled=False, description="∆%(Engine Mass)",description_tooltip="% Engine Mass", style=style, layout=layout)

        self.NEO_3a = widgets.BoundedFloatText(min=-10000,max=100000,step=1,value=0,disabled=True,description="∆(Wetted Area)",description_tooltip="Delta Nacelle Wetted Area",style=style,layout=layout)
        self.NEO_3b = widgets.BoundedFloatText(min=-10000, max=100000, step=1, value=0, disabled=False, description="∆%(Wetted Area)",description_tooltip="% Nacelle Wetted Area", style=style, layout=layout)



        Button = widgets.Button(description="SAVE",tooltip="SAVE THE NEO MODIFICATION",layout=layout_button,style=dict(button_color="#33ffcc"))
        Button.on_click(self.NEO_save_1)
        Button_variation = widgets.Button(description="Update",tooltip="Update values",layout=layout_button)
        Button_variation.on_click(self.percent_NEO_S1_delta)

        self.NEO_V1 = widgets.VBox(children=[self.NEO_1, self.NEO_1b,self.NEO_11,self.NEO_1a], layout=widgets.Layout(border='5px solid black', padding='10px', align_items='center', width='100%',justify_content='space-around'))
        self.NEO_V2 = widgets.VBox(children=[self.NEO_2, self.NEO_2b,self.NEO_22,self.NEO_2a], layout=widgets.Layout(border='5px solid black', padding='10px', align_items='center', width='100%',justify_content='space-around'))
        self.NEO_V3 = widgets.VBox(children=[self.NEO_3, self.NEO_3b,self.NEO_33,self.NEO_3a], layout=widgets.Layout(border='5px solid black', padding='10px', align_items='center', width='100%',justify_content='space-around'))
        self.NEO_Horizontal = widgets.HBox(children=[self.NEO_V1, self.NEO_V2,self.NEO_V3], layout=widgets.Layout(border='0px solid black', padding='0px', width='100%',justify_content='space-around'))
        self.NEO_box = widgets.VBox(children=[title,self.NEO_Horizontal,Button_variation,Button], layout=widgets.Layout(border='5px solid black', padding='10px', align_items='center', width='100%',justify_content='space-around'))
        display(self.NEO_box)



    def percent_NEO_S1_delta(self,event):
        percent_area = self.NEO_3b.value
        percent_mass = self.NEO_2b.value
        percent_sfc  = self.NEO_1b.value

        delta_area = (percent_area * self.NEO_3.value)/100
        delta_mass = (percent_mass * self.NEO_2.value) / 100
        delta_sfc = (percent_sfc * self.NEO_1.value) / 100


        self.NEO_3a.value= round(delta_area, 3)
        self.NEO_2a.value = round(delta_mass, 3)
        self.NEO_1a.value = round(delta_sfc, 10)


        self.NEO_33.value = self.NEO_3.value + delta_area
        self.NEO_22.value = self.NEO_2.value + delta_mass
        self.NEO_11.value = self.NEO_1.value + delta_sfc



    def NEO_save_1(self,event):
        # from fastoad_cs25.models.aerodynamics.components.compute_polar import ComputePolar
        from fastoad_cs25.models.aerodynamics.components.cd0_nacelles_pylons import Cd0NacellesAndPylons
        from fastoad_cs25.models.aerodynamics.components.cd0_total import Cd0Total
        #Here we add new SFC, NEW ENGINE MASS, NEW ENGINE NACELLE
        #self.Para_DataNEO["data:propulsion:MTO_thrust"].value = self.NEO_33.value
        self.ID_Type = self.ID_Type + ["NEO"]
        NEO_NEW=self.NEO_11.value # +self.List_SFC[0]
        self.List_SFC.append(NEO_NEW)
        self.Para_DataNEO["data:weight:propulsion:engine:mass"].value = self.NEO_22.value
        self.Para_DataNEO["data:geometry:propulsion:nacelle:wetted_area"].value = self.NEO_33.value

        #Here we change the value of the OWE because of the change of the engine weight
        New_OWE = self.OWE_REF - self.EngineMass + self.NEO_22.value
        self.Para_DataNEO["data:weight:aircraft:OWE"].value = New_OWE
        self.var_owe = New_OWE - self.OWE_REF
        #Here we SAVE direct variation
        self.Para_DataNEO.save()

        inputs = {}
        inputs["data:geometry:propulsion:engine:count"]  = self.Para_DataNEO["data:geometry:propulsion:engine:count"].value[0]
        inputs["data:geometry:wing:area"] = self.Para_DataNEO["data:geometry:wing:area"].value[0]
        inputs["data:aerodynamics:aircraft:takeoff:mach"] = self.Para_DataNEO["data:aerodynamics:aircraft:takeoff:mach"].value[0]
        inputs["data:aerodynamics:wing:low_speed:reynolds"] = self.Para_DataNEO["data:aerodynamics:wing:low_speed:reynolds"].value[0]
        inputs["data:TLAR:cruise_mach"] = self.Para_DataNEO["data:TLAR:cruise_mach"].value[0]
        inputs["data:aerodynamics:wing:cruise:reynolds"] = self.Para_DataNEO["data:aerodynamics:wing:cruise:reynolds"].value[0]
        inputs["data:TLAR:cruise_mach"] = self.Para_DataNEO["data:TLAR:cruise_mach"].value[0]
        inputs["data:aerodynamics:wing:cruise:reynolds"] = self.Para_DataNEO["data:aerodynamics:wing:cruise:reynolds"].value[0]
        inputs["data:geometry:propulsion:nacelle:length"] = self.Para_DataNEO["data:geometry:propulsion:nacelle:length"].value[0]
        inputs["data:geometry:propulsion:nacelle:wetted_area"] = self.Para_DataNEO["data:geometry:propulsion:nacelle:wetted_area"].value
        inputs["data:geometry:propulsion:fan:length"] = self.Para_DataNEO["data:geometry:propulsion:fan:length"].value[0]
        inputs["data:geometry:propulsion:pylon:length"] = self.Para_DataNEO["data:geometry:propulsion:pylon:length"].value[0]
        inputs["data:geometry:propulsion:pylon:wetted_area"] = self.Para_DataNEO["data:geometry:propulsion:pylon:wetted_area"].value[0]
        inputs["data:geometry:aircraft:wetted_area"] = self.Para_DataNEO["data:geometry:aircraft:wetted_area"].value[0]
        inputs["data:aerodynamics:wing:low_speed:CD0"] = self.Para_DataNEO["data:aerodynamics:wing:low_speed:CD0"].value[:]
        inputs["data:aerodynamics:wing:cruise:CD0"] = numpy.array(self.Para_DataNEO["data:aerodynamics:wing:cruise:CD0"].value[:])
        inputs["data:aerodynamics:fuselage:cruise:CD0"] = numpy.array(self.Para_DataNEO["data:aerodynamics:fuselage:cruise:CD0"].value[:])
        inputs["data:aerodynamics:horizontal_tail:cruise:CD0"] = self.Para_DataNEO["data:aerodynamics:horizontal_tail:cruise:CD0"].value[:]
        inputs["data:aerodynamics:vertical_tail:cruise:CD0"] = self.Para_DataNEO["data:aerodynamics:vertical_tail:cruise:CD0"].value[:]
        inputs["data:aerodynamics:nacelles:cruise:CD0"] = self.Para_DataNEO["data:aerodynamics:nacelles:cruise:CD0"].value[:]
        inputs["data:aerodynamics:pylons:cruise:CD0"] = self.Para_DataNEO["data:aerodynamics:pylons:cruise:CD0"].value[:]

        inputs["tuning:aerodynamics:aircraft:cruise:CD:k"] = self.Para_DataNEO["tuning:aerodynamics:aircraft:cruise:CD:k"].value[0]
        inputs["tuning:aerodynamics:aircraft:cruise:CD:offset"] = self.Para_DataNEO["tuning:aerodynamics:aircraft:cruise:CD:offset"].value[0]
        inputs["tuning:aerodynamics:aircraft:cruise:CD:winglet_effect:k"] = self.Para_DataNEO["tuning:aerodynamics:aircraft:cruise:CD:winglet_effect:k"].value[0]
        inputs["tuning:aerodynamics:aircraft:cruise:CD:winglet_effect:offset"] = self.Para_DataNEO["tuning:aerodynamics:aircraft:cruise:CD:winglet_effect:offset"].value[0]
        inputs["data:aerodynamics:aircraft:low_speed:CL"] = self.Para_DataNEO["data:aerodynamics:aircraft:low_speed:CL"].value[:]
        inputs["data:aerodynamics:aircraft:low_speed:CD0"] = self.Para_DataNEO["data:aerodynamics:aircraft:low_speed:CD0"].value[:]
        inputs["data:aerodynamics:aircraft:low_speed:CD:trim"] = self.Para_DataNEO["data:aerodynamics:aircraft:low_speed:CD:trim"].value[:]
        inputs["data:aerodynamics:aircraft:low_speed:induced_drag_coefficient"] = self.Para_DataNEO["data:aerodynamics:aircraft:low_speed:induced_drag_coefficient"].value[0]
        inputs["data:aerodynamics:high_lift_devices:takeoff:CL"] = self.Para_DataNEO["data:aerodynamics:high_lift_devices:takeoff:CL"].value[0]
        inputs["data:aerodynamics:high_lift_devices:takeoff:CD"] = self.Para_DataNEO["data:aerodynamics:high_lift_devices:takeoff:CD"].value[0]
        inputs["data:aerodynamics:high_lift_devices:landing:CL"] = self.Para_DataNEO["data:aerodynamics:high_lift_devices:landing:CL"].value[0]
        inputs["data:aerodynamics:high_lift_devices:landing:CD"] = self.Para_DataNEO["data:aerodynamics:high_lift_devices:landing:CD"].value[0]
        inputs["data:aerodynamics:aircraft:cruise:CL"] = self.Para_DataNEO["data:aerodynamics:aircraft:cruise:CL"].value[:]
        inputs["data:aerodynamics:aircraft:cruise:CD0"] = self.Para_DataNEO["data:aerodynamics:aircraft:cruise:CD0"].value[:]
        inputs["data:aerodynamics:aircraft:cruise:CD:trim"] = self.Para_DataNEO["data:aerodynamics:aircraft:cruise:CD:trim"].value[:]
        inputs["data:aerodynamics:aircraft:cruise:CD:compressibility"] = self.Para_DataNEO["data:aerodynamics:aircraft:cruise:CD:compressibility"].value[:]
        inputs["data:aerodynamics:aircraft:cruise:induced_drag_coefficient"] = self.Para_DataNEO["data:aerodynamics:aircraft:cruise:induced_drag_coefficient"].value[0]

        #Here we start calculating other variation because of the change of Wetted Area
        outputs= {}
        compute_cd0_nacelle = Cd0NacellesAndPylons()
        compute_cd0_nacelle.compute(inputs,outputs)
        inputs.update(outputs)

        compute_cd0_total = Cd0Total()
        compute_cd0_total.compute(inputs,outputs)
        inputs.update(outputs)

        k_cd = inputs["tuning:aerodynamics:aircraft:cruise:CD:k"]
        offset_cd = inputs["tuning:aerodynamics:aircraft:cruise:CD:offset"]
        k_winglet_cd = inputs["tuning:aerodynamics:aircraft:cruise:CD:winglet_effect:k"]
        offset_winglet_cd = inputs["tuning:aerodynamics:aircraft:cruise:CD:winglet_effect:offset"]
        cl = self.Para_DataNEO["data:aerodynamics:aircraft:cruise:CL"].value[:]#inputs["data:aerodynamics:aircraft:cruise:CL"]
        cd0 = inputs["data:aerodynamics:aircraft:cruise:CD0"]

        cd_trim = inputs["data:aerodynamics:aircraft:cruise:CD:trim"]

        cd_c = inputs["data:aerodynamics:aircraft:cruise:CD:compressibility"]

        coef_k = inputs["data:aerodynamics:aircraft:cruise:induced_drag_coefficient"]
        delta_cl_hl = 0.0
        delta_cd_hl = 0.0

        cl = numpy.array(cl)
        cd0 = numpy.array(cd0)
        cd_trim = numpy.array(cd_trim)
        cd_c = numpy.array(cd_c)
        cl = cl + delta_cl_hl
        cd = (cd0 + cd_c + cd_trim + coef_k * cl ** 2 * k_winglet_cd + offset_winglet_cd + delta_cd_hl) * k_cd + offset_cd

        lift_drag_ratio = cl / cd

        optimum_index = numpy.argmax(lift_drag_ratio)
        optimum_Cz = cl[optimum_index]
        optimum_Cd = cd[optimum_index]
        outputs["data:aerodynamics:aircraft:cruise:L_D_max"] = optimum_Cz / optimum_Cd

        self.Para_DataNEO["data:aerodynamics:aircraft:cruise:L_D_max"].value = optimum_Cz / optimum_Cd
        self.Para_DataNEO["data:aerodynamics:aircraft:cruise:CD"].value = cd
        self.Para_DataNEO["data:aerodynamics:aircraft:cruise:CD0"].value = cd0
        self.Para_DataNEO["data:aerodynamics:aircraft:cruise:CD:trim"].value = cd_trim
        self.Para_DataNEO["data:aerodynamics:aircraft:cruise:CD:compressibility"].value = cd_c

        if self.Para_DataNEO["data:geometry:propulsion:nacelle:wetted_area"].value != self.NEO_3.value:
            self.Para_DataNEO.save()

        clear_output()
        display( self.ID2_box)
        print("--------------------NEW ENGINE MODIFICATIONS SAVED---------------------")




    def NEO_UI_2(self,event):
        clear_output()
        display(self.ID2_box)

        path="OUTPUT_FILE"
        file_name="IncrementalDevelopment_Aircraft_File.xml"
        para_path=pth.join(path,file_name)
        self.Para_DataNEO_S2=self.OAD.Input_File(para_path)

        self.MTO_Thrust = self.Para_DataNEO_S2["data:propulsion:MTO_thrust"].value[0]
        self.nacelle_wetted_area = self.Para_DataNEO_S2["data:geometry:propulsion:nacelle:wetted_area"].value[0]
        self.nacelle_diameter = self.Para_DataNEO_S2["data:geometry:propulsion:nacelle:diameter"].value[0]
        self.nacelle_length = self.Para_DataNEO_S2["data:geometry:propulsion:nacelle:length"].value[0]
        self.engine_mass = self.Para_DataNEO_S2["data:weight:propulsion:engine:mass"].value[0]



        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        layout_H=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')
        layout=widgets.Layout(width="100%", height='50px',justify_content='space-around')
        style=style={'description_width': 'initial'}

        title = widgets.HTML(value=" <b>MODIFY NEO </b>")
        title2 = widgets.HTML(value=" <b>-OLD ENGINE OPTION- </b>", layout=widgets.Layout(border='0px solid black', padding='5px', align_items='center', width='100%',justify_content='space-around'))
        title3 = widgets.HTML(value=" <b>-NEW ENGINE OPTION- </b>", layout=widgets.Layout(border='0px solid black', padding='5px', align_items='center', width='100%',justify_content='space-around'))

        self.NEO_S2_1 = widgets.BoundedFloatText(min=0, max=1000000, step=0.001, value=round(self.MTO_Thrust,5),disabled=True,description="Engine Thrust (N)",description_tooltip="Thrust of one engine",style=style,layout=layout)

        self.NEO_S2_2 = widgets.BoundedFloatText(min=0, max=1000000, step=1, value=round(self.nacelle_wetted_area,3),disabled=True,description="Nacelle Wetted Area[m^2]",description_tooltip="Engine nacelle wetted area",style=style,layout=layout)
        self.NEO_S2_3 = widgets.BoundedFloatText(min=0, max=1000000, step=1, value=round(self.nacelle_diameter, 3),disabled=True, description="Nacelle Diameter[m]",description_tooltip="Engine nacelle diameter", style=style,layout=layout)
        self.NEO_S2_4 = widgets.BoundedFloatText(min=0, max=1000000, step=1, value=round(self.nacelle_length, 3),disabled=True, description="Nacelle Length[m]",description_tooltip="Engine nacelle length", style=style,layout=layout)
        self.NEO_S2_5 = widgets.BoundedFloatText(min=0, max=1000000, step=1, value=round(self.engine_mass, 3),disabled=True, description="Engines Mass [kg]",description_tooltip="Engines mass (two engines)", style=style, layout=layout)

        self.NEO_S2_2_new = widgets.BoundedFloatText(min=0, max=1000000, step=1, value=0,disabled=True, description="Nacelle Wetted Area[m^2]",description_tooltip="Engine nacelle wetted area", style=style,layout=layout)
        self.NEO_S2_3_new = widgets.BoundedFloatText(min=0, max=1000000, step=1, value=0,disabled=True, description="Nacelle Diameter[m]",description_tooltip="Engine nacelle diameter", style=style,layout=layout)
        self.NEO_S2_4_new = widgets.BoundedFloatText(min=0, max=1000000, step=1, value=0,disabled=True, description="Nacelle Length[m]",description_tooltip="Engine nacelle length", style=style,layout=layout)
        self.NEO_S2_5_new = widgets.BoundedFloatText(min=0, max=1000000, step=1, value=0,disabled=True, description="Engines Mass [kg]",description_tooltip="Engines mass (two engines)", style=style,layout=layout)

        self.NEO_S2_2_new.observe(self.delta_NEO_S2_percent, names="value")
        self.NEO_S2_3_new.observe(self.delta_NEO_S2_percent, names="value")
        self.NEO_S2_4_new.observe(self.delta_NEO_S2_percent, names="value")
        self.NEO_S2_5_new.observe(self.delta_NEO_S2_percent, names="value")

        self.NEO_S2_2_new.observe(self.percent_NEO_S2_delta, names="value")
        self.NEO_S2_3_new.observe(self.percent_NEO_S2_delta, names="value")
        self.NEO_S2_4_new.observe(self.percent_NEO_S2_delta, names="value")
        self.NEO_S2_5_new.observe(self.percent_NEO_S2_delta, names="value")


        self.NEO_S2_1a = widgets.BoundedFloatText(min=-1000000, max=1000000, step=1,value=0,disabled=False,description="∆(MTO_THRUST)",description_tooltip="Delta MTO_THRUST",style=style,layout=layout)
        self.NEO_S2_1a.observe(self.delta_NEO_S2_percent, names="value")
        self.NEO_S2_1b = widgets.BoundedFloatText(min=-1000000, max=1000000, step=1, value=0, disabled=False, description="∆%(MTO_THRUST)",description_tooltip="% MTO_THRUST", style=style, layout=layout)
        self.NEO_S2_1b.observe(self.percent_NEO_S2_delta, names="value")


        Button = widgets.Button(description="SAVE",tooltip="SAVE THE NEO MODIFICATION",layout=layout_button,style=dict(button_color="#33ffcc"))
        Button.on_click(self.NEO_save_2)
        #Button_Variation = widgets.Button(description="Show Variation",tooltip="Show the delta and percent variations",layout=layout_button)
        #Button_Variation.on_click(variation_NEO)
        self.NEO_S2_H1 = widgets.HBox(children=[title2,title3], layout=widgets.Layout(border='5px solid black',width='100%',justify_content='center'))
        self.NEO_S2_H2 = widgets.HBox(children=[self.NEO_S2_1,self.NEO_S2_1a,self.NEO_S2_1b], layout=widgets.Layout(border='5px solid black', padding='10px', align_items='center', width='100%',justify_content='space-around'))
        self.NEO_S2_V1 = widgets.VBox(children=[self.NEO_S2_2,self.NEO_S2_3,self.NEO_S2_4, self.NEO_S2_5], layout=widgets.Layout(border='5px solid black', padding='10px', align_items='center', width='100%',justify_content='space-around'))
        self.NEO_S2_V2 = widgets.VBox(children=[self.NEO_S2_2_new,self.NEO_S2_3_new,self.NEO_S2_4_new, self.NEO_S2_5_new], layout=widgets.Layout(border='5px solid black', padding='10px', align_items='center', width='100%',justify_content='space-around'))
        self.NEO_S2_Horizontal = widgets.HBox(children=[self.NEO_S2_V1,self.NEO_S2_V2], layout=widgets.Layout(border='0px solid black', padding='0px', width='100%',justify_content='space-around'))
        self.NEO_S2_box = widgets.VBox(children=[title,self.NEO_S2_H2,self.NEO_S2_H1,self.NEO_S2_Horizontal,Button], layout=widgets.Layout(border='5px solid black', padding='10px', align_items='center', width='100%',justify_content='space-around'))
        display(self.NEO_S2_box)


    def delta_NEO_S2_percent(self,change):
        delta=self.NEO_S2_1a.value
        percent=(delta/self.NEO_S2_1.value)*100
        self.NEO_S2_1b.value=round(percent,3)

        #Computed with formulation retrieved from FAST-OAD_CS25 geometry module and weight module (not propulsion)
        New_MTO_Thrust = self.NEO_S2_1.value + delta
        #Relations Extracted from FASTOAD-CS25 geometry components
        NacelleWettedArea = (0.0004 * New_MTO_Thrust * 0.225) + 11
        NacelleDiameter = 0.00904 * numpy.sqrt(New_MTO_Thrust * 0.225) + 0.7
        NacelleLength = 0.032 * numpy.sqrt(New_MTO_Thrust * 0.225)

        n_engines = self.Para_DataNEO_S2["data:geometry:propulsion:engine:count"].value[0]
        k_b1 = self.Para_DataNEO_S2["tuning:weight:propulsion:engine:mass:k"].value[0]
        offset_b1 = self.Para_DataNEO_S2["tuning:weight:propulsion:engine:mass:offset"].value[0]
        temp_b1 = 22.2e-3 * New_MTO_Thrust
        temp_b1 *= n_engines * 1.55
        EngineMass= k_b1 * temp_b1 + offset_b1

        self.NEO_S2_2_new.value = round(NacelleWettedArea, 3)
        self.NEO_S2_3_new.value = round(NacelleDiameter, 3)
        self.NEO_S2_4_new.value = round(NacelleLength, 3)
        self.NEO_S2_5_new.value = round(EngineMass, 3)

    def percent_NEO_S2_delta(self,change):
        percent=self.NEO_S2_1b.value
        delta=(percent*self.NEO_S2_1.value)/100
        self.NEO_S2_1a.value=round(delta,3)

        # Computed with formulation retrieved from FAST-OAD_CS25 geometry module and weight module (not propulsion)
        New_MTO_Thrust = self.NEO_S2_1.value + delta
        # Relations Extracted from FASTOAD-CS25 geometry components
        NacelleWettedArea = (0.0004 * New_MTO_Thrust * 0.225) + 11
        NacelleDiameter = 0.00904 * numpy.sqrt(New_MTO_Thrust * 0.225) + 0.7
        NacelleLength = 0.032 * numpy.sqrt(New_MTO_Thrust * 0.225)

        n_engines = self.Para_DataNEO_S2["data:geometry:propulsion:engine:count"].value[0]
        k_b1 = self.Para_DataNEO_S2["tuning:weight:propulsion:engine:mass:k"].value[0]
        offset_b1 = self.Para_DataNEO_S2["tuning:weight:propulsion:engine:mass:offset"].value[0]
        temp_b1 = 22.2e-3 * New_MTO_Thrust
        temp_b1 *= n_engines * 1.55
        EngineMass = k_b1 * temp_b1 + offset_b1

        self.NEO_S2_2_new.value = round(NacelleWettedArea,3)
        self.NEO_S2_3_new.value = round(NacelleDiameter,3)
        self.NEO_S2_4_new.value = round(NacelleLength,3)
        self.NEO_S2_5_new.value = round(EngineMass,3)


    def NEO_save_2(self,event):
        #Here we add new SFC, NEW ENGINE MASS, NEW ENGINE NACELLE
        self.Para_DataNEO_S2["data:propulsion:MTO_thrust"].value = self.NEO_S2_1.value + self.NEO_S2_1a.value
        self.ID_Type = self.ID_Type + ["NEO Step 2"]


        #Here we SAVE direct variation
        self.Para_DataNEO_S2.save()


        clear_output()
        display( self.ID2_box)
        print("--------------------NEW ENGINE MODIFICATIONS SAVED---------------------")



    def Drag_Saving_UI(self,event):
        path="OUTPUT_FILE"
        file_name="IncrementalDevelopment_Aircraft_File.xml"
        para_path=pth.join(path,file_name)
        self.Para_Data2=self.OAD.Input_File(para_path)
        self.CD=self.Para_Data2["data:aerodynamics:aircraft:cruise:CD"].value
        finesse=self.Para_Data2["data:aerodynamics:aircraft:cruise:L_D_max"].value[0]

        clear_output()
        display(self.ID2_box)

        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        layout_H=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%',justify_content='space-between')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')
        layout=widgets.Layout(width="50%", height='50px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        layout_H=widgets.Layout( padding='10px', align_items='center', width='100%',justify_content='space-between')
        layout_V=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%')
        title=widgets.HTML(value=" <b>DRAG SAVING </b>")

        self.DRAG_1=widgets.BoundedFloatText(min=0,max=60,step=0.001,value=round(finesse,2),disabled=True,description="(L/D)_max",description_tooltip="max lift/drag ratio in cruise conditions",style=style,layout=layout)



        box1=widgets.VBox(children=[self.DRAG_1],layout=layout_V)



        self.DRAG_2=widgets.BoundedFloatText(min=-100,max=100,step=0.001,value=0,disabled=False,description=" %∆(CD)",description_tooltip="%∆ (drag coefficient in cruise conditions)", style=style,layout=layout)
        self.DRAG_2.observe(self.percent_drag_finesse,names="value")

        self.DRAG_3=widgets.BoundedFloatText(min=-20,max=20,step=0.001,value=0,disabled=True,description="∆(L/D)_max",description_tooltip="∆ (max lift/drag ratio in cruise conditions)",style=style,layout=layout)
        self.DRAG_4=widgets.BoundedFloatText(min=-100,max=100,step=0.001,value=0,disabled=True,description="%∆(L/D)_max",description_tooltip="%∆ (max lift/drag ratio in cruise conditions)",style=style,layout=layout)


        box2=widgets.VBox(children=[self.DRAG_2],layout=layout_V)
        box3=widgets.HBox(children=[self.DRAG_3,self.DRAG_4],layout=layout_H)
        box4=widgets.VBox(children=[box3],layout=layout_V)
        Button=widgets.Button(description="SAVE",tooltip="SAVE THE DRAG MODIFICATION",layout=layout_button,style=dict(button_color="#33ffcc"))
        Button.on_click(self.Drag_Saving)
        self.CD_box=widgets.VBox(children=[title,box1,box2,box4,Button],layout=layout_box)
        display(self.CD_box)




    def percent_drag_finesse(self,change):
        delta_percent=self.DRAG_2.value
        new_percent=100+delta_percent
        new_finesse=(100*self.DRAG_1.value)/new_percent

        delta_finesse= new_finesse-self.DRAG_1.value
        delta_percent_finesse=(delta_finesse*100)/self.DRAG_1.value
        self.DRAG_3.value=round(delta_finesse,3)
        self.DRAG_4.value=round(delta_percent_finesse,3)



    def Drag_Saving(self,event):
        self.ID_Type = self.ID_Type + ["Drag Saving"]
        percent=1+self.DRAG_2.value/100
        new_CD=[cd*percent for cd in self.CD]
        new_finesse=self.DRAG_1.value+self.DRAG_3.value
        self.Para_Data2["data:aerodynamics:aircraft:cruise:CD"].value=new_CD
        self.Para_Data2["data:aerodynamics:aircraft:cruise:L_D_max"].value=new_finesse
        self.Para_Data2.save()
        clear_output()
        display(self.ID2_box)
        print("-------------------------------------DRAG MODIFICATIONS SAVED----------------------------------------")

    def MTOW_Increase_UI(self,event):
        path="OUTPUT_FILE"
        file_name="IncrementalDevelopment_Aircraft_File.xml"
        para_path=pth.join(path,file_name)
        self.Para_Data4=self.OAD.Input_File(para_path)
        self.MTOW_REF=self.Para_Data4["data:weight:aircraft:MTOW"].value[0]
        self.List_MTOW.append(self.MTOW_REF)

        clear_output()
        display(self.ID2_box)


        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')
        layout=widgets.Layout(width="50%", height='50px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        title=widgets.HTML(value=" <b>MTOW INCREASE </b>")
        self.MTOW_1=widgets.BoundedFloatText(min=0,max=1000000,step=0.001,value=self.MTOW_REF,disabled=True,description="MTOW (Kg) ",description_tooltip="MTOW OF THE REFERENCE AICRAFT",style=style,layout=layout)
        self.MTOW_2=widgets.BoundedFloatText(min=0,max=1000000,step=100,value=0,disabled=False,description=" ∆(MTOW)",description_tooltip="THE DELTA MTOW INCREASE",style=style,layout=layout)
        self.MTOW_2.observe(self.delta_MTOW_percent,names="value")

        self.MTOW_3=widgets.BoundedFloatText(min=0,max=100,step=1,value=0,disabled=False,description="%∆(MTOW)",description_tooltip="THE % OF DELTA MTOW INCREASE",style=style,layout=layout)
        self.MTOW_3.observe(self.percent_MTOW_delta,names="value")

        Button=widgets.Button(description="SAVE",tooltip="SAVE THE MTOW MODIFICATIONS",layout=layout_button,style=dict(button_color="#33ffcc"))
        Button.on_click(self.MTOW_Saving)
        self.MTOW_box=widgets.VBox(children=[title,self.MTOW_1,self.MTOW_2,self.MTOW_3,Button],layout=layout_box)
        display(self.MTOW_box)


    def delta_MTOW_percent(self,change):
        delta=self.MTOW_2.value
        percent=(delta/self.MTOW_1.value)*100
        self.MTOW_3.value=percent

    def percent_MTOW_delta(self,change):
        percent=self.MTOW_3.value
        delta=(percent*self.MTOW_1.value)/100
        self.MTOW_2.value=delta

    def MTOW_Saving(self,event):
        self.ID_Type = self.ID_Type + ["MTOW Increase"]
        delta_MTOW=self.MTOW_2.value
        MTOW_New=self.MTOW_REF+delta_MTOW
        self.var_mtow =  delta_MTOW

        self.Para_Data4["data:weight:aircraft:MTOW"].value=MTOW_New
        self.Para_Data4["data:mission:MTOW_mission:TOW"].value = MTOW_New
        self.Para_Data4.save()

        clear_output()
        display(self.ID2_box)
        print("---------------------------------------------------MTOW MODIFICATION SAVED-------------------------------------")




    def Fuselage_Stretch_UI(self,event):

        path="OUTPUT_FILE"
        file="IncrementalDevelopment_Aircraft_File.xml"
        para_path=pth.join(path,file)
        para_data=self.OAD.Input_File(para_path)



        FUSE_1=para_data["data:geometry:fuselage:length"].value[0]

        self.CD0_fus=para_data["data:aerodynamics:fuselage:cruise:CD0"].value
        FUSE_2=statistics.mean(self.CD0_fus)

        self.CD0_ac=para_data["data:aerodynamics:aircraft:cruise:CD0"].value
        FUSE_3=statistics.mean(self.CD0_ac)

        self.CD_ac=para_data["data:aerodynamics:aircraft:cruise:CD"].value
        FUSE_4=statistics.mean(self.CD_ac)

        FUSE_5=para_data["data:aerodynamics:aircraft:cruise:L_D_max"].value[0]
        FUSE_6=para_data["data:geometry:cabin:NPAX1"].value[0]
        FUSE_7=para_data["data:weight:aircraft:OWE"].value[0]

        FUSE_16=para_data["data:weight:aircraft:payload"].value[0]
        FUSE_17=para_data["data:weight:aircraft:max_payload"].value[0]

        # Compute the coeffecient k from the expression of the aircraft CD0 implemented in FAST-OAD
        CD0_clean=statistics.mean(para_data["data:aerodynamics:aircraft:cruise:CD0:clean"].value)
        CD0_parasitic=statistics.mean(para_data["data:aerodynamics:aircraft:cruise:CD0:parasitic"].value)
        self.K_CD0=CD0_clean/CD0_parasitic


        clear_output()
        display(self.ID2_box)

        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        layout_button=widgets.Layout(width='40%', height='40px', border='4px solid black')
        layout_H=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%')
        layout_box=widgets.Layout(border='6px solid black', padding='10px', align_items='center', width='100%')
        layout=widgets.Layout(width="50%", height='50px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        layout_H=widgets.Layout( padding='10px', align_items='center', width='100%',justify_content='space-between')
        layout_V=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%')

        title=widgets.HTML(value=" <b>FUSELAGE STRETCH </b>")

        self.FUSE_1=widgets.BoundedFloatText(min=0,max=100,step=0.001,value=round(FUSE_1,2),disabled=True,description="fuselage:length (m)",description_tooltip="total fuselage length (m)",style=style,layout=layout)
        self.FUSE_2=widgets.BoundedFloatText(min=0,max=100,step=0.001,value=round(FUSE_2,4),disabled=True,description="fuselage:cruise:CD0_mean",description_tooltip="The mean CD0 of the fuselage in cruise",style=style,layout=layout)
        self.FUSE_3=widgets.BoundedFloatText(min=0,max=100,step=0.001,value=round(FUSE_3,4),disabled=True,description="aircraft:cruise:CD0_mean",description_tooltip="the mean CD0 of the aircraft in cruise",style=style,layout=layout)
        self.FUSE_4=widgets.BoundedFloatText(min=0,max=100,step=0.001,value=round(FUSE_4,4),disabled=True,description="aircraft:cruise:CD_mean",description_tooltip="the mean CD0 of the aircraft in cruise",style=style,layout=layout)
        self.FUSE_5=widgets.BoundedFloatText(min=0,max=100,step=0.001,value=round(FUSE_5,2),disabled=True,description="aircraft:cruise:L_D_max",description_tooltip="the max lift_drag ratio",style=style,layout=layout)
        box1=widgets.HBox(children=[self.FUSE_2,self.FUSE_3],layout=layout_H)
        box2=widgets.HBox(children=[self.FUSE_4,self.FUSE_5],layout=layout_H)
        self.FUSE_6=widgets.BoundedFloatText(min=0,max=1000,step=1,value=round(FUSE_6,0),disabled=True,description="cabin:NPAX1",description_tooltip="number of passengers",style=style,layout=layout)
        self.FUSE_7=widgets.BoundedFloatText(min=0,max=60000,step=1,value=round(FUSE_7,3),disabled=True,description="OWE (Kg)",description_tooltip="Empty Operating Weight of the aircraft",style=style,layout=layout)
        box3=widgets.HBox(children=[self.FUSE_6,self.FUSE_7],layout=layout_H)

        self.FUSE_16=widgets.BoundedFloatText(min=0,max=60000,step=1,value=round(FUSE_16,3),disabled=True,description="aircraft:payload (Kg)",description_tooltip="design payload weight",style=style,layout=layout)
        self.FUSE_17=widgets.BoundedFloatText(min=0,max=60000,step=1,value=round(FUSE_17,3),disabled=True,description="aircraft:max_payload(Kg)",description_tooltip="design max payload weight",style=style,layout=layout)

        box11=widgets.HBox(children=[self.FUSE_16,self.FUSE_17],layout=layout_H)
        box4=widgets.VBox(children=[self.FUSE_1,box1,box2,box3,box11],layout=layout_V)


        self.FUSE_8=widgets.BoundedFloatText(min=0,max=100,step=0.01,value=0,disabled=False,description=" ∆ fuselage:length (m)",description_tooltip="variation of total fuselage length (m)",style=style,layout=layout)
        self.FUSE_8.observe(self.delta_length_percent,names="value")

        self.FUSE_9=widgets.BoundedFloatText(min=0,max=100,step=0.01,value=0,disabled=False,description=" ∆ fuselage:length (%)",description_tooltip="variation of total fuselage length (m)",style=style,layout=layout)
        self.FUSE_9.observe(self.percent_length_delta,names="value")
        box5=widgets.HBox(children=[self.FUSE_8,self.FUSE_9],layout=layout_H)
        box6=widgets.VBox(children=[box5],layout=layout_V)


        self.FUSE_10=widgets.BoundedFloatText(min=-100,max=100,step=0.01,value=0,disabled=True,description="∆ aircraft:cruise:L_D_max",description_tooltip="the max lift_drag ratio ",style=style,layout=layout)

        self.FUSE_11=widgets.BoundedFloatText(min=-100,max=100,step=0.01,value=0,disabled=True,description="∆ aircraft:cruise:L_D_max (%)",description_tooltip="the max lift_drag ratio ",style=style,layout=layout)

        box7=widgets.HBox(children=[self.FUSE_10,self.FUSE_11],layout=layout_H)


        self.FUSE_12=widgets.BoundedFloatText(min=0,max=1000,step=1,value=0,disabled=True,description="∆ cabin:NPAX1",description_tooltip="number of passengers",style=style,layout=layout)

        self.FUSE_13=widgets.BoundedFloatText(min=0,max=1000,step=0.01,value=0,disabled=True,description="∆ cabin:NPAX1(%)",description_tooltip="number of passengers",style=style,layout=layout)


        box8=widgets.HBox(children=[self.FUSE_12,self.FUSE_13],layout=layout_H)

        self.FUSE_14=widgets.BoundedFloatText(min=0,max=60000,step=0.01,value=0,disabled=True,description="∆ OWE (Kg)",description_tooltip="Empty Operating Weight of the aircraft",style=style,layout=layout)


        self.FUSE_15=widgets.BoundedFloatText(min=0,max=100,step=0.01,value=0,disabled=True,description=" ∆ OWE (%)",description_tooltip="Empty Operating Weight of the aircraft",style=style,layout=layout)


        box9=widgets.HBox(children=[self.FUSE_14,self.FUSE_15],layout=layout_H)

        self.FUSE_18=widgets.BoundedFloatText(min=0,max=60000,step=1,value=0,disabled=True,description="∆ aircraft:max_payload(Kg)",description_tooltip="variation of the  design max payload weight",style=style,layout=layout)
        self.FUSE_19=widgets.BoundedFloatText(min=0,max=60000,step=1,value=0,disabled=True,description="∆ aircraft:max_payload(%)",description_tooltip="∆ variation of the  design max payload weight(%)",style=style,layout=layout)

        box12=widgets.HBox(children=[self.FUSE_18,self.FUSE_19],layout=layout_H)
        box10=widgets.VBox(children=[box7,box8,box9,box12],layout=layout_V)

        Button=widgets.Button(description="SAVE",tooltip="SAVE THE FUSELAGE MOFIFICATIONS ",layout=layout_button,style=dict(button_color="#33ffcc"))
        Button.on_click(self.Fuselage_Stretch)

        self.FUSE_box=widgets.VBox(children=[title,box4,box6,box10,Button],layout=layout_box)
        display(self.FUSE_box)


    def delta_length_percent(self,change):
        length_ref=self.FUSE_1.value
        delta_length=self.FUSE_8.value
        percent=(100*delta_length)/length_ref
        self.FUSE_9.value=round(percent,2)

        #NEW FUSELAGE LENGTH
        length_new=length_ref+delta_length

        #NEW NPAX
        Npax_ref=self.FUSE_6.value
        Npax_new=(length_new/length_ref)*Npax_ref
        delta_Npax=(Npax_new-Npax_ref)
        percent_Npax=(delta_Npax*100)/Npax_ref
        self.FUSE_12.value=round(delta_Npax,0)
        self.FUSE_13.value=round(percent_Npax,2)


        #NEW OWE
        OWE_ref=self.FUSE_7.value
        OWE_new=(length_new/length_ref)*OWE_ref
        delta_OWE=(OWE_new-OWE_ref)
        percent_OWE=(delta_OWE*100)/OWE_ref
        self.FUSE_14.value=round(delta_OWE,3)
        self.FUSE_15.value=round(percent_OWE,2)


        #NEW PAYLOAD
        Payload_ref=self.FUSE_17.value
        Payload_new=(Npax_new/Npax_ref)*Payload_ref
        delta_Payload=(Payload_new-Payload_ref)
        percent_Payload=(delta_Payload*100)/Payload_ref
        self.FUSE_18.value=round(delta_Payload,3)
        self.FUSE_19.value=round(percent_Payload,2)

        #NEW AERODYNAMICS

        #New CD0 of the fuselage
        CD0_ref=self.FUSE_2.value
        CD0_fus_new=(length_new/length_ref)*CD0_ref

        # Delta CD0 of the fuselage
        delta_CD0_fus=CD0_fus_new-CD0_ref

        # Delta CD0 of the aircraft
        delta_CD0_ac=self.K_CD0*delta_CD0_fus

        # Delta CD of the aircraft
        delta_CD_ac=delta_CD0_ac

        # Delta CD of the aircraft in %
        CD_ref=self.FUSE_4.value
        percent_CD=(100*delta_CD_ac)/CD_ref

        # new the lift drag ration in %
        finesse_ref=self.FUSE_5.value
        finesse_new=(100*finesse_ref)/(100+percent_CD)
        delta_finesse=finesse_new-finesse_ref
        percent_finesse=(100*delta_finesse)/finesse_ref

        self.FUSE_10.value=round(delta_finesse,2)

        self.FUSE_11.value=round(percent_finesse,2)


    def percent_length_delta(self,change):
        length_ref=self.FUSE_1.value
        percent=self.FUSE_9.value
        delta_length=(percent*length_ref)/100
        self.FUSE_8.value=round(delta_length,2)

        #NEW FUSELAGE LENGTH
        length_new=length_ref+delta_length

        #NEW NPAX
        Npax_ref=self.FUSE_6.value
        Npax_new=(length_new/length_ref)*Npax_ref
        delta_Npax=(Npax_new-Npax_ref)
        percent_Npax=(delta_Npax*100)/Npax_ref
        self.FUSE_12.value=round(delta_Npax,0)
        self.FUSE_13.value=round(percent_Npax,2)


        #NEW OWE
        OWE_ref=self.FUSE_7.value
        OWE_new=(length_new/length_ref)*OWE_ref
        delta_OWE=(OWE_new-OWE_ref)
        percent_OWE=(delta_OWE*100)/OWE_ref
        self.FUSE_14.value=round(delta_OWE,3)
        self.FUSE_15.value=round(percent_OWE,2)


        #NEW PAYLOAD
        Payload_ref=self.FUSE_17.value
        Payload_new=(Npax_new/Npax_ref)*Payload_ref
        delta_Payload=(Payload_new-Payload_ref)
        percent_Payload=(delta_Payload*100)/Payload_ref
        self.FUSE_18.value=round(delta_Payload,3)
        self.FUSE_19.value=round(percent_Payload,2)

        #NEW AERODYNAMICS

        #New CD0 of the fuselage
        CD0_ref=self.FUSE_2.value
        CD0_fus_new=(length_new/length_ref)*CD0_ref


        # Delta CD0 of the fuselage
        delta_CD0_fus=CD0_fus_new-CD0_ref
        self.percent_CD0_fus=(100*delta_CD0_fus)/CD0_ref

        # Delta CD0 of the aircraft
        delta_CD0_ac=self.K_CD0*delta_CD0_fus
        self.percent_CD0_ac=(100*delta_CD0_ac)/self.FUSE_3.value
        # Delta CD of the aircraft
        delta_CD_ac=delta_CD0_ac

        # Delta CD of the aircraft in %
        CD_ref=self.FUSE_4.value
        self.percent_CD=(100*delta_CD_ac)/CD_ref

        # new the lift drag ration in %
        finesse_ref=self.FUSE_5.value
        finesse_new=(100*finesse_ref)/(100+self.percent_CD)
        delta_finesse=finesse_new-finesse_ref
        percent_finesse=(100*delta_finesse)/finesse_ref

        self.FUSE_10.value=round(delta_finesse,2)

        self.FUSE_11.value=round(percent_finesse,2)


    def Fuselage_Stretch(self,event):
        self.ID_Type = self.ID_Type + ["Fuselage Simple Stretch"]
        # new length
        length=self.FUSE_1.value+self.FUSE_8.value
        # new lift_drag ratio
        finesse=self.FUSE_5.value+self.FUSE_10.value
        # new NPAX1
        Npax=self.FUSE_6.value+self.FUSE_12.value
        # new OWE
        OWE=self.FUSE_7.value+self.FUSE_14.value
        self.var_owe = self.FUSE_14.value
        # new MAX PAYLOAD
        Payload=self.FUSE_17.value+self.FUSE_18.value

        # new CD0 fuselage
        part_CD0_fus=1+self.percent_CD0_fus/100
        new_CD0_fus=[cd*part_CD0_fus for cd in self.CD0_fus]

        part_CD0_ac=1+self.percent_CD0_ac/100
        new_CD0_ac=[cd*part_CD0_ac for cd in self.CD0_ac]

        part_CD_ac=1+self.percent_CD/100
        new_CD_ac=[cd*part_CD_ac for cd in self.CD_ac]

        path="OUTPUT_FILE"
        file="IncrementalDevelopment_Aircraft_File.xml"
        para_path=pth.join(path,file)
        para_data=self.OAD.Input_File(para_path)

        para_data["data:geometry:fuselage:length"].value=length
        para_data["data:geometry:cabin:NPAX1"].value=Npax
        para_data["data:aerodynamics:aircraft:cruise:L_D_max"].value=finesse
        para_data["data:weight:aircraft:OWE"].value=OWE
        para_data["data:weight:aircraft:max_payload"].value=Payload
        para_data["data:aerodynamics:fuselage:cruise:CD0"].value=new_CD0_fus
        para_data["data:aerodynamics:aircraft:cruise:CD0"].value=new_CD0_ac
        para_data["data:aerodynamics:aircraft:cruise:CD"].value=new_CD_ac

        para_data.save()
        clear_output()
        display(self.ID2_box)
        print("-------------------------------------FUSELAGE STRETCH SAVED----------------------------------------")



    def BlockFuel_ID(self,OWE,PL,RANGE,coefficient,reserve):
        BF_DOC = math.exp((1000 * RANGE * 1.852) / (coefficient)) * (OWE + PL + reserve) - (OWE + PL + reserve)
        return BF_DOC


    def INCREMENTAL_DEVELOPEMENT_STEP1(self,event):

        clear_output()
        display(self.ID2_box)

        ac_ref=self.AC_ref
        mission_ref=self.mission_ref

        path_ac="OUTPUT_FILE"
        file_para="IncrementalDevelopment_Aircraft_File.xml"
        ac_para=pth.join(path_ac,file_para)

        # Compute the new redesigned aircraft performance
        print("---------------NEW PERFORMANCE COMPUTING -----------------------")
        print('The problem is being solved: ☕... ')
        # Function to update the progress bar
        def update_progress_bar():
            total_iterations = 100
            custom_widget = [
                'Progress: ', progressbar.Bar(marker='█', left=' ', right='|'),
                ' ', progressbar.Percentage()]
            with progressbar.ProgressBar(widgets=custom_widget, max_value=total_iterations) as bar:

                for i in range(total_iterations):
                    # Update progress bar
                    time.sleep(0.02)  # Simulate time for updating progress
                    bar.update(i + 1)
        # Create a thread for the simulation
        update_progress_bar()
        print('Problem solved.')
        print("------------------NEW PERFORMANCE COMPUTED----------------------------")

        time.sleep(1.5)
        clear_output()
        display(self.ID2_box)

        path_miss="workdir"
        file_miss="para_perfo.csv"
        mission_para=pth.join(path_miss,file_miss)


        # COMPUTE THE  MEAN_SFC
        SFC_ref=float(self.List_SFC[0])
        if (len(self.List_SFC)>1):
            SFC_para=float(self.List_SFC[len(self.List_SFC)-1])
        else:
            SFC_para=SFC_ref

        #mass_para=self.OAD.mass(mission_para)

        # COMPUTE THE BLOCK FUEL

        data_ref=self.OAD.Input_File(ac_ref)
        OWE_ref=data_ref["data:weight:aircraft:OWE"].value[0]
        PL_DOC_ref = data_ref["data:weight:aircraft:payload"].value[0]
        Range_DOC_ref = 4000  # np.asarray(Data["data:TLAR:range"].value)
        coefficient_ref = self.OAD.para_coefficient_range(data_ref,SFC_ref)
        reserve_ref = data_ref["data:mission:MTOW_mission:reserve:fuel"].value[0]
        BF_ref = self.BlockFuel_ID(OWE_ref,PL_DOC_ref,Range_DOC_ref,coefficient_ref,reserve_ref)

        data_para = self.OAD.Input_File(ac_para)
        OWE_para=data_para["data:weight:aircraft:OWE"].value[0]
        PL_DOC_para = data_para["data:weight:aircraft:payload"].value[0]
        Range_DOC_para = 4000  # np.asarray(Data["data:TLAR:range"].value)
        coefficient_para = self.OAD.para_coefficient_range(data_para, SFC_para)
        reserve_para = data_para["data:mission:MTOW_mission:reserve:fuel"].value[0]
        BF_para = self.BlockFuel_ID(OWE_para, PL_DOC_para, Range_DOC_para, coefficient_para,reserve_para)

        # COMPUTE THE SPECIFIC RANGE
        SR_ref=self.OAD.compute_SR(ac_ref,SFC_ref,BF_ref)[0]
        SR_para=self.OAD.compute_SR(ac_para,SFC_para,BF_para)[0]

        # COMPUTE THE MEAN MASS
        mass_ref= OWE_ref +PL_DOC_ref +(reserve_ref+BF_ref/2)
        mass_para = OWE_para + PL_DOC_para + (reserve_para+BF_para/2)

        Percent_BF = 100*(BF_para-BF_ref)/BF_ref
        Percent_SR = 100 * (SR_para - SR_ref) / SR_ref
        Percent_Mass = 100 * (mass_para - mass_ref) / mass_ref
        data = [
            ["<u>Ref A/C</u>",  "<u>New A/C</u>", "<u>Variation %</u>"],
            ["<i>Block Fuel = </i>  " + "<b>"+str(round(BF_ref,2))+"</b>" + "  [kg]", "<i>Block Fuel = </i>  "+"<b>"+str(round(BF_para,2))+"</b>"+"  [kg]", "<b>"+str(round(Percent_BF,2))+"</b>"],
            ["<i>Mean Specific Range = </i>  "+ "<b>"+str(round(SR_ref,3))+"</b>" + "  [NM/kg]", "<i>Mean Specific Range = </i>  "+"<b>"+str(round(SR_para,3))+"</b>" +"  [NM/kg]", "<b>"+str(round(Percent_SR,2))+"</b>"],
            ["<i>Mean Mass = </i>  " + "<b>"+str(round(mass_ref, 2))+"</b>" + "  [kg]", "<i>Mean Mass = </i>  " + "<b>"+str(round(mass_para, 2))+"</b>" + "  [kg]","<b>"+str(round(Percent_Mass, 2))+"</b>"],
            ]
        table_widget = widgets.GridBox(children=[widgets.HTML(str(value)) for row in data for value in row],
            layout=widgets.Layout(grid_template_columns="repeat(3, auto)",width='100%'))

        buttonINFO = widgets.Button(description='')
        buttonINFO.icon = 'fa-info-circle'
        buttonINFO.layout.width = 'auto'
        buttonINFO.layout.height = 'auto'
        output = widgets.Output()

        def info_message(event):
            with output:
                output.clear_output()
                if len(output.outputs) > 0:
                    output.clear_output()

                else:
                    print('Block Fuel is computed for Max Range at Max Payload.\n'
                          'The mass used to compute the Specific Range is the average over the climb and cruise phase.\n'
                          'BF/Npax-BF is computed at DOC (TLAR RANGE at SPP)'
                          )
        buttonINFO.on_click(info_message)
        infobox = widgets.Box(children=[buttonINFO, output], layout=Layout(border='0px solid black',
                                                                           margin='50 0 50 0px', padding='5px',
                                                                           align_items='center', width='100'))
        if self.var_owe == None:
            self.var_owe =0
        if self.var_mtow == None:
            self.var_mtow = 0

        # Plot the payload-range diagram
        fig=self.OAD.para_payload_range(ac_ref,SFC_ref,var_owe=None,var_mtow=None,name="REF AC",Color='blue')

        fig=self.OAD.para_payload_range(ac_para,SFC_para,self.var_owe,self.var_mtow,"NEW AC",fig=fig,Color='red')

        C_V_BF = widgets.VBox(children=[fig],
                                     layout=widgets.Layout(border='0px solid black', align_items='center',
                                                           padding='0px', width='100%'))

        fig2=self.OAD.Npax_BF_Diagramm(ac_ref,SFC_ref,"REF AC",Color='blue')
        fig2=self.OAD.Npax_BF_Diagramm(ac_para,SFC_para,"NEW AC",fig=fig2,Color='red')

        C_V_BlockFuel = widgets.VBox(children=[fig2,table_widget,infobox],
            layout=widgets.Layout(border='0px solid black', align_items='center', padding='0px', width='100%'))

        C_para1 = widgets.HTML(value=" <b><u>Analysis Toolbox</u></b>")
        C_para2 = widgets.HTML(value=" <b>Incremental Developments Applied: </b>" + "," .join(self.ID_Type))

        self.tab_Analysis_Para = widgets.Tab(children=[C_V_BF,C_V_BlockFuel],layout=widgets.Layout(border='0px solid black',
                                                                    align_items='center', padding='0px', width='100%'))
        self.tab_Analysis_Para.set_title(0, 'Payload - Range ')
        self.tab_Analysis_Para.set_title(1, 'BF/Npax & SR')
        C_Vertical_Para = widgets.VBox(children=[C_para1,C_para2,self.tab_Analysis_Para],
            layout=widgets.Layout(border='2px solid black', align_items='center', padding='2px', width='100%'))

        display(C_Vertical_Para)
        print('Problem solved.')
        print("------------------NEW PERFORMANCE COMPUTED----------------------------")

    def INCREMENTAL_DEVELOPEMENT_STEP2_OWE(self,event):

        clear_output()
        display(self.ID2_box)

        #DATA AC REFERENCE
        ac_ref=self.AC_ref
        mission_ref=self.mission_ref
        data_ref = self.OAD.Input_File(ac_ref)
        OWE_ref = data_ref["data:weight:aircraft:OWE"].value[0]
        CD_ref = data_ref["data:aerodynamics:aircraft:cruise:CD"].value[0]

        #DATA AC STEP1
        path_ac="OUTPUT_FILE"
        file_para_S1="IncrementalDevelopment_Aircraft_File.xml"
        ac_para_S1=pth.join(path_ac,file_para_S1)
        SOURCE = ac_para_S1
        data_para = self.OAD.Input_File(ac_para_S1)
        # Getting the inputs optimization problem from the user interface
        if "Weight Saving" in self.ID_Type:
            delta_percent_owe_extra = 0.0102
        else:
            delta_percent_owe_extra=0

        #DATA OWE or FUSELAGE OWE or NEO OWE STEP 2
        OWE_step1 = data_para["data:weight:aircraft:OWE"].value[0]
        OWE_percent = (1 - (OWE_ref-OWE_step1) / OWE_ref) + delta_percent_owe_extra
        data_para["data:weight:k_factor_OWE"].value=OWE_percent

        #DATA DRAG SAVING or FUSELAGE STRETCH EXTRA DRAG or NEO DRAG STEP 2
        CD_step1 = data_para["data:aerodynamics:aircraft:cruise:CD"].value[0]
        CD_percent = (1 - (CD_ref - CD_step1) / CD_ref)
        data_para["tuning:aerodynamics:aircraft:cruise:CD:k"].value = CD_percent

        #DATA SFC or NEO SFC STEP 2
        if "SFC" in self.ID_Type:
            SFC_ref = float(self.List_SFC[0])
            SFC_para_S1 = float(self.List_SFC[len(self.List_SFC) - 1])
            SFC_percent = (1 - (SFC_ref - SFC_para_S1) / SFC_ref)
            data_para["tuning:propulsion:rubber_engine:SFC:k_cr"].value = SFC_percent

        data_para.save()


        #BUILD CONFIG AND INPUTS FOR STEP 2 problem

        path_config="data"
        file_config="oad_sizing_step2_owe.yml" #"para_performance.yml"
        CONFIGURATION=pth.join(path_config,file_config)
        oad.generate_inputs(CONFIGURATION,SOURCE, overwrite=True)

        # here, after this save function, the new values modifies by the user are changed in the input file
        def RUN_MDA_PARA():
            self.OWE_STEP2=oad.evaluate_problem(CONFIGURATION, overwrite=True)
            self.OAD.Save_File(self.OWE_STEP2.output_file_path, "OUTPUT_FILE", "STEP2_OWE")


        # Function to update the progress bar
        def update_progress_bar():
            total_iterations = 100
            custom_widget = [
                'Progress: ', progressbar.Bar(marker='█', left=' ', right='|'),
                ' ', progressbar.Percentage()]
            with progressbar.ProgressBar(widgets=custom_widget, max_value=total_iterations) as bar:
                for i in range(total_iterations):
                    # Update progress bar
                    time.sleep(0.8)  # Simulate time for updating progress
                    bar.update(i + 1)


        # Create a thread for the simulation
        simulation_thread = threading.Thread(target=RUN_MDA_PARA)
        print('The problem is being solved: ☕... ')
        # Start the simulation thread
        simulation_thread.start()
        # Start the progress bar thread
        update_progress_bar()
        # Wait for the simulation thread to complete
        simulation_thread.join()
        print('Problem solved.')
        print("------------------NEW PERFORMANCE COMPUTED----------------------------")

        time.sleep(1.5)
        clear_output()
        display(self.ID2_box)

        #NEW DATA OF THE STEP 2 AC
        path_miss="workdir"
        file_miss="para_perfo.csv"
        mission_para_S2=pth.join(path_miss,file_miss) #new aircraft mission after looping

        path_ac="OUTPUT_FILE"
        file_para="STEP2_OWE.xml"
        ac_para_S2=pth.join(path_ac,file_para)  #new aircraft after ID and looping


        # COMPUTE THE  MEAN_SFC
        SFC_ref=float(self.List_SFC[0])
        if (len(self.List_SFC)>1):
            SFC_para_S1=float(self.List_SFC[len(self.List_SFC)-1])
        else:
            SFC_para_S1=self.OAD.para_sfc(mission_ref)
        SFC_para_S2 = self.OAD.para_sfc(mission_para_S2)

        # COMPUTE THE BLOCK FUEL
        # FOR THE REC AC
        OWE_ref=data_ref["data:weight:aircraft:OWE"].value[0]
        PL_DOC_ref = data_ref["data:weight:aircraft:payload"].value[0]
        Range_DOC_ref = 4000  # np.asarray(Data["data:TLAR:range"].value)
        coefficient_ref = self.OAD.para_coefficient_range(data_ref,SFC_ref)
        reserve_ref = data_ref["data:mission:MTOW_mission:reserve:fuel"].value[0]
        BF_ref = self.BlockFuel_ID(OWE_ref,PL_DOC_ref,Range_DOC_ref,coefficient_ref,reserve_ref)


        #FOR THE STEP 1 AC
        OWE_para_S1=data_para["data:weight:aircraft:OWE"].value[0]
        PL_DOC_para_S1 = data_para["data:weight:aircraft:payload"].value[0]
        Range_DOC_para_S1 = 4000  # np.asarray(Data["data:TLAR:range"].value)
        coefficient_para_S1 = self.OAD.para_coefficient_range(data_para, SFC_para_S1)
        reserve_para_S1 = data_para["data:mission:MTOW_mission:reserve:fuel"].value[0]
        BF_para_S1 = self.BlockFuel_ID(OWE_para_S1, PL_DOC_para_S1, Range_DOC_para_S1, coefficient_para_S1,reserve_para_S1)


        #FOR THE STEP 2 AC
        data_para = self.OAD.Input_File(ac_para_S2)
        OWE_para_S2=data_para["data:weight:aircraft:OWE"].value[0]
        PL_DOC_para_S2 = data_para["data:weight:aircraft:payload"].value[0]
        Range_DOC_para_S2 = 4000  # np.asarray(Data["data:TLAR:range"].value)
        coefficient_para_S2 = self.OAD.para_coefficient_range(data_para, SFC_para_S2)
        reserve_para_S2 = data_para["data:mission:MTOW_mission:reserve:fuel"].value[0]
        BF_para_S2 = self.BlockFuel_ID(OWE_para_S2, PL_DOC_para_S2, Range_DOC_para_S2, coefficient_para_S2,reserve_para_S2)


        # COMPUTE THE SPECIFIC RANGE
        SR_ref=self.OAD.compute_SR(ac_ref,SFC_ref,BF_ref)[0]
        SR_para_S1=self.OAD.compute_SR(ac_para_S1,SFC_para_S1,BF_para_S1)[0]
        SR_para_S2 = self.OAD.compute_SR(ac_para_S2, SFC_para_S2, BF_para_S2)[0]

        # COMPUTE THE MEAN MASS
        mass_ref= OWE_ref +PL_DOC_ref +(reserve_ref+BF_ref/2)
        mass_para_S1 = OWE_para_S1 + PL_DOC_para_S1 + (reserve_para_S1 + BF_para_S1/2)
        mass_para_S2 = OWE_para_S2 + PL_DOC_para_S2 + (reserve_para_S2 + BF_para_S2/2)

        Percent_BF_S1 = 100*(BF_para_S1-BF_ref)/BF_ref
        Percent_SR_S1 = 100 * (SR_para_S1 - SR_ref) / SR_ref
        Percent_Mass_S1 = 100 * (mass_para_S1 - mass_ref) / mass_ref
        data = [
            ["<u>Ref A/C</u>",  "<u>STEP 1 A/C</u>", "<u>Variation w.r.t REF %</u>"],
            ["<i>Block Fuel = </i>  " + "<b>"+str(round(BF_ref,2))+"</b>" + "  [kg]", "<i>Block Fuel = </i>  "+"<b>"+str(round(BF_para_S1,2))+"</b>"+"  [kg]", "<b>"+str(round(Percent_BF_S1,2))+"</b>"],
            ["<i>Mean Specific Range = </i>  "+ "<b>"+str(round(SR_ref,3))+"</b>" + "  [NM/kg]", "<i>Mean Specific Range = </i>  "+"<b>"+str(round(SR_para_S1,3))+"</b>" +"  [NM/kg]", "<b>"+str(round(Percent_SR_S1,2))+"</b>"],
            ["<i>Mean Mass = </i>  " + "<b>"+str(round(mass_ref, 2))+"</b>" + "  [kg]", "<i>Mean Mass = </i>  " + "<b>"+str(round(mass_para_S1, 2))+"</b>" + "  [kg]","<b>"+str(round(Percent_Mass_S1, 2))+"</b>"],
            ]
        table_widget_S1 = widgets.GridBox(children=[widgets.HTML(str(value)) for row in data for value in row],
            layout=widgets.Layout(grid_template_columns="repeat(3, auto)",width='100%'))

        Percent_BF_S2 = 100*(BF_para_S2-BF_ref)/BF_ref
        Percent_SR_S2 = 100 * (SR_para_S2 - SR_ref) / SR_ref
        Percent_Mass_S2 = 100 * (mass_para_S2 - mass_ref) / mass_ref
        data = [
            ["<u>Ref A/C</u>",  "<u>STEP 2 A/C</u>", "<u>Variation w.r.t REF %</u>"],
            ["<i>Block Fuel = </i>  " + "<b>"+str(round(BF_ref,2))+"</b>" + "  [kg]", "<i>Block Fuel = </i>  "+"<b>"+str(round(BF_para_S2,2))+"</b>"+"  [kg]", "<b>"+str(round(Percent_BF_S2,2))+"</b>"],
            ["<i>Mean Specific Range = </i>  "+ "<b>"+str(round(SR_ref,3))+"</b>" + "  [NM/kg]", "<i>Mean Specific Range = </i>  "+"<b>"+str(round(SR_para_S2,3))+"</b>" +"  [NM/kg]", "<b>"+str(round(Percent_SR_S2,2))+"</b>"],
            ["<i>Mean Mass = </i>  " + "<b>"+str(round(mass_ref, 2))+"</b>" + "  [kg]", "<i>Mean Mass = </i>  " + "<b>"+str(round(mass_para_S2, 2))+"</b>" + "  [kg]","<b>"+str(round(Percent_Mass_S2, 2))+"</b>"],
            ]
        table_widget_S2 = widgets.GridBox(children=[widgets.HTML(str(value)) for row in data for value in row],
            layout=widgets.Layout(grid_template_columns="repeat(3, auto)",width='100%'))


        buttonINFO = widgets.Button(description='')
        buttonINFO.icon = 'fa-info-circle'
        buttonINFO.layout.width = 'auto'
        buttonINFO.layout.height = 'auto'
        output = widgets.Output()

        def info_message(event):
            with output:
                output.clear_output()
                if len(output.outputs) > 0:
                    output.clear_output()
                else:
                    print('Block Fuel is computed for DOC.\n')
        buttonINFO.on_click(info_message)
        infobox = widgets.Box(children=[buttonINFO, output], layout=Layout(border='0px solid black',
                                                                           margin='50 0 50 0px', padding='5px',
                                                                           align_items='center', width='100'))


        if self.var_owe == None:
            self.var_owe =0
        if self.var_mtow == None:
            self.var_mtow = 0
        # Plot the payload-range diagram
        fig=self.OAD.para_payload_range(ac_ref,SFC_ref,var_owe=None,var_mtow=None,name="REF AC",Color='blue')
        fig=self.OAD.para_payload_range(ac_para_S1,SFC_para_S1,self.var_owe,self.var_mtow,"STEP1",fig=fig,Color='red')
        fig=self.OAD.para_payload_range(ac_para_S2,SFC_para_S2,var_owe=None,var_mtow=None,name="STEP2",fig=fig,Color='green')
        # Plot the BF/NPAX DIAGRAM
        fig2 = self.OAD.Npax_BF_Diagramm(ac_ref,SFC_ref,"REF AC",Color='blue')
        fig2 = self.OAD.Npax_BF_Diagramm(ac_para_S1,SFC_para_S1,"STEP 1",fig=fig2,Color='red')
        fig2 = self.OAD.Npax_BF_Diagramm(ac_para_S2, SFC_para_S2, "STEP 2", fig=fig2, Color='green')

        C_V_BlockFuel = widgets.VBox(children=[fig2,table_widget_S1,table_widget_S2,infobox],
            layout=widgets.Layout(border='1px solid black', align_items='center', padding='2px', width='100%'))

        C_para1 = widgets.HTML(value=" <b><u>Analysis Toolbox</u></b>")
        C_para2 = widgets.HTML(value=" <b>Incremental Developments Applied: </b>" + "," .join(self.ID_Type))

        self.tab_Analysis_Para = widgets.Tab(children=[fig,C_V_BlockFuel],
                                             layout=widgets.Layout(border='0px solid black', align_items='center', padding='2px', width='100%'))
        self.tab_Analysis_Para.set_title(0, 'Payload - Range ')
        self.tab_Analysis_Para.set_title(1, 'BF/Npax & SR')
        C_Vertical_Para = widgets.VBox(children=[C_para1,C_para2,self.tab_Analysis_Para],
            layout=widgets.Layout(border='5px solid black', align_items='center', padding='5px', width='100%'))

        display(C_Vertical_Para)
        print('Problem solved.')
        print("------------------NEW PERFORMANCE COMPUTED----------------------------")






    def INCREMENTAL_DEVELOPEMENT_STEP2_DRAG(self,event):

        clear_output()
        display(self.ID2_box)

        ac_ref=self.AC_ref
        mission_ref=self.mission_ref

        path_ac="OUTPUT_FILE"
        file_para="IncrementalDevelopment_Aircraft_File.xml"
        ac_para=pth.join(path_ac,file_para)

        # Compute the new redesigned aircraft performance

        SOURCE=ac_para
        path_config="data"
        file_config="para_sizing.yml" #"para_performance.yml"
        CONFIGURATION=pth.join(path_config,file_config)
        oad.generate_inputs(CONFIGURATION,SOURCE, overwrite=True)

        # here, after this save function, the new values modifies by the user are changed in the input file

        def RUN_MDA_PARA():
            self.ParametricProblem = oad.evaluate_problem(CONFIGURATION, overwrite=True)
            self.OAD.Save_File(self.ParametricProblem.output_file_path, "OUTPUT_FILE", "para_OUT")


        # Function to update the progress bar
        def update_progress_bar():
            total_iterations = 100
            custom_widget = [
                'Progress: ', progressbar.Bar(marker='█', left=' ', right='|'),
                ' ', progressbar.Percentage()]
            with progressbar.ProgressBar(widgets=custom_widget, max_value=total_iterations) as bar:
                for i in range(total_iterations):
                    # Update progress bar
                    time.sleep(2)  # Simulate time for updating progress
                    bar.update(i + 1)


        # Create a thread for the simulation
        simulation_thread = threading.Thread(target=RUN_MDA_PARA)
        print('The problem is being solved: ☕... ')
        # Start the simulation thread
        simulation_thread.start()
        # Start the progress bar thread
        update_progress_bar()
        # Wait for the simulation thread to complete
        simulation_thread.join()
        print('Problem solved.')
        print("------------------NEW PERFORMANCE COMPUTED----------------------------")

        time.sleep(1.5)
        clear_output()
        display(self.ID2_box)

        path_miss="workdir"
        file_miss="para_perfo.csv"
        mission_para=pth.join(path_miss,file_miss) #new aircraft mission after looping

        path_ac="OUTPUT_FILE"
        file_para="para_OUT.xml"
        ac_para=pth.join(path_ac,file_para)  #new aircraft after ID and looping


        # COMPUTE THE  MEAN_SFC


        SFC_ref=float(self.List_SFC[0])
        if (len(self.List_SFC)>1):
            SFC_para=float(self.List_SFC[len(self.List_SFC)-1])
        else:
            SFC_para=self.OAD.para_sfc(mission_para)

        # COMPUTE THE MEAN MASS
        #mass mission includes cruise and main route climb
        mass_ref=self.OAD.mass(mission_ref)
        mass_para=self.OAD.mass(mission_para)
        # COMPUTE THE SPECIFIC RANGE
        SR_ref=self.OAD.compute_SR(ac_ref,SFC_ref,mass_ref)[0]
        SR_para=self.OAD.compute_SR(ac_para,SFC_para,mass_para)[0]


        # COMPUTE THE BLOCK FUEL

        data_ref=self.OAD.Input_File(ac_ref)
        OWE_ref=data_ref["data:weight:aircraft:OWE"].value[0]
        PL_DOC_ref = data_ref["data:weight:aircraft:payload"].value[0]
        Range_DOC_ref = 4000  # np.asarray(Data["data:TLAR:range"].value)
        coefficient_ref = self.OAD.para_coefficient_range(data_ref,SFC_ref)
        BF_ref = self.BlockFuel_ID(OWE_ref,PL_DOC_ref,Range_DOC_ref,coefficient_ref)
        reserve_ref = data_ref["data:mission:MTOW_mission:reserve:fuel"].value[0]
        #MTOW_ref=data_ref["data:weight:aircraft:MTOW"].value[0]
        #Max_Payload_ref=data_ref["data:weight:aircraft:max_payload"].value[0]
        #BF_ref=MTOW_ref-OWE_ref-Max_Payload_ref


        data_para = self.OAD.Input_File(ac_para)
        OWE_para=data_para["data:weight:aircraft:OWE"].value[0]
        PL_DOC_para = data_para["data:weight:aircraft:payload"].value[0]
        Range_DOC_para = 4000  # np.asarray(Data["data:TLAR:range"].value)
        coefficient_para = self.OAD.para_coefficient_range(data_para, SFC_para)
        BF_para = self.BlockFuel_ID(OWE_para, PL_DOC_para, Range_DOC_para, coefficient_para)
        reserve_para = data_para["data:mission:MTOW_mission:reserve:fuel"].value[0]
        #MTOW_para=data_para["data:weight:aircraft:MTOW"].value[0]
        #Max_Payload_para=data_para["data:weight:aircraft:max_payload"].value[0]
        #BF_para=MTOW_para-OWE_para-Max_Payload_para

        # COMPUTE THE SPECIFIC RANGE
        SR_ref=self.OAD.compute_SR(ac_ref,SFC_ref,BF_ref)[0]
        SR_para=self.OAD.compute_SR(ac_para,SFC_para,BF_para)[0]

        # COMPUTE THE MEAN MASS
        #mass mission includes cruise and main route climb
        mass_ref=self.OAD.mass(mission_ref)
        if self.var_mtow == None:
            mass_para = self.OAD.mass(mission_ref) # It is the same as the MDA is not run in STEP1
        else:
            mass_para = self.OAD.mass(mission_ref) + self.var_mtow

        mass_ref= OWE_ref +PL_DOC_ref +(reserve_ref+BF_ref/2)
        mass_para = OWE_para + PL_DOC_para + (reserve_para+BF_para/2)

        Percent_BF = 100*(BF_para-BF_ref)/BF_ref
        Percent_SR = 100 * (SR_para - SR_ref) / SR_ref
        Percent_Mass = 100 * (mass_para - mass_ref) / mass_ref
        data = [
            ["<u>Ref A/C</u>",  "<u>New A/C</u>", "<u>Variation %</u>"],
            ["<i>Block Fuel = </i>  " + "<b>"+str(round(BF_ref,2))+"</b>" + "  [kg]", "<i>Block Fuel = </i>  "+"<b>"+str(round(BF_para,2))+"</b>"+"  [kg]", "<b>"+str(round(Percent_BF,2))+"</b>"],
            ["<i>Mean Specific Range = </i>  "+ "<b>"+str(round(SR_ref,3))+"</b>" + "  [NM/kg]", "<i>Mean Specific Range = </i>  "+"<b>"+str(round(SR_para,3))+"</b>" +"  [NM/kg]", "<b>"+str(round(Percent_SR,2))+"</b>"],
            ["<i>Mean Mass = </i>  " + "<b>"+str(round(mass_ref, 2))+"</b>" + "  [kg]", "<i>Mean Mass = </i>  " + "<b>"+str(round(mass_para, 2))+"</b>" + "  [kg]","<b>"+str(round(Percent_Mass, 2))+"</b>"],
            ]
        table_widget = widgets.GridBox(children=[widgets.HTML(str(value)) for row in data for value in row],
            layout=widgets.Layout(grid_template_columns="repeat(3, auto)",width='100%'))

        buttonINFO = widgets.Button(description='')
        buttonINFO.icon = 'fa-info-circle'
        buttonINFO.layout.width = 'auto'
        buttonINFO.layout.height = 'auto'
        output = widgets.Output()

        def info_message(event):
            with output:
                output.clear_output()
                if len(output.outputs) > 0:
                    output.clear_output()

                else:
                    print('Block Fuel is computed for Max Range at Max Payload.\n'
                          'The mass used to compute the Specific Range is the average over the climb and cruise phase.\n'
                          'BF/Npax-BF is computed at DOC (TLAR RANGE at SPP)'
                          )
        buttonINFO.on_click(info_message)
        infobox = widgets.Box(children=[buttonINFO, output], layout=Layout(border='0px solid black',
                                                                           margin='50 0 50 0px', padding='5px',
                                                                           align_items='center', width='100'))
        #Plot the payload-range diagramm

        if self.var_owe == None:
            self.var_owe =0
        if self.var_mtow == None:
            self.var_mtow = 0
        fig=self.OAD.para_payload_range(ac_ref,SFC_ref,var_owe=None,var_mtow=None,name="REF AC",Color='blue')

        fig=self.OAD.para_payload_range(ac_para,SFC_para,self.var_owe,self.var_mtow,"NEW AC",fig=fig,Color='red')


        fig2=self.OAD.Npax_BF_Diagramm(ac_ref,SFC_ref,"REF AC",Color='blue')
        fig2=self.OAD.Npax_BF_Diagramm(ac_para,SFC_para,"NEW AC",fig=fig2,Color='red')

        C_V_BlockFuel = widgets.VBox(children=[fig2,table_widget,infobox],
            layout=widgets.Layout(border='1px solid black', align_items='center', padding='2px', width='100%'))

        C_para1 = widgets.HTML(value=" <b><u>Analysis Toolbox</u></b>")
        C_para2 = widgets.HTML(value=" <b>Incremental Developments Applied: </b>" + "," .join(self.ID_Type))

        self.tab_Analysis_Para = widgets.Tab(children=[fig,C_V_BlockFuel],
                                             layout=widgets.Layout(border='0px solid black', align_items='center', padding='2px', width='100%'))
        self.tab_Analysis_Para.set_title(0, 'Payload - Range ')
        self.tab_Analysis_Para.set_title(1, 'BF/Npax & SR')
        C_Vertical_Para = widgets.VBox(children=[C_para1,C_para2,self.tab_Analysis_Para],
            layout=widgets.Layout(border='5px solid black', align_items='center', padding='5px', width='100%'))

        display(C_Vertical_Para)
        print('Problem solved.')
        print("------------------NEW PERFORMANCE COMPUTED----------------------------")














    def GEO3D(self,Model3dFile):
        # -------------------------------------------------------------------------------------------------
        OuputFolder="OUTPUT_FILE"
        Base_folder = "Base files"
        WORK_FOLDER_PATH = "CSMworkdir"

        # Check if the destination folder already exists
        if os.path.exists(WORK_FOLDER_PATH):
            # If it does, delete the existing folder and its contents
            shutil.rmtree(WORK_FOLDER_PATH)
        # Copies contents of base file to new work folder
        shutil.copytree(Base_folder, WORK_FOLDER_PATH)

        csm_file = os.path.join(WORK_FOLDER_PATH, "CsmBaseModel.csm")
        batch_file = os.path.join(WORK_FOLDER_PATH, "ESP.bat")
        # -------------------------------------------------------------------------------------------------
        self.MODEL3D_Liste_Name=Model3dFile
        xml_data_file = os.path.join(WORK_FOLDER_PATH, self.MODEL3D_Liste_Name[0])

        # -------------------------------------------------------------------------------------------------

        # Opening the xml file in read mode
        with open(xml_data_file, "r") as xml_obj:
            # coverting the xml data to a Python ordered dictionary
            data_dict_ordered = xmltodict.parse(xml_obj.read())
            # closing the file
            xml_obj.close()
            # print(data_dict_ordered)

        # converts nested ordered dict to dict
        data_dict = {}
        data_dict = json.loads(json.dumps(data_dict_ordered))
        # print(data_dict)
        # filters out the necessary geometry data values
        geometry_dict = data_dict['FASTOAD_model']['data']['geometry']
        # print(geometry_dict)
        area = geometry_dict['aircraft']['wetted_area']

        # -------------------------------------------------------------------------------------------------

        xml_parameters = {}

        def update_globals(d, namespace):
            for k, v in d.items():
                if 'is_input' in k or '@units' in k:  # removes unwanted variables
                    continue

                if isinstance(v, dict):  # this line checks if v is a dictionary
                    update_globals(v, namespace + k + '_')
                else:
                    # This assigns each entry of the dict to a global variable
                    # This also removes the _#text from the end of the variable names
                    # globals()[(namespace + k).removesuffix('_#text')] = round(float(v),5)
                    xml_parameters[(namespace + k).removesuffix('_#text')] = round(float(v), 5)
                    # xml_parameters[f"{namespace}{k[:-5]}"] = round(float(v),5)

        # -------------------------------------------------------------------------------------------------

        update_globals(geometry_dict, '')

        # -------------------------------------------------------------------------------------------------

        data_file = []
        with open(csm_file, 'r') as data:
            for line in data.readlines():
                data_file.append(line)
            data.close()
        # List of CSM variable names - XML variable names
        variables = {  # 'test':'test',
            'fus:height': 'fuselage_maximum_height',
            'fus:width': 'fuselage_maximum_width',
            'fus:length': 'fuselage_length',
            'fus:front_length': 'fuselage_front_length',
            'fus:rear_length': 'fuselage_rear_length',
            'fus:width': 'fuselage_maximum_width',
            'fus:length': 'fuselage_length',
            'wing:mac:Xat25': 'wing_MAC_at25percent_x',
            'wing:mac:leadingX': 'wing_MAC_leading_edge_x_local',
            'wing:mac:length': 'wing_MAC_length',
            'wing:kink:leadingX': 'wing_kink_leading_edge_x_local',
            'wing:kink:y': 'wing_kink_y',
            'wing:tip:leadingX': 'wing_tip_leading_edge_x_local',
            'wing:tip:y': 'wing_tip_y',
            'vtp:mac25:Xat25': 'vertical_tail_MAC_at25percent_x_local',
            'vtp:mac25:wingMac': 'vertical_tail_MAC_at25percent_x_from_wingMAC25',
            'vtp:sweep:0': 'vertical_tail_sweep_0',
            'vtp:span': 'vertical_tail_span',
            'htp:mac25:Xat25': 'horizontal_tail_MAC_at25percent_x_local',
            'htp:mac25:wingMac': 'horizontal_tail_MAC_at25percent_x_from_wingMAC25',
            'htp:sweep:0': 'horizontal_tail_sweep_0',
            'htp:span': 'horizontal_tail_span',
            # 'wing:root:Y':,#
            # 'wing:root:Z':'wing_root_z',#
            'wing:root:c': 'wing_root_chord',
            'wing:root:t': 'wing_root_thickness_ratio',
            # 'wing:root:m':'wing_root_camber',#
            # 'wing:root:a':'wing_root_aoa',#
            # 'wing:kink:Y':,#
            'wing:kink:c': 'wing_kink_chord',
            'wing:kink:t': 'wing_kink_thickness_ratio',
            # 'wing:kink:m':'wing_kink_camber',#
            # 'wing:kink:a':'wing_kink_aoa',#
            'wing:tip:c': 'wing_tip_chord',
            'wing:tip:t': 'wing_tip_thickness_ratio',
            # 'wing:tip:m':'wing_tip_camber',#
            # 'wing:tip:a':'wing_tip_aoa',#
            'htp:root:c': 'horizontal_tail_root_chord',
            'htp:root:t': 'horizontal_tail_thickness_ratio',
            # 'htp:root:m':'',#
            # 'htp:root:a':'',#
            'htp:tip:c': 'horizontal_tail_tip_chord',
            'htp:tip:t': 'horizontal_tail_thickness_ratio',
            # 'htp:tip:m':'',#
            # 'htp:tip:a':'',#
            'vtp:root:c': 'vertical_tail_root_chord',
            'vtp:root:t': 'vertical_tail_thickness_ratio',
            # 'vtp:root:m':'',#
            # 'vtp:root:a':'',#
            'vtp:tip:c': 'vertical_tail_tip_chord',
            'vtp:tip:t': 'vertical_tail_thickness_ratio',
            # 'vtp:tip:m':'',#
            # 'vtp:tip:a':'',#
        }

        # Make a dict with updated values
        csm_values = {}
        for i, j in variables.items():
            # print(j)
            #csm_values[i] = xml_parameters[j]
            if j in xml_parameters:
                 csm_values[i] = xml_parameters[j]
                 # print(xml_parameters[j])

            else:
                continue

        # -------------------------------------------------------------------------------------------------

        def updateCSM(data_file, csm_file):
            count = 0
            tempString = ''
            val = 0
            des = 'DESPMTR'

            while count < len(data_file):
                tempString = data_file[count].split()  # splits line with search word
                for i in csm_values:
                    if des in data_file[count] and (i in data_file[count]):
                        val = tempString[tempString.index(i) + 1]  # finds next word of search word, i.e, the value
                        data_file[count] = data_file[count].replace(val, str(
                            csm_values[i]))  # replaces the value with chosen value
                        # If value was found and replaced, search is ended
                        break
                    else:
                        continue
                count += 1
                # find old file name and add 'updated'
            new_file = os.path.basename(csm_file)
            new_file = ('Updated_' + new_file)
            new_file_path = os.path.join(WORK_FOLDER_PATH, new_file)
            print(new_file_path)
            # Creating a new .csm file with changes
            # opening file in 'w' or write mode
            with open(new_file_path, 'w') as x:
                for i in data_file:
                    x.write(i)

                x.close()
            return new_file

        # -------------------------------------------------------------------------------------------------

        new_file = updateCSM(data_file, csm_file)
        print(new_file)
        print("Charging Model...")

        # -------------------------------------------------------------------------------------------------

        # editing ESP run batch file
        # opening file in 'r' or read mode
        batch_file_data = []
        with open(batch_file, 'r') as x:
            for line in x.readlines():
                batch_file_data.append(line)
            x.close()
        batch_file_path = (os.getcwd() + "\\" + WORK_FOLDER_PATH)
        count = 0
        while count < len(batch_file_data):
            if 'cd /d ' in batch_file_data[count]:
                batch_file_data[count] = 'cd /d ' + batch_file_path
            elif 'serveCSM' in batch_file_data[count]:
                batch_file_data[count] = '\nserveCSM "' + new_file + '"'
            # else:
            #     data_file[len(data_file)-1] = 'cd /d ' + new_file_path
            #     data_file.append('serveCSM "' + new_file + '"')

            count += 1

        with open(batch_file, 'w') as x:
            for i in batch_file_data:
                x.write(i)
            x.close()

            # -------------------------------------------------------------------------------------------------

        # %%capture captured_output
        with open('CSMworkdir\esp_logs.txt', 'w') as outfile:
            subprocess.run(['CSMworkdir\ESP.bat'], stdout=outfile, text=True)



        
        
        
        
        

        
        
        
    
        
        

        


        
    
