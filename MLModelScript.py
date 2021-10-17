"""
ML MODEL CREATION CODE
The University of Melbourne 2021
Engineering Capstone Project: Advanced Lower Exoskeleton (ALEX) RnD Team
Author(s): Karoline Bernacki
Date created:  07/07/2021
Date modified: 21/09/2021
"""

from MLModelFunctions import *
from ExtractIntentFunctions import * 

merge_filepaths = glob.glob(DIR_MERGE + "*.csv")

### Step 2: Read data from csv file ###
# csvFile = merge_filepaths[8]
# filename = os.path.basename(csvFile) 
# print(filename)
#'standCSVData-SR_100-TR_90'

# 0) Read full data
data = pd.read_csv(filename)
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

label = 0                                   # label corresponds to a numerical unique intent starting from 0
for i in range(0,len(unique_intents)):
    intents[unique_intents[i]] = label
    label += 1

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
    
#print(exp_data)

### Step 4: Split into test and training data and normalise dataset ###
# Splitting the dataset into the Training set and Test set
expinfo = exp_data.iloc[:,0:-2]
intent = exp_data.iloc[:,-2]
expinfo_train, expinfo_test, intent_train, intent_test = train_test_split(expinfo, intent, test_size=0.25, random_state=0) # random_state=0 will give same result, will need to randomise 


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






# =============================================================================
# === Save Model file =========================================================
# =============================================================================


## Step 6c: Save ML model ##
# Reference: https://scikit-learn.org/stable/modules/model_persistence.html

model_name = 'stand_ML_model.joblib'   # change this depending on state

dump(model, model_name)
imported_model = load(model_name)


