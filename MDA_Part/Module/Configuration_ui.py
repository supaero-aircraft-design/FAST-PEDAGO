from ipywidgets import Button, Layout,HBox,VBox,HTML
from IPython.display import display
def Menu_1():
    text = 'OAD Configuration'
    widget1 = HTML(value = f"<b><font color='blue'>{text}</b>")
    table=['Import','Use Folder','Refrence File','Configuration file']
    layout=Layout(display='flex',flex_flow='column',align_items='center',width='50%')
    box_layout =Layout(display='flex',flex_flow='column',align_items='center',width='50%')
    Menu_layout = Layout(width='100%',padding='5px',display='center')
    Button_C1=Button(description=table[0], layout=layout, style=dict(button_color='red'))
    Button_C2=Button(description=table[1], layout=layout, style=dict(button_color='red'))
    Button_C3=Button(description=table[2], layout=layout, style=dict(button_color='red'))
    Button_C4=Button(description=table[3], layout=layout, style=dict(button_color='red'))
    but=[Button_C1,Button_C2,Button_C3,Button_C4]
    box1 =HBox(children=[widget1],layout=box_layout)
    box2 = HBox(children=but,layout=Menu_layout)
    box=VBox(children=[box1,box2],layout=Layout(border='6px solid blue', padding='10px', align_items='center', width='100'))
    display(box)
    return box