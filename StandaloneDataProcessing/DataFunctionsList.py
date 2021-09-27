from ControlParameters import *
from CommandIndex import *

# =============================================================================
# === Import, IO, CSV and File Directory things =============================== 
# =============================================================================
import sys
import glob
import csv
import os

DIR_CWD  = os.getcwd()
DIR_RAW = DIR_CWD + "/RawRecords/"
DIR_INTENT = DIR_CWD + "/CSVperIntent/" 
DIR_MODEL = DIR_CWD + "/Final_CSVperModel/"
all_filepaths = glob.glob(DIR_RAW + "*.csv")

# output filenames
FNAME_EXTRACTION = "extractionIndex.txt"
FNAME_DESCRIPTION = "intentTrail.txt"

def checkDirectoryRAW():
    if not (os.path.isdir(DIR_RAW)):
        os.mkdir(DIR_RAW)
        print("Please Insert Data into: RawRecords")
        sys.exit(1)
        
def checkMakeDirectoryIntent():
    if not (os.path.isdir(DIR_INTENT)):
        os.mkdir(DIR_INTENT)

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
def sampleIntent(csvList):
    # convert to samples and sample rate
    recordTime = RECORD_TIME*100;
    sampleRate = int(100/SAMPLE_RATE)
    
    # Added delay here if needed
    captureDelay = CAPTURE_DELAY*100
    
    endRec = len(csvList) - captureDelay
    startRec = endRec - recordTime
    
    filterList = []
    for i in range(startRec, endRec, sampleRate):
        filterList.append(csvList[i])
    
    return filterList



# <-> Label the intent
def labelIntent(csvList, intentLabel, intent_ID):
    out = []
    for listRow in csvList:
        listRow.append(intentLabel)
        listRow.append(intent_ID)
        
        out.append(listRow)
    
    return out





# =============================================================================
# === Miscellaneous ===========================================================
# =============================================================================

# <-> Extracts prev and next State from file name
# TODO: there's definitely a smarter way to do this
def namesplitter(filename):
    split1 = filename.split('_')[1]
    split2 = split1.split('~')
    prevstate = split2[0]
    nextstate = ((split2[1]).split('.'))[0]

    return((prevstate, nextstate))

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