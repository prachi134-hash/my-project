# Cummins College Website & Interactive Chatbot

A complete web portal for Cummins College of Engineering for Women, including:

- Interactive, AI-powered chatbot providing college-specific information.
- Dashboard displaying notifications, events, achievements, and statistics.
- Contact form integrated with database storage.
- Multiple pages: Sports, Cultural, Tech, Clubs, Fests, Social Initiatives.
- Admin login for managing dashboard.

## Features
- [x] Responsive multi-page website (index, sports, cultural, tech, clubs, fests, social)
- [x] Interactive chatbot with session-based chat history stored in SQLite
- [x] Dashboard with notifications, upcoming events, top students, achievements, and stats
- [x] Contact form with input validation and database integration
- [x] Admin login with session management
- [x] Base template with reusable header & footer
- [ ] Real-time notifications (planned)
- [ ] Multi-language support (planned)

## Tech Stack
- Python 3.x
- Flask (backend)
- HTML / CSS / JavaScript (frontend)
- SQLite (database)
- Hugging Face API (AI chatbot)
- BeautifulSoup (web scraping for content)

## Project Structure
my_site/
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  ├─ chatbot.html
│  ├─ dashboard.html
│  ├─ login.html
│  ├─ sports.html
│  ├─ cultural.html
│  ├─ tech.html
│  ├─ club.html
│  ├─ fest.html
│  └─ social.html
├─ database.db
├─ contact_messages.txt
├─ check_db.py
├─ app.py
├─ app.log
├─ app_errors.log
├─ .env
├─ .env.example
├─ .gitignore
└─ README.md

