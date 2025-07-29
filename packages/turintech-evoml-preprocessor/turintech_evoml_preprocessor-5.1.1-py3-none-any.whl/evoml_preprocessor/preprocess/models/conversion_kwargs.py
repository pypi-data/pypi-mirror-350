from pydantic import BaseModel
from typing import Optional


class ToDatetimeKwargs(BaseModel):
    dayfirst: bool = False
    yearfirst: bool = False
    format: Optional[str] = None


class ToIntegerKwargs(BaseModel): ...
