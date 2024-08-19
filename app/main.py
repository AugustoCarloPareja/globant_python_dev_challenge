# -*- coding: utf-8 -*-
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.controllers.root_controller import router as root_router
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

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(root_router)
app.include_router(berry_router)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)