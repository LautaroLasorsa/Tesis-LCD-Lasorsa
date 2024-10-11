import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import inspect

def SaveFig(fig):
    llamador = inspect.stack()[1]
    ruta_llamador = llamador.filename
    nombre_script = os.path.basename(ruta_llamador)
    nombre = os.path.splitext(nombre_script)[0]
    fig.savefig("../figuras/"+nombre+".png", bbox_inches='tight')