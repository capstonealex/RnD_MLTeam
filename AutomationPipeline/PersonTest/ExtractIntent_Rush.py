from pdb import set_trace as bp
from FileManager_Rush import *
from ExtractIntentFunctions import *     # functions stored in separate file

checkDirectoryRAW_Rush()
checkMakeDirectoryIntent_Rush()

print("<Extracting Intents - Rush ...>\n")
data_index = "ID,\t\tIntent,\t\t\tFilename\n"    # data source audit
intentCounter = {}      # Intent Tally
intent_ID = 0           # unique intent "experiment" ID


# for all files in record
for name in all_filepaths:
    filename = os.path.basename(name)
    print("Reading:",filename)
    rowCount = 0
    
    
    # Open CSV file and skip (extract) header    
    csvfile = open(name, 'r')
    reader = csv.reader(csvfile)
    listHeader = next(reader)
    
    nextState = 0
    
        
    # Propogate loop til end of csv
    for rawRow in reader:
        rowCount +=1
    
    
    # - Check for Invalid rows
        
        # Skip any unfilled rows (corrupted/stopped mid recording)
        if not len(rawRow) == FILLEDROW:
            print(" + Skipped Unfilled row at: "+str(rowCount))
            continue
        
        # Unstring all number
        row = numifyStringList(rawRow)
        
        # Recording determined by Crutch Sensors (time, 1:12, forceplates)
        if notRecording(row):
            continue
        
        prevState = row[ID_CURRSTATE]
        
    # - Found stationary State
        if(prevState in STATIONARY_STATES):
            
            intent_ID += 1
            
        # - Collect all the stationary States prior to exo movement
            capture = []
            for statRow in reader:
                rowCount += 1
                statRow = numifyStringList(statRow)
                nextState = statRow[ID_CURRSTATE]
                
                # End of stationary state, end capture loop
                if not (nextState == prevState):
                    break
                
                capture.append(getSelectRows(statRow))
                
        # - Extracting intent into string CSV
            intent = categoriseIntent(nextState)
            if "NA" in intent:
                print(" + No Transition ("+str(int(nextState))+") - row: "+str(rowCount)+"\n")
                continue
            
            intentCounter = intentAccumulate(intentCounter, intent)
            filtCapture = sampleIntent(capture) #-record & sample as global Variables                
            labelledCapture = labelIntent(filtCapture, intent, intent_ID)                
            csvOutput = csvList2String(labelledCapture, False)
                             
        # - Automate naming and saving file to directory
            f = open(DIR_R_INTENT+"Exp_"+str(intent_ID)+"-"+intent+"-SR_"+str(SAMPLE_RATE)+"-RT_"+str(RECORD_TIME)+".csv", "w")
            f.write(csvOutput)
            f.close()
                
                
            data_index += str(intent_ID) + ",\t\t" + intent + ",\t\t" + filename + "\n"
    
    csvfile.close()




# Generate header for model CSV stitching
filtHeader = getSelectRows(listHeader) + [" Intent"," ExpID"]
csvHeader = list2string(filtHeader,True)+"\n\n"

strIntentCounter = intentDic2String(intentCounter)

# Write the file
f = open(FNAME_R_EXTRACTION,'w')
f.write(csvHeader + strIntentCounter + data_index)
f.close()

print("Done")