from fastapi import FastAPI

from ain.model.inference import model
from api.routes.analyze import router as analyze_router


app = FastAPI(
    title="AIN API",
    description="AI-powered child safety risk detection API",
    version="2.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model": "loaded" if model is not None else "not_loaded",
    }


app.include_router(analyze_router)
