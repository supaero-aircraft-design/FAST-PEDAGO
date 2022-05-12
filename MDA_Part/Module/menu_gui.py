import os
import ipywidgets as widgets
from IPython.display import display
from ipywidgets import Button, Layout,HBox,VBox,HTML
from Module.Configuration_ui import Menu_1
def fon(b):
    menu3=Menu_1()
    
import csv
def Menu():
    path='Table\menu.csv'
    table = []
    f = open(path)
    myreader = csv.reader(f, delimiter=';')
    headings = next(myreader)
    for row in myreader:
        table.append(row[0])
        
    h1=widgets.HTML(value=" <b>MDA Menu</b>")
    
    layout=Layout(width='16.5%', height='80px', border='2px solid green')     
    # override the default width of the button to 'auto' to let the button grow
    Menu_layout = Layout(border='4px solid black',width='100%',padding='10px')
    box_layout = widgets.Layout(display='flex',flex_flow='column',align_items='center',width='50%')
    Button_M1=Button(description=table[0], layout=layout, style=dict(button_color='lightgreen'))
    Button_M2=Button(description=table[1], layout=layout, style=dict(button_color='lightgreen'))
    Button_M3=Button(description=table[2], layout=layout, style=dict(button_color='lightgreen'))
    Button_M4=Button(description=table[3], layout=layout, style=dict(button_color='lightgreen'))
    Button_M5=Button(description=table[4], layout=layout, style=dict(button_color='lightgreen'))
    Button_M6=Button(description=table[5], layout=layout, style=dict(button_color='lightgreen'))
    but = [Button_M1,Button_M2,Button_M3,Button_M4,Button_M5,Button_M6]
    box2 = HBox(children=but,layout=Menu_layout)
    box1 = widgets.HBox(children=[h1],layout=box_layout)
    form = VBox(children=[box1,box2], layout=Layout(border='6px solid green', padding='10px', align_items='center', width='100'))
    display(form)
    Button_M1.on_click(fon)
    
    
    

    
    



