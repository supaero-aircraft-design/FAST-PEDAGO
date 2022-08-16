from IPython.display import display,clear_output
import os
import fastoad.api as oad
import openmdao.api as om
import ipywidgets as widgets
from ipywidgets import Layout
from Module.OAD import*
import csv
import yaml
import statistics
import plotly.graph_objects as go
class Interface:
    
    
    def __init__(self):
        self.path1="File\Reference"
        self.path2="File\Configuration"
        self.OAD=MDA()
               
        

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
        
    #The principal FAST-OAD ANALYSIS INTERFACE
    def Menu(self):
        table=["REFERENCE","CONFIGURATION","AIRCRAFT DATA","MDA","ANALYSIS","OPTIMIZATION"]
        title=widgets.HTML(value=" <b>FAST OVERALL AIRCRAFT DESIGN </b>")
        layout_button=Layout(width='17%', height='80px', border='4px solid black')
        layout_box = Layout(width='100%')
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        self.Button_M1=widgets.Button(description=table[0], layout=layout_button, style=dict(button_color="#00d600"))
        self.Button_M2=widgets.Button(description=table[1], layout=layout_button, style=dict(button_color='#ebebeb'))
        self.Button_M3=widgets.Button(description=table[2], layout=layout_button, style=dict(button_color='#ebebeb'))
        self.Button_M4=widgets.Button(description=table[3], layout=layout_button, style=dict(button_color='#ebebeb'))
        self.Button_M5=widgets.Button(description=table[4], layout=layout_button, style=dict(button_color='#ebebeb'))
        self.Button_M6=widgets.Button(description=table[5], layout=layout_button, style=dict(button_color='#ebebeb'))
        
        self.Button_M1.on_click(self.menu_to_reference)
        self.Button_M2.on_click(self.configuration_file)
        self.Button_M3.on_click(self.menu_to_input)
        self.Button_M4.on_click(self.MDA_UI)
        self.Button_M5.on_click(self.POST_PROCESSING_UI)
        self.Button_M6.on_click(self.OPT_DESIGN)
        
        but=[self.Button_M1,self.Button_M2,self.Button_M3,self.Button_M4,self.Button_M5,self.Button_M6]
        
        file=open("Images/bwb.PNG", "rb")
        image=file.read()
        img=widgets.Image(value=image,format="PNG",width="100%",height="50 px")
    
        box1 = widgets.HBox(children=[title],layout=layout_title)
        box2=widgets.HBox(children=but,layout=layout_box)
        box3=widgets.HBox(children=[img])
        self.menu=widgets.VBox(children=[box1,box2,box3],layout=Layout(border='6px solid green',margin='100 0 100 0px', padding='10px', align_items='center', width='100'))
        
        return self.menu
    
#function to move from the principal menu to the aircraft_reference interface

    def menu_to_reference(self,event):
        clear_output()
        self.ref=self.reference_aircraft(self.path1)
        print("REFERNCE AIRCRAFT PHASE")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        return self.ref


    

#The Interface for choosing the reference aircraft file   
    
        
    def dropdown_reference(self,change):
       
        ref=self.OAD.Source_File(self.path1,change.new)
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
        display(self.menu)
        print("CONFIGRATION PHASE")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------------------------")
    

   #User interface for the reference aircrfat choice step
        

    def reference_aircraft(self,path_to_target):
        
        self.path_to_target=path_to_target
        self.path_to_file_list = []
        temp=os.listdir(self.path_to_target)
        for i in range(0, len(temp)):
            if temp[i][-3:] =='xml':
                self.path_to_file_list.append(temp[i])
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        title=widgets.HTML(value=" <b>Choose your reference aircraft file</b>") 
        box1 = widgets.HBox(children=[title],layout=layout_title)
        datafile_name = widgets.Dropdown(options=self.path_to_file_list,description='Choose your file:',disabled=False,style={'description_width': 'initial'})
        datafile_name.observe(self.dropdown_reference,names="value")
        box2=widgets.HBox(children=[datafile_name])
        
       # Display the data of your reference aircraft 
        Button_S1=widgets.Button(description="Reference data",layout=Layout(width='20%', height='50px', border='4px solid black'),style=dict(button_color='#adadad'))
        Button_S1.on_click(self.view_source)
        
        # Delete the reference aircraft file already choser
        Button_S2=widgets.Button(description="Delete",layout=Layout(width='20%', height='50px', border='4px solid black'),style=dict(button_color='#ff5252'))
        Button_S2.on_click(self.delete_reference)
        
        
        # Show the principal interface user for   the configuration step 
        
        
        Button_S3=widgets.Button(description="Next",layout=Layout(width='20%', height='50px', border='4px solid black'),style=dict(button_color='#77db5c'))
        Button_S3.on_click (self.reference_to_configuration)
        
        box3=widgets.HBox(children=[Button_S1,Button_S2,Button_S3],layout=Layout(justify_content='space-between',width='100%'))
        self.REF_BOX=widgets.VBox(children=[box1,box2,box3],layout=Layout(border='6px solid green', padding='10px', align_items='center', width='100%'))
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
        
        
        
        
        Button_F1=widgets.Button(description="Modules list",layout=Layout(width='20%', height='50px', border='4px solid black'),style=dict(button_color='#ebebeb'))
        Button_F1.on_click(self.view_modules)
        
        Button_F2=widgets.Button(description="Variables list",layout=Layout(width='20%', height='50px', border='4px solid black'),style=dict(button_color='#ebebeb'))
        Button_F2.on_click(self.view_variables)
        
        Button_F3=widgets.Button(description="N2 Diagramm",layout=Layout(width='20%', height='50px', border='4px solid black'),style=dict(button_color='#ebebeb'))
        Button_F3.on_click(self.n2_diagramm)
        
        Button_F4=widgets.Button(description="XDSM Diagramm",layout=Layout(width='20%', height='50px', border='4px solid black'),style=dict(button_color='#ebebeb'))
        Button_F4.on_click(self.xdsm_diagramm)
        
        box2=widgets.HBox(children=[Button_F1,Button_F2,Button_F3,Button_F4],layout=Layout(justify_content='space-between',width='100%'))
        
        Button_F5=widgets.Button(description="BACK",layout=Layout(width='20%', height='45px', border='4px solid black'),style=dict(button_color='#3785d8'))
        Button_F5.on_click(self.configuration_to_reference)
        
        
        Button_F6=widgets.Button(description="NEXT",layout=Layout(width='20%', height='45px', border='4px solid black'),style=dict(button_color='#77db5c'))
        Button_F6.on_click(self.configuration_to_input)
            
        box3=widgets.HBox(children=[Button_F5,Button_F6],layout=Layout(justify_content='space-between',width='100%'))
        self.BOX_CONFIG=widgets.VBox(children=[box1,self.module,button, box2,box3],layout=Layout(border='6px solid green', padding='10px', align_items='center', width='100%'))
        display(self.BOX_CONFIG)
      
    
 #WRITE THE CHOSEN MODULES IN THE CONFIGURATION FILE
    def Write_Configuration_File(self,event):
        clear_output()
        display(self.BOX_CONFIG)
        modules=self.module.value
        self.OAD.write_configuration(modules)
        file_name="oad_sizing.yml"
        
        self.OAD.Configuration_File(file_name)
        
    # Function back to the aircrft reference file user
    def configuration_to_reference(self,event):
        clear_output()
        display(self.REF_BOX)
        
    # Configuration step to inputs data step
    
    def configuration_to_input (self,event):
        clear_output()
        self.Button_M2.style.button_color='#ebebeb'
        self.Button_M3.style.button_color="#00d600"
        display(self.menu)
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
        
        table1=["VIEW AIRCRAFT DATA","EDIT AIRCRAFT INPUT DATA","SAVE AIRCRAFT  INPUT FILE"]
        table2=["BACK", "DELETE INPUT FILE", "NEXT"]
        title=widgets.HTML(value=" <b>AIRCRFAT INPUTS DATA </b>")
        layout_button=Layout(width='30%', height='40px', border='4px solid black')
        layout_box = Layout(width='100%',padding='10px')
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        Button_I1=widgets.Button(description=table1[0], layout=layout_button, style=dict(button_color='#ebebeb'))
        Button_I1.on_click(self.view_input_data)
        
        Button_I2=widgets.Button(description=table1[1], layout=layout_button, style=dict(button_color='#ebebeb'))
        Button_I2.on_click(self.Inputs_Edit_Ui)
        Button_I3=widgets.Button(description=table1[2], layout=layout_button, style=dict(button_color='#ebebeb'))
        Button_I3.on_click(self.Save_In_F_UI)
       
        
        Button_I4=widgets.Button(description=table2[0], layout=Layout(width='30%', height='40px', border='4px solid #3785d8'), style=dict(button_color='#3785d8'))
        Button_I4.on_click(self.input_to_configuration)
        
        Button_I5=widgets.Button(description=table2[1], layout=Layout(width='30%', height='40px', border='4px solid  #ff5252'), style=dict(button_color='#ff5252'))
        Button_I5.on_click(self.input_aircraft_file)

        
        Button_I6=widgets.Button(description=table2[2], layout=Layout(width='30%', height='40px', border='4px solid  #77db5c'), style=dict(button_color='#77db5c'))
        Button_I6.on_click(self.input_to_mda)
        
        box1 = widgets.HBox(children=[title],layout=Layout(display='flex',flex_flow='column',align_items='center',width='70%'))
        box2=widgets.HBox(children=[Button_I1,Button_I2,Button_I3],layout=Layout(justify_content='space-between',width='100%'))
        box3=widgets.HBox(children=[Button_I4,Button_I5,Button_I6],layout=Layout(justify_content='space-between',width='100%'))
        self.BOX_INPUT=widgets.VBox(children=[box1,box2,box3],layout=Layout(border='6px solid green', padding='10px', align_items='center', width='100%'))
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
        display(self.menu)
        print("MDA ANALYSIS PHASE")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        
        
#INTERFCE FOR THE AIRCRAFT INPUT DATA

    def Inputs_Edit_Ui(self,event):
        clear_output()
        display(self.BOX_INPUT)
        self.INPUT=self.OAD.Input_File(self.INPUT_FILE)
        
        #Layout widget
        layout=widgets.Layout(width="50%", height='50px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        layout_button=widgets.Layout(width='30%', height='50px', border='4px solid black')
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')
        
        #TLARS UI
        self.T_value1=self.INPUT["data:TLAR:NPAX"].value[0]
        self.T_value2=self.INPUT["data:TLAR:approach_speed"].value[0]
        self.T_value3=self.INPUT["data:TLAR:cruise_mach"].value[0]
        self.T_value4=self.INPUT["data:TLAR:range"].value[0]
       
        
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
        
        self.TLAR_1=widgets.BoundedFloatText(min=100,max=400,step=1,value=self.T_value1, disabled=False,description=T_Table4[0],description_tooltip=T_Table3[0],style=style,layout=layout)
        self.TLAR_2=widgets.BoundedFloatText(min=10,max=100,step=0.01,value=self.T_value2,disabled=False,description=T_Table4[1],description_tooltip=T_Table3[1],style=style,layout=layout)
        self.TLAR_3=widgets.BoundedFloatText(min=0,max=1,step=0.01,value=self.T_value3,disabled=False,description=T_Table4[2],description_tooltip=T_Table3[2],style=style,layout=layout)
        self.TLAR_4=widgets.BoundedIntText(min=500,max=5000,step=1,value=self.T_value4,disabled=False,description=T_Table4[3],description_tooltip=T_Table3[3],style=style,layout=layout)
        
        T_box_T=widgets.VBox(children=[ self.TLAR_1,self.TLAR_2,self.TLAR_3,self.TLAR_4], layout=widgets.Layout(border='3px solid black',align_items='center', padding='10px', width='100%'))
        self.T_box=widgets.VBox(children=[T_title,T_box_T,T_Button],layout=layout_box)

        
        
        
        #GEOMETRY UI
        
        #FUSELAGE UI
        self.C_value1=self.INPUT["data:geometry:cabin:aisle_width"].value[0]
        self.C_value2=self.INPUT["data:geometry:cabin:exit_width"].value[0]
        self.C_value3=self.INPUT["data:geometry:cabin:containers:count_by_row"].value[0]
        self.C_value4=self.INPUT["data:geometry:cabin:crew_count:technical"].value[0]
        self.C_value5=self.INPUT["data:geometry:cabin:seats:economical:count_by_row"].value[0]
        self.C_value6=self.INPUT["data:geometry:cabin:seats:economical:length"].value[0]
        self.C_value7=self.INPUT["data:geometry:cabin:seats:economical:width"].value[0]
        
        C_path1="Table/cab_name.csv"
        C_path2="Table/cab_unit.csv"
        C_path3="Table/cab_des.csv"
        C_Table1=self.csv_to_table(C_path1)
        C_Table2=self.csv_to_table(C_path2)
        C_Table3=self.csv_to_table(C_path3)
        C_Table4=[C_Table1[i]+C_Table2[i] for i in range(len(C_Table1))]
        C_title=widgets.HTML(value=" <b>FUSELAGE </b>")
        C_Button=widgets.Button(description="Save",layout=layout_button,style=dict(button_color="#33ffcc"))
        C_Button.on_click(self.Save_FUSELAGE)
        
        self.CAB_1=widgets.BoundedFloatText(min=0,max=2,step=0.001,value=self.C_value1,disabled=False,description=C_Table4[0],description_tooltip=C_Table3[0],style=style,layout=layout)
        self.CAB_2=widgets.BoundedFloatText(min=0,max=2,step=0.001,value=self.C_value2,disabled=False,description=C_Table4[1],description_tooltip=C_Table3[1],style=style,layout=layout)
        self.CAB_3=widgets.BoundedFloatText(min=0,max=4,step=1,value=self.C_value3,disabled=False,description=C_Table4[2],description_tooltip=C_Table3[2],style=style,layout=layout)
        self.CAB_4=widgets.BoundedFloatText(min=1,max=4,step=1,value=self.C_value4,disabled=False,description=C_Table4[3],description_tooltip=C_Table3[3],style=style,layout=layout)
        self.CAB_5=widgets.BoundedFloatText(min=1,max=10,step=1,value=self.C_value5,disabled=False,description=C_Table4[4],description_tooltip=C_Table3[4],style=style,layout=layout)
        self.CAB_6=widgets.BoundedFloatText(min=0,max=2,step=0.001,value=self.C_value6,disabled=False,description=C_Table4[5],description_tooltip=C_Table3[5],style=style,layout=layout)
        self.CAB_7=widgets.BoundedFloatText(min=0,max=2,step=0.001,value=self.C_value7,disabled=False,description=C_Table4[6],description_tooltip=C_Table3[6],style=style,layout=layout)
        
        C_file=open("Images/cabin.PNG", "rb")
        C_image=C_file.read()
        C_img=widgets.Image(value=C_image,format="PNG",width="45%",height="100%")
        C_box_C=widgets.VBox(children=[self.CAB_1,self.CAB_2,self.CAB_3,self.CAB_4,self.CAB_5,self.CAB_6,self.CAB_7],layout=widgets.Layout(border='3px solid black',align_items='center', padding='10px', width='100%'))
        self.C_box=widgets.VBox(children=[C_title,C_box_C,C_img,C_Button],layout=layout_box)
        
        
        #WING UI
        self.W_value1=self.INPUT["data:geometry:wing:aspect_ratio"].value[0]
        self.W_value2=self.INPUT["data:geometry:wing:sweep_25"].value[0]
        self.W_value3=self.INPUT["data:geometry:wing:virtual_taper_ratio"].value[0]
        self.W_value4=self.INPUT["data:geometry:wing:kink:span_ratio"].value[0]
        self.W_value5=self.INPUT["data:geometry:wing:spar_ratio:front:kink"].value[0]
        self.W_value6=self.INPUT["data:geometry:wing:spar_ratio:front:root"].value[0]
        self.W_value7=self.INPUT["data:geometry:wing:spar_ratio:front:tip"].value[0]
        self.W_value8=self.INPUT["data:geometry:wing:spar_ratio:rear:kink"].value[0]
        self.W_value9=self.INPUT["data:geometry:wing:spar_ratio:rear:root"].value[0]
        self.W_value10=self.INPUT["data:geometry:wing:spar_ratio:rear:tip"].value[0]
        
        W_path1="Table/wing_name.csv"
        W_path2="Table/wing_unit.csv"
        W_path3="Table/wing_des.csv"
        W_Table1=self.csv_to_table(W_path1)
        W_Table2=self.csv_to_table(W_path2)
        W_Table3=self.csv_to_table(W_path3)
        W_Table4=[W_Table1[i]+W_Table2[i] for i in range(len(W_Table1))]
        W_title=widgets.HTML(value=" <b> WING GEOMETRY </b>")
        
        W_Button=widgets.Button(description="Save",tooltip="Save data to the aircraft inputs file",layout=layout_button,style=dict(button_color="#33ffcc"))
        W_Button.on_click(self.Save_WING)
        
        self.WING_1=widgets.BoundedFloatText(min=4,max=20,step=0.01,value=self.W_value1,disabled=False,description=W_Table4[0],description_tooltip=W_Table3[0],style=style,layout=layout)
        self.WING_2=widgets.BoundedFloatText(min=15,max=60,step=0.001,value=self.W_value2,disabled=False,description=W_Table4[1],description_tooltip=W_Table3[1],style=style,layout=layout)
        self.WING_3=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.W_value3,disabled=False,description=W_Table4[2],description_tooltip=W_Table3[2],style=style,layout=layout)
        self.WING_4=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.W_value4,disabled=False,description=W_Table4[3],description_tooltip=W_Table3[3],style=style,layout=layout)
        self.WING_5=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.W_value5,disabled=False,description=W_Table4[4],description_tooltip=W_Table3[4],style=style,layout=layout)
        self.WING_6=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.W_value6,disabled=False,description=W_Table4[5],description_tooltip=W_Table3[5],style=style,layout=layout)
        self.WING_7=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.W_value7,disabled=False,description=W_Table4[6],description_tooltip=W_Table3[6],style=style,layout=layout)
        self.WING_8=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.W_value8,disabled=False,description=W_Table4[7],description_tooltip=W_Table3[7],style=style,layout=layout)
        self.WING_9=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.W_value9,disabled=False,description=W_Table4[8],description_tooltip=W_Table3[8],style=style,layout=layout)
        self.WING_10=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.W_value10,disabled=False,description=W_Table4[9],description_tooltip=W_Table3[9],style=style,layout=layout)
        W_box_W=widgets.VBox(children=[self.WING_1,self.WING_2,self.WING_3,self.WING_4,self.WING_5,self.WING_6,self.WING_7,self.WING_8,self.WING_9,self.WING_10],layout=widgets.Layout(border='3px solid black',align_items='center', padding='10px', width='100%'))
        W_file=open("Images/Wing.PNG", "rb")
        W_image=W_file.read()
        W_img=widgets.Image(value=W_image,format="PNG",width="100%",height="50%")
        self.W_box=widgets.VBox(children=[W_title,W_box_W,W_img, W_Button],layout=layout_box)
        
        
        #FLAPS UI
        self.F_value1=self.INPUT["data:geometry:flap:chord_ratio"].value[0]
        self.F_value2=self.INPUT["data:geometry:flap:span_ratio"].value[0]
        
        F_path1="Table/flap_name.csv"
        F_path2="Table/flap_unit.csv"
        F_path3="Table/flap_des.csv"
        F_Table1=self.csv_to_table(F_path1)
        F_Table2=self.csv_to_table(F_path2)
        F_Table3=self.csv_to_table(F_path3)
        F_Table4=[F_Table1[i]+F_Table2[i] for i in range(len(F_Table1))]
        F_title=widgets.HTML(value=" <b> FLAPS </b>")
        F_Button=widgets.Button(description="Save",tooltip="Save data to the aircraft inputs file",layout=layout_button,style=dict(button_color="#33ffcc"))
        F_Button.on_click(self.Save_FLAPS)
        
        self.FLAP_1=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.F_value1,disabled=False,description=F_Table4[0],description_tooltip=F_Table3[0],style=style,layout=layout)
        self.FLAP_2=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.F_value2,disabled=False,description=F_Table4[1],description_tooltip=F_Table3[1],style=style,layout=layout)
        
        F_box_F=widgets.VBox(children=[ self.FLAP_1,self.FLAP_2], layout=widgets.Layout(border='3px solid black',align_items='center', padding='10px', width='100%'))
        F_file=open("Images/flaps.PNG", "rb")
        F_image=F_file.read()
        F_img=widgets.Image(value=F_image,format="PNG",width="70%",height="100%")
        self.F_box=widgets.VBox(children=[F_title,F_box_F,F_img, F_Button],layout=layout_box)
        
        
        #SLATS UI
        self.S_value1=self.INPUT["data:geometry:slat:chord_ratio"].value[0]
        self.S_value2=self.INPUT["data:geometry:slat:span_ratio"].value[0]
        
        S_path1="Table/slat_name.csv"
        S_path2="Table/slat_unit.csv"
        S_path3="Table/slat_des.csv"
        S_Table1=self.csv_to_table(S_path1)
        S_Table2=self.csv_to_table(S_path2)
        S_Table3=self.csv_to_table(S_path3)
        S_Table4=[S_Table1[i]+S_Table2[i] for i in range(len(S_Table1))]
        S_title=widgets.HTML(value=" <b> SLATS </b>")
        S_Button=widgets.Button(description="Save",tooltip="Save data to the aircraft inputs file",layout=layout_button,style=dict(button_color="#33ffcc"))
        S_Button.on_click(self.Save_SLATS)
        
        self.SLAT_1=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.S_value1,disabled=False,description=S_Table4[0],description_tooltip=S_Table3[0],style=style,layout=layout)
        self.SLAT_2=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.S_value2,disabled=False,description=S_Table4[1],description_tooltip=S_Table3[1],style=style,layout=layout)
        
        S_box_S=widgets.VBox(children=[self.SLAT_1,self.SLAT_2], layout=widgets.Layout(border='3px solid black',align_items='center', padding='10px', width='100%'))
        S_file=open("Images/SLATS.PNG", "rb")
        S_image=S_file.read()
        S_img=widgets.Image(value=S_image,format="PNG",width="70%",height="100%")
        self.S_box=widgets.VBox(children=[S_title,S_box_S,S_img, S_Button],layout=layout_box)
        
        
        #HORIZONTAL TAIL UI
        self.H_value1=self.INPUT["data:geometry:horizontal_tail:aspect_ratio"].value[0]
        self.H_value2=self.INPUT["data:geometry:horizontal_tail:sweep_25"].value[0]
        self.H_value3=self.INPUT["data:geometry:horizontal_tail:taper_ratio"].value[0]
        self.H_value4=self.INPUT["data:geometry:horizontal_tail:thickness_ratio"].value[0]
        
        H_path1="Table/ht_name.csv"
        H_path2="Table/ht_unit.csv"
        H_path3="Table/ht_des.csv"
        H_Table1=self.csv_to_table(H_path1)
        H_Table2=self.csv_to_table(H_path2)
        H_Table3=self.csv_to_table(H_path3)
        H_Table4=[H_Table1[i]+H_Table2[i] for i in range(len(H_Table1))]
        H_title=widgets.HTML(value=" <b> HORIZONTAL TAIL </b>")
        H_Button=widgets.Button(description="Save",tooltip="Save data to the aircraft inputs file",layout=layout_button,style=dict(button_color="#33ffcc"))
        H_Button.on_click(self.Save_HT)
        
        self.HT_1=widgets.BoundedFloatText(min=1,max=10,step=0.001,value=self.H_value1,disabled=False,description=H_Table4[0],description_tooltip=H_Table3[0],style=style,layout=layout)
        self.HT_2=widgets.BoundedFloatText(min=10,max=50,step=0.1,value=self.H_value2,disabled=False,description=H_Table4[1],description_tooltip=H_Table3[1],style=style,layout=layout)
        self.HT_3=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.H_value3,disabled=False,description=H_Table4[2],description_tooltip=H_Table3[2],style=style,layout=layout)
        self.HT_4=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.H_value4,disabled=False,description=H_Table4[3],description_tooltip=H_Table3[3],style=style,layout=layout)
        
        H_box_H=widgets.VBox(children=[self.HT_1,self.HT_2,self.HT_3,self.HT_4], layout=widgets.Layout(border='3px solid black',align_items='center', padding='10px',width='100%'))
        H_file=open("Images/HT.PNG", "rb")
        H_image=H_file.read()
        H_img=widgets.Image(value=H_image,format="PNG",width="70%",height="100%")
        self.H_box=widgets.VBox(children=[H_title,H_box_H,H_img, H_Button],layout=layout_box)
        
        
        
        #VERTICAL TAIL UI
        self.V_value1=self.INPUT["data:geometry:vertical_tail:aspect_ratio"].value[0]
        self.V_value2=self.INPUT["data:geometry:vertical_tail:sweep_25"].value[0]
        self.V_value3=self.INPUT["data:geometry:vertical_tail:taper_ratio"].value[0]
        self.V_value4=self.INPUT["data:geometry:vertical_tail:thickness_ratio"].value[0]
        
        V_path1="Table/vt_name.csv"
        V_path2="Table/vt_unit.csv"
        V_path3="Table/vt_des.csv"
        V_Table1=self.csv_to_table(V_path1)
        V_Table2=self.csv_to_table(V_path2)
        V_Table3=self.csv_to_table(V_path3)
        V_Table4=[V_Table1[i]+V_Table2[i] for i in range(len(V_Table1))]
        V_title=widgets.HTML(value=" <b> VERTICAL TAIL </b>")
        V_Button=widgets.Button(description="Save",tooltip="Save data to the aircraft inputs file",layout=layout_button,style=dict(button_color="#33ffcc"))
        V_Button.on_click(self.Save_VT)
        
        self.VT_1=widgets.BoundedFloatText(min=1,max=10,step=0.001,value=self.V_value1,disabled=False,description=V_Table4[0],description_tooltip=V_Table3[0],style=style,layout=layout)
        self.VT_2=widgets.BoundedFloatText(min=10,max=50,step=0.1,value=self.V_value2,disabled=False,description=V_Table4[1],description_tooltip=V_Table3[1],style=style,layout=layout)
        self.VT_3=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.V_value3,disabled=False,description=V_Table4[2],description_tooltip=V_Table3[2],style=style,layout=layout)
        self.VT_4=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.V_value4,disabled=False,description=V_Table4[3],description_tooltip=V_Table3[3],style=style,layout=layout)
        
        V_box_V=widgets.VBox(children=[self.VT_1,self.VT_2,self.VT_3,self.VT_4], layout=widgets.Layout(border='3px solid black',align_items='center', padding='10px', width='100%'))
        V_file=open("Images/HT.PNG", "rb")
        V_image=V_file.read()
        V_img=widgets.Image(value=V_image,format="PNG",width="70%",height="100%")
        self.V_box=widgets.VBox(children=[V_title,V_box_V,V_img, V_Button],layout=layout_box)
        
        
        #PROPULSION UI
        self.P_value1=self.INPUT["data:geometry:propulsion:layout"].value[0]
        self.P_value2=self.INPUT["data:geometry:propulsion:engine:count"].value[0]
        self.P_value3=self.INPUT["data:geometry:propulsion:engine:y_ratio"].value[0]
        
        P_path1="Table/prop_name.csv"
        P_path2="Table/prop_unit.csv"
        P_path3="Table/prop_des.csv"
        P_Table1=self.csv_to_table(P_path1)
        P_Table2=self.csv_to_table(P_path2)
        P_Table3=self.csv_to_table(P_path3)
        P_Table4=[P_Table1[i]+P_Table2[i] for i in range(len(P_Table1))]
        P_title=widgets.HTML(value=" <b> PROPULSION GEOMETRY </b>")
        P_Button=widgets.Button(description="Save",tooltip="Save data to the aircraft inputs file",layout=layout_button,style=dict(button_color="#33ffcc"))
        P_Button.on_click(self.Save_P)
        
        self.PROP_1=widgets.BoundedFloatText(min=1,max=2,step=1,value=self.P_value1,disabled=False,description=P_Table4[0],description_tooltip=P_Table3[0],style=style,layout=layout)
        self.PROP_2=widgets.BoundedFloatText(min=1,max=10,step=1,value=self.P_value2,disabled=False,description=P_Table4[1],description_tooltip=P_Table3[1],style=style,layout=layout)
        self.PROP_3=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.P_value3,disabled=False,description=P_Table4[2],description_tooltip=P_Table3[2],style=style,layout=layout)
        
        P_box_P=widgets.VBox(children=[self.PROP_1,self.PROP_2,self.PROP_3], layout=widgets.Layout(border='3px solid black',align_items='center', padding='10px', width='100%'))
        P_file=open("Images/Engine.PNG", "rb")
        P_image=P_file.read()
        P_img=widgets.Image(value=P_image,format="PNG",width="100%",height="100%")  
        self.P_box=widgets.VBox(children=[P_title,P_box_P,P_img, P_Button],layout=layout_box)
        
        #GEOMETRY MENU
        self.tab_GEO = widgets.Tab(children = [self.C_box,self.W_box,self.F_box, self.S_box,self.H_box,self.V_box,self.P_box])
        self.tab_GEO.set_title(0, 'FUSELAGE')
        self.tab_GEO.set_title(1, 'WING')
        self.tab_GEO.set_title(2, 'FLAPS')
        self.tab_GEO.set_title(3, 'SLATS')
        self.tab_GEO.set_title(4, 'HORIZONTAL TAIL')
        self.tab_GEO.set_title(5, 'VERTICAL TAIL')
        self.tab_GEO.set_title(6, 'PROPULSION')
        
        # WEIGHT UI
        self.We_value1=self.INPUT["data:weight:aircraft:max_payload"].value[0]
        self.We_value2=self.INPUT["data:weight:aircraft:payload"].value[0]
        
        We_path1="Table/We_name.csv"
        We_path2="Table/We_unit.csv"
        We_path3="Table/We_des.csv"
        We_Table1=self.csv_to_table(We_path1)
        We_Table2=self.csv_to_table(We_path2)
        We_Table3=self.csv_to_table(We_path3)
        We_Table4=[We_Table1[i]+We_Table2[i] for i in range(len(We_Table1))]
        We_title=widgets.HTML(value=" <b>WEIGHT</b>")
        We_Button=widgets.Button(description="Save",layout=layout_button,style=dict(button_color="#33ffcc"))
        We_Button.on_click(self.Save_WEIGHT)
        self.We_1=widgets.BoundedFloatText(min=10000,max=60000,step=1,value=self.We_value1,disabled=False,description=We_Table4[0],description_tooltip=We_Table3[0],style=style,layout=layout)
        self.We_2=widgets.BoundedFloatText(min=10000,max=60000,step=1,value=self.We_value2,disabled=False,description=We_Table4[1],description_tooltip=We_Table3[1],style=style,layout=layout)
        We_box_We=widgets.VBox(children=[self.We_1,self.We_2], layout=widgets.Layout(border='3px solid black',align_items='center',padding='10px', width='100%'))
        We_file=open("Images/WE.PNG", "rb")
        We_image=We_file.read()
        We_img=widgets.Image(value=We_image,format="PNG",width="100%",height="50%")
        self.We_box=widgets.VBox(children=[We_title,We_box_We,We_img, We_Button],layout=layout_box)
        
        
        
        #AERODYNAMICS UI
        self.A_value1=self.INPUT["data:aerodynamics:aircraft:landing:CL_max_clean_2D"].value[0]
        self.A_value2=self.INPUT["data:aerodynamics:aircraft:takeoff:mach"].value[0]
        
        A_path1="Table/aero_name.csv"
        A_path2="Table/aero_unit.csv"
        A_path3="Table/aero_des.csv"
        A_Table1=self.csv_to_table(A_path1)
        A_Table2=self.csv_to_table(A_path2)
        A_Table3=self.csv_to_table(A_path3)
        A_Table4=[A_Table1[i]+A_Table2[i] for i in range(len(A_Table1))]

        A_title=widgets.HTML(value=" <b> AERODYNAMICS </b>")
        A_Button=widgets.Button(description="Save",tooltip="Save data to the aircraft inputs file",layout=layout_button,style=dict(button_color="#33ffcc"))
        A_Button.on_click(self.Save_AERO)
        
        self.AERO_1=widgets.BoundedFloatText(min=0.5,max=3,step=0.01,value=self.A_value1,disabled=False,description=A_Table4[0],description_tooltip=A_Table3[0],style=style,layout=layout)
        self.AERO_2=widgets.BoundedFloatText(min=0,max=1,step=0.001,value=self.A_value2,disabled=False,description=A_Table4[1],description_tooltip=A_Table3[1],style=style,layout=layout)
        
        A_box_A=widgets.VBox(children=[self.AERO_1,self.AERO_2], layout=widgets.Layout(border='3px solid black',align_items='center', padding='10px', width='100%'))
        A_file=open("Images/aero.PNG", "rb")
        A_image=A_file.read()
        A_img=widgets.Image(value=A_image,format="PNG",width="100%",height="50%")
        self.A_box=widgets.VBox(children=[A_title,A_box_A,A_img, A_Button],layout=layout_box)
        
        
        
        #LOADS UI
        self.L_value1=self.INPUT["data:load_case:lc1:U_gust"].value[0]
        self.L_value2=self.INPUT["data:load_case:lc1:Vc_EAS"].value[0]
        self.L_value3=self.INPUT["data:load_case:lc1:altitude"].value[0]
        self.L_value4=self.INPUT["data:load_case:lc2:U_gust"].value[0]
        self.L_value5=self.INPUT["data:load_case:lc2:Vc_EAS"].value[0]
        self.L_value6=self.INPUT["data:load_case:lc2:altitude"].value[0]
        L_path1="Table/load_name.csv"
        L_path2="Table/load_unit.csv"
        L_path3="Table/load_des.csv"
        L_Table1=self.csv_to_table(L_path1)
        L_Table2=self.csv_to_table(L_path2)
        L_Table3=self.csv_to_table(L_path3)
        L_Table4=[L_Table1[i]+L_Table2[i] for i in range(len(L_Table1))]

        L_title=widgets.HTML(value=" <b> LOADS CASE </b>")
        L_Button=widgets.Button(description="Save",tooltip="Save data to the aircraft inputs file",layout=layout_button,style=dict(button_color="#33ffcc"))
        L_Button.on_click(self.Save_LOAD)

        self.LOAD_1=widgets.BoundedFloatText(min=5,max=50,step=0.01,value=self.L_value1,disabled=False,description=L_Table4[0],description_tooltip=L_Table3[0],style=style,layout=layout)
        self.LOAD_2=widgets.BoundedFloatText(min=100,max=1000,step=0.1,value=self.L_value2,disabled=False,description=L_Table4[1],description_tooltip=L_Table3[1],style=style,layout=layout)
        self.LOAD_3=widgets.BoundedFloatText(min=1000,max=100000,step=1,value=self.L_value3,disabled=False,description=L_Table4[2],description_tooltip=L_Table3[2],style=style,layout=layout)
        self.LOAD_4=widgets.BoundedFloatText(min=5,max=50,step=0.01,value=self.L_value4,disabled=False,description=L_Table4[3],description_tooltip=L_Table3[3],style=style,layout=layout)
        self.LOAD_5=widgets.BoundedFloatText(min=100,max=1000,step=0.001,value=self.L_value5,disabled=False,description=L_Table4[4],description_tooltip=L_Table3[4],style=style,layout=layout)
        self.LOAD_6=widgets.BoundedFloatText(min=1000,max=100000,step=1,value=self.L_value6,disabled=False,description=L_Table4[5],description_tooltip=L_Table3[5],style=style,layout=layout)
        
        L_box_L=widgets.VBox(children=[self.LOAD_1,self.LOAD_2,self.LOAD_3,self.LOAD_4,self.LOAD_5,self.LOAD_6], layout=widgets.Layout(border='3px solid black',align_items='center', padding='10px', width='100%'))
        L_file=open("Images/load.PNG", "rb")
        L_image=L_file.read()
        L_img=widgets.Image(value=L_image,format="PNG",width="100%",height="50%")
        self.L_box=widgets.VBox(children=[L_title,L_box_L,L_img, L_Button],layout=layout_box)
        
        
        #MISSION UI
        
        #MTOW MISSION
        self.MTOW_value1=self.INPUT["data:mission:MTOW_mission:diversion:distance"].value[0]
        self.MTOW_value2=self.INPUT["data:mission:MTOW_mission:holding:duration"].value[0]
        self.MTOW_value3=self.INPUT["data:mission:MTOW_mission:main_route:range"].value[0]
        self.MTOW_value4=self.INPUT["data:mission:MTOW_mission:takeoff:V2"].value[0]
        self.MTOW_value5=self.INPUT["data:mission:MTOW_mission:takeoff:fuel"].value[0]
        
        MTOW_path1="Table/MTOW_name.csv"
        MTOW_path2="Table/MTOW_unit.csv"
        MTOW_path3="Table/MTOW_des.csv"
        MTOW_Table1=self.csv_to_table(MTOW_path1)
        MTOW_Table2=self.csv_to_table(MTOW_path2)
        MTOW_Table3=self.csv_to_table(MTOW_path3)
        MTOW_Table4=[MTOW_Table1[i]+MTOW_Table2[i] for i in range(len(MTOW_Table1))]
        MTOW_title=widgets.HTML(value=" <b>MTOW MISSION </b>")
        MTOW_Button=widgets.Button(description="Save",layout=layout_button,style=dict(button_color="#33ffcc"))
        MTOW_Button.on_click(self.Save_MTOW)
        self.MTOW_1=widgets.BoundedFloatText(min=50,max=500,step=1,value=self.MTOW_value1,disabled=False,description=MTOW_Table4[0],description_tooltip=MTOW_Table3[0],style=style,layout=layout)
        self.MTOW_2=widgets.BoundedFloatText(min=10,max=100,step=1,value=self.MTOW_value2,disabled=False,description=MTOW_Table4[1],description_tooltip=MTOW_Table3[1],style=style,layout=layout)
        self.MTOW_3=widgets.BoundedFloatText(min=1000,max=10000,step=1,value=self.MTOW_value3,disabled=False,description=MTOW_Table4[2],description_tooltip=MTOW_Table3[2],style=style,layout=layout)
        self.MTOW_4=widgets.BoundedFloatText(min=10,max=200,step=0.1,value=self.MTOW_value4,disabled=False,description=MTOW_Table4[3],description_tooltip=MTOW_Table3[3],style=style,layout=layout)
        self.MTOW_5=widgets.BoundedFloatText(min=10,max=200,step=0.1,value=self.MTOW_value5,disabled=False,description=MTOW_Table4[4],description_tooltip=MTOW_Table3[4],style=style,layout=layout)
        MTOW_box_MTOW=widgets.VBox(children=[self.MTOW_1,self.MTOW_2,self.MTOW_3,self.MTOW_4,self.MTOW_5], layout=widgets.Layout(border='3px solid black',align_items='center',padding='10px', width='100%'))
        MTOW_file=open("Images/Mission.PNG", "rb")
        MTOW_image=MTOW_file.read()
        MTOW_img=widgets.Image(value=MTOW_image,format="PNG",width="100%",height="50%")
        self.MTOW_box=widgets.VBox(children=[MTOW_title,MTOW_box_MTOW,MTOW_img, MTOW_Button],layout=layout_box)
        
        #SIZING MISSION
        self.Size_value1=self.INPUT["data:mission:sizing:landing:flap_angle"].value[0]
        self.Size_value2=self.INPUT["data:mission:sizing:landing:slat_angle"].value[0]
        self.Size_value3=self.INPUT["data:mission:sizing:takeoff:flap_angle"].value[0]
        self.Size_value4=self.INPUT["data:mission:sizing:takeoff:slat_angle"].value[0]
        self.Size_value5=self.INPUT["data:mission:sizing:main_route:cruise:altitude"].value[0]
        
        Size_path1="Table/Size_name.csv"
        Size_path2="Table/Size_unit.csv"
        Size_path3="Table/Size_des.csv"
        Size_Table1=self.csv_to_table(Size_path1)
        Size_Table2=self.csv_to_table(Size_path2)
        Size_Table3=self.csv_to_table(Size_path3)
        Size_Table4=[Size_Table1[i]+Size_Table2[i] for i in range(len(Size_Table1))]
        Size_title=widgets.HTML(value=" <b>SIZING MISSION </b>")
        Size_Button=widgets.Button(description="Save",layout=layout_button,style=dict(button_color="#33ffcc"))
        Size_Button.on_click(self.Save_SIZE)
        self.Size_1=widgets.BoundedFloatText(min=10,max=60,step=0.1,value=self.Size_value1,disabled=False,description=Size_Table4[0],description_tooltip=Size_Table3[0],style=style,layout=layout)
        self.Size_2=widgets.BoundedFloatText(min=10,max=60,step=0.1,value=self.Size_value2,disabled=False,description=Size_Table4[1],description_tooltip=Size_Table3[1],style=style,layout=layout)
        self.Size_3=widgets.BoundedFloatText(min=10,max=60,step=0.1,value=self.Size_value3,disabled=False,description=Size_Table4[2],description_tooltip=Size_Table3[2],style=style,layout=layout)
        self.Size_4=widgets.BoundedFloatText(min=10,max=60,step=0.1,value=self.Size_value4,disabled=False,description=Size_Table4[3],description_tooltip=Size_Table3[3],style=style,layout=layout)
        self.Size_5=widgets.BoundedFloatText(min=10000,max=60000,step=100,value=self.Size_value5,disabled=False,description=Size_Table4[4],description_tooltip=Size_Table3[4],style=style,layout=layout)
        Size_box_Size=widgets.VBox(children=[self.Size_1,self.Size_2,self.Size_3,self.Size_4,self.Size_5], layout=widgets.Layout(border='3px solid black',align_items='center',padding='10px', width='100%'))
        Size_file=open("Images/Mission.PNG", "rb")
        Size_image=Size_file.read()
        Size_img=widgets.Image(value=Size_image,format="PNG",width="100%",height="50%")
        self.Size_box=widgets.VBox(children=[Size_title,Size_box_Size,Size_img, Size_Button],layout=layout_box)
    
        
        
        #MISSION MENU
        self.tab_MISS = widgets.Tab(children = [self.MTOW_box,self.Size_box])
        self.tab_MISS.set_title(0, 'MTOW MISSION')
        self.tab_MISS.set_title(1, 'SIZING MISSION')
     
        
         #PROPULSION UI 
        self.PR_value1=self.INPUT["data:propulsion:MTO_thrust"].value[0]
        self.PR_value2=self.INPUT["data:propulsion:rubber_engine:bypass_ratio"].value[0]
        self.PR_value3=self.INPUT["data:propulsion:rubber_engine:design_altitude"].value[0]
        self.PR_value4=self.INPUT["data:propulsion:rubber_engine:maximum_mach"].value[0]
        self.PR_value5=self.INPUT["data:propulsion:rubber_engine:overall_pressure_ratio"].value[0]
        self.PR_value6=self.INPUT["data:propulsion:rubber_engine:turbine_inlet_temperature"].value[0]
        
        PR_path1="Table/pro_name.csv"
        PR_path2="Table/pro_unit.csv"
        PR_path3="Table/pro_des.csv"
        PR_Table1=self.csv_to_table(PR_path1)
        PR_Table2=self.csv_to_table(PR_path2)
        PR_Table3=self.csv_to_table(PR_path3)
        PR_Table4=[PR_Table1[i]+PR_Table2[i] for i in range(len(PR_Table1))]
        PR_title=widgets.HTML(value=" <b>PROPULSION  </b>")
        PR_Button=widgets.Button(description="Save",tooltip="Save data to the aircraft inputs file",layout=layout_button,style=dict(button_color="#33ffcc"))
        PR_Button.on_click(self.Save_PR)
        
        
        self.PR_1=widgets.BoundedFloatText(min=5000,max=500000,step=1,value=self.PR_value1,disabled=False,description=PR_Table4[0],description_tooltip=PR_Table3[0],style=style,layout=layout)
        self.PR_2=widgets.BoundedFloatText(min=1,max=20,step=1,value=self.PR_value2,disabled=False,description=PR_Table4[1],description_tooltip=PR_Table3[1],style=style,layout=layout)
        self.PR_3=widgets.BoundedFloatText(min=1000,max=20000,step=0.1,value=self.PR_value3,disabled=False,description=PR_Table4[2],description_tooltip=PR_Table3[2],style=style,layout=layout)
        self.PR_4=widgets.BoundedFloatText(min=0,max=1,step=0.1,value=self.PR_value4,disabled=False,description=PR_Table4[3],description_tooltip=PR_Table3[3],style=style,layout=layout)
        self.PR_5=widgets.BoundedFloatText(min=1,max=100,step=0.1,value=self.PR_value5,disabled=False,description=PR_Table4[4],description_tooltip=PR_Table3[4],style=style,layout=layout)
        self.PR_6=widgets.BoundedFloatText(min=500,max=3000,step=1,value=self.PR_value6,disabled=False,description=PR_Table4[5],description_tooltip=PR_Table3[5],style=style,layout=layout)
        PR_box_PR=widgets.VBox(children=[self.PR_1,self.PR_2,self.PR_3,self.PR_4,self.PR_5,self.PR_6], layout=widgets.Layout(border='3px solid black',align_items='center', padding='10px', width='100%'))
        PR_file=open("Images/Engine.PNG", "rb")
        PR_image=PR_file.read()
        PR_img=widgets.Image(value=PR_image,format="PNG",width="100%",height="50%")
        self.PR_box=widgets.VBox(children=[PR_title,PR_box_PR,PR_img, PR_Button],layout=layout_box)

            
        
        
        
        #GENERAL INPUTS MENU
        self.tab_IN = widgets.Tab(children = [self.T_box,self.tab_GEO,self.We_box,self.A_box,self.L_box,self.tab_MISS,self.PR_box])
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
        self.INPUT["data:TLAR:NPAX"].value=self.TLAR_1.value
        self.INPUT["data:TLAR:approach_speed"].value=self.TLAR_2.value
        self.INPUT["data:TLAR:cruise_mach"].value=self.TLAR_3.value
        self.INPUT["data:TLAR:range"].value=self.TLAR_4.value
        self.INPUT.save()
        
#SAVE GEOMETRY DATA

#SAVE THE FUSELAGE DATA
    def Save_FUSELAGE(self,event):
        self.INPUT["data:geometry:cabin:aisle_width"].value= self.CAB_1.value
        self.INPUT["data:geometry:cabin:exit_width"].value=self.CAB_2.value
        self.INPUT["data:geometry:cabin:containers:count_by_row"].value=self.CAB_3.value
        self.INPUT["data:geometry:cabin:crew_count:technical"].value=self.CAB_4.value
        self.INPUT["data:geometry:cabin:seats:economical:count_by_row"].value=self.CAB_5.value
        self.INPUT["data:geometry:cabin:seats:economical:length"].value=self.CAB_6.value
        self.INPUT["data:geometry:cabin:seats:economical:width"].value=self.CAB_7.value
        
        self.INPUT.save()

       
    
#SAVE WING DATA

    def Save_WING(self,event):
        self.INPUT["data:geometry:wing:aspect_ratio"].value=self.WING_1.value
        self.INPUT["data:geometry:wing:sweep_25"].value=self.WING_2.value
        self.INPUT["data:geometry:wing:virtual_taper_ratio"].value=1.5*self.WING_3.value
        self.INPUT["data:geometry:wing:kink:span_ratio"].value=self.WING_4.value
        self.INPUT["data:geometry:wing:spar_ratio:front:kink"].value=self.WING_5.value
        self.INPUT["data:geometry:wing:spar_ratio:front:root"].value=self.WING_6.value
        self.INPUT["data:geometry:wing:spar_ratio:front:tip"].value=self.WING_7.value
        self.INPUT["data:geometry:wing:spar_ratio:rear:kink"].value=self.WING_8.value
        self.INPUT["data:geometry:wing:spar_ratio:rear:root"].value=self.WING_9.value
        self.INPUT["data:geometry:wing:spar_ratio:rear:tip"].value=self.WING_10.value
        self.INPUT.save()

        
#SAVE FLAPS DATA
    def Save_FLAPS(self,event):
        self.INPUT["data:geometry:flap:chord_ratio"].value=self.FLAP_1.value
        self.INPUT["data:geometry:flap:span_ratio"].valuevalue=self.FLAP_2.value
        self.INPUT.save()
        
#SAVE SLATS DATA
    def Save_SLATS(self,event):
        self.INPUT["data:geometry:slat:chord_ratio"].value=self.SLAT_1.value
        self.INPUT["data:geometry:slat:span_ratio"].valuevalue=self.SLAT_2.value
        self.INPUT.save()
        
#SAVE HORIZONTAL TAIL  DATA
    def Save_HT(self,event):
        self.INPUT["data:geometry:horizontal_tail:aspect_ratio"].value= self.HT_1.value
        self.INPUT["data:geometry:horizontal_tail:sweep_25"].value=self.HT_2.value
        self.INPUT["data:geometry:horizontal_tail:taper_ratio"].value=self.HT_3.value
        self.INPUT["data:geometry:horizontal_tail:thickness_ratio"].value= self.HT_4.value
        self.INPUT.save()
    
    
        
#SAVE VERITICAL TAIL  DATA
    def Save_VT(self,event):
        self.INPUT["data:geometry:vertical_tail:aspect_ratio"].value= self.VT_1.value
        self.INPUT["data:geometry:vertical_tail:sweep_25"].value=self.VT_2.value
        self.INPUT["data:geometry:vertical_tail:taper_ratio"].value=self.VT_3.value
        self.INPUT["data:geometry:vertical_tail:thickness_ratio"].value= self.VT_4.value
        self.INPUT.save()

    
#SAVE PROPULSION GEOMETRY DATA
    def Save_P(self,event):
        
        self.INPUT["data:geometry:propulsion:layout"].value= self.PROP_1.value
        self.INPUT["data:geometry:propulsion:engine:count"].value= self.PROP_2.value
        self.INPUT["data:geometry:propulsion:engine:y_ratio"].value= self.PROP_3.value
        self.INPUT.save()

#SAVE WEIGHT DATA
    def Save_WEIGHT(self,event):
        self.INPUT["data:weight:aircraft:max_payload"].value=self.We_1.value
        self.INPUT["data:weight:aircraft:payload"].value=self.We_2.value
        self.INPUT.save()      

    
#SAVE AERODYNAMICS DATA
    def Save_AERO(self,event):
        self.INPUT["data:aerodynamics:aircraft:landing:CL_max_clean_2D"].value=self.AERO_1.value
        self.INPUT["data:aerodynamics:aircraft:takeoff:mach"].value=self.AERO_2.value
        self.INPUT.save()

#SAVE LOADS DATA
    def Save_LOAD(self,event):
        self.INPUT["data:load_case:lc1:U_gust"].value=self.LOAD_1.value
        self.INPUT["data:load_case:lc1:Vc_EAS"].value=self.LOAD_2.value
        self.INPUT["data:load_case:lc1:altitude"].value=self.LOAD_3.value
        self.INPUT["data:load_case:lc2:U_gust"].value=self.LOAD_4.value
        self.INPUT["data:load_case:lc2:Vc_EAS"].value=self.LOAD_5.value
        self.INPUT["data:load_case:lc2:altitude"].value=self.LOAD_6.value
        self.INPUT.save()

#SAVE MISSION DATA

#SAVE THE MTOW MISSION DATA
    def Save_MTOW(self,event):
        self.INPUT["data:mission:MTOW_mission:diversion:distance"].value=self.MTOW_1.value
        self.INPUT["data:mission:MTOW_mission:holding:duration"].value=self.MTOW_2.value
        self.INPUT["data:mission:MTOW_mission:main_route:range"].value=self.MTOW_3.value
        self.INPUT["data:mission:MTOW_mission:takeoff:V2"].value=self.MTOW_4.value
        self.INPUT["data:mission:MTOW_mission:takeoff:fuel"].value=self.MTOW_5.value
        self.INPUT.save()


#SAVE THE SIZING MISSION

    def Save_SIZE(self,event):
        self.INPUT["data:mission:sizing:landing:flap_angle"].value=self.Size_1.value
        self.INPUT["data:mission:sizing:landing:slat_angle"].value=self.Size_2.value
        self.INPUT["data:mission:sizing:takeoff:flap_angle"].value=self.Size_3.value
        self.INPUT["data:mission:sizing:takeoff:slat_angle"].value=self.Size_4.value
        self.INPUT["data:mission:sizing:main_route:cruise:altitude"].value=self.Size_5.value
        self.INPUT.save()
        



#SAVE THE ENGINE DATA     
    def Save_PR(self,event):
        self.INPUT["data:propulsion:MTO_thrust"].value=self.PR_1.value
        self.INPUT["data:propulsion:rubber_engine:bypass_ratio"].value=self.PR_2.value
        self.INPUT["data:propulsion:rubber_engine:design_altitude"].value=self.PR_3.value
        self.INPUT["data:propulsion:rubber_engine:maximum_mach"].value=self.PR_4.value
        self.INPUT["data:propulsion:rubber_engine:overall_pressure_ratio"].value=self.PR_5.value
        self.INPUT["data:propulsion:rubber_engine:turbine_inlet_temperature"].value=self.PR_6.value
        self.INPUT["tuning:propulsion:rubber_engine:SFC:k_cr"].value = 1.0
        self.INPUT.save()
        

# SAVE THE INPUT FILE IN A FOLDER WITH ANOTHER NAME 
    def Save_In_F_UI(self,event):
        
        clear_output()
        display(self.BOX_INPUT)
        layout=widgets.Layout(width="50%", height='40px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        layout_button=widgets.Layout(width='30%', height='50px', border='4px solid black')
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')
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
        
        self.DI_BOX=widgets.VBox(children=[box1,box2],layout=Layout(border='6px solid green', padding='10px', align_items='center', width='100%'))
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
        
        table1=["RUN MDA","MISSION ANALYSIS","PARAMETRIC BRANCH"]
        table2=["MDA OUTPUTS ", "SAVE AIRCRAFT DATA", "DELETE AIRCRAFT DATA"]
        table3=["BACK","NEXT"]
        
        layout_button1=widgets.Layout(width='30%', height='60px', border='4px solid black')
        layout_button2=widgets.Layout(width='30%', height='40px', border='4px solid black')
        layout_box1=widgets.Layout(justify_content='space-between',width='100%')
        layout_box2=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')
        
        title=widgets.HTML(value=" <b>MDA ANALYSIS </b>")
        
        Button_MD11=widgets.Button(description=table1[0],tooltip="Run the MDA Design Problem", layout=layout_button1, style=dict(button_color='#ebebeb'))
        Button_MD11.on_click(self.RUN_MDA)
        
        Button_MD12=widgets.Button(description=table1[1], layout=layout_button1, style=dict(button_color='#ebebeb'))
        Button_MD12.on_click(self. Mission_Analysis_UI)
        
        Button_MD13=widgets.Button(description=table1[2], layout=layout_button1, style=dict(button_color='#ebebeb'))
        Button_MD13.on_click(self. PARAMETRIC_UI1)
        
        box1=widgets.HBox(children=[Button_MD11,Button_MD12,Button_MD13],layout=layout_box1)
        
        Button_MD21=widgets.Button(description=table2[0],tooltip="view the outputs of the mda design problem", layout=layout_button2, style=dict(button_color='#ffccb3'))
        Button_MD21.on_click(self.View_Ouput_Data)
        
        Button_MD22=widgets.Button(description=table2[1], layout=layout_button2, style=dict(button_color='#00ffbf'))
        Button_MD22.on_click(self.Save_OUT_F_UI)
        
        Button_MD23=widgets.Button(description=table2[2], layout=layout_button2, style=dict(button_color='#ff5252'))
        Button_MD23.on_click(self.Output_aircraft_file)
        
        box2=widgets.HBox(children=[Button_MD21,Button_MD22,Button_MD23],layout=layout_box1)

        Button_MD31=widgets.Button(description=table3[0], layout=layout_button2, style=dict(button_color='#3785d8'))
        Button_MD31.on_click(self.mda_to_input)
        
        Button_MD32=widgets.Button(description=table3[1], layout=layout_button2, style=dict(button_color='#77db5c'))
        Button_MD32.on_click(self.mda_to_analysis)
        
        box3=widgets.HBox(children=[Button_MD31,Button_MD32],layout=layout_box1)
        
        self.BOX_MDA=widgets.VBox(children=[title,box1,box2,box3],layout=layout_box2)
        display(self.BOX_MDA)
        return self.BOX_MDA
        

        

# RUN THE MDA ANALYSIS
    def RUN_MDA(self,event):
        
        self.MDA_problem=self.OAD.RUN_OAD()
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
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')
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
        self.OPM_value6=self.OUTPUT_DATA["data:mission:MTOW_mission:takeoff:altitude"].value[0]
        self.OPM_value7=self.OUTPUT_DATA["data:mission:MTOW_mission:takeoff:fuel"].value[0]
        self.OPM_value8=self.OUTPUT_DATA["data:mission:MTOW_mission:taxi_in:duration"].value[0]
        self.OPM_value9=self.OUTPUT_DATA["data:mission:MTOW_mission:taxi_out:duration"].value[0]
        self.OPM_value10=self.OUTPUT_DATA["data:mission:MTOW_mission:taxi_out:thrust_rate"].value[0]
        
        
        
        layout=widgets.Layout(width="50%", height='50px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        layout_button=widgets.Layout(width='30%', height='50px', border='4px solid black')
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')
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
        self.OP_INPUT_DATA["data:mission:op_mission:takeoff:altitude"].value=self.OPM_6.value
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
        display(self.menu)
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
        
        self.DO_BOX=widgets.VBox(children=[box1,box2],layout=Layout(border='6px solid green', padding='10px', align_items='center', width='100%'))
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
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%',justify_content='space-between')
        layout_H=widgets.Layout( padding='10px', align_items='center', width='100%',justify_content='space-between')
        title=widgets.HTML(value=" <b>POST-PROCESSING </b>")
        RES_options=["GEOMETRY","MASS BREAKDOWN","AERODYNAMIC","PAYLOAD/RANGE","MISSION"]
        self.RES_choice=widgets.Dropdown(description="CHOOSE THE ANALYSIS TOOL", options=RES_options,style=style,layout=layout)
        RES_Button1=widgets.Button(description="SAVE",tooltip=" CONFIRM THE  CHOOSEN ANALYSIS TOOL",layout=layout_button,style=dict(button_color="#33ffcc"))
        RES_Button1.on_click(self.PLOT_UI)
        
        RES_Button2=widgets.Button(description="BACK",layout=layout_button,style=dict(button_color='#3785d8'))
        RES_Button3=widgets.Button(description="NEXT",layout=layout_button,style=dict(button_color='#77db5c'))
        
        RES_Button2.on_click(self.analysis_to_mda)
        RES_Button3.on_click(self.analysis_to_optimization)
        
        
        box=widgets.HBox(children=[RES_Button2,RES_Button1,RES_Button3],layout=widgets.Layout(justify_content='space-between',width='100%',padding='10 px'))       
        self.RES_box=widgets.VBox(children=[title,self.RES_choice,box],layout=layout_box)
        display(self.RES_box)
    
        
# FUNCTION: FROM THE ANAYSIS PHASE TO OPTIMIZATION PHASE        
        
    def analysis_to_optimization (self,event):
        clear_output()
        self.Button_M5.style.button_color='#ebebeb'
        self.Button_M6.style.button_color="#00d600"
        display(self.menu)
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

        AERO_title=widgets.HTML(value=" <b>GAERODYNAMIC ANALYSIS</b>") 
        AERO_box1 = widgets.HBox(children=[AERO_title],layout=layout_title)
        self.output_file_aero = widgets.SelectMultiple(options=path_to_file_list,description='CHOOSE THE AIRCRAFTS TO ANALYZE:',disabled=False,style={'description_width': 'initial'},layout=widgets.Layout(width="500px", height="150 px"),rows=len(path_to_file_list))
        AERO_box2=widgets.HBox(children=[self.output_file_aero])
        AERO_Button=widgets.Button(description="PLOT",tooltip="PLOT THE DRAG POLAR OF THE SELECTED AIRCRAFTS",layout=layout_button,style=dict(button_color="#33ffcc"))
        AERO_Button.on_click(self.Aerodynamic_Plot)
        self.AERO_UI_BOX=widgets.VBox(children=[AERO_box1,AERO_box2,AERO_Button],layout=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%'))

        
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
        
        self.MASS_UI_BOX=widgets.VBox(children=[MASS_box1,MASS_box2,MASS_box3,MASS_Button],layout=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%'))
        
        
        
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
        
        self.MISS_UI_BOX=widgets.VBox(children=[MISS_box1,MISS_box2,MISS_Button],layout=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%'))
        
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
        
        self.PAY_UI_BOX=widgets.VBox(children=[PAY_box1,PAY_box2,PAY_Button],layout=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%'))
        
        
        
        
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
        elif (self.RES_choice.value=="PAYLOAD/RANGE "):
            clear_output()
            display(self.RES_box)
            display(self.PAY_UI_BOX)
        
        
    
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
            
        
        fig=self.OAD.payload_range(FILE_PATH[0],MISSION_PATH[0])
        k=1
        while (k<len(FILE_PATH)):
            fig=self.OAD.payload_range(FILE_PATH[k],MISSION_PATH[k],fig=fig)
            k=k+1
        
        fig.show()
        
        
        
                
   
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  # # # # # # # # # # # # # # #  # # # # # # # # # # # # #   OPTIMIZATION   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')
        title=widgets.HTML(value=" <b>OPTMIZATION</b>") 
        self.AC_Opt = widgets.Select(options=path_to_file_list,description='CHOOSE THE AIRCRAFT TO OPTIMIZE:',disabled=False,style={'description_width':'initial'},layout=widgets.Layout(width="500px", height="150 px"),rows=len(path_to_file_list))
        AC_Button=widgets.Button(description="SAVE THE CHOICE",tooltip="SAVE THE CHOSEN AIRCRAFT ",layout=layout_button,style=dict(button_color="#33ffcc"))
        AC_Button.on_click(self.OPT_PROBLEM_UI)
        box1=widgets.HBox(children=[self.AC_Opt])
        self.AC_BOX=widgets.VBox(children=[title,self.AC_Opt,AC_Button],layout=layout_box)
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
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')
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
        self.OPT_BOX=widgets.VBox(children=[OPT_Title,DES_BOX,CONS_BOX,OBJ_BOX,OPT_Button],layout=layout_box)
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
        print("OPTIMIZATION PROBLEM SAVED")
        print("-------------------------------------------------------------------------------------------------------------------------")
        layout=widgets.Layout(width="30%", height='40px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        layout_button=widgets.Layout(width='30%', height='50px', border='4px solid black')
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')
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
        
        OPT_Button5=widgets.Button(description="SAVE THE AIRCRFAT DATA ",tooltip="SAVE THE DATA OF THE OPTIMIZED AIRCRFAT",layout=layout_button,style=dict(button_color='#ebebeb'))
        OPT_Button5.on_click(self.Save_OPT_F_UI)
        OPT_Button6=widgets.Button(description="AIRCRAFT ANALYSIS",tooltip="ANALYSE THE OPTIMIZED AIRCRFAT ",layout=layout_button,style=dict(button_color='#ebebeb'))
        OPT_Button6.on_click(self.Opt_Analysis)
        OPT_Button7=widgets.Button(description="CLOSE",tooltip="CLOSE THE OPTIMIZATION WINDOW",layout=layout_button,style=dict(button_color='#FF0800'))
        OPT_Button7.on_click(self.close_optimization )
        box1=widgets.HBox(children=[OPT_Button1,OPT_Button2],layout=layout_H)
        box2=widgets.HBox(children=[OPT_Button3,OPT_Button4],layout=layout_H)
        box3=widgets.HBox(children=[OPT_Button5,OPT_Button6],layout=layout_H)
        self.OPT_BOX=widgets.VBox(children=[title,box1,box2,box3,OPT_Button7],layout=layout_box)
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
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')
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
        display(self.menu)        

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # PARAMETRIC BRANCH # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         

                            
    def PARAMETRIC_UI1(self,event):
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')
        self.List_SFC=[]
        self.List_OWE=[]
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
                
        title=widgets.HTML(value=" <b>INCREMENTAL DEVELOPPEMENT </b>") 
        self.AC=widgets.Select(options=path_to_file_list,description='AIRCRFAT SELECTION:',disabled=False,style={'description_width': 'initial'},layout=widgets.Layout(width="500px", height="150 px"),rows=len(path_to_file_list))
        Button=widgets.Button(description="SAVE",tooltip="SAVE THE SELECTED AIRCRAFT",layout=layout_button,style=dict(button_color="#33ffcc"))
        Button.on_click(self.PARAMETRIC_UI2)
        self.ID1_box=widgets.VBox(children=[title,self.AC,Button],layout=layout_box)
        display(self.ID1_box)
        
        
    def PARAMETRIC_UI2(self,event):
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

        self.OAD.PARA_AC_FILE(aircraft)
        
        
        
        print("THE REFERENCE ARICRAFT SAVED")
        print("-----------------------------------------------------------------------------------------------------")
              
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        layout_H=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%')
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')
        title=widgets.HTML(value=" <b>STEP 1 INCREMENTAL DEVELOPPEMENT </b>") 
        Button1=widgets.Button(description="WEIGHT SAVING",tooltip="MODIFY THE AIRCRAFT OWE",layout=layout_button,style=dict(button_color='#ebebeb'))
        Button1.on_click(self.Weight_Saving_UI)
        Button2=widgets.Button(description="NEO",tooltip="MODIFY THE AIRCRAFT ENGINE",layout=layout_button,style=dict(button_color='#ebebeb'))
        Button2.on_click(self.NEO_UI)
            
        
        Button3=widgets.Button(description="DRAG SAVING",tooltip="MODIFY THE AIRCRAFT DRAG",layout=layout_button,style=dict(button_color='#ebebeb'))
        Button3.on_click(self.Drag_Saving_UI)
        Button4=widgets.Button(description="FUSELAGE STRETCH ",tooltip="MODIFY THE FUSELAGE GEOMETRY",layout=layout_button,style=dict(button_color='#ebebeb'))
        Button4.on_click(self.Fuselage_Stretch_UI)
        
        box_H=widgets.HBox(children=[Button1,Button2,Button3,Button4],layout=layout_H)
        Button=widgets.Button(description="LUNCH ANALYSIS",tooltip="SAVE THE SELECTED AIRCRAFT",layout=layout_button,style=dict(button_color="#33ffcc"))
        Button.on_click(self.INCREMENTAL_DEVELOPEMENT)
        
        self.ID2_box=widgets.VBox(children=[title,box_H,Button],layout=layout_box)
        display(self.ID2_box)
        
    
    def Weight_Saving_UI(self,event):
        path="OUTPUT_FILE"
        file_name="ID_Aircraft_File.xml"
        para_path=pth.join(path,file_name)
        self.Para_Data1=self.OAD.Input_File(para_path)
        self.OWE_REF=self.Para_Data1["data:weight:aircraft:OWE"].value[0]
        self.List_OWE.append(self.OWE_REF)
        
        self.MTOW=self.Para_Data1["data:weight:aircraft:MTOW"].value[0]
        self.Max_Payload=self.Para_Data1["data:weight:aircraft:max_payload"].value[0]
        self.BF_REF=self.MTOW-(self.OWE_REF-self.Max_Payload)
        self.List_BF.append(self.BF_REF)
        
        clear_output()
        display(self.ID1_box)
        display(self.ID2_box)
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        layout_H=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%')
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')
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
        delta_OWE=self.OWES_2.value
        OWE_New=self.OWE_REF+delta_OWE
        self.Para_Data1["data:weight:aircraft:OWE"].value=OWE_New
        self.Para_Data1.save()
        clear_output()
        print("---------------------------------------------------OWE MODIFCATION SAVED-------------------------------------")
        display( self.ID1_box)
        display( self.ID2_box)
            
        
    def NEO_UI(self,event):
        clear_output()
        display(self.ID1_box)
        display(self.ID2_box)
        
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        layout_H=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%')
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')
        layout=widgets.Layout(width="50%", height='50px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        title=widgets.HTML(value=" <b>NEW ENGINE OPTION </b>") 
        self.NEO_1=widgets.BoundedFloatText(min=0,max=100,step=0.001,value=self.List_SFC[0],disabled=True,description="ENGINE SFC (kg/N/s)",description_tooltip="THE SFC OF THE AIRCRAFT ENGINE",style=style,layout=layout)
        self.NEO_2=widgets.BoundedFloatText(min=-100,max=100,step=0.001,value=0,disabled=False,description=" ∆(SFC)",description_tooltip="THE DELTA SFC",style=style,layout=layout)
        self.NEO_2.observe(self.delta_NEO_percent,names="value")
        self.NEO_3=widgets.BoundedFloatText(min=-100,max=100,step=0.001,value=0,disabled=False,description="%∆(SFC)",description_tooltip="THE % OF DELTA SFC",style=style,layout=layout)
        self.NEO_3.observe(self.percent_NEO_delta,names="value")
        Button=widgets.Button(description="SAVE",tooltip="SAVE THE ENGINE MODIFICATION",layout=layout_button,style=dict(button_color="#33ffcc"))
        Button.on_click(self.NEO)
        self.NEO_box=widgets.VBox(children=[title,self.NEO_1,self.NEO_2,self.NEO_3,Button],layout=layout_box)
        display(self.NEO_box)
        
        
    def delta_NEO_percent(self,change):
        delta=self.NEO_2.value
        percent=(delta/self.NEO_1.value)*100
        self.NEO_3.value=percent
        
    def percent_NEO_delta(self,change):
        percent=self.NEO_3.value
        delta=(percent*self.NEO_1.value)/100
        self.NEO_2.value=delta
    def NEO(self,event):
        SFC_NEW=self.List_SFC[0]+self.NEO_2.value
        self.List_SFC.append(SFC_NEW)
        clear_output()
        print("--------------------ENGINE MODIFICATIONS SAVED---------------------")
        display( self.ID1_box)
        display( self.ID2_box)
        
        
            
              
                
           

    def Drag_Saving_UI(self,event):
        path="OUTPUT_FILE"
        file_name="ID_Aircraft_File.xml"
        para_path=pth.join(path,file_name)
        self.Para_Data2=self.OAD.Input_File(para_path)
        self.CD=self.Para_Data2["data:aerodynamics:aircraft:cruise:CD"].value
        finesse=self.Para_Data2["data:aerodynamics:aircraft:cruise:L_D_max"].value[0]
        
        clear_output()
        display(self.ID1_box)
        display(self.ID2_box)
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        layout_button=widgets.Layout(width='40%', height='50px', border='4px solid black')
        layout_H=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%',justify_content='space-between')
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')
        layout=widgets.Layout(width="50%", height='50px',justify_content='space-between')
        style=style={'description_width': 'initial'}
        layout_H=widgets.Layout( padding='10px', align_items='center', width='100%',justify_content='space-between')
        layout_V=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%')
        title=widgets.HTML(value=" <b>DRAG SAVING </b>") 

        self.DRAG_1=widgets.BoundedFloatText(min=0,max=60,step=0.001,value=round(finesse,2),disabled=True,description="(L/D)_max",description_tooltip="max lift/drag ratio in cruise conditions",style=style,layout=layout)
        Button=widgets.Button(description="SAVE",tooltip="SAVE THE DRAG MODIFICATION",layout=layout_button,style=dict(button_color="#33ffcc"))
        
        
        box1=widgets.VBox(children=[self.DRAG_1],layout=layout_V)
        
        
        
        self.DRAG_2=widgets.BoundedFloatText(min=-100,max=0,step=0.001,value=0,disabled=False,description=" %∆(CD)",description_tooltip="%∆ (drag coefficient in cruise conditions)", style=style,layout=layout)
        self.DRAG_2.observe(self.percent_drag_finesse,names="value")
        
        self.DRAG_3=widgets.BoundedFloatText(min=-20,max=20,step=0.001,value=0,disabled=True,description="∆(L/D)_max",description_tooltip="∆ (max lift/drag ratio in cruise conditions)",style=style,layout=layout)
        self.DRAG_4=widgets.BoundedFloatText(min=0,max=100,step=0.001,value=0,disabled=True,description="%∆(L/D)_max",description_tooltip="%∆ (max lift/drag ratio in cruise conditions)",style=style,layout=layout)
       
       
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
        
        delta_finesse=new_finesse-self.DRAG_1.value
        delta_percent_finesse=(delta_finesse*100)/self.DRAG_1.value
        self.DRAG_3.value=round(delta_finesse,2)
        self.DRAG_4.value=round(delta_percent_finesse,2)
    
            
    def Drag_Saving(self,event):
        percent=1+self.DRAG_2.value/100
        new_CD=[cd*percent for cd in self.CD]
        new_finesse=self.DRAG_1.value+self.DRAG_3.value
        path="OUTPUT_FILE"
        file="ID_Aircraft_File.xml"
        para_path=pth.join(path,file)
        para_data=self.OAD.Input_File(para_path)
        para_data["data:aerodynamics:aircraft:cruise:CD"].value=new_CD
        para_data["data:aerodynamics:aircraft:cruise:L_D_max"].value=new_finesse
        para_data.save()
        print("-------------------------------------DRAG MODIFICATIONS SAVED----------------------------------------")
        
    
        
   
    def Fuselage_Stretch_UI(self,event):
        
        path="OUTPUT_FILE"
        file="ID_Aircraft_File.xml"
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
        display(self.ID1_box)
        display(self.ID2_box)
        
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        layout_button=widgets.Layout(width='40%', height='40px', border='4px solid black')
        layout_H=widgets.Layout(border='4px solid black', padding='10px', align_items='center', width='100%')
        layout_box=widgets.Layout(border='6px solid green', padding='10px', align_items='center', width='100%')
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
        # new length
        length=self.FUSE_1.value+self.FUSE_8.value
        # new lift_drag ratio
        finesse=self.FUSE_5.value+self.FUSE_10.value
        # new NPAX1
        Npax=self.FUSE_6.value+self.FUSE_12.value
        # new OWE
        OWE=self.FUSE_7.value+self.FUSE_11.value
        # new PAYLOAD
        Payload=self.FUSE_16.value+self.FUSE_18.value
        
        # new CD0 fuselage 
        part_CD0_fus=1+self.percent_CD0_fus/100
        new_CD0_fus=[cd*part_CD0_fus for cd in self.CD0_fus]
        
        part_CD0_ac=1+self.percent_CD0_ac/100
        new_CD0_ac=[cd*part_CD0_ac for cd in self.CD0_ac]
        
        part_CD_ac=1+self.percent_CD/100
        new_CD_ac=[cd*part_CD_ac for cd in self.CD_ac]
        
        path="OUTPUT_FILE"
        file="ID_Aircraft_File.xml"
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
        
        print("-------------------------------------FUSELAGE STRETCH SSAVED----------------------------------------")
        
        
        
        
        
        
    def INCREMENTAL_DEVELOPEMENT(self,event):
        clear_output()
        display(self.ID2_box)
        ac_ref=self.AC_ref
        mission_ref=self.mission_ref
        
        path_ac="OUTPUT_FILE"
        file_para="ID_Aircraft_File.xml"
        ac_para=pth.join(path_ac,file_para)
        
        # Compute the new redesigned aircraft performance
        print("---------------NEW PERFORMANCE COMPUTING -----------------------")
        print("----------------------3 mn---------------------------------------")
        
        SOURCE=ac_para
        path_config="data"
        file_config="para_performance.yml"
        CONFIGURATION=pth.join(path_config,file_config)
        oad.generate_inputs(CONFIGURATION,SOURCE, overwrite=True)
        oad.evaluate_problem(CONFIGURATION,overwrite=True)
        
        print("------------------NEW PERFORMANCE COMPUTED----------------------------")
        
        
        path_miss="workdir"
        file_miss="para_perfo.csv"
        mission_para=pth.join(path_miss,file_miss)
        
        
        # COMPUTE THE  MEAN_SFC 
        
        
        SFC_ref=float(self.List_SFC[0])
        if (len(self.List_SFC)>1):
            SFC_para=float(self.List_SFC[len(self.List_SFC)-1])
        else:
            SFC_para=self.OAD.para_sfc(mission_para)
        
        # COMPUTE THE MEAN MASS
        mass_ref=self.OAD.mass(mission_ref)
        mass_para=self.OAD.mass(mission_para)
        # COMPUTE THE SPECIFIC RANGE
        SR_ref=self.OAD.compute_SR(ac_ref,SFC_ref,mass_ref)[0]
        SR_para=self.OAD.compute_SR(ac_para,SFC_para,mass_para)[0]
        
        
        # COMPUTE THE BLOCK FUEL
        
        data_ref=self.OAD.Input_File(ac_ref)
        OWE_ref=data_ref["data:weight:aircraft:OWE"].value[0]
        MTOW_ref=data_ref["data:weight:aircraft:MTOW"].value[0]
        Max_Payload_ref=data_ref["data:weight:aircraft:max_payload"].value[0]
        
        BF_ref=MTOW_ref-OWE_ref-Max_Payload_ref
        
        data_para=self.OAD.Input_File(ac_para)
        OWE_para=data_para["data:weight:aircraft:OWE"].value[0]
        MTOW_para=data_para["data:weight:aircraft:MTOW"].value[0]
        Max_Payload_para=data_para["data:weight:aircraft:max_payload"].value[0]
        
        BF_para=MTOW_para-OWE_para-Max_Payload_para
        
        #Plot the payload-range diagramm
        
        fig=self.OAD.para_payload_range(ac_ref,SFC_ref,"REFERENCE AIRCRAFT")

        fig=self.OAD.para_payload_range(ac_para,SFC_para,"REDESIGNED AIRCRAFT",fig=fig)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Indicator(mode = "number+delta",value = BF_para,number={'suffix': " Kg "},title = {"text": "BLOCK FUEL"},domain = {'row': 0, 'column': 0},delta = {'reference': BF_ref, 'relative': True, 'position' : "top"}))
        fig1.add_trace(go.Indicator(mode = "number+delta",value = SR_para,number = {'suffix': " Nm/Kg fuel"},title = {"text": "SPECIFIC RANGE"},domain = {'row': 1, 'column': 0},delta = {'reference': SR_ref, 'relative': True, 'position' : "top"}))
   
        
        fig1.update_layout(paper_bgcolor = "lightgray",height=350,width=1000, grid = {'rows': 2, 'columns': 1, 'pattern': "independent"})
        
        fig2=self.OAD.Npax_BF_Diagramm(ac_ref,"REFERENCE AIRCRAFT")
        fig2=self.OAD.Npax_BF_Diagramm(ac_para,"REDESIGNED AIRCRAFT",fig=fig2)
        
        
        display(fig,fig2,fig1)
        
        


        
        
        
        
        

        
        
        
    
        
        

        


        
    
