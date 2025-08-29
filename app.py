from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from bs4 import BeautifulSoup
import os, requests, re, time, html, logging
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from functools import wraps
import sqlite3

DB_PATH = "database.db"

# ===== Database helper functions =====
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ===== Load environment variables =====
load_dotenv()
import os
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "meta-llama/Llama-3.1-8B-Instruct")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Validate required env variables
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not set in environment variables")
if not (ADMIN_USERNAME and ADMIN_PASSWORD):
    raise ValueError("Admin credentials not set in environment variables")

# ===== Logging =====
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("CumminsApp")

# ===== Initialize Flask =====
app = Flask(__name__)
app.secret_key = os.urandom(24)

# ===== Hugging Face Client =====
client = InferenceClient(provider="fireworks-ai", api_key=HF_TOKEN)

# ===== Scrape & combine content =====
full_content_chunks = []

TEMPLATE_FOLDER = os.path.join(os.path.dirname(__file__), "templates")
HTML_FILES = [f for f in os.listdir(TEMPLATE_FOLDER) if f.endswith(".html")]

for file_name in HTML_FILES:
    path = os.path.join(TEMPLATE_FOLDER, file_name)
    try:
        with open(path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            texts = [t.get_text(separator=" ", strip=True) for t in soup.find_all(
                ["p","h1","h2","h3","h4","h5","h6","li"]
            )]
            words = " ".join(texts).split()
            for i in range(0, len(words), 250):
                full_content_chunks.append(" ".join(words[i:i+250]))
    except Exception as e:
        logger.error(f"Failed to read {file_name}: {e}")

try:
    url = "https://cumminscollege.edu.in/"
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        main_content = soup.find_all(["p","h1","h2","h3","h4","h5","h6","li"])
        words = " ".join([t.get_text(separator=" ", strip=True) for t in main_content]).split()
        for i in range(0, len(words), 250):
            full_content_chunks.append(" ".join(words[i:i+250]))
except Exception as e:
    logger.error(f"Failed to scrape college website: {e}")

# ===== Helper: get relevant chunks =====
def get_best_chunks(user_msg, chunks, top_n=3):
    if not chunks:
        return ""
    corpus = chunks + [user_msg]
    tfidf = TfidfVectorizer().fit_transform(corpus)
    cosine_sim = cosine_similarity(tfidf[-1], tfidf[:-1])[0]
    top_indices = cosine_sim.argsort()[-top_n:][::-1]
    return " ".join([chunks[i] for i in top_indices])

# ===== Dashboard mock data =====
notifications = [
    {"type":"Announcement","title":"Happy Ganesh Chaturthi! 🙏✨","message":"May Lord Ganesha bless us with wisdom, strength, and joy. 🌺✨ Ganpati Bappa Morya! 🎉","date":"2025-09-01"},
    {"type":"Event","title":"NSS – E-Waste Collection Drive ♻🌿","message":"Old mobiles, chargers, batteries, wires? Bring them today! 📍 Wing A, near Admin. ⏳ Ongoing","date":"2025-09-02"},
    {"type":"Competition","title":"🚀 WebWay Full Stack Competition","message":"Participate now! Don’t miss out!","date":"2025-09-05"}
]

upcoming_events = [
    {"name":"Robotics Workshop","date":"2025-09-10","time":"10:00 AM - 4:00 PM","venue":"Lab 101"},
    {"name":"Annual Tech Fest","date":"2025-09-20","time":"9:00 AM - 6:00 PM","venue":"Main Auditorium"},
    {"name":"Cultural Night","date":"2025-09-25","time":"6:00 PM - 10:00 PM","venue":"Open Ground"}
]

top_students = [
    {"name":"Alice Sharma","event":"Robotics Winner","photo":"https://randomuser.me/api/portraits/women/65.jpg"},
    {"name":"Priya Singh","event":"Chess Champion","photo":"https://randomuser.me/api/portraits/men/75.jpg"},
    {"name":"Neha Patil","event":"Dance Competition","photo":"https://randomuser.me/api/portraits/women/45.jpg"}
]

achievements = [
    {"title":"Robotics Club","desc":"Won 1st place in inter-college robotics competition"},
    {"title":"Debate Team","desc":"Secured 2nd position at National Debate Championship"},
    {"title":"Eco Club","desc":"Organized successful tree plantation drive across campus"}
]

stats = {"Active Activities":60, "Student Members":2100, "Annual Fests":22}

# ===== Login Required Decorator =====
def require_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

# ===== Routes =====
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html", error=None)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@require_login
def dashboard():
    return render_template(
        "dashboard.html",
        notifications=notifications,
        events=upcoming_events,
        top_students=top_students,
        achievements=achievements,
        stats=stats
    )

pages = ["sports","cultural","tech","club","fest","social","coderclub","gdsc","robotics"]
for page in pages:
    app.add_url_rule(f'/{page}', page, (lambda p: lambda: render_template(f"{p}.html"))(page))

# ===== Chatbot and Contact Endpoints (DB integration) =====
CHAT_LIMIT = 5
CHAT_WINDOW = 60
chat_requests = {}

@app.route("/chat", methods=["POST"])
def chat():
    try:
        session_id = request.headers.get("Session-Id") or session.get("session_id")
        if not session_id:
            session_id = f"{request.remote_addr}_{int(time.time())}"
            session["session_id"] = session_id

        user_ip = request.remote_addr
        now = time.time()
        chat_requests.setdefault(user_ip, [])
        chat_requests[user_ip] = [t for t in chat_requests[user_ip] if now - t < CHAT_WINDOW]

        if len(chat_requests[user_ip]) >= CHAT_LIMIT:
            return jsonify({"reply": "Slow down! You are sending messages too quickly. ⏳"}), 429

        chat_requests[user_ip].append(now)

        data = request.get_json()
        user_msg = data.get("message", "").strip()

        if not user_msg:
            reply = "Hello! I’m your Cummins College assistant 🤖. Ask me about clubs, sports, cultural activities, fests, and more!"
        else:
            greetings = ["hi","hello","hey","good morning","good afternoon","good evening"]
            if user_msg.lower() in greetings:
                reply = "Hello! I’m your Cummins College assistant 🤖. How can I help you today?"
            else:
                top_chunks = get_best_chunks(user_msg, full_content_chunks, top_n=3)
                system_prompt = f"""
You are a helpful and friendly assistant for Cummins College of Engineering for Women.
Answer concisely in 1-2 sentences using ONLY the content below.
Do NOT explain your thought process. Do NOT make up answers.
Content:
{top_chunks}
"""
                completion = client.chat.completions.create(
                    model=HF_MODEL,
                    messages=[{"role": "system", "content": system_prompt},{"role": "user", "content": user_msg}],
                )
                reply_text = completion.choices[0].message["content"]
                reply = ' '.join(re.split(r'(?<=[.!?]) +', reply_text)[:2]).strip()
                if not reply:
                    reply = "Sorry, I don't have information about that in the college content."

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chat_history (session_id, role, message) VALUES (?, ?, ?)", (session_id, "user", user_msg))
        cursor.execute("INSERT INTO chat_history (session_id, role, message) VALUES (?, ?, ?)", (session_id, "bot", reply))
        conn.commit()
        conn.close()

    except Exception as e:
        logger.exception("Chatbot error: %s", e)
        reply = "Sorry, something went wrong while fetching the response."

    return jsonify({"reply": reply})

@app.route("/chat_history", methods=["GET"])
def chat_history():
    session_id = request.headers.get("Session-Id") or session.get("session_id")
    if not session_id:
        return jsonify({"history": []})

    conn = get_db_connection()
    rows = conn.execute(
        "SELECT role, message FROM chat_history WHERE session_id=? ORDER BY created_at ASC",
        (session_id,)
    ).fetchall()
    conn.close()
    history = [{"role": row["role"], "text": row["message"]} for row in rows]
    return jsonify({"history": history})

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    try:
        session_id = request.headers.get("Session-Id") or session.get("session_id")
        if session_id:
            conn = get_db_connection()
            conn.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))
            conn.commit()
            conn.close()
            logger.info(f"Cleared chat history for session: {session_id}")
        return jsonify({"success": True})
    except Exception as e:
        logger.exception("Error clearing chat: %s", e)
        return jsonify({"success": False, "message": "Failed to clear chat."})

@app.route("/contact", methods=["POST"])
def contact():
    try:
        data = request.get_json()
        first_name = html.escape(data.get("first_name","").strip())
        last_name = html.escape(data.get("last_name","").strip())
        email = html.escape(data.get("email","").strip())
        message = html.escape(data.get("message","").strip())

        if not (first_name and last_name and email and message):
            return jsonify({"success": False, "message": "Please fill all fields!"})
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"success": False, "message": "Please enter a valid email address."})

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (first_name, last_name, email, message) VALUES (?, ?, ?, ?)",
                       (first_name, last_name, email, message))
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Thank you! Your message has been submitted."})
    except Exception as e:
        logger.exception("Contact form error: %s", e)
        return jsonify({"success": False, "message": "Error saving message. Try again later."})

@app.errorhandler(Exception)
def handle_exception(e):
    logger.exception("Unhandled exception: %s", e)
    return jsonify({"error": "An unexpected error occurred."}), 500

if __name__ == "__main__":
    app.run(debug=True)
