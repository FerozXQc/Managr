from fastapi import FastAPI
import backend.db
from backend.api import empRouter,deptRouter,attLogRouter,authRouter

app = FastAPI()
app.include_router(router=empRouter)
app.include_router(router=deptRouter)
app.include_router(router=attLogRouter)
app.include_router(router=authRouter)
@app.get("/")
def hello():
    return "Hello world"