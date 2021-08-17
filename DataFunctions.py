ALLINTENTS = ["sitting","walking"]

def detectIntent(filepath):
    for intent in ALLINTENTS:
        if (intent in filepath.lower()):
            return intent
