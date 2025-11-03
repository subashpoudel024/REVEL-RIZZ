from fastapi import FastAPI, Request
from my_fast_api.routers import reply_generator
from my_fast_api.routers import pickup_line_generator
from my_fast_api.routers import looks_analyzer
app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {'response':'Hello'}

app.include_router(reply_generator.router, prefix="/api")
app.include_router(pickup_line_generator.router, prefix="/api")
app.include_router(looks_analyzer.router, prefix="/api")