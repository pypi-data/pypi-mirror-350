from pocketbase import PocketBase

class PocketbaseUtils:
    def __init__(self):
        from ekko_cli.utils.singleton_utils import get_session_utils
        session_utils = get_session_utils()
        auth = session_utils.get_session()
        self.pb = PocketBase('https://pocketbase.sv-eu.zykkl.dev/')
        if auth:
            self.pb.collection('users').auth_with_password(auth["username"], auth["password"])