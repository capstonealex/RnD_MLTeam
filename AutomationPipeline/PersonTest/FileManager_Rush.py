# =============================================================================
# === Import, IO, CSV and File Directory things ===============================
# =============================================================================

import sys
import glob
import os

# output filenames
FNAME_R_EXTRACTION = "extractionIndex_Rush.txt"
FNAME_R_DESCRIPTION = "intentTrail_Rush.txt"

DIR_R_CWD = os.getcwd()
DIR_R_RAW = DIR_R_CWD + "/RawRecords_Rush/"
DIR_R_INTENT = DIR_R_CWD + "/CSVperIntent_Rush/"
DIR_R_MERGE = DIR_R_CWD + "/CSVperModel_Rush/"
DIR_R_MODEL = DIR_R_CWD + "/MLModelObjects_Rush/"
all_filepaths = glob.glob(DIR_R_RAW + "*.csv")

CSV_R_STAND = "standCSVData_Rush"
CSV_R_WALKL = "walkFLCSVData_Rush"
CSV_R_WALKR = "walkFRCSVData_Rush"

def checkDirectoryRAW_Rush():
    if not (os.path.isdir(DIR_R_RAW)):
        os.mkdir(DIR_R_RAW)
        print("Please Insert Data into: RawRecords_Rush")
        sys.exit(1)


def checkMakeDirectoryIntent_Rush():
    if not (os.path.isdir(DIR_R_INTENT)):
        os.mkdir(DIR_R_INTENT)


def checkMakeDirectoryMerge_Rush():
    if not (os.path.isdir(DIR_R_MERGE)):
        os.mkdir(DIR_R_MERGE)


def checkMakeDirectoryModel_Rush():
    if not (os.path.isdir(DIR_R_MODEL)):
        os.mkdir(DIR_R_MODEL)
