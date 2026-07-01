from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
app = FastAPI()

@app.get("/")
async def read_root():
 return {"Hello":"World"}


@app.get("/greet")
async def show_videos(name: str):
    return {"hello": name}

#using both query and path parameter

@app.get("/greet_user/{name}")
async def greet(name:str , age:int):
   return{"hello": name , "age":age}

#using default values without path parameter

@app.get("/greet_default")
async def greet(name:Optional[str]="user",age :int=0):
   return {"Hello":name , "age": age}

# using pydantic models to understand the requst body

class Users(BaseModel):
   name:str
   age:int
   salary:float

@app.post("/Create_user")
async def Create(user:Users):
   return{
      "Username":user.name,
      "Age":user.age,
      "Income":user.salary

   }