RECORD_TIME = 1;    # seconds: intent before movement
SAMPLE_RATE = 50;    # samples wanted per second (cannot exceed 100)

import pandas as pd             # data processing, CSV file I/O (e.g. pd.read_csv)
import glob
import csv

ALLINTENTS = ["sitting","walking"]
def filenameIntent(filepath):
    for intent in ALLINTENTS:
        if (intent in filepath.lower()):
            return intent

FILLEDROW = 44

ID_CURRSTATE = -2
SELECTROWS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, ID_CURRSTATE]      # time = 0, nonzero features are 29 -> 38 incl
STATIONARY_STATES = [4,2,5];

# <-> 2D List of csv rows
def getSelectRows(row):
    out = []
    for ind in SELECTROWS:
        out.append(row[ind])
    return out

# <-> Converts strings in list cells to numeric
def numifyStringList(rowList):
    out = []
    for i in rowList:
        out.append(float(i))
    return(out)



TRANSITIONS = ["sit>stand","stand>walk","stand>sit","walk>walk","walk>stand"]

# <-> Find Category
def categoriseIntent(prevState, nextState):
    state = ""
    prevState = int(prevState)
    # - From Sit
    if prevState == 5:
        state += "sit~"
        
        if nextState == 7:
            return(state + "stand")
        

    # - From Stand
    if prevState == 4:
        state += "stand~"
        # to Sit
        if nextState == 6:
            return(state + "sit")
        # to Walk
        if nextState == 8:
            return(state + "walk")
        

    # - From Walk: left or right foot
    if prevState == 2: # or prevState == right footforward
        state += "walk~"
        # to Stand
        if nextState == 11: # or nextState == right foot --> stand
            return(state + "stand")
        # to Walk
   
        
    # - We dun goofed, print what number next state was
    print("nextState N/A: " + state + "," + str(nextState))
    return(state +"NA")
   

# <-> Cuts to filter Record time and  Sampling rate
def sampleIntent(csvList):
    # convert to samples and sample rate
    recordTime = RECORD_TIME*100;
    sampleRate = int(100/SAMPLE_RATE);
    
    # can add delay here
    
    endRec = len(csvList)
    startRec = endRec - recordTime;
    
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



# <-> Extracts prev and next State from file name
def namesplitter(filename):
    split1 = filename.split('_')[1]
    split2 = split1.split('~')
    prevstate = split2[0]
    nextstate = ((split2[1]).split('.'))[0]

    return((prevstate, nextstate))

# <-> Extracts prev and next State from file name
def intentTallier(dic,intent):
    if intent in dic.keys():
        dic[intent] += 1
    else:
        dic[intent] = 0
    return(dic)