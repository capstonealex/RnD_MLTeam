from ControlParameters import *
from CommandIndex import *
from collections import deque

# =============================================================================
# === Dequeue and ML Functions ================================================ 
# =============================================================================

def extractQueue(queue):
    modelInput = []
    for moment in queue:
        modelInput += moment
    return(modelInput)


def feedModel(modelInput):
    # feeds list of features to model and returns decision
    return()


def outputUI(result):
    # sort provide ordered UI list to model
    return()

def extractOrderlist(queue):
    modelInput = extractQueue(queue)
    result = feedModel(modelInput)
    outputUI(result)
    return()



# =============================================================================
# === Read ExoDataScript ====================================================== 
# =============================================================================

EXODATA_RATE = 100      # seconds to discrete time = 100 samples a second
FIRST_DELAY = 10        # seconds: first exit transition state delay
STATIONARY_DELAY = 5    # seconds: loop in stationary intent  delay
#TRANSITION_DELAY = 3   # if we need to optimise computation

tick = 0
firstDelay = (10 - RECORD_TIME)*EXODATA_RATE
stationaryDelay = (5 - RECORD_TIME)*EXODATA_RATE



MAX_Q_LENGTH = RECORD_TIME*100*SAMPLE_RATE/100
queue = deque(maxlen=MAX_Q_LENGTH)
exoReading = [0,0,0]
inStationary = False

while(True):
    # queue automatically pops data
    # investigate how to do sampling (i.e. ignore certain features)
    queue.appendleft(exoReading)
    
    # left transition state
    if ~inStationary and exoReading[ID_CURRSTATE] in STATIONARY_STATES:
        extractOrderlist(queue)
        inStationary = True
        tick = 0
        while tick < FIRST_DELAY:
            tick += 1
    
    # loop readings in stationary
    if inStationary:
        tick +=1
        if tick >= STATIONARY_DELAY:
            extractOrderlist(queue)
            tick = 0
    
    if exoReading[ID_CURRSTATE] in TRANSITION_STATES:
        inStationary = False
        
        
    
    
    
    
    



        



