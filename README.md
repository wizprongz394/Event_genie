
# 🎉 Event Genie

**Event Genie** is a Flask-based web application that helps users manage and interact with campus events. Users can RSVP, leave feedback, and view AI-generated summaries using Google Gemini. It also features a chatbot that answers questions based on event data.

---

## 🚀 Features

- 📅 **Browse Upcoming Events**
- 📝 **RSVP to Events**
- 💬 **Submit and View Feedback**
- 🤖 **AI-Powered Chatbot (Google Gemini)**
- 🧠 **Summarize Feedback Using Gemini**

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Database:** SQLite
- **Frontend:** HTML/CSS (Google-style theme)
- **AI Integration:** Gemini API (via `gemini_utils.py`)
- **Env Management:** `python-dotenv`

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/wizprongz394/Event_genie.git
cd Event_genie
````

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory and add:

```
FLASK_SECRET_KEY=your_flask_secret
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Run the App

```bash
python app.py
```

Visit: `http://localhost:5000` in your browser

---

## 📁 Project Structure

```
├── app.py                   # Main Flask app
├── gemini_utils.py          # Gemini API integration
├── events.db                # SQLite database
├── templates/               # HTML templates
│   ├── index.html
│   ├── feedback.html
│   ├── summary.html
│   └── chatbot.html
├── static/                  # (Optional CSS or assets)
├── .env                     # Environment config
├── requirements.txt         # Dependencies
└── README.md                # You are here
```

---

## 🤖 AI Features (Gemini)

* Generates **smart summaries** of feedback per event.
* **Chatbot** answers natural language questions using live event data.

---

## 📸 Screenshots

(Add screenshots here if available)

---

## 🧑‍💻 Author

**[@wizprongz394](https://github.com/wizprongz394)**
Built with ❤️ using Flask and Gemini API

---

## 📃 License

MIT License
See [`LICENSE`](LICENSE) for more details.

```


