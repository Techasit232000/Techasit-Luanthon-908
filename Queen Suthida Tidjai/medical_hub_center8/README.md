# Medical Hub Center 8 - Queen Suthida Tidjai

Simple Flask web application for a Medical Hub Center (Center 8) intended as a starter template to upload to GitHub.

## Features
- Patient registry (add, edit, list)
- Appointment scheduling (add, list)
- SQLite database (Flask-SQLAlchemy)
- Simple, responsive UI using Bootstrap CDN

## Quick start (local)
1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create database:
   ```bash
   python create_db.py
   ```
4. Run app:
   ```bash
   flask run --host=0.0.0.0 --port=5000
   ```
   Or:
   ```bash
   python app.py
   ```

## Notes
- This project is provided as a starting point. For production use, add authentication, HTTPS, input validation, role-based access control, and audit logging.
- Replace placeholder names and texts to match official branding and legal requirements before publishing.

