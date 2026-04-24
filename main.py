from fastapi import FastAPI

from app.routes.chart import router

app = FastAPI()
app.include_router(router)
