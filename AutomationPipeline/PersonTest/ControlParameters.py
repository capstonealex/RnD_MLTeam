# =============================================================================
# === Intent Sampling Controls ================================================ 
# =============================================================================
# exoskeleton records data at 100 Hz or samples per second

RECORD_TIME = 58        # centiseconds: desired intent window before transition state
SAMPLE_RATE = 100       # desired samples per second (must be value between 1 to 100)

# =============================================================================
# === Exoskeleton Field Index Guide ===== 28th Aug 2021 ======================= 
# =============================================================================
# Crutches: L/R --> Forces: {x,y,z}, Torques: {x,y,z} 

# - time                    x 01     ind: 0
# - CrutchReadingsL         x 06     ind: 01 - 06        # I think Left?
# - CrutchReadingsR         x 06     ind: 07 - 12        # I think right?
# - ForcePlateReadings      x 16     ind: 13 - 28
# - MotorPositions          x 04     ind: 29 - 32
# - MotorVelocities         x 04     ind: 33 - 36
# - MotorTorques            x 04     ind: 37 - 41
# - GoButton                x 01     ind: 42
# - CurrentState            x 01     ind: 43
# - CurrentMovement         x 01     ind: 44

SELECTROWS = [0,1,2,3,4,5,6,7,8,9,10,11,12,29,30,31,32,33,34,35,36,37,38,39,40,41]

# SELECTROWS = [0,37,38,39,40,41]

# Don't touch these probably
FILLEDROW = 44              # If exo did a full row reading, sometimes row can come up incomplete (usually end <- termination mid recording)
ID_CURRSTATE = -2           # left at -2 for multipurpose select of current state


RAND_SEEDS = [655, 143, 517, 529, 886, 212, 931, 422, 210, 94, 752, 7]

SEED_OF_LIFE = 42