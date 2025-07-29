from __future__ import annotations
from typing import Optional, TypedDict
from googleapiclient import errors
from mst.googlelib import GoogleSDK, models
from mst.googlelib.GoogleSDK import retry
from mst.googlelib.lazy_load import LazyLoad


class Name(TypedDict):
    """Name Type"""

    displayname: str
    familyName: str
    fullName: str
    givenName: str


class Email(TypedDict):
    """Email Type"""

    address: str
    customType: str
    primary: bool
    type: str


class Address(TypedDict):
    """Address Type"""

    country: str
    countryCode: str
    customType: str
    extendedAddress: str


class Language(TypedDict):
    """Lauguage Type"""

    languageCode: str
    preference: str


class Organization(TypedDict):
    """Organization Type"""

    location: str
    title: str
    department: str
    name: str
    customType: str
    customType: str
    primary: bool


class User(LazyLoad):
    """Represents the User model for interacting with the GoogleSDK"""

    archived: bool
    customerId: str
    emails: list[Email]
    etag: str
    id: str
    includeInGlobalAddressList: bool
    ipWhitelisted: bool
    isAdmin: bool
    isDelegatedAdmin: bool
    kind: str
    languages: list[Language]
    lastLoginTime: str
    loaded: bool
    name: Name
    organizations: list[Organization]
    primaryEmail: str
    suspended: bool

    def __init__(self, user_key: str, preload=False, **kwargs):
        """Represents a Google user. Data is only loaded once accessed.
        Args:
            key (str): The value used to lookup the user. Can be one of: primary email address, alias email address, or unique user ID.
        """
        self.user_key = user_key
        self.__dict__.update(kwargs)

        if preload:
            self.load_data()

    @retry
    def _load_data(self):
        """Load user data."""
        with GoogleSDK().build() as service:
            _user = service.users().get(userKey=self.user_key).execute()
            if _user:
                self.__dict__.update(**_user)

    def __eq__(self, other: models.User | models.Member) -> bool:
        """Check if two users are same."""
        if not isinstance(other, User) and not isinstance(other, models.Member):
            return False
        if self.loaded:
            return (
                other.user_key == self.user_key
                or other.user_key == self.primaryEmail
                or other.user_key == self.id
                or other.user_key in self.aliases
            )
        if not (self.loaded and other.loaded):
            return self.user_key == other.user_key
        return self.id == other.id or self.primaryEmail == other.primaryEmail

    def __repr__(self) -> str:
        """String representation of user object"""
        return f"User {self.user_key} (Loaded: {self.loaded})"

    @classmethod
    @retry
    def list(cls, limit=None, query=None, sort_order="ASCENDING") -> list[User]:
        """Provide list of google users

        Args:
            limit (int, optional): max results to return. Defaults to 200.
            query (str, optional): query string for searching user fields
            sort_order (str, optional): Whether to return results in ascending or descending order

        Returns:
            list[User]: list of users
        """

        with GoogleSDK().build() as service:
            page_size = 200
            total_users = []
            page_token = None

            while limit is None or limit > 0:
                max_results = page_size
                if limit:
                    if limit < page_size:
                        max_results = limit
                    limit -= page_size

                response = (
                    service.users()
                    .list(
                        domain=GoogleSDK.user_domain,
                        maxResults=max_results,
                        pageToken=page_token,
                        query=query,
                        sortOrder=sort_order,
                    )
                    .execute()
                )

                users = response.get("users", [])
                page_token = response.get("nextPageToken")

                total_users.extend([User(user_key=user["primaryEmail"], **user) for user in users])
                if not page_token:
                    break
            return total_users

    @property
    def groups(self) -> list[models.Group]:
        """Returns a list of groups the user is a member of."""
        _groups = models.Group.list(user_key=self.user_key)
        return _groups

    @property
    def owned_groups(self) -> list[models.Group]:
        """Returns a list of groups the user is an owner of."""
        groups = []

        def list_builder(request_id: str, response, exception: Optional[errors.HttpError]):
            nonlocal groups
            if exception is not None:
                raise exception

            for member_res in response.get("members", []):
                member = models.Member(group_key=request_id, user_key=member_res["email"], **member_res)
                if self == member:
                    groups.append(models.Group(group_key=request_id))

        with GoogleSDK().build() as service:
            batch = service.new_batch_http_request()
            for group in self.groups:
                batch.add(
                    service.members().list(groupKey=group.group_key, roles="OWNER"),
                    callback=list_builder,
                    request_id=group.group_key,
                )
        batch.execute()
        return groups

    def join_group(self, group: models.Group) -> models.Member:
        """Join a group."""
        self._load_data()  # to validate if the user is in google
        return group.add_member(self)

    def leave_group(self, group: models.Group):
        """Leave a group"""
        return group.remove_member(self)
