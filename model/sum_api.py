from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
from logging import getLogger

app = FastAPI()
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
log = getLogger(__name__)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextRequest(BaseModel):
    text: str


@app.post("/summarize/")
async def summarize_text(request: TextRequest):
    try:
        summary = summarizer(
            request.text, max_length=256, min_length=50, do_sample=False
        )
    except Exception:
        log.error(f"Summarizing text of length {len(request.text)}")
        log.error("Error summarizing text")
        return {"summary": "text too long"}
    return {"summary": summary[0]["summary_text"]}
