# =============================================================================
# === Import, IO, CSV and File Directory things ===============================
# =============================================================================

import sys
import glob
import os

# output filenames
FNAME_K_DESCRIPTION = "intentTrail_Karo.txt"
FNAME_K_EXTRACTION = "extractionIndex_Karo.txt"

DIR_K_CWD = os.getcwd()
DIR_K_RAW = DIR_K_CWD + "/RawRecords_Karo/"
DIR_K_INTENT = DIR_K_CWD + "/CSVperIntent_Karo/"
DIR_K_MERGE = DIR_K_CWD + "/CSVperModel_Karo/"
# DIR_K_MODEL = DIR_K_CWD + "/MLModelObjects_Karo/"
all_filepaths = glob.glob(DIR_K_RAW + "*.csv")

CSV_K_STAND = "standCSVData_Karo"
CSV_K_WALKL = "walkFLCSVData_Karo"
CSV_K_WALKR = "walkFRCSVData_Karo"


def checkDirectoryRAW_Karo():
    if not (os.path.isdir(DIR_K_RAW)):
        os.mkdir(DIR_K_RAW)
        print("Please Insert Data into: RawRecords_Karo")
        sys.exit(1)


def checkMakeDirectoryIntent_Karo():
    if not (os.path.isdir(DIR_K_INTENT)):
        os.mkdir(DIR_K_INTENT)


def checkMakeDirectoryMerge_Karo():
    if not (os.path.isdir(DIR_K_MERGE)):
        os.mkdir(DIR_K_MERGE)


# def checkMakeDirectoryModel_Karo():
#     if not (os.path.isdir(DIR_K_MODEL)):
#         os.mkdir(DIR_K_MODEL)
