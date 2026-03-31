# app.py
import os
from flask import Flask, request, jsonify

# Replace these imports with the ADK classes you have available.
# Example placeholder import; adapt to the ADK package name/version in your environment.
# from google.adk.agents import LlmAgent

app = Flask(__name__)

# --- Configure model/agent ---
# Use environment variables so you can change model or credentials at deploy time.
MODEL_ID = os.environ.get("GEMINI_MODEL", "gemini-1.5-pro")
INSTRUCTION = os.environ.get("AGENT_INSTRUCTION", "You are a concise summarizer. Return a short summary.")

# Initialize the ADK LLM agent once at startup.
# Replace the following stub with the actual ADK agent initialization call in your environment.
# Example (pseudocode):
# agent = LlmAgent(model=MODEL_ID, name="summarizer", instruction=INSTRUCTION)

# For demonstration, here's a simple fallback if ADK is not available:
class DummyAgent:
    def __init__(self, instruction):
        self.instruction = instruction
    def run(self, text):
        # Very small fallback summarizer (not used in production)
        words = text.split()
        summary = " ".join(words[:min(30, len(words))])
        return type("R", (), {"text": summary})

# Try to create a real agent; if ADK import fails, use dummy.
try:
    # Uncomment and adapt to your ADK import
    # agent = LlmAgent(model=MODEL_ID, name="summarizer", instruction=INSTRUCTION)
    raise ImportError("ADK not installed in this runtime")  # remove in real code
except Exception:
    agent = DummyAgent(INSTRUCTION)

@app.route("/summarize", methods=["POST"])
def summarize():
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "")
    if not isinstance(text, str) or text.strip() == "":
        return jsonify({"error": "Provide non-empty 'text' in JSON body."}), 400

    # Call the ADK agent (or dummy) to get a response
    resp = agent.run(text)
    # ADK agent responses often have .text or .content; adapt if needed.
    summary = getattr(resp, "text", str(resp))
    return jsonify({"summary": summary})

@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "ok", "endpoint": "/summarize"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
