from fastapi import FastAPI
import backend.db
from backend.api import empRouter

app = FastAPI()
app.include_router(router=empRouter)
@app.get("/")
def hello():
    return "Hello world"