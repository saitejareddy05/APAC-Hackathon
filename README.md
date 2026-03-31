# ADK Gemini Summarizer Agent

Simple Flask app that exposes /summarize and uses ADK + Gemini to produce short summaries.

## Run locally
1. pip install -r requirements.txt
2. export GEMINI_MODEL=gemini-1.5-pro
3. python app.py
4. POST to http://localhost:8080/summarize with JSON {"text":"..."}

## Deploy to Cloud Run
See the Cloud Run deployment steps in the project README.
