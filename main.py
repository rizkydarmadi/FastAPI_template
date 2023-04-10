from fastapi import FastAPI
from routes.user import router as user_router
from routes.triangle import router as triangle_router
from routes.logs import router as logs_router

app = FastAPI(title="Study Case Recruitment Associate Python Backend Engineer")

app.include_router(user_router)
app.include_router(triangle_router)
app.include_router(logs_router)
