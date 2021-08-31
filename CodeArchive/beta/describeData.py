from DataFunctionsRecord import *     # functions stored in separate file

# - Directory
# Laptop
PC_DIR = "/mnt/c/Users/david/OneDrive - The University of Melbourne/Work/2021/Capstone/MLTeam//DataProcessing/"

# Desktop
# PC_DIR = "/mnt/d/Education/Unimelb/OneDrive - Unimelb Student/OneDrive - The University of Melbourne/Work/2021/Capstone/MLTeam/DataProcessing/"

DATAPATH = PC_DIR +"recordings/"
all_filepaths = glob.glob(DATAPATH + "*.csv")

ALIGNMENT = 50
ARROW = "[->]"
SPACER = ARROW + 10*' '

outputTXT = "Filename"+ 42*' ' + SPACER +"Intents\n"+200*'=' + "\n"
for name in all_filepaths:
    # Extract file name from path
    filename = (name.split(DATAPATH))[1]
    tabBuffer = (ALIGNMENT-len(filename))*' '
    
    # CSV things
    csvfile = open(name, 'r')
    reader = csv.reader(csvfile)
    next(reader)    #skip header
    
    intentList = "" 
    recordState = 0
    for row in reader:
    # - Valid row checks
    
        # Skip any unfilled rows (corrupted/stopped mid recording)
        if not len(row) == FILLEDROW:
            print("unfilled row")
            continue
            
        # Unstring all number
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
    

f = open(PC_DIR+"/DataDescription/"+"Intents_Per_File.txt",'w')
f.write(outputTXT)
f.close()
        
            
