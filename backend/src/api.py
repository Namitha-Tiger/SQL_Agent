from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .app import SQLAgentApp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = SQLAgentApp()


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
def chat(req: ChatRequest):

    result = agent.run(req.question)

    return result