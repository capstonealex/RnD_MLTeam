from DataFunctions import *     # functions stored in separate file

PC_DIR = "/mnt/d/Education/Unimelb/OneDrive - Unimelb Student/OneDrive - The University of Melbourne/Work/2021/Capstone/MLTeam/DataProcessing/"
DATAPATH = PC_DIR +"csvSegments/"
all_filepaths = glob.glob(DATAPATH + "*.csv")

HEADER = 'time, CrutchReadings_1, CrutchReadings_2, CrutchReadings_3, CrutchReadings_4, CrutchReadings_5, CrutchReadings_6, CrutchReadings_7, CrutchReadings_8, CrutchReadings_9, CrutchReadings_10, CrutchReadings_11, CrutchReadings_12, MotorPositions_1, MotorPositions_2, MotorPositions_3, MotorPositions_4, MotorVelocities_1, MotorVelocities_2, MotorVelocities_3, MotorVelocities_4, MotorTorques_1, MotorTorques_2, CurrentState,Intent,ExpID\n'
sitModel = HEADER
walkModel = HEADER
standModel = HEADER

for name in all_filepaths:
    
    filename = name.split(DATAPATH)[1]
    (prevstate, nextstate) = namesplitter(filename)
    
    file = open(name, 'r')
    csvData = file.read()
    
    if prevstate == "sit":
        sitModel += csvData
    
    if prevstate == "stand":
        standModel += csvData
        
    if prevstate == "walk":    
        walkModel += csvData
    
    file.close()
    

MODELPATH = PC_DIR + "csvPerModel/"

f = open(MODELPATH + "sitCSVData.csv",'w')
f.write(sitModel)
f.close()

f = open(MODELPATH + "standCSVData.csv",'w')
f.write(standModel)
f.close()

f = open(MODELPATH + "walkCSVData.csv",'w')
f.write(walkModel)
f.close()
