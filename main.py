from fastapi import FastAPI, Response  # type: ignore
from app.routers import router as api_router
from app.core.config import settings

app = FastAPI(title="URL Shortener")

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "URL Shortener Service is running."}

@app.get("/favicon.ico", include_in_schema=False)  # handle browser favicon requests
async def favicon():
    return Response(status_code=204)

if __name__ == "__main__":
    import uvicorn  # type: ignore
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
