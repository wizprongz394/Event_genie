import requests
from flask import session
from dotenv import load_dotenv
import os

load_dotenv() 

# Replace this with a secure method in production (e.g., environment variable)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# ✅ Correct model endpoint
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

HEADERS = {
    "Content-Type": "application/json",
    "X-goog-api-key": GEMINI_API_KEY
}


def get_gemini_response(query, events=None):
    """
    Generates a response using Gemini based on user query and event data.
    Maintains chat history in session.
    """
    # Format events if any
    event_section = ""
    if events:
        event_section = "\n\nUpcoming Events:\n" + "\n".join(
            [f"- {title} on {date}: {description}" for title, date, description in events]
        )

    # Chat history for context
    chat_history = session.get('chat_history', [])
    history_text = "\n".join([f"User: {msg['text']}" for msg in chat_history])

    prompt = (
        "You are Event Genie, a helpful assistant for campus events.\n"
        "Provide concise and friendly answers to user queries.\n"
        f"{event_section}\n"
        f"{history_text}\n"
        f"User: {query}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        text = response.json()['candidates'][0]['content']['parts'][0]['text']

        # Update session history
        chat_history.append({"role": "user", "text": query})
        session['chat_history'] = chat_history

        return text

    except requests.RequestException as e:
        return f"⚠️ Error from Gemini API: {e}"


def summarize_feedback(event_id, feedback_list):
    """
    Uses Gemini to summarize feedback for an event.
    """
    feedback_text = "\n".join(feedback_list)

    prompt = (
        f"Summarize the following feedback for Event ID {event_id}.\n"
        "Identify common themes, suggestions, and general sentiment.\n\n"
        f"{feedback_text}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']

    except requests.RequestException as e:
        return f"⚠️ Could not summarize feedback: {e}"
