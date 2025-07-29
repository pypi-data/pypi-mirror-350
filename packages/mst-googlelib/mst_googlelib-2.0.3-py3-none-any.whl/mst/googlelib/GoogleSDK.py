from google.oauth2 import service_account
from google.api_core import retry as _retry
from googleapiclient.discovery import build
from mst.core.local_env import local_env

import json
from typing import Callable


class GoogleSDK:
    """Provides a wrapper around the Google Admin SDK API. May be subclassed to access specific resources."""

    if local_env() != "prod":
        user_domain = "qa-um.umsystem.edu"
        group_domain = "grp.gtest.umsystem.edu"
    else:
        user_domain = "umsystem.edu"
        group_domain = "grp.umsystem.edu"

    default_api = "admin"
    default_version = "directory_v1"
    default_scopes = (
        "https://www.googleapis.com/auth/admin.directory.group",
        "https://www.googleapis.com/auth/admin.directory.user.readonly",
    )

    def __init__(self, api=default_api, version=default_version, scopes=default_scopes):
        self.api = api
        self.version = version
        self.scopes = scopes

    @property
    def scoped_credentials(self):
        if self.scopes:
            return GoogleSDK.credentials.with_scopes(self.scopes)
        return GoogleSDK.credentials

    @classmethod
    def init(cls, google_json, user):
        subject = f"{user}@{cls.user_domain}"
        cls.credentials = service_account.Credentials.from_service_account_info(google_json, subject=subject)

    def build(self):
        return build(
            self.api,
            self.version,
            credentials=self.scoped_credentials,
            cache_discovery=False,
        )


def if_retryable(retryable_errors: list[int]) -> Callable[[BaseException], bool]:
    """Creates a predicate to check if the caught exception has one of the http status codes passed
        in. The codes should correspond to http errors that we want to retry.

    Args:
        retryable_errors (list[int]): The http status codes to check for.

    Returns:
        Callable[Exception]: A predicate that returns True if the provided exception has a
            retryable status code and False otherwise.
    """

    def if_error_type_predicate(error: BaseException) -> bool:
        """Bound predicate for checking an exception type."""
        if hasattr(error, "resp"):
            status = getattr(error.resp, "status", 0)
            if status not in retryable_errors:
                return False

            # Special case: skip retry if it's 409 with reason 'duplicate'
            if status == 409:
                try:
                    error_json = json.loads(error.content.decode("utf-8"))
                    reason = error_json["error"]["errors"][0].get("reason")
                    if reason == "duplicate":
                        return False  # skip retry
                except Exception:
                    pass

            return True

        return False

    return if_error_type_predicate


def retry(func):
    nonretryable_errors = {404: "Not Found"}

    retryable_errors = (
        400,  # Bad request
        401,  # Unauthorized
        402,  # Payment Required
        403,  # Forbidden
        405,  # Method Not Allowed
        406,  # Not Acceptable
        407,  # Proxy Authentication Required
        408,  # Request Timeout
        410,  # Gone
        411,  # Length Required
        412,  # Precondition Failed
        413,  # Payload Too Large
        414,  # URI Too Long
        415,  # Unsupported Media Type
        416,  # Range Not Satisfiable
        417,  # Expectation Failed
        418,  # I'm a teapot
        421,  # Misdirected Request
        422,  # Unprocessable Content
        423,  # Locked
        424,  # Failed Dependency
        425,  # Too Early
        426,  # Upgrade Required
        428,  # Precondition Required
        429,  # Too Many Requests
        431,  # Header Fields Too Large
        451,  # Unavailable For Legal Reasons
        500,  # Internal Server Error
        501,  # Not Implemented
        502,  # Bad Gateway
        503,  # Service Unavailable
        504,  # Gateway Timeout
        505,  # HTTP Version Not Supported
        506,  # Variant Also Negotiates
        507,  # Insufficient Storage
        508,  # Loop Detected
        510,  # Not Extended
        511,  # Network Authentication Required
    )

    @_retry.Retry(
        predicate=if_retryable(retryable_errors),
        initial=1,
        maximum=5,
        timeout=30,
    )
    def wrapper(*args, **kwargs):
        return_object = func(*args, **kwargs)
        return return_object

    return wrapper
