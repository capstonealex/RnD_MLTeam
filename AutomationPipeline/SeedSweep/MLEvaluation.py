import pickle
import matplotlib.pyplot as plt
from MLModelFunctions import *
from ControlParameters import *
from CommandIndex import *

# loading da pickle
# infile = open("allMLDataPickle",'rb')
# pickleDict = pickle.load(infile)

infile = open("avgStatsPickle",'rb')
statsDict = pickle.load(infile)
print("dict loaded")

# =============================================================================
# === Separate Mean and Std Dev per State per Plot ============================
# =============================================================================

# for each key in statsDict
for state in statsDict:
    
    # label for title
    stateLabel = state.split("CSVData")[0]
    
    # collect value of each
    strLabels = []
    
    meanList_Prec = []
    stdevList_Prec = []
    
    meanList_Recall = []
    stdevList_Recall = []
    
    meanList_f1 = []
    stdevList_f1 = []
    
    meanList_sup = []
    stdevList_sup = []
    
    for intents in statsDict[state]:
        strLabels.append(ALLSTATES_DIC[int(intents)])
        scoresDict = (statsDict[state])[intents]
        
        # Precision
        meanList_Prec.append((scoresDict['precision'])[0])
        stdevList_Prec.append((scoresDict['precision'])[1])
        
        # Recall
        meanList_Recall.append((scoresDict['recall'])[0])
        stdevList_Recall.append((scoresDict['recall'])[1])
        
        # F1 score
        meanList_f1.append((scoresDict['f1-score'])[0])
        stdevList_f1.append((scoresDict['f1-score'])[1])
        
        # Support
        meanList_sup.append((scoresDict['support'])[0])
        stdevList_sup.append((scoresDict['support'])[1])

# =============================================================================
# === Plotting bar charts per State ===========================================
# =============================================================================

    x_pos = np.arange(len(strLabels))

    # Plot bar graph Precision
    fig, ax = plt.subplots()    
    ax.bar(x_pos, meanList_Prec, 
           yerr = stdevList_Prec,
           align='center',
           alpha=0.5,
           ecolor='black',
           capsize=10)
    
    ax.set_ylabel('Precision values')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(strLabels)
    ax.set_title('Precision Plot for '+ stateLabel)
    ax.yaxis.grid(True)
    plt.tight_layout()
    plt.show()
        
    # Plot bar graph Recall
    fig, ax = plt.subplots()
    ax.bar(x_pos, meanList_Prec,
           yerr=stdevList_Prec,
           align='center',
           alpha=0.5,
           ecolor='black',
           capsize=10)

    ax.set_ylabel('Precision values')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(strLabels)
    ax.set_title('Precision Plot for ' + stateLabel)
    ax.yaxis.grid(True)
    plt.tight_layout()
    plt.show()

    
    # Plot bar graph F1 Score
    fig, ax = plt.subplots()
    ax.bar(x_pos, meanList_Prec,
           yerr=stdevList_Prec,
           align='center',
           alpha=0.5,
           ecolor='black',
           capsize=10)

    ax.set_ylabel('Precision values')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(strLabels)
    ax.set_title('Precision Plot for ' + stateLabel)
    ax.yaxis.grid(True)
    plt.tight_layout()
    plt.show()

    
    # Plot bar graph Support
    fig, ax = plt.subplots()
    ax.bar(x_pos, meanList_Prec,
           yerr=stdevList_Prec,
           align='center',
           alpha=0.5,
           ecolor='black',
           capsize=10)

    ax.set_ylabel('Precision values')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(strLabels)
    ax.set_title('Precision Plot for ' + stateLabel)
    ax.yaxis.grid(True)
    plt.tight_layout()
    plt.show()


# https://problemsolvingwithpython.com/06-Plotting-with-Matplotlib/06.07-Error-Bars/
