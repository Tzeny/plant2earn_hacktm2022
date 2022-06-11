from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel



class LoginModel(BaseModel):
    username: str
    password: str

app = FastAPI()

@app.post('/login/')
def login(login_model: LoginModel):
    

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
