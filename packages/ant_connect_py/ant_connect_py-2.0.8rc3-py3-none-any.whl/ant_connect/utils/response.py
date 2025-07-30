from __future__ import annotations
from dataclasses import dataclass


@dataclass
class TokenResponse:
    token_type: str
    expires_in: int
    access_token: str
    refresh_token: str

    @classmethod
    def from_json(cls, request_response: dict) -> TokenResponse:
        return cls(
            token_type=request_response["token_type"],
            expires_in=request_response["expires_in"],
            access_token=request_response["access_token"],
            refresh_token=request_response["refresh_token"],
        )
