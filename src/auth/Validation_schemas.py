from pydantic import BaseModel,Field

class UserCreateModel(BaseModel):
    username:str=Field(max_length=15)
    email:str=Field(max_length=15)
    Password:str=Field(min_length=8,max_length=15)
