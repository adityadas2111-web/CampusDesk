# CampusDesk

A campus maintenance request tracker built with Python, Flask, SQLite, HTML, CSS and JavaScript.

## Features

- Submit maintenance requests with a location, category, priority and description.
- Track Open, In Progress and Resolved requests.
- Search titles and locations; filter by status.
- View global summary counts and delete unwanted requests.
- Responsive interface, input validation and CSRF form tokens.

## Run locally

Requires Python 3.10 or later.

```bash
python -m venv .venv
```

Activate on Windows:

```bat
.venv\Scripts\activate
```

Activate on macOS/Linux:

```bash
source .venv/bin/activate
```

Install and run:

```bash
python -m pip install -r requirements.txt
python seed.py
python app.py
```

Open http://127.0.0.1:5000. The optional seed command adds three sample requests only when the database is empty. SQLite creates `campusdesk.db` automatically.

## Tests

```bash
python -m unittest -v
```

## Scope

This is a local classroom prototype with a shared workspace. It has no authentication or staff permissions; every visitor can modify requests. Do not deploy the development server for public use. Publishing this source repository does not host the Flask application. Set a persistent `SECRET_KEY` environment variable if sessions must survive restarts.

## Authors

Siddharth Sreeram and Aditya Das.
