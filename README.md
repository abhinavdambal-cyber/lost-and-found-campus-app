# CampusFind — College Lost & Found Website

A beginner-friendly Flask + SQLite website for students to report lost and found belongings.

## Features
- Report a lost item or a found item
- Browse all reports
- Search by item name, description or location
- Filter by Lost/Found status and category
- View report details and contact the reporter
- Responsive layout for mobile and desktop
- SQLite database is created automatically

## Requirements
- Python 3.9 or newer
- pip

## Run locally

### 1. Open this folder in VS Code or a terminal

### 2. Create and activate a virtual environment

Windows:
```bash
py -m venv .venv
.venv\\Scripts\\activate
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the website
```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Push to GitHub

Create an empty repository on GitHub, then run these commands from this project folder:

```bash
git init
git add .
git commit -m "Initial CampusFind website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the URL with your own GitHub repository URL.

## Important before real deployment
This is a hackathon learning prototype. It does not yet have student login, report moderation, image uploads or private messaging. Contact information is visible on report detail pages. Do not use real personal contact details until you add authentication and privacy controls. Also change `app.secret_key` in `app.py` to a secure environment variable before deployment.
