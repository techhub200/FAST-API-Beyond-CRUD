from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    author: str


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int
