from typing import Any, Literal, Mapping, Optional

from pydantic import BaseModel

FilterInfo = Mapping[str, Any]
SortInfo = Mapping[str, Literal["asc", "desc"]]


class PaginationInfo(BaseModel):
    page: int = 1
    page_size: int = 20
    offset: int = 0


class QueryOpts(BaseModel):
    filter: Optional[FilterInfo] = None
    sort: Optional[SortInfo] = None
    pagination: PaginationInfo = PaginationInfo()
