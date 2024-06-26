"""
This file contains the text of the tutorial, sorted by slide.
"""

class Slide:
    class Introduction:
        WELCOME = "Welcome! In this app, you are going to "\
            "design a derivative of a reference aircraft of your choice."

        SELECTION = "When you have finished reading this tutorial, "\
        "please select the source file of a reference aircraft below."
        
        NOTA = "(You can always come back to this tutorial and file "\
        "selection by clicking on the logo of FAST-OAD at the top.)"
    
    class Process:
        GLOBAL = "You will have the possibility to make Multi "\
        "Disciplinary Analyses (MDA) or Multi Disciplinary Optimizations (MDO)."
        
        MDA = "The first one is a process that, with given inputs, will solve "\
        "the multidisciplinary couplings using the different nested solvers in "\
        "the model, and compute all outputs."
        
        MDO = "The second will, with a set of design variables and constraints, "\
        "try to optimize an objective variable."

    class Inputs:
        EXPLANATIONS = "After choosing the source file, you will have to set your inputs:"
        DASH_1 =  "- Choose between doing a MDA or a MDO"
        DASH_2 = "- Write a name for the output"
        DASH_3 = "- Use the sliders and buttons to configure your inputs"
        DASH_4 = "- And launch your process !"
    
    class Launch:
        EXPLANATIONS = "When launching, the inputs are retrieved and merged with the source "\
        "file other inputs."\
        "Then process is set up (association of all the modules together to make them loop) "\
        "and the evolution of the process is plotted. When the graph stops plotting, it is done!"

    class Configuration:
        EXPLANATIONS = "You have the possibility to see N2 and XDSM graphs. Both represents "\
        "the way FAST-OAD modules interact with each other, what variables are inputs and outputs. "
    
    class Outputs:
        SELECTION = "When you are done with your processes, you can open a second tab to "\
        "display graphs on the outputs you got. "\
        "Simply select all the outputs you want to compare, and they will display. "\
        "For some graphs you can display variants:"
        
        WARNING = "WARNING : Some graphs can only display a single output. You will "\
        "have to select which output you want to plot."