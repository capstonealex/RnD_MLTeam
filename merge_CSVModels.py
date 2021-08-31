from DataFunctionsList import *     # functions stored in separate file
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

sitModel = header
walkModel = header
standModel = header
backModel = header

intent_filepaths = glob.glob(DIR_INTENT + "*.csv")

for pathname in intent_filepaths:
    filename = os.path.basename(pathname)

    (prevstate, nextstate) = namesplitter(filename)    
    file = open(pathname, 'r')
    csvData = file.read()
    
    if prevstate == "sit":
        sitModel += csvData
    
    if prevstate == "stand":
        standModel += csvData
        
    if prevstate == "walk":    
        walkModel += csvData
    
    file.close()
    

f = open(DIR_MODEL + "sitCSVData.csv",'w')
f.write(sitModel)
f.close()

f = open(DIR_MODEL + "standCSVData.csv",'w')
f.write(standModel)
f.close()

f = open(DIR_MODEL + "walkCSVData.csv",'w')
f.write(walkModel)
f.close()

print("Done")