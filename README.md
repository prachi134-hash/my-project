# Cummins College Campus Activities Portal

This is the official Cummins College Campus Activities Portal, a web application designed to showcase college events, clubs, sports, cultural activities, and provide a chatbot for student assistance. It is built with Flask (Python) for the backend and standard **HTML, CSS, and JavaScript** for the frontend.



## 📁 Project Structure


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
├─ database.db             # SQLite database for storing data
├─ contact_messages.txt    # Text file storing contact form messages
├─ check_db.py             # Script to check database entries
├─ app.py                  # Main Flask application
├─ app.log                 # Application log
├─ app_errors.log          # Error log
├─ .env                    # Environment variables (hidden)
├─ .env.example            # Example environment file
├─ .gitignore              # Git ignore rules
└─ README.md               # Project documentation




## 🚀 Features

-Homepage & Navigation:Clean homepage with navigation to different sections like sports, cultural, tech, club, fest, and social activities.  
-Chatbot:AI-powered chatbot providing **college-specific information** using TF-IDF, cosine similarity, and Hugging Face Meta AI model.  
-Dashboard:Admin dashboard to manage notifications, events, and club data.  
-Login System:Secure login using Flask sessions and hashed passwords for authorized access.  
-Event Pages:Separate pages for sports, cultural, technical events, clubs, and fests with interactive elements like calendars, popups, and carousels.  
-Contact Form:Stores student messages in `contact_messages.txt` for administrative review.  
-Error Handling & Logging:Runtime errors logged in `app_errors.log` and general application activities in `app.log` for reliability and debugging.  

## 🛠️ Technologies Used

-Backend:Python, Flask (`app.py`)  
-Frontend:HTML, CSS, JavaScript, Bootstrap  
-Database:SQLite (`database.db`)  
-AI & ML:Hugging Face Inference API, Meta AI model, Scikit-learn (TF-IDF, cosine similarity)  
-Web Scraping:BeautifulSoup4  
-Version Control:Git, GitHub  
-Environment Management & Security: `.env` for API keys, `.gitignore` to exclude sensitive files  
-Logging & Error Handling:** `app.log` and `app_errors.log`  



## ⚙️ Setup Instructions

1. Clone the project (if using Git) or download the project folder `my_site`.
2. Navigate to the project folder:
   ```bash
   cd my_site
   ```
3. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up environment variables:  
   Copy `.env.example` to `.env` and update with your own configuration (like API keys).
6. Run the Flask app:
   ```bash
   python app.py
   ```
7. Access the website:  
   Open your browser and go to `http://127.0.0.1:5000/`



## 📂 Notes

- All HTML files are based on a single template (`base.html`) for consistent styling.  
- Logs are maintained in `app.log` and `app_errors.log` for debugging.  
- Chatbot only provides college-related information.  




## 💡 Contact

For queries or contributions, please reach out to the project administrator or open a pull request if using GitHub.
