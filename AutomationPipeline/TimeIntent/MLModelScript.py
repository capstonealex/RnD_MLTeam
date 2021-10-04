"""
ML MODEL CREATION CODE
The University of Melbourne 2021
Engineering Capstone Project: Advanced Lower Exoskeleton (ALEX) RnD Team
Author(s): Karoline Bernacki, David Pham
Date created:  07/07/2021
Date modified: 21/09/2021
"""
import pickle
from ControlParameters import *
from MLModelFunctions import *
from pdb import set_trace as bp

# =============================================================================
# === Sort files into stationary states =======================================
# =============================================================================
merge_filepaths = glob.glob(DIR_MERGE + "*.csv")
dic = {}
dic[CSV_STAND] = []
dic[CSV_WALKL] = []
dic[CSV_WALKR] = []

for path in merge_filepaths:
    if CSV_STAND in path:
        dic[CSV_STAND].append(path)
    
    if CSV_WALKL in path:
        dic[CSV_WALKL].append(path)
    
    if CSV_WALKR in path:
        dic[CSV_WALKR].append(path)

# =============================================================================
# === ML Model Automation Engine ==============================================
# =============================================================================
BAR = 50*'-'
metricText = ""
allMLData = {}
for statState in dic:
    stateTitle = "\n"+BAR+statState+BAR+"\n\n\n\n"
    print(BAR,statState,BAR)
    metricText += stateTitle
    pathlist = dic[statState]
    
    
    stateMLData = {}
    for path in pathlist:
        filename = os.path.basename(path) 
        
        # Where the magic happens 
        seed = SEED_OF_LIFE
        score, params, model, cfm, txtResult, jsonResult, testTrainData = processMLModel(path, seed)
        # score = basic accuracy metric
        # params = best parameters for the model, keys: {'C', 'kernal'}
        # model = actual ML model for that data set
        # cfm = confusion matrix
        # result: txt = text report, json = dictionary object
        # testTrainData dictionary, keys: {'expinfo_train', 'expinfo_test', 'intent_train', 'intent_test', 'intent_predict'}
        
        # Export model dumps:
        # model_name = DIR_MODEL+filename.strip(".csv")+".joblib"   # change this depending on state
        # dump(model, model_name)
        
        # Print to terminal to see progress
        print(filename)
        print("score: ",100*score,"%")
        print(txtResult)
        print(params)
        print(model)
        print()
        
        
        # Stuff to put into the output files
        modelReport=("Filename: " + filename,"Model Score: "+str(score*100)+"%", txtResult, "Model Details: "+str(model))
        metricText += "\n".join(modelReport)
        metricText += "\n\n"+BAR*2+"\n\n"
        
        # Important data
        stateMLData[filename] = {"metrics": jsonResult, "testTrainData": testTrainData, "modelObj": model}
            
    
    # In the loop: Plot metrics for one stationary state (use {stateMLData})
    # ------------------------ can code here --------------------------------- #
    
    # ------------------------------------------------------------------------ #
    # File writer (clears metric text per stationary state)
    f = open(statState+"Report.txt",'w')
    f.write(metricText)
    f.close()
    metricText = ""
    
    # Important data
    allMLData[statState] = stateMLData

# Output Json Object file
with open("allMLDataPickle", "wb") as outfile:
    pickle.dump(allMLData, outfile)

# Out the loop: Plot metrics between all stationary states (use {allMLData})
# ------------------------ or can code here --------------------------------- #
# in or out loop is up to you whatever floats your boat





# --------------------------------------------------------------------------- #


# =============================================================================
# === Save Model file =========================================================
# =============================================================================


## Step 6c: Save ML model ##
# Reference: https://scikit-learn.org/stable/modules/model_persistence.html

# model_name = 'stand_ML_model.joblib'   # change this depending on state

# dump(model, model_name)
# imported_model = load(model_name)


# Dictionary JSON structure
#
# allMLDATA = {
#   <str>stationaryState: {
#               <str>filename: {
#                                 "metrics"       : jsonResult,
#                                 "cfm"           : cfm,
#                                 "testTrainData" : testTrainData,
#                                 "params"        : params
#                               }
#                           }
#               }
