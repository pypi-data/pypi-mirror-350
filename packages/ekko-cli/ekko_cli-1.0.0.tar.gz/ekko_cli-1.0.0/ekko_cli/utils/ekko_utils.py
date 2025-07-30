import tempfile
import subprocess
from ekko.dto import EntryDTO, DayDTO
from datetime import date

from ekko.dto.label_dto import LabelDTO


class EkkoUtils:
    def __init__(self):
        from ekko.utils.singleton_utils import get_config_utils, get_database_utils
        self.db = get_database_utils()
        self.config_utils = get_config_utils()

    @staticmethod
    def get_description():
        initial_content="# Input your description here. Lines starting with a '#' are ignored\n"
        lines=[]

        with tempfile.NamedTemporaryFile(suffix='.tmp', mode='w+', delete=False) as file:
            file.write(initial_content)
            file.flush()
            file_path = file.name
        
        subprocess.run(['vim', file_path])

        with open(file_path, 'r') as f:
            lines = [line for line in f.readlines() if not line.startswith('#')]
        
        file.close()

        content = ''.join(lines)
        
        return content
    
    def add_entry(self, summary: str, description: str, labels: list[LabelDTO]):
        entry = EntryDTO(summary, description, labels)
        self.db.create_entry(entry)
