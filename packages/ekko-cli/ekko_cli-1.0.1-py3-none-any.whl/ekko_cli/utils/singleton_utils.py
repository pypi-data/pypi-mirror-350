from ekko_cli.utils.config_utils import ConfigUtils
from ekko_cli.utils.database_utils import DatabaseUtils
from ekko_cli.utils.label_utils import LabelUtils
from ekko_cli.utils.pocketbase_utils import PocketbaseUtils
from ekko_cli.utils.session_utils import SessionUtils
from ekko_cli.utils.ekko_utils import EkkoUtils

_config_utils = None
_database_utils = None
_session_utils = None
_ekko_utils = None
_pocketbase_utils = None
_label_utils = None


def get_config_utils():
    global _config_utils
    if _config_utils is None:
        _config_utils = ConfigUtils()
    return _config_utils


def get_database_utils():
    global _database_utils
    if _database_utils is None:
        _database_utils = DatabaseUtils()
    return _database_utils


def get_session_utils():
    global _session_utils
    if _session_utils is None:
        _session_utils = SessionUtils()
    return _session_utils


def get_ekko_utils():
    global _ekko_utils
    if _ekko_utils is None:
        _ekko_utils = EkkoUtils()
    return _ekko_utils

def get_pocketbase_utils():
    global _pocketbase_utils
    if _pocketbase_utils is None:
        _pocketbase_utils = PocketbaseUtils()
    return _pocketbase_utils

def get_label_utils():
    global _label_utils
    if _label_utils is None:
        _label_utils = LabelUtils()
    return _label_utils