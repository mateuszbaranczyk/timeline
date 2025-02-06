from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


class TextRequest(BaseModel):
    text: str


@app.post("/summarize/")
async def summarize_text(request: TextRequest):
    summary = summarizer(request.text, max_length=256, min_length=50, do_sample=False)
    return {"summary": summary[0]["summary_text"]}
