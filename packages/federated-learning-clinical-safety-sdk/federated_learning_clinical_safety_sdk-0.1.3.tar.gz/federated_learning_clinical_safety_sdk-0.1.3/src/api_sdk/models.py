from typing import Optional
from pydantic import BaseModel, Field

class FlModel(BaseModel):
    id: Optional[int] = None
    name: str
    accuracy: Optional[float] = None
    generalisability: Optional[float] = None
    privacy: Optional[float] = None
    leakage_chance: Optional[float] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class LocalModel(BaseModel):
    id: Optional[int] = None
    fl_model: int  # just the FK id
    name: str
    privacy: Optional[float] = None
    leakage_chance: Optional[float] = None
    noise: Optional[float] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
