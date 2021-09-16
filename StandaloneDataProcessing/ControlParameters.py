# =============================================================================
# === Intent Sampling Controls ================================================ 
# =============================================================================

CAPTURE_DELAY = 0      # seconds: space between end of intent and exoskeleton moving
RECORD_TIME = 1        # seconds: intent before movement (only up to 2 decimal places)
SAMPLE_RATE = 100       # samples wanted per second (cannot exceed 100)



# =============================================================================
# === Exoskeleton Field Index Guide ===== 28th Aug 2021 ======================= 
# =============================================================================
# - time                    x 01     ind: 0
# - CrutchReadings          x 12     ind: 01 - 12
# - ForcePlateReadings      x 16     ind: 13 - 28
# - MotorPositions          x 04     ind: 29 - 32
# - MotorVelocities         x 04     ind: 33 - 36
# - MotorTorques            x 04     ind: 37 - 41
# - GoButton                x 01     ind: 42
# - CurrentState            x 01     ind: 43
# - CurrentMovement         x 01     ind: 44

FILLEDROW = 44
ID_CURRSTATE = -2           # left at -2 for multipurpose

# There's a smarter way to do this but I can't be bothered
# This is also probably computationally faster
SELECTROWS = [0,1,2,3,4,5,6,7,8,9,10,11,12,29,30,31,32,33,34,35,36,37,38,39,40,41]

# Deprecated method
# SELECTHEADER = 'time, CrutchReadings_1, CrutchReadings_2, CrutchReadings_3, CrutchReadings_4, CrutchReadings_5, CrutchReadings_6, CrutchReadings_7, CrutchReadings_8, CrutchReadings_9, CrutchReadings_10, CrutchReadings_11, CrutchReadings_12, MotorPositions_1, MotorPositions_2, MotorPositions_3, MotorPositions_4, MotorVelocities_1, MotorVelocities_2, MotorVelocities_3, MotorVelocities_4, MotorTorques_1, MotorTorques_2, MotorTorques_3, MotorTorques_4, Intent, ExpID\n'



# Feel free to do below
# interestTerms = ["time", "Crutch", "Motor"]
# TODO: loop over a CSV header and append indexes matching above terms
