import numpy as np              # linear algebra
import pandas as pd             # data processing, CSV file I/O (e.g. pd.read_csv)
import glob

from DataFunctions import *     # functions stored in separate file

# LP_DIR = "/mnt/c/Users/david/OneDrive - The University of Melbourne/Work/2021/Capstone/MLTeam//DataProcessing/"
PC_DIR = "/mnt/d/Education/Unimelb/OneDrive - Unimelb Student/OneDrive - The University of Melbourne/Work/2021/Capstone/MLTeam/DataProcessing/"
DATAPATH = PC_DIR +"recordings/"


PC_DIR = "/mnt/d/Education/Unimelb/OneDrive - Unimelb Student/OneDrive - The University of Melbourne/Work/2021/Capstone/MLTeam/DataProcessing/"
DATAPATH = PC_DIR +"recordings/"
all_filepaths = glob.glob(DATAPATH + "*.csv")

name = all_filepaths[0]
csvfile = open(name, 'r')
reader = csv.reader(csvfile)
listHeader = next(reader)
listHeader += ["Intent","ExpID"]
csvHeader = list2string(listHeader,True)

currState = 0

# Keep looping til end of csv
for row in reader:
    
    if not (currState == row[ID_CURRSTATE]):
        currState = row[ID_CURRSTATE]
        print("State: "+currState)
    
    
    if(int(row[ID_CURRSTATE]) in STATIONARY_STATES):
        count = 0
        prevState = str(row[ID_CURRSTATE])        
        for row2 in reader:
            if not (int(prevState) == int(row2[ID_CURRSTATE])):
                break
            count+=1;
            
        nextState = str(int(row2[ID_CURRSTATE]))
        print("Prev: "+prevState+", Next: "+nextState+" - "+str(count))
        
        
        
    