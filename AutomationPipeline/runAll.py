# - Run all scripts
SCRIPT1 = "ExtractIntent.py"
SCRIPT2 = "MergeCSVs.py"

# Add or remove as necessary
processingScripts = [SCRIPT1, SCRIPT2]

for i in processingScripts:
    exec(open(i).read())