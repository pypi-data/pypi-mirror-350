from datetime import datetime

class EntryDTO:
    def __init__(self, summary, description, labels):
        timestamp = datetime.now().isoformat()
        self.summary = summary
        self.description = description
        self.labels = labels
        self.creation_date = timestamp