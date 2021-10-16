import sys
import glob
import os

# =============================================================================
# === Import, IO, CSV and File Directory things ===============================
# =============================================================================

# output filenames
FNAME_EXTRACTION = "extractionIndex.txt"
FNAME_DESCRIPTION = "intentTrail.txt"

DIR_CWD = os.getcwd()
DIR_RAW = DIR_CWD + "/RawRecords/"
DIR_INTENT = DIR_CWD + "/CSVperIntent/"
DIR_MERGE = DIR_CWD + "/CSVperModel/"
DIR_MODEL = DIR_CWD + "/MLModelObjects/"
all_filepaths = glob.glob(DIR_RAW + "*.csv")


def checkDirectoryRAW():
    if not (os.path.isdir(DIR_RAW)):
        os.mkdir(DIR_RAW)
        print("Please Insert Data into: RawRecords")
        sys.exit(1)


def checkMakeDirectoryIntent():
    if not (os.path.isdir(DIR_INTENT)):
        os.mkdir(DIR_INTENT)


def checkMakeDirectoryMerge():
    if not (os.path.isdir(DIR_MERGE)):
        os.mkdir(DIR_MERGE)


def checkMakeDirectoryModel():
    if not (os.path.isdir(DIR_MODEL)):
        os.mkdir(DIR_MODEL)
