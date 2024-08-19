from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.berry_controller import router as berry_router

app = FastAPI(
    title="Poke-berries Statistics API",
    description="An API to provide statistics on berries from PokeAPI.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(berry_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)