import json
import os

import click


class SessionUtils:
    def __init__(self):
        from ekko.utils.singleton_utils import get_config_utils
        config_utils = get_config_utils()
        self.session_file = config_utils.session_file

    def save_session(self, username, password):
        from ekko.utils.singleton_utils import get_pocketbase_utils
        pocketbase_utils = get_pocketbase_utils()
        pb = pocketbase_utils.pb
        user = pb.collection('users').auth_with_password(username, password)
        if (user.is_valid):
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            with open(self.session_file, "w") as f:
                json.dump({'username': username, 'password': password}, f)

    def clear_session(self):
        if os.path.exists(self.session_file):
            os.remove(self.session_file)

    def get_session(self):
        if not os.path.exists(self.session_file):
            return None
        with open(self.session_file) as f:
            return json.load(f)

    def check_session(self):
        if os.path.exists(self.session_file):
            return True
        else:
            return False

    def require_auth(self):
        session = self.get_session()
        if not session:
            click.echo("You have to be logged in to execute this command.")
            click.echo("Login with `ekko auth login`")
            raise click.Abort()

