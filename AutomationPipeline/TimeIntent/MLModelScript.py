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
# accumulate a list of filepaths per stationary state

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

BAR = 50*'-'
# =============================================================================
# === ML Model Automation Engine ==============================================
# =============================================================================
metricText = ""

allMLData = {}
allStatsData = {}
allRocAucData = {}

for statState in dic:
    stateTitle = "\n"+BAR+statState+BAR+"\n\n\n\n"
    print(BAR,statState,BAR)
    metricText += stateTitle
    pathlist = dic[statState]
    # list of paths taken per state
    
    stateMLData = {}
    stateStatsData = {}
    stateROCAUCData = {}
    for path in pathlist:
        filename = os.path.basename(path) 
        
        # Where the magic happens 
        seed = SEED_OF_LIFE
        score, params, model, cfm, rocAuc, txtResult, jsonResult, testTrainData = processMLModel(path, seed)
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
        metricText = logMLDataTerminal(SEED_OF_LIFE, filename, score, rocAuc, txtResult, params, model, metricText)
        metricText += "\n\n"+BAR*2+"\n\n"   # formatting
        
        # Important data
        stateMLData[filename] = {"metrics": jsonResult, "testTrainData": testTrainData, "modelObj": model}
        stateStatsData[filename] = jsonResult
        stateROCAUCData[filename] = rocAuc
    # File writer (clears metric text per stationary state)
    f = open(statState+"Report.txt",'w')
    f.write(metricText)
    f.close()
    metricText = ""
    
    # Important data
    allMLData[statState] = stateMLData
    allStatsData[statState] = stateStatsData
    allRocAucData[statState] = stateROCAUCData
# Output Json Object file
with open("allMLDataPickle", "wb") as outfile:
    pickle.dump(allMLData, outfile)

with open("allStatsDataPickle", "wb") as outfile:
    pickle.dump(allStatsData, outfile)

with open("allRocAucDataPickle", "wb") as outfile:
    pickle.dump(allRocAucData, outfile)

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
