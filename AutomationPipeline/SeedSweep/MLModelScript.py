"""
ML MODEL CREATION CODE
The University of Melbourne 2021
Engineering Capstone Project: Advanced Lower Exoskeleton (ALEX) RnD Team
Author(s): Karoline Bernacki, David Pham
Date created:  07/07/2021
Date modified: 21/09/2021
"""
import pickle
import statistics as st
from MLModelFunctions import *
from pdb import set_trace as bp
checkMakeDirectoryModel()
# =============================================================================
# === Sort files into stationary states =======================================
# =============================================================================
merge_filepaths = glob.glob(DIR_MERGE + "*.csv")
dic = {}
dic[CSV_STAND] = []
dic[CSV_WALKL] = []
dic[CSV_WALKR] = []

# find all merge data files for each stationary state
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
avgMLStats = {}
for statState in dic:
    stateTitle = "\n"+BAR+statState+BAR+"\n\n\n\n"
    print(BAR,statState,BAR)
    metricText += stateTitle
    
    
    pathlist = dic[statState]
    # stateMLData = {}
    for path in pathlist:
        filename = os.path.basename(path) 
        
        # Where the magic happens 
        seedMLData = {}
        resultList = []
        for seed in RAND_SEEDS:
            
        # -- Outputs of ML Data Generation explained
            # score = basic accuracy metric
            # params = best parameters for the model, keys: {'C', 'kernal'}
            # model = actual ML model for that data set
            # cfm = confusion matrix
            # result: txt = text report, json = dictionary object
            # testTrainData dictionary, keys: {'expinfo_train', 'expinfo_test', 'intent_train', 'intent_test', 'intent_predict'}

            score, params, model, cfm, txtResult, jsonResult, testTrainData = processMLModel(path, seed)
            
            
            # Print to terminal to see progress and log into the output files
            metricText = logMLDataTerminal(seed, filename, score, txtResult, params, model, metricText)
            metricText += "\n\n"+BAR*2+"\n\n"   # formatting

            # change this depending on state
            model_name = DIR_MODEL + filename.split(".csv")[0]+"-Seed_"+str(seed)+".joblib"
            dump(model, model_name)
            
            # Record in dictionary 
            seedMLData[seed] = {"metrics": jsonResult, "cfm":cfm, "testTrainData": testTrainData, "params": params}

            # Collect metrics per json result seed for mean and stdev
            resultList.append(jsonResult)
            
    # Find Average Metrics
        # filters keys: find intents 
        for exp in resultList:
            keys_metrics = list(exp.keys())
            keys_statMeasures = list(exp[keys_metrics[0]].keys())
            
            
            filtkeys = []
            for key in keys_metrics:
            # extract accuracy
            
            # remove non-intents
                try:
                    int(key)
                except ValueError:
                    continue
                filtkeys.append(key)
            filtkeys.append('accuracy')
        # Collect results
        avg = {}
        for intent in filtkeys:
            # Important data
            l_accuracy = []
            l_precision = []
            l_recall = []
            l_f1score = []
            l_support = []
            for exp in resultList:
                measures = exp[intent]
            
                l_precision.append(measures['precision'])
                l_recall.append(measures['recall'])
                l_f1score.append(measures['f1-score'])
                l_support.append(measures['support'])
                
            t_precision = [st.mean(l_precision),st.stdev(l_precision)]
            t_recall = [st.mean(l_recall),st.stdev(l_recall)]
            t_f1score = [st.mean(l_f1score),st.stdev(l_f1score)]
            t_support = [st.mean(l_support),st.stdev(l_support)]
        
            avg[intent] = {'precision': t_precision, 'recall': t_recall, 'f1-score': t_f1score, 'support': t_support}
        
            
    
    # File writer (clears metric text per stationary state)
    f = open(DIR_MODEL+statState+"Report.txt", 'w')
    f.write(metricText)
    f.close()
    metricText = ""
    
    # Important data
    avgMLStats[statState] = avg
    allMLData[statState] = seedMLData

# Output Json Object file
with open("allMLDataPickle", "wb") as outfile:
    pickle.dump(allMLData, outfile)

with open("avgStatsPickle", "wb") as outfile:
    pickle.dump(avgMLStats, outfile)



################################################################################
# Dictionary JSON structure
#
# allMLDATA = {
#   <str>stationaryState: {
#                       <int>seed: {
#                                       "metrics"       : jsonResult,
#                                       "cfm"           : cfm,
#                                       "testTrainData" : testTrainData,
#                                       "params"        : params
#                                   }
#                               }
#                           }
#               }

'''
-- Dictionary layers --

allMLDATA = { <str>stationaryState    :   {} }

{ <str>stationaryState } = { <int>seed  :   {} }

{ <int>seed } = { 
                "metrics"       : jsonResult,
                "cfm"           : cfm,
                "testTrainData" : testTrainData,
                "params"        : params
                }
                    jsonResult = {
                            '0'     : { 'precision': 1.0,
                                        'recall': 1.0,
                                        'f1-score': 1.0,
                                        'support': 20
                                        },
                            '1'     : { 'precision': 1.0,
                                        'recall': 1.0,
                                        'f1-score': 1.0,
                                        'support': 28
                                        },
                    'accuracy'      : 1.0,
                    'macro avg'     : { 'precision': 1.0,
                                        'recall': 1.0,
                                        'f1-score': 1.0,
                                        'support': 48
                                        },
                    'weighted avg'  : { 'precision': 1.0,
                                        'recall': 1.0,
                                        'f1-score': 1.0,
                                        'support': 48
                                        }
                    }

                    cfm = [tp, .. , fn]
                    testTrainData = {                  
                                    "expinfo_train"  : expinfo_train  = [[]] <float: intent instance -x- timeshift data >,
                                    "expinfo_test"   : expinfo_test   = [[]] <float: intent instance -x- timeshift data >,
                                    "intent_train"   : intent_train   = []   <int: enum(0,1)>,
                                    "intent_test"    : intent_test    = []   <int: enum(0,1)>,
                                    "intent_predict" : intent_predict = []   <int: enum(0,1)>
                                    },
                    params = {  'C'     : <float>, 
                                'kernel': <str: enum('linear', 'rbf,...etc)>
                                'gamma' : <float: when poly, sig, rbf> || 0 (where 0 is undefined)
}

'''
