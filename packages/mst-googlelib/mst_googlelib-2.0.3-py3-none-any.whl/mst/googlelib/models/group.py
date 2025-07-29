from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import logging
import time
from typing import Literal, Optional
from googleapiclient import errors
from mst.googlelib import GoogleSDK, models
from mst.googlelib.GoogleSDK import retry
from mst.googlelib.lazy_load import LazyLoad

logger = logging.getLogger(__name__)


class Group(LazyLoad):
    """Represents the Group model for interacting with the GoogleSDK"""

    adminCreated: bool
    aliases: list[str]
    description: str
    directMembersCount: int
    email: str
    etag: str
    id: str
    nonEditableAliases: list[str]
    name: str
    kind: str

    attrs = [
        "adminCreated",
        "aliases",
        "description",
        "directMembersCount",
        "email",
        "etag",
        "id",
        "nonEditableAliases",
        "name",
        "kind",
    ]

    def __init__(self, group_key: str, preload=False, **kwargs):
        self.group_key = group_key
        self.__dict__.update(kwargs)
        if preload:
            self.load_data()

    @retry
    def _load_data(self):
        """Update self with the data provided by the API call."""
        with GoogleSDK().build() as service:
            _group = service.groups().get(groupKey=self.group_key).execute()

        self.__dict__.update(**_group)

    def get_body(self):
        """Create group body with attr

        Returns:
            dict: dictionary of group attrs
        """
        body = {key: val for (key, val) in self.__dict__.items() if key in Group.attrs}
        return body

    def __repr__(self):
        return f"Group {self.group_key} (Loaded: {self.loaded})"

    def __contains__(self, user: models.User | models.Member) -> bool:
        """Allows for the usage of the `in` keyword.

        Args:
            user (models.User | models.Member): The user or member to check the membership of

        Returns:
            bool: True if the user or member is in the group, false otherwise
        """
        return user in self.members

    @classmethod
    @retry
    def list(cls, limit=None, query=None, sort_order="ASCENDING", user_key=None) -> list[Group]:
        """List the whole groups in the group domain.

        Args:
            limit (int, optional): Maximum number of results to return. If none is provided,
                will return all results
            query (str, optional): Query string search. Should be of the form ""
            sort_order (sort_order, optional): whether to return results in ascending or
                descending order
            user_key (str, optional): Email or immutable ID of the user if only those
                groups are to be listed, the given user is a member of

        Returns:
            list[Group]: list of groups
        """

        with GoogleSDK().build() as service:
            page_size = 200  # 200 is most api will allow
            total_groups = []
            page_token = None

            while limit is None or limit > 0:
                max_results = page_size
                if limit:
                    if limit < page_size:
                        max_results = limit
                    limit -= page_size

                response = (
                    service.groups()
                    .list(
                        domain=GoogleSDK.group_domain,
                        maxResults=max_results,
                        pageToken=page_token,
                        query=query,
                        sortOrder=sort_order,
                        userKey=user_key,
                    )
                    .execute()
                )
                groups = response.get("groups", [])
                page_token = response.get("nextPageToken")

                total_groups.extend([Group(group["email"], **group) for group in groups])
                if not page_token:  # No page token means everything has been returned
                    break
        return total_groups

    @retry
    def get_members(self, include_derived_membership=False, roles=None) -> list[models.Member]:
        """Get members of group.

        Args:
            include_derived_membership (boolean, optional): Whether to list indirect memberships. Default: false
            roles (str, optional): The 'roles' query parameter allows you to retrieve group members by role. Allowed values are 'OWNER', 'MANAGER', and 'MEMBER'.

        Returns:
            list[models.Member]: list of members
        """

        with GoogleSDK().build() as service:
            request = service.members().list(
                groupKey=self.group_key,
                includeDerivedMembership=include_derived_membership,
                roles=roles,
            )
            members = []
            while request:
                response = request.execute()
                members.extend(response.get("members", []))
                request = service.members().list_next(previous_request=request, previous_response=response)

        if members:
            return [models.Member(user_key=member["email"], group_key=self.group_key, **member) for member in members]
        return []

    @property
    def members(self) -> list[models.Member]:
        """Returns the list of all members including owner, manager."""
        return self.get_members()

    @property
    def owners(self) -> list[models.Member]:
        """Returns the list of owners."""
        return self.get_members(roles="OWNER")

    @property
    def managers(self) -> list[models.Member]:
        """Returns the list of managers."""
        return self.get_members(roles="MANAGER")

    @classmethod
    @retry
    def create(cls, group_key, **kwargs) -> Group:
        """Creates a Google group and returns associated object.

        Returns: API response if successful
        """
        new_group = cls(group_key, **kwargs)

        body = new_group.get_body()
        body["email"] = group_key
        with GoogleSDK().build() as service:
            _group = service.groups().insert(body=body).execute()
            new_group.__dict__.update(**_group)
        return new_group

    @retry
    def update(self, **kwargs):
        """Updates group in Google based on current state of instance.

        Returns: API response if successful
        """

        self.__dict__.update({key: val for (key, val) in kwargs.items() if key in Group.attrs})
        body = self.get_body()

        with GoogleSDK().build() as service:
            _group = service.groups().update(groupKey=self.group_key, body=body).execute()
            self.__dict__.update(**_group)
        return self

    @retry
    def delete(self):
        """Deletes group in Google corresponding to current instance.

        Returns: API response if successful
        """
        with GoogleSDK().build() as service:
            return service.groups().delete(groupKey=self.group_key).execute()

    def add_member(self, user: models.User | models.Member, role="MEMBER") -> models.Member:
        """Add a member to the group.

        Args:
            user (models.User|models.Member): user to be added to the group
            role (str, optional): user's role in a group. Defaults to 'MEMBER'.

        Returns:
            models.Member
        """
        body = {"email": user.user_key, "role": role}
        with GoogleSDK().build() as service:
            _member = service.members().insert(groupKey=self.group_key, body=body).execute()

            return models.Member(user_key=_member["email"], group_key=self.group_key, **_member)

    def add_owner(self, user: models.User | models.Member):
        """Add owner to a group."""
        member = self.add_member(user, role="OWNER")
        return member

    def remove_member(self, member: models.User | models.Member):
        """Remove a member or user from the group."""
        with GoogleSDK().build() as service:
            try:
                response = service.members().delete(groupKey=self.group_key, memberKey=member.user_key).execute()
            except errors.HttpError as exception:
                if exception.reason == "Resource Not Found: memberKey":
                    response = ""
                else:
                    raise
        return response

    def add_members(
        self,
        users: list[models.User | models.Member],
        role: Literal["MEMBER", "OWNER"] = "MEMBER",
        _batch_size: int = 50,
        _delay: float = 0.1,
    ) -> list[BatchResponse]:
        """Adds a list of users to the group.

        Args:
            users (list[models.User  |  models.Member]): The list of users or member objects to add.
            role (str, optional): The role the members should be. Defaults to "MEMBER".
            _batch_size (int): The number of members to process at a time
            _delay (float): The delay between each batch

        Returns:
            list[BatchResponse]: A list containing the BatchResponse for each user.
        """

        return self._batch_process(
            users,
            role=role,
            batch_size=_batch_size,
            delay=_delay,
            action=BatchActions.ADD,
        )

    def add_owners(self, users: list[models.User | models.Member]) -> list[BatchResponse]:
        """Adds a list of owners to the group.

        Args:
            users (list[models.User | models.Member]): The list of users or member objects to add.

        Returns:
            list[BatchResponse]: A list containing the BatchResponse for each user.
        """
        return self.add_members(users, role="OWNER")

    def remove_members(
        self,
        members: list[models.User | models.Member],
        _batch_size: int = 15,
        _delay: float = 0.5,
    ) -> list[BatchResponse]:
        """Removes a list of members from a group.

        Args:
            members (list[models.User | models.Member]): The list of members to remove
            _batch_size (int): The number of members to process at a time
            _delay (float): The delay between each batch

        Returns:
            list[BatchResponse]: A list with a BatchResponse for each member in `members`.
        """
        return self._batch_process(members, batch_size=_batch_size, delay=_delay, action=BatchActions.REMOVE)

    def _batch_process(
        self,
        members: list[models.Member | models.User],
        batch_size: int,
        delay: float,
        action: Literal[BatchActions.ADD, BatchActions.REMOVE],
        role: Optional[Literal["MEMBER", "OWNER"]] = None,
    ) -> list[BatchResponse]:
        """Performs a batch operation. Called recursively for any failures until batch size is 1.

        Args:
            members (list[models.Member  |  models.User]): The list of members or users to operate against
            batch_size (int): The size of each batch
            delay (float): The delay in seconds between each batch
            action (Literal[BatchActions.ADD, BatchActions.REMOVE]): The action to take. Only supports `BatchActions.ADD` and `BatchActions.REMOVE`
            role (Optional[Literal["MEMBER", "OWNER"]], optional): The role to use, either `MEMBER` or `OWNER`. Only used for `BatchActions.ADD`. Defaults to None.

        Raises:
            NotImplementedError: Raised if action set to something other than add or remove.

        Returns:
            list[BatchResponse]: _description_
        """
        if action not in [BatchActions.ADD, BatchActions.REMOVE]:
            raise NotImplementedError("_batch_process only supports actions 'add' and 'remove'.")

        # Which failed requests should be retried
        retry_reasons = [
            "Request rate higher than configured.",
            "Service unavailable. Please try again",
            "The service is currently unavailable.",
            "Backend Error",
        ]

        results = []

        def list_builder(request_id: str, response, exception: errors.HttpError):
            """Callback function for batch operation. Will add to the `results` list from parent scope.

            Args:
                request_id (str): Set to the user key
                response: Response from the server
                exception (errors.HttpError): The exception returned, if any. Will be None if no exception.
            """
            nonlocal results

            # Set Member to None if there is an exception or the action type is not add
            member = (
                models.Member(user_key=request_id, group_key=self.group_key, **response)
                if action == BatchActions.ADD and not exception
                else None
            )
            result = BatchResponse(
                user_key=request_id,
                group_key=self.group_key,
                member=member,
                exception=exception,
                successful=bool(not exception),
                action=action,
            )
            results.append(result)

        running_error_count = 0
        chunks = [members[i : i + batch_size] for i in range(0, len(members), batch_size)]
        google_sdk = GoogleSDK()
        with google_sdk.build() as service:
            for chunk in chunks:
                batch = service.new_batch_http_request()
                for member in chunk:
                    if action == BatchActions.ADD:
                        body = {"email": member.user_key, "role": role}
                        batch.add(
                            service.members().insert(groupKey=self.group_key, body=body),
                            callback=list_builder,
                            request_id=member.user_key,
                        )
                    elif action == BatchActions.REMOVE:
                        batch.add(
                            service.members().delete(groupKey=self.group_key, memberKey=member.user_key),
                            callback=list_builder,
                            request_id=member.user_key,
                        )
                batch.execute()
                error_count = len([result for result in results if not result.successful])
                error_count -= running_error_count
                running_error_count += error_count
                logger.debug(f"Chunk size {len(chunk)} finished with {error_count} errors")
                time.sleep(delay + 1) if error_count else time.sleep(delay)

        failures = [result for result in results if not result.successful and result.exception.reason in retry_reasons]

        results = [result for result in results if result not in failures]

        # Don't retry any failures if batch size is already 1, just return the results
        if failures and batch_size != 1:
            next_batch_size = max(1, int(batch_size / 2))

            logger.debug(f"Detected {len(failures)} failures, trying again with batch size {next_batch_size}")

            results.extend(
                self._batch_process(
                    failures,
                    batch_size=next_batch_size,
                    delay=delay,
                    action=action,
                    role=role,
                )
            )

        return results


class BatchActions(Enum):
    """Valid actions for currently implemented batch operations"""

    ADD = "add"
    REMOVE = "remove"


@dataclass
class BatchResponse:
    """Represents the response from adding or removing a member to a group in a batch"""

    action: BatchActions
    user_key: str
    group_key: str
    member: Optional[models.Member]
    exception: Optional[Exception]
    successful: bool
