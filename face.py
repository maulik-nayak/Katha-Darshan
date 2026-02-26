from fastapi import FastAPI
from pydantic import BaseModel
from mana import Mana, warmup_system
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from aatma import get_last_memories
from buddhi import short_term_memory

app = FastAPI()
assistant = Mana()

@app.get("/memory")
def memory():
    return {
        "short_term": short_term_memory,
        "long_term": get_last_memories(3)
    }

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("static/index.html")

warmup_system()


class Message(BaseModel):
    text: str


@app.post("/chat")
def chat(message: Message):
    reply = assistant.process(message.text)

    # If the reply is an action tuple (like stopping), just grab the text
    if isinstance(reply, tuple):
        reply = reply[0]

    return {"response": reply}