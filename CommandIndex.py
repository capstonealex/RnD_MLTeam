# Stationary
COM_LeftForward    =  2       # 
COM_RightForward   =  3       # 
COM_Standing       =  4       # 
COM_Sitting        =  5       # 

STATIONARY_STATES = [COM_LeftForward,COM_RightForward,COM_Standing,COM_Sitting]


# Transition
COM_SittingDown    =  6       # sit FROM stand                      
COM_StandingUp     =  7       # sit TO stand                            
COM_StepFirstL     =  8       # step FROM stand                         
COM_StepFirstR     =  9       # UNUSED?                             
COM_StepLastL      =  10      # step TO stand using LEFT leg        
COM_StepLastR      =  11      # step TO stand using RIGHT leg       
COM_StepL          =  12      # continue walking using LEFT leg     
COM_StepR          =  13      # continue walking using RIGHT leg    
COM_BackStepR      =  14      # backstep using RIGHT leg            
COM_BackStepL      =  15      # backstep using LEFT leg             

TRANSITION_STATES  = [COM_SittingDown, COM_StandingUp, COM_StepFirstL, COM_StepFirstR, COM_StepLastL, COM_StepLastR, COM_StepL ,COM_StepR, COM_BackStepR, COM_BackStepL]

## Strings
STR_SittingDown    =  "stand~sit"       # sit FROM stand
STR_StandingUp     =  "sit~stand"       # sit TO stand
STR_StepFirstL     =  "stand~fwd"       # step FROM stand
STR_StepFirstR     =  "stand~fwd"       # UNUSED?
STR_StepLastL      =  "walk~stand"      # step TO stand using LEFT leg 
STR_StepLastR      =  "walk~stand"      # step TO stand using RIGHT leg
STR_StepL          =  "walk~fwd"        # continue walking using LEFT leg
STR_StepR          =  "walk~fwd"        # continue walking using RIGHT leg
STR_BackStepR      =  "walk~back"       # backstep using RIGHT leg
STR_BackStepL      =  "stand~back"      # backstep using LEFT leg 

# TODO: LWalk and RWalk
    # determine if clusters is confused between L & R leg


# Misc
COM_Init           =  0       # Starting
COM_InitSitting    =  1       # Starting
COM_Error          =  16      # Safety
COM_Debug          =  17      # Safety



# <-> Find Category
def categoriseIntent(nextState):
    
    if(nextState == COM_SittingDown):
        return(STR_SittingDown)
    
    if(nextState == COM_StandingUp):
        return(STR_StandingUp)
    
    
    if(nextState == COM_StepFirstL):
        return(STR_StepFirstL)
    
    # Should not exist, right leg never moves first (see FSM)
    if(nextState == COM_StepFirstR):
        print("StepFirstR EXISTS")
        return(STR_StepFirstR)
    
    
    if(nextState == COM_StepLastL):
        return(STR_StepLastL)
    
    if(nextState == COM_StepLastR):
        return(STR_StepLastR)
    
    
    if(nextState == COM_StepL):
        return(STR_StepL)
    
    if(nextState == COM_StepR):
        return(STR_StepR)
    
    
    if(nextState == COM_BackStepR):
        return(STR_BackStepR)
    
    if(nextState == COM_BackStepL):
        return(STR_BackStepL)
    
    
    # No transition
    return("NA")
   





