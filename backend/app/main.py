from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(
    title="Finance News + Analytics",
    version="0.1",
    description="Production-style news and finance analytics API."
)

for router in endpoints.all_routers:
    app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok"}