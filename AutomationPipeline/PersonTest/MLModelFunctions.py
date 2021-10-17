# =============================================================================
# === Imports and Dependencies ================================================ 
# =============================================================================
from pdb import set_trace as bp
from CommandIndex import * 


### Step 1: Import all necessary packages ###
import pandas as pd
from pandas import DataFrame
from pandas import concat
import numpy as np

# from sklearn import linear_model
from sklearn.svm import SVC
# from sklearn import svm, datasets
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from joblib import dump, load

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ParameterGrid
from sklearn.metrics import f1_score, roc_auc_score, make_scorer

# =============================================================================
# === Time Shifting Function ==================================================
# =============================================================================

# series_to_supervised function (should probably have this as own file, but I'll let you fix that David)
# Reference: 
# https://machinelearningmastery.com/convert-time-series-supervised-learning-problem-python/
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html

"""
    Frame a time series as a supervised learning dataset.S
    Arguments:
        data: Sequence of observations as a list or NumPy array.
        n_in: Number of lag observations as input (X).
        n_out: Number of observations as output (y).
        dropnan: Boolean whether or not to drop rows with NaN values.
    Returns:
        Pandas DataFrame of series framed for supervised learning.
    """

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    
    # number of variables depends on data shape
    n_vars = 1 if type(data) is list else data.shape[1]
    
    df = DataFrame(data)
    cols, names = list(), list()
    
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):     # goes backward n_in to 0 by decreasing by 1
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
        
    # forecast sequence (t, t+1, ... t+n)
    # instead of next point should be label
    # each label corresponds to an intent
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    
    # put it all together
    agg = concat(cols, axis=1)
    agg.columns = names
    
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
        
    return agg.iloc[0].to_frame().T  # return the data of the first row


# =============================================================================
# === ML Model Maker Code =====================================================
# =============================================================================

def timeshifter(csvFile):
    # 0) Read full data
    data = pd.read_csv(csvFile)
    data.head() # comment one to see the other
    # data.tail()

    # I) Get name of features (i.e. column titles)
    colnames = []
    i = 0
    while i < len(list(data)):
        colnames.append(list(data)[i].replace("-","").replace("<>","").replace(" ",""))
        i += 1

    # II) Read data without column names
    data = pd.read_csv(csvFile, skiprows=1, names=colnames)

    # III) Identify intents from dataset
    unique_intents = np.unique(data.Intent)
    intents = {}

    # label = 0                                   # label corresponds to a numerical unique intent starting from 0
    # for i in range(0,len(unique_intents)):
    #     intents[unique_intents[i]] = label
    #     label += 1
    
    for i in unique_intents:
        intents [i] = commandStr2Num(i) 
    
    ### Step 3: Adjust dataset to be used in ML model (time-series to supervised)
    ## Step 3a: Get lengths of each experiment for each intention (gives a dictionary of experiment lengths depending on intent) ##

        # initialise dictionaries - need as many as intents available 
        # max 3 intents for stand, walkL and walkR

        # Only need one because all experiments have the same length
        intent1_ID_lengths = {}

        # Go through all rows to find out how long each experiment is (i.e. how long is each time series data)
        for i in range(0,len(data)):
            
            if data.Intent[i] == list(intents.keys())[0]:
                # intention is first intent labelled 0
                
                # check if experiment ID already in stop_ID_lengths dict
                if intent1_ID_lengths.get(data.ExpID[i]) == None:

                    # only need to do for one experiment because all other experiments have the same length 
                    if intent1_ID_lengths:
                        break
                    else:
                        intent1_ID_lengths[data.ExpID[i]] = 1
                else:
                    intent1_ID_lengths[data.ExpID[i]] += 1
                    

    ## Step 3b: Get shortest length ##

        # Choose the smallest length because need all time series data to have the same length 
        # (otherwise need to manage that and find other examples/references)
        # adding zeros may affect ML result so why matching smallest length instead of largest length

        # Reference: https://www.geeksforgeeks.org/python-minimum-value-keys-in-dictionary/
        shortest_len = min(intent1_ID_lengths.values())


    ## Step 3c: Form time-series data to supervised learning data ##
    # All experiments are of the same length
    expID_len = shortest_len     # length of experiment           
    n = expID_len - 1            # length of timeseries (i.e. n in t-n)  
                                # can go up to shortest_len - 1 because need the first n to predict first value

    # create dataframe
    exp_data = DataFrame()

    index=0
    while index < len(data):
        # for each experiment
        raw = DataFrame()
        
        # Go through each feature and collect their data for one experiment 
        # Construct dataframe from CSV for particular experiment (and remove unnecessary features)
        for i in range(1,len(list(data))-3):    # start: 1 because ignore time, stop: -3 because last 3 columns are current state, intent and ID and not features
            # for each feature name (e.g. CrutchReading_1 etc)
            raw[list(data)[i]] = data.iloc[index:index + expID_len,i]
        
        values = raw.values
        exp_temp = series_to_supervised(values, n)

        # Reference: https://www.dunderdata.com/blog/use-the-brackets-to-select-a-single-pandas-dataframe-column-and-not-dot-notation

        # Add new columns for intent and experiment ID
        exp_temp['Intent'] = intents[data.Intent[index]]
        exp_temp['ExpID'] = data.ExpID[index]
        exp_data = exp_data.append([exp_temp], ignore_index = True)
        
        index += expID_len    # go to next experiment and label
        
    return(exp_data)









def processMLModel(csvRush, csvKaro):
    exp_data_Rush = timeshifter(csvRush)
    exp_data_Karo = timeshifter(csvKaro)    
    ### Step 4: Split into test and training data and normalise dataset ###
    # Splitting the dataset into the Training set and Test set
    # expinfo = exp_data.iloc[:,0:-2]
    # intent = exp_data.iloc[:,-2]
    
    
    expinfo_train = exp_data_Rush.iloc[:,0:-2]
    intent_train = exp_data_Rush.iloc[:,-2]
    expinfo_test = exp_data_Karo.iloc[:,0:-2]
    intent_test = exp_data_Karo.iloc[:,-2]

    # Normalise featured set
    # Removes the mean and scales to unit variance
    sc = StandardScaler()
    expinfo_train = sc.fit_transform(expinfo_train)
    expinfo_test = sc.transform(expinfo_test)

    ### Step 5: Reduce dimensionality of dataset ###
    ## Step 5a: Find optimal number of principal components in PCA ##
    # Look at total variability being above 80%

    # Apply PCA to lower the dimension of the data
    pca=PCA(0.8)
    pca.fit(expinfo_train)
    expinfo_train = pca.transform(expinfo_train)
    expinfo_test = pca.transform(expinfo_test)


    ### Step 6: Determine optimal ML model to use for this state ###
    ## Step 6a: Determine best SVM kernel and kernel parameter C ##
    # Find optimal kernel, C and gamma parameters

    # Reference: System Optimisation & Machine Learning Workshop 2 - Machine Learning - Section 4
    # by Edward Cathcart and Karoline Bernacki

    svc = SVC(decision_function_shape='ovo')
    parameter_bounds = {'kernel':['linear', 'rbf', 'poly','sigmoid'], 'C':np.linspace(0.5,1.5,20)}  # ADD if rbf case GAMMA HERE
    clf = GridSearchCV(svc, parameter_bounds)
    clf.fit(expinfo_train,intent_train)
    bestParams = clf.best_params_
    #print('Best possible Parameters \n{}'.format(bestParams))


    ## Step 6b: Train model based on SVM kernel and parameter C from Step 6a
    # probability=True needed to get priority list
    # decision_function_shape='ovo' used for more than 2 intents? Need to check 
    model = SVC(C=clf.best_params_['C'], kernel=clf.best_params_['kernel'], probability=True, decision_function_shape='ovo') # INSERT GAMMA HERE
    model.fit(expinfo_train,intent_train)
    intent_predict = model.predict(expinfo_test)
    intent_percentage = model.predict_proba(expinfo_test)
    
    
    # Collect Metrics
    cfm = metrics.confusion_matrix(intent_test,intent_predict).tolist()        #import 
    txtResults = metrics.classification_report(intent_test,intent_predict)
    jsonResults = metrics.classification_report(intent_test,intent_predict, output_dict = True)
    modelScore = model.score(expinfo_test, intent_test)
    #bp()
    
    # MultiClass ROC_AUC
    try:
        macro_roc_auc_ovo = roc_auc_score(intent_test, intent_percentage, multi_class="ovo", average="macro")
        
    except ValueError:
    # Binary ROC_AUC
        macro_roc_auc_ovo = roc_auc_score(intent_test, intent_percentage[:, 1])
        
    rocAuc = {"score": macro_roc_auc_ovo,"proba":intent_percentage}
    
    testTrainData = {"expinfo_train": expinfo_train.tolist(), "expinfo_test": expinfo_test.tolist(), "intent_train": intent_train.tolist(), "intent_test": intent_test.tolist(), "intent_predict": intent_predict.tolist()}
    #bp()
    
    
    return(modelScore, bestParams, model, cfm, rocAuc, txtResults, jsonResults, testTrainData)


# =============================================================================
# === Print Metrics to terminal ===============================================
# =============================================================================

def logMLDataTerminal(filename, score, rocAuc, txtResult, params, model, metricText):
    #Print to terminal
    print(filename, "Rush Train Karo Test")
    print("accuracy score: ", 100*score, "%")
    print(txtResult)
    print("rocAuc score: ", rocAuc["score"])
    print(params)
    print(model)
    print()

    # Stuff to put into the output files
    modelReport = ("Filename: " + filename + " Rush Train Karo Test", "Model Score: " + str(score*100)+"%", "rocAuc score: " + str(rocAuc["score"]), txtResult, "Model Details: "+str(model))
    metricText += "\n".join(modelReport)
    return metricText


# =============================================================================
# === Split State, SR, TR from file name ======================================
# =============================================================================
def splitControlsfromName(filename):
    tmp = filename.split(".csv")[0]
    tmpsplit = tmp.split('-')
    state = tmpsplit[0].split('CSVData')[0]
    sr = tmpsplit[1].split('SR_')[1]
    tr = tmpsplit[2].split('TR_')[1]
