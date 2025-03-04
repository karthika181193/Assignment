import os
from typing import List, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import openai

# ------------------------------------------------------------------------------
# Environment & Configuration
# ------------------------------------------------------------------------------
# We load our environment variables (like OPENAI_API_KEY) from a .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY is not set in your .env file.")

# ------------------------------------------------------------------------------
# FastAPI Initialization
# ------------------------------------------------------------------------------
app = FastAPI(title="Text Processing Backend (GPT-3.5-Turbo)")

# We'll store historical requests/responses in memory for demonstration purposes.
history_storage = []

# ------------------------------------------------------------------------------
# Data Models
# ------------------------------------------------------------------------------
class TextRequest(BaseModel):
    """
    This model defines the shape of data we expect in POST requests to /process.
    """
    text: str

class ProcessedText(BaseModel):
    """
    This model defines how our API will respond, including:
      - The original text
      - A summary
      - Extracted keywords
      - Sentiment classification
    """
    original_text: str
    summary: str
    keywords: List[str]
    sentiment: str

# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------
def generate_summary(text: str) -> str:
    """
    Summarize the input text in 2-3 sentences using GPT-3.5-Turbo.
    We'll feed it a 'system' role prompt and a 'user' role prompt
    to guide the conversation model.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Summarize the following text in 2-3 sentences:\n\n{text}"
        }
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,  # a moderate creativity level
    )
    
    # Extract the model’s response text and strip any leading/trailing whitespace
    summary = response["choices"][0]["message"]["content"].strip()
    return summary


def extract_keywords(text: str) -> List[str]:
    """
    Ask GPT-3.5-Turbo to extract keywords from the given text,
    returning them as a list. We prompt it to respond with
    a comma-separated list, then parse those out in Python.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": (
                "Extract the main keywords from the following text. "
                "Return them as a comma-separated list:\n\n" + text
            )
        }
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5  # slightly lower temperature for consistent keyword extraction
    )
    
    raw_keywords = response["choices"][0]["message"]["content"].strip()
    
    # Split by commas and strip extra whitespace
    keywords_list = [kw.strip() for kw in raw_keywords.split(",") if kw.strip()]
    return keywords_list


def analyze_sentiment(text: str) -> str:
    """
    Ask GPT-3.5-Turbo to classify the sentiment (Positive, Negative, or Neutral).
    We then normalize the text so it's capitalized consistently.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": (
                "Classify the sentiment of the following text as Positive, Negative, or Neutral.\n\n"
                f"{text}"
            )
        }
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.0  # deterministic responses for classification
    )
    
    sentiment_raw = response["choices"][0]["message"]["content"].strip()
    sentiment = sentiment_raw.capitalize()  # e.g. "Positive", "Negative", or "Neutral"
    return sentiment

# ------------------------------------------------------------------------------
# API Endpoints
# ------------------------------------------------------------------------------
@app.get("/")
def root():
    """
    A simple root endpoint to verify that the API is online.
    Returns a welcome message.
    """
    return {"message": "Welcome to the Text Processing API using GPT-3.5-Turbo"}

@app.post("/process", response_model=ProcessedText)
def process_text(request: TextRequest):
    """
    POST /process
      - Accepts JSON with a 'text' field.
      - Summarizes the text, extracts keywords, and determines sentiment.
      - Returns the processed result and stores it in an in-memory history.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    # Perform the three text-processing tasks
    summary = generate_summary(request.text)
    keywords = extract_keywords(request.text)
    sentiment = analyze_sentiment(request.text)

    # Construct our response according to the ProcessedText model
    processed_data = ProcessedText(
        original_text=request.text,
        summary=summary,
        keywords=keywords,
        sentiment=sentiment
    )

    # Append to history (for demonstration—use a database in a real-world app)
    history_storage.append(processed_data.dict())

    return processed_data

@app.get("/history")
def get_history() -> List[Dict]:
    """
    GET /history
      - Returns all previously processed texts and their results.
      - This is a simple in-memory store for demonstration.
    """
    return history_storage
