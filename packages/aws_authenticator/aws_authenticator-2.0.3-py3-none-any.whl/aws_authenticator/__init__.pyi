__version__: str


class AWSAuthenticator:

    def __init__(
        self,
        profile_name: str = None,
        access_key_id: str = None,
        secret_access_key: str = None,
        session_token: str = None,
        sso_url: str = None,
        sso_role_name: str = None,
        sso_account_id: str = None,
        region_name: str = None
    ) -> None: ...

    def profile(self): ...

    def iam(self): ...

    def sso(self): ...


def get_params(): ...


def main() -> None: ...
