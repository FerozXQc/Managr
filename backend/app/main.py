from fastapi import FastAPI
import backend.db
from backend.api import empRouter,deptRouter

app = FastAPI()
app.include_router(router=empRouter)
app.include_router(router=deptRouter)
@app.get("/")
def hello():
    return "Hello world"