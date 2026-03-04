from fastapi import FastAPI
from pydantic import BaseModel

from main import ask_helpcenter

app = FastAPI()

class AskReq(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: AskReq):
    html = ask_helpcenter(req.query)
    return {"html": html}
