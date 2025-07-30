from pydantic import BaseModel


class PaginationConfig(BaseModel):
    default_page: int = 1
    default_page_size: int = 10
    max_page_size: int | None = 20
    url_page_param: str = "page"
    url_page_size_param: str = "pageSize"
