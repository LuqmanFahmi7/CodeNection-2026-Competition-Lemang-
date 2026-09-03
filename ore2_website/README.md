# Ore2 — Student Workload Website

A Flask/Python implementation inspired by the supplied Ore2 screenshots.

## Features
- Home/landing page matching the sage + cream visual style.
- Workload dashboard with dynamic percentage calculations.
- Workload breakdown page.
- Functional weekly planner.
- Add, complete, and delete tasks.
- Self-Test button with a server-side Flask endpoint.
- Responsive layout for desktop and mobile.
- No database required: tasks are stored in the Flask session for a simple demo.

## Run

1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the site:

```bash
python app.py
```

5. Open `http://127.0.0.1:5000`.

## Production note

The included secret key is for development only. For production, set a secure `SECRET_KEY`
environment variable and replace session storage with SQLite/PostgreSQL.
