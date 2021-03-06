import pickle
import matplotlib.pyplot as plt
from MLModelFunctions import *
from ControlParameters import *
from CommandIndex import *

# # loading da pickle
# # infile = open("allMLDataPickle",'rb')
# # pickleDict = pickle.load(infile)

infile = open("avgStatsPickle",'rb')
statsDict = pickle.load(infile)
print("stats loaded")



# =============================================================================
# === Separate Mean and Std Dev per State per Plot ============================
# =============================================================================

l_stateLabels = []
list_Acc = []
# for each key in statsDict
for state in statsDict:
    
       # label for title
       stateLabel = state.split("CSVData")[0]
       l_stateLabels.append(stateLabel)

       # collect value of each
       strLabels = []
       list_Prec = []
       list_Recall = []
       list_F1 = []
       list_Sup = []
       
       list_Acc.append(statsDict[state]['accuracy'])
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


# Plot bar graph Accuracy
x_pos = np.arange(len(l_stateLabels))
fig, ax = plt.subplots()
ax.bar(x_pos, list_Acc,
       align='center',
       alpha=0.5,
       ecolor='black',
       capsize=10)
ax.set_ylabel('Accuracy values')
ax.set_xticks(x_pos)
ax.set_xticklabels(l_stateLabels)
ax.set_title('Accuracy Plot for all Stationary States')
ax.yaxis.grid(True)
plt.tight_layout()
plt.show()

# # https://problemsolvingwithpython.com/06-Plotting-with-Matplotlib/06

# ROC_AUC_(Macro Avg)
infile = open("allRocAucStatsPickle", 'rb')
rocAucDict = pickle.load(infile)
print("rocAuc loaded")

stateLabels = []
list_ROCAUC = []
for state in rocAucDict:
       stateLabels.append(state.split("CSVData")[0])
       list_ROCAUC.append(rocAucDict[state]['score'])

x_pos = np.arange(len(stateLabels))
fig, ax = plt.subplots()
ax.bar(x_pos, list_ROCAUC,
       align='center',
       alpha=0.5,
       ecolor='black',
       capsize=10)
ax.set_ylabel('ROCAUC score values')
ax.set_xticks(x_pos)
ax.set_xticklabels(stateLabels)
ax.set_title('ROC AUC performance Plots per State')
ax.yaxis.grid(True)
plt.tight_layout()
plt.show()
