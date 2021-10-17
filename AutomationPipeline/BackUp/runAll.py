# - Run all scripts
SCRIPT1 = "ExtractIntent.py"
SCRIPT2 = "MergeCSVs.py"
SCRIPT3 = "MLModelScript"
SCRIPT4 = "MLEva"
# Add or remove as necessary
processingScripts = [SCRIPT1, SCRIPT2, SCRIPT3 ]

for i in processingScripts:
    exec(open(i).read())