from typing import Optional

from pydantic import BaseModel

from ...utils.base_model import PaginatedBaseFilters, PaginatedBaseModel


class MLModelsIndex(BaseModel):
    model_id: int
    filename: str
    target_me: str
    active: bool


class PaginatedMLModelsIndexList(PaginatedBaseModel[MLModelsIndex]):
    pass


class MLModelsIndexFilters(PaginatedBaseFilters):
    model_id: Optional[int] = None
    model_id__in: Optional[list[int]] = None
    filename: Optional[str] = None
    filename__regex: Optional[str] = None
    target_me: Optional[str] = None
    target_me__regex: Optional[str] = None
    active: Optional[bool] = None
