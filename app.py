from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from gemini_utils import get_gemini_response
from dotenv import load_dotenv
import os

load_dotenv()  # 👈 This loads variables from .env into the environment


app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

DB_NAME = 'events.db'

# ---------------------
# Initialize Database
# ---------------------
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS rsvps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER,
                name TEXT NOT NULL,
                FOREIGN KEY(event_id) REFERENCES events(id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER,
                content TEXT NOT NULL,
                FOREIGN KEY(event_id) REFERENCES events(id)
            )
        ''')
        conn.commit()

# ---------------------
# Home: List Events
# ---------------------
@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM events")
        events = c.fetchall()
    return render_template('index.html', events=events)

# ---------------------
# RSVP Handling
# ---------------------
@app.route('/rsvp/<int:event_id>', methods=['POST'])
def rsvp(event_id):
    name = request.form.get('name', '').strip()
    if not name:
        return redirect(url_for('index'))

    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()

        # Insert RSVP
        c.execute("INSERT INTO rsvps (event_id, name) VALUES (?, ?)", (event_id, name))
        conn.commit()

        # 🔍 Fetch event title for clarity
        c.execute("SELECT title FROM events WHERE id = ?", (event_id,))
        event = c.fetchone()
        event_title = event[0] if event else "Unknown Event"

        # 📋 Print all RSVPs for this event
        c.execute("SELECT name FROM rsvps WHERE event_id = ?", (event_id,))
        all_rsvps = [row[0] for row in c.fetchall()]

    # 🖨️ Log output clearly
    print("\n🎉 New RSVP Submitted!")
    print(f"Event: {event_title} (ID: {event_id})")
    print(f"Name: {name}")
    print("✅ All RSVPs for this event:")
    for r in all_rsvps:
        print(f" - {r}")
    print("-" * 30)

    return redirect(url_for('index'))


# ---------------------
# Submit Feedback
# ---------------------
@app.route('/feedback/<int:event_id>', methods=['GET', 'POST'])
def feedback(event_id):
    if request.method == 'POST':
        feedback_text = request.form.get('feedback', '').strip()
        if feedback_text:
            with sqlite3.connect(DB_NAME) as conn:
                c = conn.cursor()
                c.execute("INSERT INTO feedback (event_id, content) VALUES (?, ?)", (event_id, feedback_text))
                conn.commit()
                
                # 🧪 Debug: Print all feedbacks for the event
                c.execute("SELECT content FROM feedback WHERE event_id = ?", (event_id,))
                all_feedback = [row[0] for row in c.fetchall()]
                print("\n📝 Feedback submitted for Event ID:", event_id)
                for fb in all_feedback:
                    print(" -", fb)
                print("-" * 30)
                
        return redirect(url_for('summary', event_id=event_id))
    return render_template('feedback.html', event_id=event_id)

# ---------------------
# Feedback Summary (uses Gemini)
# ---------------------
@app.route('/summary/<int:event_id>')
def summary(event_id):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT content FROM feedback WHERE event_id = ?", (event_id,))
        feedbacks = [row[0] for row in c.fetchall()]

    print(f"\n📚 Feedbacks fetched for summary (event_id={event_id}):")
    for fb in feedbacks:
        print(" -", fb)

    if feedbacks:
        prompt = "Summarize the following feedback:\n" + "\n".join(f"- {fb}" for fb in feedbacks)
        summary_text = get_gemini_response(prompt)
    else:
        summary_text = "No feedback available to summarize."

    print("\n📋 Summary generated:\n", summary_text)
    return render_template('summary.html', summary=summary_text, event_id=event_id)

# ---------------------
# Chatbot Interface (Gemini)
# ---------------------
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    answer = None
    if request.method == 'POST':
        user_query = request.form.get('query', '').strip()

        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT title, date, description FROM events")
            events = c.fetchall()

        if events:
            event_info = "\n".join([f"- {title} on {date}: {desc}" for title, date, desc in events])
            prompt = f"User asked: '{user_query}'\nHere are the events:\n{event_info}"
        else:
            prompt = f"User asked: '{user_query}'\nBut there are no events available."

        answer = get_gemini_response(prompt)

    return render_template('chatbot.html', answer=answer)

# ---------------------
# Start App
# ---------------------
if __name__ == '__main__':
    init_db()
    print("Gemini API Key Loaded:", os.getenv('GEMINI_API_KEY') is not None)
    print("Flask Secret Key Loaded:", os.getenv('FLASK_SECRET_KEY') is not None)

    app.run(debug=True)
