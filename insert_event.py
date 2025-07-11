import sqlite3

DB_NAME = 'events.db'

with sqlite3.connect(DB_NAME) as conn:
    c = conn.cursor()

    # Create events table
    c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    """)

    # Create rsvps table
    c.execute("""
        CREATE TABLE IF NOT EXISTS rsvps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            name TEXT NOT NULL,
            FOREIGN KEY(event_id) REFERENCES events(id)
        )
    """)

    # Create feedback table
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            content TEXT NOT NULL,
            FOREIGN KEY(event_id) REFERENCES events(id)
        )
    """)

    # 🔁 Clear existing data (optional for testing)
    c.execute("DELETE FROM events")
    c.execute("DELETE FROM rsvps")
    c.execute("DELETE FROM feedback")

    # 🔽 Insert sample events
    events = [
        ("Tech Talk: AI in 2025", "2025-08-01", "Explore the future of AI with top speakers."),
        ("Hackathon Weekend", "2025-08-10", "Join us for 48 hours of coding and fun."),
        ("Women in Tech Panel", "2025-08-15", "Inspiring conversations with women leaders in tech.")
    ]
    c.executemany("INSERT INTO events (title, date, description) VALUES (?, ?, ?)", events)

    conn.commit()

print("✅ Tables created and sample events inserted into 'events.db'.")
