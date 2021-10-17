from DataFunctionsRecord import *     # functions stored in separate file

# - Laptop
PC_DIR = "/mnt/c/Users/david/OneDrive - The University of Melbourne/Work/2021/Capstone/MLTeam//DataProcessing/"

# - Desktop
# PC_DIR = "/mnt/d/Education/Unimelb/OneDrive - Unimelb Student/OneDrive - The University of Melbourne/Work/2021/Capstone/MLTeam/DataProcessing/"
DATAPATH = PC_DIR +"recordings/"
all_filepaths = glob.glob(DATAPATH + "*.csv")

# unique intent "experiment" ID
intent_ID = 0

# data source audit
ID2Intent_index = ""

# Intent Tally
intentCounter = {}

# for all files in record
for name in all_filepaths:
    rowCount = 0
    print("\n"+(name.split(DATAPATH))[1])
    
    # Open CSV file and skip (extract) header    
    csvfile = open(name, 'r')
    reader = csv.reader(csvfile)
    listHeader = next(reader)
    filtHeader = getSelectRows(listHeader) + [" Intent"," ExpID"]
    csvHeader = list2string(filtHeader,True)+"\n"
        
    # Propogate loop til end of csv
    for row in reader:
        rowCount +=1
    
    
    # - Valid row checks
    
        # Skip any unfilled rows (corrupted/stopped mid recording)
        if not len(row) == FILLEDROW:
            print("unfilled row")
            continue
        
        
        # Unstring all number
        row = numifyStringList(row)
        
        
        # Recording determined by Crutch Sensors (time, 1:12, forceplates)
        if sum(row[1:13]) == 0:
            continue    
        
        
        
    # - Found stationary State
        if(row[ID_CURRSTATE] in STATIONARY_STATES):
            prevState = row[ID_CURRSTATE]        
            intent_ID += 1
            
        # - Collect all the stationary States prior to exo movement
            capture = []
            for innerRow in reader:
                rowCount+=1
                innerRow = numifyStringList(innerRow)
                if not (innerRow[ID_CURRSTATE] == prevState):
                    break
                capture.append(getSelectRows(innerRow))
            
        # - Extracting intent into string CSV 
            nextState = innerRow[ID_CURRSTATE]
            intent = categoriseIntent(nextState)
            if "NA" in intent:
                print("No Transation - row: "+str(rowCount))
                continue
            intentCounter = intentTallier(intentCounter, intent)
            filtCapture = sampleIntent(capture) #-record & sample as global Variables
            labelledCapture = labelIntent(filtCapture, intent, intent_ID)
            csvOutput = csvList2String(labelledCapture, False)
            
        # - Automate naming and saving file to directory  
            f = open(PC_DIR+"csvSegments/"+"Exp-"+str(intent_ID)+"_"+intent+".csv", "w")
            f.write(csvOutput)
            f.close()
            
        # - MetaData: ID'ing experiments + csvfileName
             #(name.split(DATAPATH))[1]
            ID2Intent_index += str(intent_ID) + ", \t\t" + intent + ", \t\t" + (name.split(DATAPATH))[1]+ "\n"
    
    csvfile.close()
    
# - Finishing Touches

# Extract Intent Counter Dictionary to txt
strIntentCounter = "Intent, Count\n"
for key in intentCounter:
    strIntentCounter+= key + ", " + str(intentCounter[key]) + "\n"
strIntentCounter+="\n"

# Connect Intent Counter and File Audit 
ID2Intent_index = "ID,\t\t Intent,\t\t Filename\n" + ID2Intent_index

# Write the file
f = open(PC_DIR+"/DataDescription/"+"CountExpIDIndex.txt",'w')
f.write(strIntentCounter+ID2Intent_index)
f.close()

                                

            

