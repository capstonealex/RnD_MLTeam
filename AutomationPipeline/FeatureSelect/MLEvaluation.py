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
    
    list_Prec = []
    list_Recall = []
    list_F1 = []
    list_Sup = []
    for intents in statsDict[state]:
       try:
              strLabels.append(ALLSTATES_DIC[int(intents)])
       except ValueError:
              continue
       
       scoresDict = (statsDict[state])[intents]
        
        # Precision
       list_Prec.append(scoresDict['precision'])
        
        # Recall
       list_Recall.append(scoresDict['recall'])
        
        # F1 score
       list_F1.append(scoresDict['f1-score'])
        
        # Support
       list_Sup.append(scoresDict['support'])
# =============================================================================
# === Plotting bar charts per State ===========================================
# =============================================================================
    x_pos = np.arange(len(strLabels))



    # Plot bar graph Precision
    fig, ax = plt.subplots()    
    ax.bar(x_pos, list_Prec, 
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
    ax.bar(x_pos, list_Recall,
           align='center',
           alpha=0.5,
           ecolor='black',
           capsize=10)
    ax.set_ylabel('Recall values')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(strLabels)
    ax.set_title('Recall Plot for ' + stateLabel)
    ax.yaxis.grid(True)
    plt.tight_layout()
    plt.show()


    
    # Plot bar graph F1 Score
    fig, ax = plt.subplots()
    ax.bar(x_pos, list_F1,
           align='center',
           alpha=0.5,
           ecolor='black',
           capsize=10)
    ax.set_ylabel('F1 score values')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(strLabels)
    ax.set_title('F1 score Plot for ' + stateLabel)
    ax.yaxis.grid(True)
    plt.tight_layout()
    plt.show()

    
    # Plot bar graph Support
    fig, ax = plt.subplots()
    ax.bar(x_pos, list_Sup,
           align='center',
           alpha=0.5,
           ecolor='black',
           capsize=10)
    ax.set_ylabel('Support values')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(strLabels)
    ax.set_title('Support Plot for ' + stateLabel)
    ax.yaxis.grid(True)
    plt.tight_layout()
    plt.show()


# https://problemsolvingwithpython.com/06-Plotting-with-Matplotlib/06
