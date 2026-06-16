from fastapi import FastAPI
from travel_agent_api.routes import chat_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
"http://127.0.0.1:8000", # Porta standard dell'applicazione foront-end Laravel
"http://localhost:8000"  # Alias per localhost e Porta standard Laravel
]

app.add_middleware(
CORSMiddleware,
allow_origins=origins, # Domini permessi
allow_credentials=True, # Permette l'invio di credenziali
allow_methods=["*"], # Permette tutti i metodi HTTP
allow_headers=["*"], # Permette tutti gli headers
)

app.include_router(
chat_router.router, # Il router definito in chat_router.py
tags=["Chat"], # Tag per la documentazione Swagger
prefix="/chat" # Prefisso per tutte le route del router
)