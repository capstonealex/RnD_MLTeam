from MLModelFunctions import CSV_STAND, CSV_WALKL, CSV_WALKR
from ExtractIntentFunctions import *     # functions stored in separate file
checkMakeDirectoryMerge()
checkMakeDirectoryModel()
print("<Merging Intents ...>\n")

# Get Header
try:
    f = open(FNAME_EXTRACTION,'r')
except FileNotFoundError:
    print("Header file: "+FNAME_EXTRACTION+" not found")
    exit(1)

header = next(f)
f.close()

intent_filepaths = glob.glob(DIR_INTENT + "*.csv")


standModel = header
walkModel_L = header
walkModel_R = header


for pathname in intent_filepaths:
    filename = os.path.basename(pathname)
    filename = filename.strip(".csv")
    
    (prevstate, nextstate) = intentIdentify(pathname)       # no longer file name dependent
    file = open(pathname, 'r')
    csvData = file.read()
    
    if prevstate == "stand":
        standModel += csvData
        
    if prevstate == "walkFL":    
        walkModel_L += csvData
    
    if prevstate == "walkFR":    
        walkModel_R += csvData
    
    file.close()


f = open(DIR_MERGE + CSV_STAND +"-SR_"+str(SAMPLE_RATE)+"-TR_"+str(RECORD_TIME)+".csv",'w')
f.write(standModel)
f.close()

f = open(DIR_MERGE + CSV_WALKL +"-SR_"+str(SAMPLE_RATE)+"-TR_"+str(RECORD_TIME)+".csv",'w')
f.write(walkModel_L)
f.close()

f = open(DIR_MERGE + CSV_WALKR +"-SR_"+str(SAMPLE_RATE)+"-TR_"+str(RECORD_TIME)+".csv",'w')
f.write(walkModel_R)
f.close()

print("merges done")