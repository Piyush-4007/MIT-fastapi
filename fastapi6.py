# from fastapi import FastAPI

# app = FastAPI()

# @app.post("/create_user")
# def create_user(name: str, age: int, college :str, semester:str):
#     return{
#         "message": "User created",
#         "data": {
#             "name": name,
#             "age": age,
#             "college": college,
#             "semester": semester
#         }
#     }
from fastapi import FastAPI
app = FastAPI
@app.post("/create_user")
def create_user(name: str, age:int)