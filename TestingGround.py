import numpy as np              # linear algebra
import pandas as pd             # data processing, CSV file I/O (e.g. pd.read_csv)
import glob

from DataFunctions import *     # functions stored in separate file

# LP_DIR = "/mnt/c/Users/david/OneDrive - The University of Melbourne/Work/2021/Capstone/MLTeam//DataProcessing/"
PC_DIR = "/mnt/d/Education/Unimelb/OneDrive - Unimelb Student/OneDrive - The University of Melbourne/Work/2021/Capstone/MLTeam/DataProcessing/"
DATAPATH = PC_DIR +"recordings/"


all_filepaths = glob.glob(DATAPATH + "*.csv")
