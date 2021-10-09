
import pickle
from MLModelFunctions import *
import matplotlib.pyplot as plt
from ControlParameters import *


XLABEL = 'Time Recording Length'

# loading da pickle
infile = open("allStatsDataPickle", 'rb')
statsDict = pickle.load(infile)
print("stats loaded")

xlabel = 'Time recording length'
nplot = 0
# For each state: stand, walkFL, walkFR
for state in statsDict:

    # Label for title
    stateLabel = state.split("CSVData")[0]

    # x-axis time samples
    time_records = []

    # collect value of each
    dic_Prec = {}
    dic_Recall = {}
    dic_F1 = {}
    dic_Sup = {}
    list_Accuracy = []
    # each time sample
    for filename in statsDict[state]:
        sr, tr = splitControlsfromName(filename)
        time_records.append(int(tr))
        
        jsonResult = statsDict[state][filename]
        
        for intentkey in jsonResult:
            # if intentkey == 'accuracy':
            #     list_Accuracy.append(jsonResult[intentkey]['accuracy'])
            
            # check for numbers (intention)
            try:
                int(intentkey)
            except ValueError:
                continue

            # Accumulate per intent <- new value in list of time samples 
            try:
                dic_Prec[intentkey] += [jsonResult[intentkey]['precision']]
            except KeyError:
                dic_Prec[intentkey] = [jsonResult[intentkey]['precision']]
            
            try:
                dic_Recall[intentkey] += [jsonResult[intentkey]['recall']]
            except KeyError:
                dic_Recall[intentkey] = [jsonResult[intentkey]['recall']]
            
            try:
                dic_F1[intentkey] += [jsonResult[intentkey]['f1-score']]
            except KeyError:
                dic_F1[intentkey] = [jsonResult[intentkey]['f1-score']]
            
            try:
                dic_Sup[intentkey] += [jsonResult[intentkey]['support']]
            except KeyError:
                dic_Sup[intentkey] = [jsonResult[intentkey]['support']]
    
    # -- All metrics across stationary state done
    ## Plot accuracy
    # plt.figure(nplot)
    # time_plot, pltPrec = zipsort(time_records, list_Accuracy)
    # plt.plot(time_plot, list_Accuracy)
    # plt.title(stateLabel + " Accuracy Plot")
    # plt.xlabel(XLABEL)
    # plt.ylabel("Accuracy")
    # plt.legend()
    # plt.show()
    # nplot += 1
    
    
    
    ## Plot Precision
    plt.figure(nplot)
    for intent in dic_Prec:
        time_plot, pltPrec = zipsort(time_records, dic_Prec[intent])
        plt.plot(time_plot, pltPrec, label=ALLSTATES_DIC[int(intent)])
        
    plt.title(stateLabel + " Precision Plot")
    plt.xlabel(XLABEL)
    plt.ylabel("Precision")
    plt.legend()
    plt.show()
    nplot +=1
    
    
    
    ## Plot Recall
    plt.figure(nplot)
    for intent in dic_Recall:
        time_plot, pltRecall = zipsort(time_records, dic_Recall[intent])
        plt.plot(time_plot, pltRecall, label=ALLSTATES_DIC[int(intent)])
        
    plt.title(stateLabel + " Recall Plot")
    plt.xlabel(XLABEL)
    plt.ylabel("Recall")
    plt.legend()
    plt.show()
    nplot += 1
    
    
    
    ## Plot F1-Score
    plt.figure(nplot)
    for intent in dic_Recall:
        time_plot, pltF1 = zipsort(time_records, dic_F1[intent])
        plt.plot(time_plot, pltF1, label=ALLSTATES_DIC[int(intent)])
        
    plt.title(stateLabel + " F1_Score Plot")
    plt.xlabel(XLABEL)
    plt.ylabel("F1_Score")
    plt.legend()
    plt.show()
    nplot += 1
    
    
    
    ## Plot Support?
