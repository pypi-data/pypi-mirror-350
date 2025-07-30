import subprocess
import tempfile

from ekko_cli.dto.label_dto import LabelDTO


class LabelUtils:
    def __init__(self):
        from ekko_cli.utils.singleton_utils import get_database_utils
        self.db = get_database_utils()

    def create(self, name, description):
        label = LabelDTO(name, description)
        self.db.create_label(label)

    def get_labels(self, visibility: str):
        return self.db.get_labels(visibility)

    def hide(self, label):
        self.db.hide_label(label)

    def show(self, label):
        self.db.show_label(label)

    @staticmethod
    def get_description():
        initial_content = "# Input your description here. Lines starting with a '#' are ignored\n"
        lines = []

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
