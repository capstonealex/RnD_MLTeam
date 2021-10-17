from DataFunctionsList import *     # functions stored in separate file
print("<Annotating DataSets ...>\n")
checkDirectoryRAW()

# Messy Formatting Things
ALIGN0 = 50
ALIGN1 = 25
ALIGN2 = 15
ARROW = "[->]"
SPACER = ARROW + 10*' '

TXT_HEADERROW = "Filename"+ 42*' '  + SPACER +"Intents\n"+200*'=' + "\n" 

minStationaryTime = float('inf')
minTransitionTime = float('inf')
outputTXT = TXT_HEADERROW

for name in all_filepaths:
    
    # Get Filename and Print progress
    filename = os.path.basename(name)
    print("Reading:",filename)
    
    # Extract file name from path
    tabBuffer = (ALIGN0-len(filename))*' '  
    
    # CSV processing
    csvfile = open(name, 'r')
    reader = csv.reader(csvfile)
    next(reader)                    # skip header
    
    
    
# - CSV File Row Loop
    intentList = "" 
    prevState = 0
    timeCount = 0
    
    for row in reader:
    # - Timer 
        timeCount +=1
        
    # - Valid row checks
        # Skip any unfilled rows (corrupted/stopped mid recording)
        if not len(row) == FILLEDROW:
            print(" + Skipped an unfilled row")
            continue
        
        # Unstring all numbers
        row = numifyStringList(row)
    
        currState = row[ID_CURRSTATE]
        
        # Changed states ->  intent and times between
        if(prevState != currState):
            elapsedTime = str(format(timeCount/100,".2f"))
            textState = ALLSTATES_DIC[prevState]
            tabBuffer2 = (ALIGN2-len(textState))*' ' 
            # Moved from transition to stationary
            if prevState in TRANSITION_STATES:
                #tabBuffer1 = (ALIGN1-len(elapsedTime))*' '
                #intentList += "<Tr: "+ elapsedTime+" secs>," + tabBuffer1

                if timeCount < minTransitionTime:
                    minTransitionTime = timeCount
                    mTTname = textState + tabBuffer2 + "@ " + filename

            # Moved from stationary to transition
            if prevState in STATIONARY_STATES:
                intentList += categoriseIntent(currState) +",\t"
                #intentList +=" ("+ elapsedTime+" secs)," + tabBuffer1
                if timeCount < minStationaryTime:
                    minStationaryTime = timeCount
                    mSTname = textState + tabBuffer2 + "@ " + filename
            
            # New State and Reset
            prevState = currState
            timeCount = 0
        
    outputTXT += filename + tabBuffer + SPACER + intentList + "END\n\n"

# Figuring out Recording TimeBounds
minStationaryTime = str(format(minStationaryTime/100,".3f"))
minTransitionTime = str(format(minTransitionTime/100,".3f"))
minStationaryTime = "minStationaryTime:  "+ minStationaryTime + " seconds  ->   " + mSTname
minTransitionTime = "minTransitionTime:  "+ minTransitionTime + " seconds  ->   " + mTTname
print("-")
print(minStationaryTime)
print(minTransitionTime)

# output file
outputTXT = "TimeBounds\n"+200*'='+"\n"+ minStationaryTime +"\n" + minTransitionTime+"\n\n" + outputTXT
f = open(FNAME_DESCRIPTION,'w')
f.write(outputTXT)
f.close()

print("Done")
