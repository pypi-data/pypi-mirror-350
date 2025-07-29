from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RequestConfig:
    http_verb: str
    url: str
    headers: dict = field(default_factory=dict)
    query_params: dict = None
    body: Optional[dict] = None
