"""
ML MODEL CREATION CODE
The University of Melbourne 2021
Engineering Capstone Project: Advanced Lower Exoskeleton (ALEX) RnD Team
Author(s): Karoline Bernacki
Date created:  07/07/2021
Date modified: 11/09/2021
"""

# series_to_supervised function (should probably have this as own file, but I'll let you fix that David)
# Reference: 
# https://machinelearningmastery.com/convert-time-series-supervised-learning-problem-python/
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
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
# === Imports and Dependencies ================================================ 
# =============================================================================
### Step 1: Import all necessary packages ###
import pandas as pd
from pandas import DataFrame
from pandas import concat
import numpy as np

# from sklearn import linear_model
from sklearn.svm import SVC
# from sklearn import svm, datasets
# from sklearn import metrics
# from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

from joblib import dump, load









### Step 2: Read data from csv file ###
# csvFile = 'standCSVData.csv'
csvFile = "standCSVData-SR_100-TR_80.csv"
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

label = 0                               # label corresponds to a numerical unique intent starting from 0
for i in range(0,len(unique_intents)):
    intents[unique_intents[i]] = label
    label += 1

### Step 3: Adjust dataset to be used in ML model (time-series to supervised) ###

## Step 3a: Get lengths of each experiment for each intention ##

    # initialise dictionaries - need as many as intents available 
    # max 3 intents for stand, walkL and walkR
    intent1_ID_lengths = {}
    intent2_ID_lengths = {}
    intent3_ID_lengths = {}   # comment this out for only 2 intents such as in walkL

    # Go through all rows to find out how long each experiment is (i.e. how long is each time series data)
    for i in range(0,len(data)):
        
        if data.Intent[i] == list(intents.keys())[0]:
            # intention is first option
            
            # check if experiment ID already in stop_ID_lengths dict
            if intent1_ID_lengths.get(data.ExpID[i]) == None:
                intent1_ID_lengths[data.ExpID[i]] = 1
            else:
                intent1_ID_lengths[data.ExpID[i]] += 1
                
            # check if experiment ID already in walk_ID_lengths dict
            if intent2_ID_lengths.get(data.ExpID[i]) == None:
                intent2_ID_lengths[data.ExpID[i]] = 1
            else:
                intent2_ID_lengths[data.ExpID[i]] += 1
        
        # comment this block out for states which only have 2 intents 
        else: 
            # third option
            if intent3_ID_lengths.get(data.ExpID[i]) == None:
                intent3_ID_lengths[data.ExpID[i]] = 1
            else:
                intent3_ID_lengths[data.ExpID[i]] += 1

## Step 3b: Get shortest length ##

    # Choose the smallest length because need all time series data to have the same length 
    # (otherwise need to manage that and find other examples/references)
    # adding zeros may affect ML result so why matching smallest length instead of largest length

    # Reference: https://www.geeksforgeeks.org/python-minimum-value-keys-in-dictionary/

    smallest_ID_length1 = min(intent1_ID_lengths.values())
    smallest_ID_length2 = min(intent2_ID_lengths.values())
    smallest_ID_length3 = min(intent3_ID_lengths.values())   # comment out for states which only have 2 intents

    # shortest_len = min(smallest_ID_length1, smallest_ID_length2)                      # for 2 intents
    shortest_len = min(smallest_ID_length1, smallest_ID_length2, smallest_ID_length3)   # for 3 intents

    print('shortest_len: ')
    print(shortest_len)


## Step 3c: Form time-series data to supervised learning data ##
# Combine intents
num_ExpID = len(np.unique(data.ExpID)) # number of experiments in dataset
print('Number of unique experiments = {}\n'.format(num_ExpID))

# All experiments are of the same length
expID_length = shortest_len     # length of experiment           
n = expID_length - 1            # length of timeseries (i.e. n in t-n)  
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
        raw[list(data)[i]] = data.iloc[index:index + expID_length,i]
    
    values = raw.values
    exp_temp = series_to_supervised(values, n)

    # Reference: https://www.dunderdata.com/blog/use-the-brackets-to-select-a-single-pandas-dataframe-column-and-not-dot-notation

    # Add new columns for intent and experiment ID
    exp_temp['Intent'] = intents[data.Intent[index]]
    exp_temp['ExpID'] = data.ExpID[index]
    exp_data = exp_data.append([exp_temp], ignore_index = True)
    
    index += expID_length    # go to next experiment and label
    
#print(exp_data)

### Step 4: Split into test and training data and normalise dataset ###
# Splitting the dataset into the Training set and Test set
expinfo = exp_data.iloc[:,0:-2]
intent = exp_data.iloc[:,-2]
expinfo_train, expinfo_test, intent_train, intent_test = train_test_split(expinfo, intent, test_size=0.25, random_state=0)
# random_state=0 will give same result, will need to randomise 

# Normalise featured set
# Removes the mean and scales to unit variance
sc = StandardScaler()
expinfo_train = sc.fit_transform(expinfo_train)
expinfo_test = sc.transform(expinfo_test)

#print('Shape of expinfo_train is {} where {} is the number of experiments and {} is the number of features.'.format(expinfo_train.shape,expinfo_train.shape[0],expinfo_train.shape[1]))

### Step 5: Reduce dimensionality of dataset ###
## Step 5a: Find optimal number of principal components in PCA ##
# Look at total variability being above 80%

# Apply PCA to lower the dimension of the data
pca=PCA(0.8)
pca.fit(expinfo_train)
#print('Number of components = {}'.format(pca.n_components_))

expinfo_train = pca.transform(expinfo_train)
expinfo_test = pca.transform(expinfo_test)

## Step 5b: Determine which features are most important in each principal component (to compare) ##
# Finding out which components are most important
print('Shape of pca.components_ is {}'.format(pca.components_.shape)) # 14 principal components that consist of the 1200 features with different significance
PC1 = abs(pca.components_[0])
print('PC1 is {}'.format(PC1))

# Need to develop a code here to find which components over a certain threshold 
# threshold indicates that it is significant
print('Min and min of PC1 are {} and {} respectively'.format(min(PC1),max(PC1)))

# Arbitrarily choose threshold to be 0.001 to test
threshold = 0.035
PC1_sig_feats_index = []

for j in range(0,len(PC1)):
    if PC1[j] > threshold:
        PC1_sig_feats_index.append(j)

        
print('With threshold={} then the number of significant features are {}'.format(threshold,len(PC1_sig_feats_index)))
print('Significant features of Principal Component 1 have indices')
print(PC1_sig_feats_index)

# print('\n')
# Print the name of these features
# print(expinfo)

### Step 6: Determine optimal ML model to use for this state ###
## Step 6a: Determine best SVM kernel and kernel parameter C ##
# Find optimal kernel, C and gamma parameters

# Reference: System Optimisation & Machine Learning Workshop 2 - Machine Learning - Section 4
# by Edward Cathcart and Karoline Bernacki

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ParameterGrid
from sklearn.metrics import roc_auc_score, make_scorer

svc = SVC(decision_function_shape='ovo')
parameter_bounds = {'kernel':['linear', 'rbf', 'poly','sigmoid'], 'C':np.linspace(0.5,1.5,20)}
clf = GridSearchCV(svc, parameter_bounds)
clf.fit(expinfo_train,intent_train)
print('Best possible Parameters \n{}'.format(clf.best_params_))


## Step 6b: Train model based on SVM kernel and parameter C from Step 6a
# probability=True needed to get priority list
# decision_function_shape='ovo' used for more than 2 intents? Need to check 
model = SVC(C=clf.best_params_['C'], kernel=clf.best_params_['kernel'], probability=True, decision_function_shape='ovo')
model.fit(expinfo_train,intent_train)
intent_predict = model.predict(expinfo_test)

## Step 6c: Save ML model ##
# Reference: https://scikit-learn.org/stable/modules/model_persistence.html

model_name = 'stand_ML_model.joblib'   # change this depending on state

dump(model, model_name)
imported_model = load(model_name)


