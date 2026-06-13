from fastapi import FastAPI

app = FastAPI()

@app.get("/users/")
def get_users(name: str = None, ):
    return {"name": name}