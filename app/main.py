import os
from fastapi import FastAPI
from pydantic import BaseModel
from .producer import send_message

app = FastAPI(
    title="Sistema de Mensageria",
    description="utilizando RabbitMQ",
    version="1.0.0",
)

class Message(BaseModel):
    nome: str
    texto: str

@app.get("/")
def health():
    return {"status": "ok", "message": "API ativa", "docs": "/docs"}

@app.post("/enviar")
def enviar_mensagem(msg: Message):
    queue = os.getenv("QUEUE_NAME", "mensagens")
    send_message(msg.dict(), queue_name=queue)
    return {"status": "enviado", "fila": queue, "conteudo": msg.dict()}
