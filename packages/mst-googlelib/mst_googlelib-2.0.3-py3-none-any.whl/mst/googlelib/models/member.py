from __future__ import annotations
from mst.googlelib import GoogleSDK
from mst.googlelib.GoogleSDK import retry
from mst.googlelib.lazy_load import LazyLoad


class Member(LazyLoad):
    """Represents the Member model for interacting with the GoogleSDK"""

    role: str
    kind: str
    email: str
    etag: str
    type: str
    status: str
    deliverySettings: str
    id: str

    def __init__(self, user_key: str, group_key: str, preload=False, **kwargs):
        self.member_key = user_key
        self.user_key = user_key
        self.group_key = group_key
        self.__dict__.update(kwargs)

        if preload:
            self.load_data()

    @retry
    def __repr__(self):
        return f"Member {self.user_key} in {self.group_key} (Loaded: {self.loaded})"

    def _load_data(self):
        """Update self with the data provided by the API call."""
        with GoogleSDK().build() as service:
            _member = service.members().get(groupKey=self.group_key, memberKey=self.member_key).execute()
            if _member:
                self.__dict__.update(**_member)

    def before_member(self):
        """Provide dictionary of email and role, minimum requirement to become member

        Returns:
            dict
        """
        return {"email": self.user_key, "role": self.role}

    @retry
    def is_member(self) -> bool:
        """Checks whether the given user is a member of the group. Membership can be direct or nested."""
        with GoogleSDK().build() as service:
            is_member = service.members().hasMember(groupKey=self.group_key, memberKey=self.member_key).execute()
            if is_member:
                return is_member["isMember"]

    @retry
    def update_membership(self, role) -> Member:
        """Update membership property"""
        self.role = role.upper()

        with GoogleSDK().build() as service:
            _member = (
                service.members()
                .update(
                    groupKey=self.group_key,
                    memberKey=self.member_key,
                    body=self.__dict__,
                )
                .execute()
            )
            self.__dict__.update(**_member)

        return self
