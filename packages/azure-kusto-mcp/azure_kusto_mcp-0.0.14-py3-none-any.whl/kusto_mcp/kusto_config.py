from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class KustoConfig:
    query_service_uri: str
    database_name: Optional[str]
