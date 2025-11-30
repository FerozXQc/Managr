from fastapi import FastAPI
import backend.db
from fastapi.middleware.cors import CORSMiddleware
from backend.api import empRouter,deptRouter,attLogRouter,authRouter

app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=empRouter)
app.include_router(router=deptRouter)
app.include_router(router=attLogRouter)
app.include_router(router=authRouter)
@app.get("/")
def hello():
    return "Hello world"