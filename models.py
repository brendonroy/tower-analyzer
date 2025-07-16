from sqlmodel import SQLModel, Field
from typing import Optional

class Photo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    gps: str
    azimuth: str
    content_type: str