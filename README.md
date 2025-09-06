# Cummins College Campus Activities Portal

**Cummins College Campus Activities Portal** is a web application to showcase college events, clubs, sports, cultural activities, and provide a student-assistance chatbot. It is built with **Flask (Python)** on the backend and **HTML, CSS, and JavaScript** on the frontend.

---

## 📁 Project Structure

```
my_site/
├─ templates/
│  ├─ base.html            # Base template for consistent header/footer
│  ├─ index.html           # Homepage
│  ├─ chatbot.html         # College chatbot page
│  ├─ dashboard.html       # Admin/student dashboard
│  ├─ login.html           # Login page
│  ├─ sports.html          # Sports activities page
│  ├─ cultural.html        # Cultural events page
│  ├─ tech.html            # Technical events page
│  ├─ club.html            # College clubs page
│  ├─ fest.html            # College fest page
│  └─ social.html          # Social initiatives page
├─ database.db             # SQLite database
├─ contact_messages.txt    # Contact form messages
├─ check_db.py             # Script to check database entries
├─ app.py                  # Main Flask application
├─ app.log                 # Application log
├─ app_errors.log          # Error log
├─ .env                    # Environment variables (hidden)
├─ .env.example            # Example environment file
├─ .gitignore              # Git ignore rules
└─ README.md               # Project documentation

```

---

## 🚀 Features

- **Homepage & Navigation:** Clean homepage with links to all sections: sports, cultural, tech, clubs, fests, and social initiatives.  
- **Chatbot:** AI-powered chatbot providing quick answers about college activities.  
- **Dashboard:** Admin or student dashboard to monitor notifications, events, and achievements.  
- **Event Pages:** Dedicated pages for different activities.  
- **Login System:** Secure login for dashboard access.  
- **Contact Form:** Stores messages in the database and `contact_messages.txt`.  

---

## 🛠️ Technologies Used

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** SQLite (`database.db`)  
- **AI Integration:** Hugging Face model for chatbot responses  

---

## ⚙️ Setup Instructions

1. **Clone the repository** (or download the project folder `my_site`):  
   ```bash
   git clone https://github.com/prachi134-hash/my-project.git
   cd my-project/my_site
    ```
2. **Create and activate a virtual environment**:

 ```bash
Copy code
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```
3.**Install dependencies:**

 ```bash
Copy code
pip install -r requirements.txt
 ```
4.**Set up environment variables:**
Copy .env.example to .env and update with your configuration:
 ```
ini
Copy code
HF_TOKEN=<your_huggingface_token>
HF_MODEL=<model_name>
ADMIN_USERNAME=<admin_user>
ADMIN_PASSWORD=<admin_pass>
 ```
⚠️ Important: Never commit .env to GitHub. Keep all secrets in .env.

5.**Run the Flask app:**

 ```bash
Copy code
python app.py
 ```
6.**Open your browser:**
Go to http://127.0.0.1:5000/ to access the portal.


---

# 💡 Security Notes
--Remove any API tokens or secrets from your Git history before pushing to GitHub.

--Use .gitignore to exclude .env or sensitive files.

--Enable GitHub Secret Scanning to automatically detect secret commits.

---

# 📂 Notes
--All HTML pages extend base.html for consistent design.

--Logs (app.log and app_errors.log) help track errors and activity.

--Chatbot responses are limited to college-related content.












For queries or contributions, please reach out to the project administrator or open a pull request if using GitHub.
