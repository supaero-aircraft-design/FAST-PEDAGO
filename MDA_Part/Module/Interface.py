from IPython.display import display,clear_output
import os
import ipywidgets as widgets
from ipywidgets import Layout
from Module.OAD import*
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
        table=["Aircraft reference","Configuration file","Aircraft inputs","Run MDA","Results Analysis","Optimization"]
        title=widgets.HTML(value=" <b>FAST-OAD ANALYSIS </b>")
        layout_button=Layout(width='16.5%', height='80px', border='4px solid black')
        layout_box = Layout(width='100%',padding='10px')
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        self.Button_M1=widgets.Button(description=table[0], layout=layout_button, style=dict(button_color="#00d600"))
        self.Button_M2=widgets.Button(description=table[1], layout=layout_button, style=dict(button_color='#ebebeb'))
        self.Button_M3=widgets.Button(description=table[2], layout=layout_button, style=dict(button_color='#ebebeb'))
        self.Button_M4=widgets.Button(description=table[3], layout=layout_button, style=dict(button_color='#ebebeb'))
        self.Button_M5=widgets.Button(description=table[4], layout=layout_button, style=dict(button_color='#ebebeb'))
        self.Button_M6=widgets.Button(description=table[5], layout=layout_button, style=dict(button_color='#ebebeb'))
        
        self.Button_M1.on_click(self.menu_to_reference)
        self.Button_M2.on_click(self.menu_to_configuration)
        self.Button_M3.on_click(self.menu_to_input)
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
    
   


 # Function to move from the principal menu to the configuration file interface
    def menu_to_configuration(self,event):
        clear_output()
        self.conf=self.configuration_file(self.path2)
    
   #The Interface for choosing the reference aircraft file 

    def dropdown_configuration(self,change):
        print("Your choose  "+ str(change.new) + " as configuration file.")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        config=self.OAD.Configuration_File(self.path2,change.new)
        
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
    
     #Delete the configuration file 
    
    def delete_configuration(self,event):
        clear_output()
        display(self.BOX_CONFIG)
        self.delete_conf=self.OAD.Delete_File('data\oad_sizing.yml')
        print("Your configuration file suppressed")
        
        print("Choose yourconfiguration file ")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------------------------------------------------")
        return self.delete_conf
    
    
    def configuration_file(self,path_to_target):
        self.path_to_target=path_to_target
        self.path_to_file_list = []
        temp=os.listdir(self.path_to_target)
        for i in range(0, len(temp)):
            if temp[i][-3:] =='yml':
                self.path_to_file_list.append(temp[i])
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        title=widgets.HTML(value=" <b>Choose your configuration file file</b>")     
        datafile_name = widgets.Dropdown(options=self.path_to_file_list,description='Choose your file:',disabled=False,style={'description_width': 'initial'})
        datafile_name.observe(self.dropdown_configuration,names="value")
        box1 = widgets.HBox(children=[title],layout=layout_title)
        box2=widgets.HBox(children=[datafile_name])
        
        Button_F1=widgets.Button(description="Modules list",layout=Layout(width='20%', height='50px', border='4px solid black'),style=dict(button_color='#ebebeb'))
        Button_F1.on_click(self.view_modules)
        
        Button_F2=widgets.Button(description="Variables list",layout=Layout(width='20%', height='50px', border='4px solid black'),style=dict(button_color='#ebebeb'))
        Button_F2.on_click(self.view_variables)
        
        Button_F3=widgets.Button(description="N2 Diagramm",layout=Layout(width='20%', height='50px', border='4px solid black'),style=dict(button_color='#ebebeb'))
        Button_F3.on_click(self.n2_diagramm)
        
        Button_F4=widgets.Button(description="XDSM Diagramm",layout=Layout(width='20%', height='50px', border='4px solid black'),style=dict(button_color='#ebebeb'))
        Button_F4.on_click(self.xdsm_diagramm)
        
        box3=widgets.HBox(children=[Button_F1,Button_F2,Button_F3,Button_F4],layout=Layout(justify_content='space-between',width='100%'))
        
        Button_F5=widgets.Button(description="BACK",layout=Layout(width='20%', height='45px', border='4px solid black'),style=dict(button_color='#3785d8'))
        Button_F5.on_click(self.configuration_to_reference)
        
        Button_F6=widgets.Button(description="Delete",layout=Layout(width='20%', height='45px', border='4px solid black'),style=dict(button_color='#ff5252'))
        Button_F6.on_click(self.delete_configuration)
        
        Button_F7=widgets.Button(description="NEXT",layout=Layout(width='20%', height='45px', border='4px solid black'),style=dict(button_color='#77db5c'))
        Button_F7.on_click(self.configuration_to_input)
            
        box4=widgets.HBox(children=[Button_F5,Button_F6,Button_F7],layout=Layout(justify_content='space-between',width='100%'))
        self.BOX_CONFIG=widgets.VBox(children=[box1,box2,box3,box4],layout=Layout(border='6px solid green', padding='10px', align_items='center', width='100%'))
        display(self.BOX_CONFIG)
        return datafile_name
    
    
    def view_input_data(self,event):
        clear_output()
        display(self.BOX_INPUT)
        self.INPUT_FILE=self.OAD.Generate_Input_File()
        self.input_view_data=self.OAD.View_inputs_data(self.INPUT_FILE)
        return self.input_view_data
        
    
# User interfaces for the inputs phases

# Principal inputs UI

    def inputs_ui(self):
        
        table1=["Aircraft Inputs Data","Edit Inputs Data","Save Inputs Data"]
        table2=["BACK", "Delete Inputs Data", "NEXT"]
        title=widgets.HTML(value=" <b>AIRCRFAT INPUTS DATA </b>")
        layout_button=Layout(width='30%', height='40px', border='4px solid black')
        layout_box = Layout(width='100%',padding='10px')
        layout_title= widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
        Button_I1=widgets.Button(description=table1[0], layout=layout_button, style=dict(button_color='#ebebeb'))
        Button_I1.on_click(self.view_input_data)
        
        Button_I2=widgets.Button(description=table1[1], layout=layout_button, style=dict(button_color='#ebebeb'))
        Button_I3=widgets.Button(description=table1[2], layout=layout_button, style=dict(button_color='#ebebeb'))
        
        Button_I4=widgets.Button(description=table2[0], layout=Layout(width='30%', height='40px', border='4px solid #3785d8'), style=dict(button_color='#3785d8'))
        Button_I4.on_click(self.input_to_configuration)
        
        Button_I5=widgets.Button(description=table2[1], layout=Layout(width='30%', height='40px', border='4px solid  #ff5252'), style=dict(button_color='#ff5252'))
        
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
        
        
        


        
    
