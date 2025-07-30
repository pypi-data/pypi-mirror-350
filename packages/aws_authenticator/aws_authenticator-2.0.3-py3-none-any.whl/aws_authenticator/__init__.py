"""Login to AWS using CLI named profiles, IAM access key credentials, or SSO."""
import boto3
import botocore.session
import argparse
from pprint import pprint as pp


__version__ = "2.0.3"


class AWSAuthenticator:
    """Login to AWS using CLI named profiles, IAM access key credentials, or SSO."""

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
    ):
        """Initialize AWS login parameters."""
        self._profile_name = profile_name
        self._access_key_id = access_key_id
        self._secret_access_key = secret_access_key
        self._session_token = session_token
        self._sso_url = sso_url
        self._sso_role_name = sso_role_name
        self._sso_account_id = sso_account_id
        self._region_name = region_name

    def profile(self):
        """Login with named profiles."""
        try:
            if not self._profile_name and not self._region_name:
                session = boto3.Session()
            elif self._profile_name and not self._region_name:
                session = boto3.Session(
                    profile_name=self._profile_name
                )
            elif not self._profile_name and self._region_name:
                session = boto3.Session(
                    region_name=self._region_name
                )
            else:
                session = boto3.Session(
                    profile_name=self._profile_name,
                    region_name=self._region_name
                )
            return session
        except Exception as e:
            raise Exception(f"AWS profile login: {str(e)}")

    def iam(self):
        """Login with IAM access key credentials."""
        try:
            if not self._session_token and not self._region_name:
                session = boto3.Session(
                    aws_access_key_id=self._access_key_id,
                    aws_secret_access_key=self._secret_access_key
                )
            elif not self._session_token and self._region_name:
                session = boto3.Session(
                    aws_access_key_id=self._access_key_id,
                    aws_secret_access_key=self._secret_access_key,
                    region_name=self._region_name
                )
            elif self._session_token and not self._region_name:
                session = boto3.Session(
                    aws_access_key_id=self._access_key_id,
                    aws_secret_access_key=self._secret_access_key,
                    aws_session_token=self._session_token
                )
            else:
                session = boto3.Session(
                    aws_access_key_id=self._access_key_id,
                    aws_secret_access_key=self._secret_access_key,
                    aws_session_token=self._session_token,
                    region_name=self._region_name
                )
            return session
        except Exception as e:
            raise Exception(f"AWS IAM login: {str(e)}")

    def sso(self):
        """Login with SSO."""
        try:
            import aws_ssooidc as sso

            access_token = sso.gettoken(self._sso_url)["accessToken"]
            session = botocore.session.get_session()
            # client = boto3.client("sso")
            client = session.create_client(
                "sso",
                region_name=self._region_name
            )
            response = client.get_role_credentials(
                roleName=self._sso_role_name,
                accountId=self._sso_account_id,
                accessToken=access_token
            )
            session = boto3.Session(
                aws_access_key_id=response["roleCredentials"]["accessKeyId"],
                aws_secret_access_key=response["roleCredentials"]["secretAccessKey"],
                aws_session_token=response["roleCredentials"]["sessionToken"],
                region_name=self._region_name
            )
            return session
        except Exception as e:
            raise Exception(f"AWS SSO login: {str(e)}")


def get_params():
    """Get parameters from script inputs."""
    myparser = argparse.ArgumentParser(
        add_help=True,
        allow_abbrev=False,
        description="Login to AWS using CLI named profiles, IAM access key credentials, or SSO.",
        usage="%(prog)s [options]"
    )
    myparser.add_argument(
        "-v", "--version", action="version", version="%(prog)s 2.0.3"
    )
    myparser.add_argument(
        "-m",
        "--auth_method",
        action="store",
        help="AWS authentication method. Valid values can be profile, iam, or sso.",
        required=True,
        type=str
    )
    myparser.add_argument(
        "-p",
        "--profile_name",
        action="store",
        help="AWSCLI profile name for authenticating with a profile.",
        nargs="?",
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        "-k",
        "--access_key_id",
        action="store",
        help="AWSCLI IAM access key ID for authenticating with an IAM user.",
        nargs="?",
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        "-s",
        "--secret_access_key",
        action="store",
        help="AWSCLI IAM secret access key for authenticating with an IAM user.",
        nargs="?",
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        "-t",
        "--session_token",
        action="store",
        help="AWSCLI IAM session token for authenticating with an IAM user.",
        nargs="?",
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        "-a",
        "--sso_account_id",
        action="store",
        help="AWS account ID for authenticating with AWS SSO.",
        nargs="?",
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        "-r",
        "--sso_role_name",
        action="store",
        help="AWS SSO role name for authenticating with AWS SSO.",
        nargs="?",
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        "-u",
        "--sso_url",
        action="store",
        help="AWS SSO login URL for authenticating with AWS SSO.",
        nargs="?",
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        "-z",
        "--region_name",
        action="store",
        help="AWS region name for authenticating with AWS services.",
        nargs="?",
        default="us-east-1",
        required=False,
        type=str
    )
    args = myparser.parse_args()
    return args


def main():
    """Execute class as a script for testing purposes."""
    params = get_params()
    if params.auth_method not in ["profile", "iam", "sso"]:
        raise Exception("Invalid auth method")
    auth = AWSAuthenticator(
        profile_name=params.profile_name,
        access_key_id=params.access_key_id,
        secret_access_key=params.secret_access_key,
        session_token=params.session_token,
        sso_account_id=params.sso_account_id,
        sso_url=params.sso_url,
        sso_role_name=params.sso_role_name,
        region_name=params.region_name
    )
    if params.auth_method == "profile":
        session = auth.profile()
    if params.auth_method == "iam":
        session = auth.iam()
    if params.auth_method == "sso":
        session = auth.sso()
    client = session.client("sts")
    response = client.get_caller_identity()
    response["RegionName"] = session.region_name
    pp(response)


if __name__ == "__main__":
    main()
