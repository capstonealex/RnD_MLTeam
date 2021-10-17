from ControlParameters import *
from CommandIndex import *

# =============================================================================
# === Import, IO, CSV and File Directory things =============================== 
# =============================================================================
import sys
import glob
import csv
import os
from pdb import set_trace as bp

# output filenames
FNAME_EXTRACTION = "extractionIndex.txt"
FNAME_DESCRIPTION = "intentTrail.txt"


DIR_CWD  = os.getcwd()
DIR_RAW = DIR_CWD + "/RawRecords/"
DIR_INTENT = DIR_CWD + "/CSVperIntent/" 
DIR_MERGE = DIR_CWD + "/CSVperModel/"
DIR_MODEL = DIR_CWD + "/MLModelObjects/"
all_filepaths = glob.glob(DIR_RAW + "*.csv")





def checkDirectoryRAW():
    if not (os.path.isdir(DIR_RAW)):
        os.mkdir(DIR_RAW)
        print("Please Insert Data into: RawRecords")
        sys.exit(1)
        
def checkMakeDirectoryIntent():
    if not (os.path.isdir(DIR_INTENT)):
        os.mkdir(DIR_INTENT)

def checkMakeDirectoryMerge():
    if not (os.path.isdir(DIR_MERGE)):
        os.mkdir(DIR_MERGE)

def checkMakeDirectoryModel():
    if not (os.path.isdir(DIR_MODEL)):
        os.mkdir(DIR_MODEL)



# =============================================================================
# === CSV Processing ==========================================================
# =============================================================================

# <-> Converts a list of strings to a string
# tog == True means already string
#     == False convert cell to string
def list2string(inlist, tog):
    strlist = ""
    for cell in inlist:
        if tog:
            strlist += cell + ","
        else:
            strlist += str(cell) + ","
    strlist = strlist[:-1]
    return(strlist)



# <-> Converts a full csv to string form
def csvList2String(csvList,tog):
    outString = ""
    for rowList in csvList:
        outString += list2string(rowList,tog)
        outString = outString +"\n"
    return outString



# <-> Converts strings in list cells to numeric
def numifyStringList(rowList):
    out = []
    for i in rowList:
        out.append(float(i))
    return(out)





# =============================================================================
# === Extract Intent ==========================================================
# =============================================================================

# <-> 2D List of csv rows
def getSelectRows(row):
    out = []
    for ind in SELECTROWS:
        out.append(row[ind])
    return out

# <-> Data Recording when crutch data is being populated
def notRecording(row):
    for i in range(1,13):
        if not i==0:
            return False
    
    return True


# <-> Cuts to filter Record time and  Sampling rate
def sampleIntent(csvList, timeIntent):
    # convert to samples and sample rate
    sampleRate = int(100/SAMPLE_RATE)
    
    endRec = len(csvList)
    startRec = endRec - timeIntent
    
    filterList = []
    for i in range(startRec, endRec, sampleRate):
        filterList.append(csvList[i])
    #bp()
    return filterList



# <-> Label the intent
def labelIntent(csvList, intentLabel, intent_ID):
    out = []
    for listRow in csvList:
        tmp = listRow + [intentLabel, intent_ID]
        out.append(tmp)
    #bp()
    return out





# =============================================================================
# === Miscellaneous ===========================================================
# =============================================================================

# <-> Extracts prev and next State from file name
# TODO: there's definitely a smarter way to do this
def namesplitter(filename):
    attribSplit = filename.split("-")
    intent = attribSplit[1]
    sr = attribSplit[2]
    tr = attribSplit[3]
    
    sr = sr.split("_")[1]
    tr = tr.split("_")[1]
    
    return((intent,sr,tr))

def intentIdentify(file):
    with open(file,'r') as csvfile:
        fcsv = csv.reader(csvfile)
        next(fcsv)                              # in case I want to implment headers
        sampleLine = next(fcsv)
        intent = sampleLine[ID_CURRSTATE]       # currentState and Intent line up, fix this if modified in the future
        separate = intent.split('~')
        return((separate[0],separate[1]))
    

# <-> Extracts prev and next State from file name
def intentAccumulate(dic,intent):
    if intent in dic.keys():
        dic[intent] += 1
    else:
        dic[intent] = 0
    return(dic)

def intentDic2String(intentCounter):
    # Extract Intent Counter Dictionary to txt
    strIntentCounter = "Intent, Count\n"
    for key in intentCounter:
        strIntentCounter+= key + ", " + str(intentCounter[key]) + "\n"
    strIntentCounter+="\n"
    
    return (strIntentCounter)