from datetime import date, datetime

class DayDTO:
    def __init__(self):
        datestamp = date.now().isoformat()
        timestamp = datetime.now().isoformat()
        self.id = datestamp
        self.date = datestamp
        self.entries = []
        self.last_synced = timestamp
