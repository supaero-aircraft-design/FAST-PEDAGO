import ipywidgets as widgets
from ipywidgets import Button, Layout,HBox,VBox
import csv
def Menu():
    path='Liste\menu.csv'

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
    but = [Button(description=word, layout=layout, style=dict(button_color='lightgreen')) for word in table]
    box2 = HBox(children=but,layout=Menu_layout)
    box1 = widgets.HBox(children=[h1],layout=box_layout)
    form = VBox(children=[box1,box2], layout=Layout(border='6px solid green', padding='10px', align_items='center', width='100'))
    display(form)

    
    



