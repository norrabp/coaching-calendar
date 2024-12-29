from typing import Optional
from backend.types.query_opts import PaginationInfo

MAX_PAGE_SIZE = 100


def get_pagination(pagination: Optional[PaginationInfo]) -> PaginationInfo:
    """This will fetch default pagination info if none is provided and ensure the page size is not greater than MAX_PAGE_SIZE"""
    if pagination is None:
        pagination = PaginationInfo()
    if pagination.page_size > MAX_PAGE_SIZE:
        pagination.page_size = MAX_PAGE_SIZE
    return pagination
