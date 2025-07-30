"""
This module provides ressources for getting token information.
"""

from typing import Any, List, Optional, Self

from fortytwo_client.json import register_serializer
from fortytwo_client.resources.ressource import FortyTwoRessource, RessourceTemplate


class FortyTwoToken:
    """
    This class provides a representation of a token
    """

    def __init__(self: Self, data: Any) -> None:
        self.owner: Optional[int] = data["resource_owner_id"]
        self.scopes: List[str] = data["scopes"]

        self.expires: int = data["expires_in_seconds"]
        self.uid: str = data["application"]["uid"]

    def __repr__(self: Self) -> str:
        return f"<FortyTwoToken {self.uid}>"

    def __str__(self: Self) -> str:
        return self.uid


register_serializer(
    FortyTwoToken,
    lambda p: {
        "owner": p.owner,
        "scopes": p.scopes,
        "expires": p.expires,
        "uid": p.uid,
    },
)


class GetToken(FortyTwoRessource[FortyTwoToken]):
    """
    This class provides a ressource for getting all project users.
    """

    method: str = "GET"
    _url: str = "https://api.intra.42.fr/oauth/token/info"

    @property
    def url(self: Self) -> str:
        return self._url

    def parse_response(self: Self, response_data: Any) -> RessourceTemplate:
        return FortyTwoToken(response_data)


__all__ = ["FortyTwoToken", "GetToken"]
