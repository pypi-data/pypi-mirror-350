from datetime import datetime, timedelta

from ekko_cli.dto import EntryDTO
from ekko_cli.dto.label_dto import LabelDTO


class DatabaseUtils:
    def __init__(self):
        from ekko_cli.utils.singleton_utils import get_pocketbase_utils
        pocketbase_utils = get_pocketbase_utils()
        self.pb = pocketbase_utils.pb

    def create_entry(self, entry: EntryDTO):
        day_id = self._get_daily_journal()
        new_entry = self.pb.collection("entries").create({
            "summary": entry.summary,
            "description": entry.description,
            "fk_user_id": self.pb.auth_store.base_model.id,
            "fk_day_id": day_id
        })
        for label in entry.labels:
            self.pb.collection("entries_labels").create({
                "fk_entry_id": new_entry.id,
                "fk_label_id": label.id
            })

    def create_label(self, entry: LabelDTO):
        self.pb.collection("labels").create({
            "name": entry.name,
            "description": entry.description,
            "fk_user_id": self.pb.auth_store.base_model.id
        })

    def get_labels(self, visibility: str = "visible"):
        if visibility == "all":
            filter_str = f"fk_user_id = '{self.pb.auth_store.base_model.id}'"
        elif visibility == "visible":
            filter_str = f"fk_user_id = '{self.pb.auth_store.base_model.id}' && hidden = false"
        else:
            filter_str = f"fk_user_id = '{self.pb.auth_store.base_model.id}' && hidden = true"
        return self.pb.collection("labels").get_list(1, 50, {
            "filter": filter_str
        }).items


    def hide_label(self, entry: LabelDTO):
        self.pb.collection("labels").update(entry.id, {
            "name": entry.name,
            "description": entry.description,
            "fk_user_id": entry.fk_user_id,
            "hidden": True
        })

    def show_label(self, entry: LabelDTO):
        self.pb.collection("labels").update(entry.id, {
            "name": entry.name,
            "description": entry.description,
            "fk_user_id": entry.fk_user_id,
            "hidden": False
        })

    def _get_daily_journal(self):
        today = datetime.combine(datetime.now().date(), datetime.min.time())
        lower_threshold = today.date().isoformat()
        upper_threshold = (today + timedelta(days=1)).date().isoformat()
        day = self.pb.collection('days').get_list(1, 1, {"filter": f"date > '{lower_threshold}' && date < '{upper_threshold}'"})
        if day.items:
            return day.items[0].id
        else:
            day = self.pb.collection("days").create({
                "date": today.isoformat()
            })
            return day.id