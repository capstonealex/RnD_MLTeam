import sys
import json
import pickle
from MLModelFunctions import *
import matplotlib.pyplot as plt

# loading da pickle
infile = open("allMLDataPickle",'rb')
tmpdict = pickle.load(infile)
print("dict loaded")


# # sample of iteration
# print("tmpdict keys = ",tmpdict.keys())
# print()
# a = tmpdict['standCSVData']
# print("a keys = ",a.keys())
# print()
# b=a['standCSVData-SR_100-TR_10.csv']
# print("b keys = ",b.keys())
# print()
# c = b['modelObj']
# d = b['testTrainData']
# e = b['metrics']
# print("d keys = ",d.keys())
# print()
# print(c.score(d['expinfo_test'],d['intent_test']))
# print()
# print("e keys = ",e.keys())
# print()



# Plot TR against C parameter, precision, recall, f1-score, accuracy/score
time_record_len = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

########## Standing state ############
standData = tmpdict['standCSVData']

s_precision0 = []
s_precision1 = []

s_recall0 = []
s_recall1 = []

s_f1score0 = []
s_f1score1 = []

s_accuracy = []

s_Cparams = []

for tr in time_record_len:
    filename = 'standCSVData-SR_100-TR_' + str(tr) + '.csv'
    TR_data = standData[filename]

    s_precision0.append(TR_data['metrics']['0']['precision'])
    s_precision1.append(TR_data['metrics']['1']['precision'])

    s_recall0.append(TR_data['metrics']['0']['recall'])
    s_recall1.append(TR_data['metrics']['1']['recall'])

    s_f1score0.append(TR_data['metrics']['0']['f1-score'])
    s_f1score1.append(TR_data['metrics']['1']['f1-score'])

    s_accuracy.append(TR_data['metrics']['accuracy'])

    s_Cparams.append(TR_data['modelObj'].get_params()['C'])


## Plot precision
plt.figure(1)
plt.plot(time_record_len, s_precision0, label='0')
plt.xlabel('Time recording length')
plt.ylabel('Precision of class 0 and class 1')
plt.title('Stand: Precision of both classes with respect to length of time recording')
plt.plot(time_record_len, s_precision1, label='1')
plt.legend()
plt.show()

### Plot recall
plt.figure(2)
plt.plot(time_record_len, s_recall0, label='0')
plt.xlabel('Time recording length')
plt.ylabel('Recall of class 0 and class 1')
plt.title('Stand: Recall of both classes with respect to length of time recording')
plt.plot(time_record_len, s_recall1, label='1')
plt.legend()
plt.show()

### Plot F1-score
plt.figure(3)
plt.plot(time_record_len, s_f1score0, label='0')
plt.xlabel('Time recording length')
plt.ylabel('F1-score of class 0 and class 1')
plt.title('Stand: F1-score of both classes with respect to length of time recording')
plt.plot(time_record_len, s_f1score1, label='1')
plt.legend()
plt.show()

# ### Plot accuracy
# plt.figure(4)
# plt.plot(time_record_len, s_accuracy)
# plt.xlabel('Time recording length')
# plt.ylabel('Accuracy')
# plt.title('Stand: Accuracy of the ML model chosen with respect to length of time recording')
# plt.show()

# ## Plot C parameters
# plt.figure(5)
# plt.plot(time_record_len, s_Cparams)
# plt.xlabel('Time recording length')
# plt.ylabel('C parameter value')
# plt.title('Stand: Value of C parameter of SVM kernel with respect to length of time recording')
# plt.show()






######## Walk FL state ############
walkFLData = tmpdict['walkFLCSVData']

wFL_precision0 = []
wFL_precision1 = []

wFL_recall0 = []
wFL_recall1 = []

wFL_f1score0 = []
wFL_f1score1 = []

wFL_accuracy = []

wFL_Cparams = []

for tr in time_record_len:
    filename = 'walkFLCSVData-SR_100-TR_' + str(tr) + '.csv'
    TR_data = walkFLData[filename]

    wFL_precision0.append(TR_data['metrics']['0']['precision'])
    wFL_precision1.append(TR_data['metrics']['1']['precision'])

    wFL_recall0.append(TR_data['metrics']['0']['recall'])
    wFL_recall1.append(TR_data['metrics']['1']['recall'])

    wFL_f1score0.append(TR_data['metrics']['0']['f1-score'])
    wFL_f1score1.append(TR_data['metrics']['1']['f1-score'])

    wFL_accuracy.append(TR_data['metrics']['accuracy'])

    wFL_Cparams.append(TR_data['modelObj'].get_params()['C'])


### Plot precision
# plt.figure(1)
# plt.plot(time_record_len, wFL_precision0, label='0')
# plt.xlabel('Time recording length')
# plt.ylabel('Precision of class 0 and class 1')
# plt.title('WalkFL: Precision of both classes with respect to length of time recording')
# plt.plot(time_record_len, wFL_precision1, label='1')
# plt.legend()
# plt.show()

# ### Plot recall
# plt.figure(2)
# plt.plot(time_record_len, wFL_recall0, label='0')
# plt.xlabel('Time recording length')
# plt.ylabel('Recall of class 0 and class 1')
# plt.title('WalkFL: Recall of both classes with respect to length of time recording')
# plt.plot(time_record_len, wFL_recall1, label='1')
# plt.legend()
# plt.show()

# ### Plot F1-score
# plt.figure(3)
# plt.plot(time_record_len, wFL_f1score0, label='0')
# plt.xlabel('Time recording length')
# plt.ylabel('F1-score of class 0 and class 1')
# plt.title('WalkFL: F1-score of both classes with respect to length of time recording')
# plt.plot(time_record_len, wFL_f1score1, label='1')
# plt.legend()
# plt.show()

# ### Plot accuracy
# plt.figure(4)
# plt.plot(time_record_len, wFL_accuracy)
# plt.xlabel('Time recording length')
# plt.ylabel('Accuracy')
# plt.title('WalkFL: Accuracy of the ML model chosen with respect to length of time recording')
# plt.show()

# ## Plot C parameters
# plt.figure(5)
# plt.plot(time_record_len, wFL_Cparams)
# plt.xlabel('Time recording length')
# plt.ylabel('C parameter value')
# plt.title('WalkFL: Value of C parameter of SVM kernel with respect to length of time recording')
# plt.show()







######## Walk FR state ############
walkFRData = tmpdict['walkFRCSVData']

wFR_precision0 = []
wFR_precision1 = []
wFR_precision2 = []

wFR_recall0 = []
wFR_recall1 = []
wFR_recall2 = []

wFR_f1score0 = []
wFR_f1score1 = []
wFR_f1score2 = []

wFR_accuracy = []

wFR_Cparams = []

for tr in time_record_len:
    filename = 'walkFRCSVData-SR_100-TR_' + str(tr) + '.csv'
    TR_data = walkFRData[filename]

    wFR_precision0.append(TR_data['metrics']['0']['precision'])
    wFR_precision1.append(TR_data['metrics']['1']['precision'])
    wFR_precision2.append(TR_data['metrics']['2']['precision'])

    wFR_recall0.append(TR_data['metrics']['0']['recall'])
    wFR_recall1.append(TR_data['metrics']['1']['recall'])
    wFR_recall2.append(TR_data['metrics']['2']['recall'])

    wFR_f1score0.append(TR_data['metrics']['0']['f1-score'])
    wFR_f1score1.append(TR_data['metrics']['1']['f1-score'])
    wFR_f1score2.append(TR_data['metrics']['2']['f1-score'])

    wFR_accuracy.append(TR_data['metrics']['accuracy'])

    wFR_Cparams.append(TR_data['modelObj'].get_params()['C'])


### Plot precision
plt.figure(1)
plt.plot(time_record_len, wFR_precision0, label='0')
plt.xlabel('Time recording length')
plt.ylabel('Precision of class 0, 1, and 2')
plt.title('WalkFR: Precision of all classes with respect to length of time recording')
plt.plot(time_record_len, wFR_precision1, label='1')
plt.plot(time_record_len, wFR_precision2, label='2')
plt.legend()
plt.show()

### Plot recall
plt.figure(2)
plt.plot(time_record_len, wFR_recall0, label='0')
plt.xlabel('Time recording length')
plt.ylabel('Recall of class 0, 1, and 2')
plt.title('WalkFR: Recall of all classes with respect to length of time recording')
plt.plot(time_record_len, wFR_recall1, label='1')
plt.plot(time_record_len, wFR_recall2, label='2')
plt.legend()
plt.show()

### Plot F1-score
plt.figure(3)
plt.plot(time_record_len, wFR_f1score0, label='0')
plt.xlabel('Time recording length')
plt.ylabel('F1-score of class 0, 1, and 2')
plt.title('WalkFR: F1-score of all classes with respect to length of time recording')
plt.plot(time_record_len, wFR_f1score1, label='1')
plt.plot(time_record_len, wFR_f1score2, label='2')
plt.legend()
plt.show()

### Plot accuracy
plt.figure(4)
plt.plot(time_record_len, wFR_accuracy)
plt.xlabel('Time recording length')
plt.ylabel('Accuracy')
plt.title('WalkFR: Accuracy of the ML model chosen with respect to length of time recording')
plt.show()

## Plot C parameters
plt.figure(5)
plt.plot(time_record_len, wFR_Cparams)
plt.xlabel('Time recording length')
plt.ylabel('C parameter value')
plt.title('WalkFR: Value of C parameter of SVM kernel with respect to length of time recording')
plt.show()
