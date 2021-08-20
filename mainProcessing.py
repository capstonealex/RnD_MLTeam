RECORD_TIME = 5;    # seconds: intent before movement
SAMPLE_RATE = 50;    # samples wanted per second (cannot exceed 100)

from DataFunctions import *     # functions stored in separate file

# LP_DIR = "/mnt/c/Users/david/OneDrive - The University of Melbourne/Work/2021/Capstone/MLTeam//DataProcessing/"
PC_DIR = "/mnt/d/Education/Unimelb/OneDrive - Unimelb Student/OneDrive - The University of Melbourne/Work/2021/Capstone/MLTeam/DataProcessing/"
DATAPATH = PC_DIR +"recordings/"
all_filepaths = glob.glob(DATAPATH + "*.csv")

# unique intent "experiment" ID
intent_ID = 0
ID2Intent_index = ""

# for all files in record
for name in all_filepaths:
    
    # Open CSV file and skip (extract) header    
    with open(name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        listHeader = next(reader)
        listHeader += ["Intent","ExpID"]
        csvHeader = list2string(listHeader)
         
    # Keep looping til end of csv
        while(next(reader)):
            row = next(reader)
            
    # - Found stationary State
            if(row[ID_CURRSTATE] in STATIONARY_STATES):
                prevState = row[ID_CURRSTATE]        
                intent_ID += 1
                
    # - Collect all the stationary States prior to exo movement
                capture = []
                while (row[ID_CURRSTATE] == prevState):
                    row = next(reader)
                    capture.append(getSelectRows(row))
                
    # - Extracting intent into string CSV 
                nextState = row[ID_CURRSTATE]
                intent = categoriseIntent(prevState, nextState)
                filtCapture = sampleIntent(capture) #-record & sample as global Variables
                labelledCapture = labelIntent(filtCapture, intent, intent_ID)
                csvOutput = csvHeader + csvList2String(labelledCapture)
                
    # - Automate naming and saving file to directory  
                f = open(PC_DIR+"csvSegments/"+"Exp-"+intent_ID+"_"+intent+".csv", "w")
                f.write(csvOutput)
                f.close()
                
    # - MetaData: ID'ing experiments + csvfileName
                ID2Intent_index += intent_ID + "," + intent + "," (name.split(DATAPATH))[1]+ "\n"


f = open("ExpIDIndex.txt")
f.write(ID2Intent_index)
f.close()

                                

            

