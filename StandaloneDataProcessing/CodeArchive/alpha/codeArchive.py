from DataFunctions import *     # functions stored in separate file
from mainProcessing import *     # functions stored in separate file
##################################################################################################
# <+> Find intent from
# <-> Removed because doesn't contain transition
# <~> var ALLINTENTS, allfilepaths; def detectIntent(filepath)

for name in all_filepaths:
    intent = filenameIntent(name)

##################################################################################################