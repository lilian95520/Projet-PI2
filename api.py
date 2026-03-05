from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from main import ask_helpcenter

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # autorise Vue
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class AskReq(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: AskReq):
    html = ask_helpcenter(req.query)
    return {"html": html}
