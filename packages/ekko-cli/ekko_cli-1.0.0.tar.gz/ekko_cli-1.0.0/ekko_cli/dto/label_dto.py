class LabelDTO:
    def __init__(self, name, description, entry_id=None, fk_user_id=None):
        self.id = entry_id
        self.name = name
        self.description = description
        self.fk_user_id = fk_user_id
