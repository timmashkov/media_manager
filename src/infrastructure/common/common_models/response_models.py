from dataclasses import dataclass


@dataclass(frozen=True)
class StatusResponse:
    status: bool
