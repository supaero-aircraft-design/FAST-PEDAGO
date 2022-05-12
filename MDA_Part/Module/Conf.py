def Configuration():
    import os.path as pth
    import sys
    import logging
    import shutil
    import warnings

    warnings.filterwarnings(action='ignore')

    import openmdao.api as om

    import fastoad.api as oad
    sys.path.append(pth.abspath("."))
    import ipywidgets as widgets
    out = widgets.Output()
    display(out)
    with out:
        print('All necessary imports done')
    logging.basicConfig(level=logging.INFO, format="%(levelname)-8s: %(message)s")
    DATA_FOLDER_PATH = "data"
    WORK_FOLDER_PATH = "workdir"