from pathlib import Path
from platformdirs import user_config_dir, user_data_dir

class ConfigUtils:
    config_dir = Path(user_config_dir("ekko", ensure_exists=True))
    config_file = config_dir / "config.json"
    session_file = config_dir / "session.json"
    data_dir = Path(user_data_dir("ekko"))
    journal_file = data_dir / "journal.json"
