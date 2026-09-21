from fastapi import FastAPI

from api.routes.analyze import router as analyze_router
from api.routes.parents import router as parents_router
from api.routes.dashboard import router as dashboard_router
from ain.database.database import init_db


app = FastAPI(
    title="AIN API",
    description="AI-powered child safety risk detection API",
    version="2.0.0",
)


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model": "available",
    }


app.include_router(analyze_router)
app.include_router(parents_router)
app.include_router(dashboard_router)