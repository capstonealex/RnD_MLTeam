RECORD_TIME = 1;    # seconds: intent before movement
SAMPLE_RATE = 50;    # samples wanted per second (cannot exceed 100)

#from CommandIndex import *

# import pandas as pd             # data processing, CSV file I/O (e.g. pd.read_csv)
import glob
import csv


FILLEDROW = 44
ID_CURRSTATE = -2
# time = 0, nonzero features are 29 -> 38 incl
SELECTROWS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, ID_CURRSTATE]

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

