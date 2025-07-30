"""
This module provides ressources for location of users from the 42 API.
"""

from typing import TYPE_CHECKING, Any, List, Optional, Self

from dateutil.parser import parse as parse_date

from fortytwo_client.json import register_serializer
from fortytwo_client.resources.ressource import FortyTwoRessource, RessourceTemplate

if TYPE_CHECKING:
    from datetime import datetime


class FortyTwoLocation:
    """
    This class provides a representation of a 42 location.
    """

    def __init__(self: Self, data: Any) -> None:
        self.id: int = data["id"]
        self.host: str = data["host"]

        self.begin_at: datetime = parse_date(data["begin_at"])
        self.end_at: Optional[datetime] = (
            parse_date(data["end_at"]) if data["end_at"] else None
        )

    def __repr__(self: Self) -> str:
        return f"<FortyTwoLocation {self.id}>"

    def __str__(self: Self) -> str:
        return self.id


register_serializer(
    FortyTwoLocation,
    lambda u: {
        "id": u.id,
        "begin_at": u.begin_at.isoformat(),
        "end_at": u.end_at.isoformat() if u.end_at else None,
    },
)


class GetLocationsByUserId(FortyTwoRessource[List[FortyTwoLocation]]):
    """
    This class provides a ressource for getting the locations of a user.
    """

    method: str = "GET"
    _url: str = "/users/%s/locations"

    def __init__(self: Self, user_id: int) -> None:
        self.user_id = user_id

    @property
    def url(self: Self) -> str:
        return self.config.endpoint + self._url % self.user_id

    def parse_response(self: Self, response_data: Any) -> RessourceTemplate:
        return [FortyTwoLocation(location) for location in response_data]


__all__ = [
    "FortyTwoLocation",
    "GetLocationsByUserId",
]
