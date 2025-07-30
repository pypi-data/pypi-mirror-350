from pydantic import HttpUrl, BaseModel

__all__ = [
    "PaginationInfo",
    "Paginated",
]


class PaginationInfo(BaseModel):
    page: int
    page_size: int
    total_pages: int | None = None
    total: int | None = None
    next_page: HttpUrl | None = None
    prev_page: HttpUrl | None = None


class Paginated[T: BaseModel](BaseModel):
    data: list[T]
    pagination: PaginationInfo
