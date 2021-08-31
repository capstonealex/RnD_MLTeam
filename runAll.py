# - Run all scripts
SCRIPT0 = "annotate_DataSets.py"
SCRIPT1 = "extract_IntentCSVs.py"
SCRIPT2 = "merge_CSVModels.py"

# Add or remove as necessary
processingScripts = [SCRIPT0, SCRIPT1, SCRIPT2]

for i in processingScripts:
    exec(open(i).read())