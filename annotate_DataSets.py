from DataFunctionsList import *     # functions stored in separate file
print("<Annotating DataSets ...>\n")
checkDirectoryRAW()

# Messy Formatting Things
ALIGNMENT = 50
ARROW = "[->]"
SPACER = ARROW + 10*' '
outputTXT = "Filename"+ 42*' ' + SPACER +"Intents\n"+200*'=' + "\n"

# Main File Reading
for name in all_filepaths:
    filename = os.path.basename(name)
    print("Reading:",filename)
    
    # Extract file name from path
    tabBuffer = (ALIGNMENT-len(filename))*' '
    
    # CSV things
    csvfile = open(name, 'r')
    
    reader = csv.reader(csvfile)
    next(reader)    # skip header
    
    intentList = "" 
    recordState = 0
    for row in reader:
    
    # - Valid row checks
    
        # Skip any unfilled rows (corrupted/stopped mid recording)
        if not len(row) == FILLEDROW:
            print(" + Skipped an unfilled row")
            continue
            
        # Unstring all numbers
        row = numifyStringList(row)
        
        currState = row[ID_CURRSTATE]
        
        # skip unnecessary
        if (currState == recordState):
            continue
    
        # transition detected
        if (currState in TRANSITION_STATES):    
            recordState = row[ID_CURRSTATE]
            intentList += categoriseIntent(recordState) +",\t"
    
    
    outputTXT += filename + tabBuffer + SPACER + intentList + "END\n\n"
    

f = open(FNAME_DESCRIPTION,'w')
f.write(outputTXT)
f.close()

print("Done")