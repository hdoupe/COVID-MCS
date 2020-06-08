import sys
import os
import json
import numpy as np
import pandas as pd
import sys
import paramtools
import rpy2.robjects as ro
import rpy2.robjects.packages as rp
import warnings



# Install packages if they are not already installed
# utils.install_packages("quadprog", repos = "https://cloud.r-project.org")
# utils.install_packages("lubridate", repos = "https://cloud.r-project.org")
# utils.install_packages("dplyr", repos = "https://cloud.r-project.org")


utils = rp.importr("utils")
base = rp.importr("base")
dplyr = rp.importr("dplyr")



CURRENT_PATH = os.path.abspath(os.path.dirname("mcs_shape"))
mcs_shapes = os.path.join(CURRENT_PATH, "main.R")


class COVID_MCS_PARAMETERS(paramtools.Parameters) :
    defaults = os.path.join(CURRENT_PATH, "defaults.json")

class COVID_MCS_TEST:
    """
    Parameters:

    adjustment_file: a json file with adjusted parameters.

    """
    ADJ_PATH = os.path.join(CURRENT_PATH, "adjustment_file.json")

    def __init__(self, adjustment = ADJ_PATH):
        self.params = COVID_MCS_PARAMETERS()
        self.adjustment = self.adjust_inputs()
        self.params.adjust(self.adjustment)

    def adjust_inputs(self):
        self.adjustment = self.ADJ_PATH
        return self.adjustment

    def run_model(self):
        nested = self.params.Nested[0].get('value')
        shapes = self.params.Shapes[0].get('value').split(', ')
        t = self.params.Days[0].get('value').split(',')
        t = list(map(int, t))
        n = self.params.NumTests[0].get('value').split(',')
        n = list(map(int, n))
        y1 = self.params.NumPositive[0].get('value').split(',')
        alpha = self.params.Alpha[0].get('value')
        ceil = np.float64(self.params.Ceil[0].get('value'))
        lag = self.params.Lag[0].get('value')
        seed = self.params.Seed[0].get('value')
        seed = float(seed)
        nsim = self.params.nsim[0].get('value')

        if seed == 0:
            seed = ro.r("NULL")

        # Intitalize R object and source main
        r1 = ro.r
        r1['source'](mcs_shapes)

        z = r1['mcs_shapes'](t = ro.IntVector(t), n =  ro.IntVector(n), y1 = ro.IntVector(y1),
                             shape=  ro.StrVector(shapes), ceiling = float(ceil), lag = float(lag))
        zb = r1['mcs_shapes_boot'](z = z, nsim = float(nsim), seed = seed)
        m = r1['mcs_shapes_test'](z, zb, nested = False, alpha = .1)
        t = r1['summary'](m)


c = COVID_MCS_TEST()
c.run_model()
