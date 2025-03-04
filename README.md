
---

# Text Processing Backend

This project provides a **RESTful API** for text processing, powered by **FastAPI** and **OpenAI GPT**. You can send any text to the `/process` endpoint to get:
1. A concise **summary**  
2. Extracted **keywords**  
3. **Sentiment** classification

All operations are handled by **GPT-3.5-turbo** (or a later variant) to ensure quality results.

## Key Endpoints

- **POST /process**  
  Accepts JSON with a `text` field. Returns a summary, keywords, and sentiment.

- **GET /history**  
  Lists all the text inputs processed so far, along with their generated summaries, keywords, and sentiments.

## Features

- **Real-time AI processing** using GPT-3.5 (ChatCompletion API)  
- **.env** file support via `python-dotenv`, ensuring no API keys are leaked  
- **FastAPI** framework for high-performance, easy-to-use REST endpoints  
- **In-memory storage** for history, so you can retrieve past requests (replace with a database as needed)

## Requirements

- **Python 3.7+**  
- [FastAPI](https://fastapi.tiangolo.com/) and [Uvicorn](https://www.uvicorn.org/)  
- [python-dotenv](https://pypi.org/project/python-dotenv/)  
- [OpenAI Python Library](https://pypi.org/project/openai/)

## Installation and Setup

1. **Clone the Repository**

   ```bash
   git clone (URL)
   cd text-processing-backend
   ```

2. **Create a Virtual Environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Linux/Mac
   # or
   venv\Scripts\activate       # On Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```
   Make sure `requirements.txt` includes:
   ```
   fastapi
   uvicorn
   python-dotenv
   openai
   ```

4. **Configure Environment Variables**

   Create a file named `.env` in the root of your project (same folder as `main.py`), and add:
   ```
   OPENAI_API_KEY=your-real-openai-api-key
   ```
   > **Warning**: Don’t commit `.env` to a public repo!

5. **Run the Server**

   ```bash
   uvicorn main:app --reload
   ```
   The app should now be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Usage

### 1. Test the Root Endpoint

```bash
curl http://127.0.0.1:8000/
```

You should receive a small JSON welcome message.

### 2. Process a Text

Send a `POST` request to `/process` with a JSON body, for example:

```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"text":"FastAPI is a modern Python framework..."}' \
     http://127.0.0.1:8000/process
```

Expect a response with fields like:
```json
{
  "original_text": "FastAPI is a modern Python framework...",
  "summary": "A concise summary here...",
  "keywords": ["fastapi","modern","python","framework"],
  "sentiment": "positive"
}
```

### 3. View Processing History

```bash
curl http://127.0.0.1:8000/history
```

This returns an array of all previous requests and the corresponding results:
```json
[
  {
    "original_text": "FastAPI is a modern Python framework...",
    "summary": "A concise summary here...",
    "keywords": ["fastapi","modern","python","framework"],
    "sentiment": "positive"
  },
  ...
]
```

## Customization

1. **Expand Business Logic**  
   - Add rules to handle short texts, special keywords, or any domain-specific logic.
   - For instance, you can skip summarization if the text is under 10 words.

2. **Use a Database**  
   - The code currently saves results to an in-memory list (`history_storage`). For production, integrate a real database (e.g., PostgreSQL, MongoDB).

3. **Fine-tune GPT Parameters**  
   - Adjust `temperature`, `max_tokens`, or your prompt style to control the creativity and length of responses.

4. **Replace the Model**  
   - You can switch from `gpt-3.5-turbo` to `gpt-4` if you have access, or even a local Hugging Face model with slight modifications.

## Contributing

Feel free to open issues or submit pull requests to improve the API, add more NLP features, or enhance the user experience.

## License

This project is licensed under the **MIT License**. You’re free to use, modify, and distribute it in any way you see fit.

---
