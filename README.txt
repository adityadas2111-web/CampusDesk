CAMPUSDESK - Semester V Web Technology Project
Siddharth Sreeram (240911626), Aditya Das (240911632)

Requires Python 3.10 or later and an internet connection for initial installation.
Open a terminal in this folder:
  python -m venv .venv
  .venv\Scripts\activate
  python -m pip install -r requirements.txt
  python app.py
Then visit http://127.0.0.1:5000 in a browser.
On macOS/Linux activate with: source .venv/bin/activate

Run automated checks: python -m unittest -v
Optional sample records: python seed.py (only inserts when database is empty).
The database is created automatically next to app.py. Stop the server and
copy campusdesk.db to back it up. No sample database is included.

Features: submit requests, search title/location, filter status, update status,
delete requests, global summary counts, responsive layout, CSRF protection.
JavaScript adds a character counter and delete confirmation; core forms work
without it. Deletion is immediate without JavaScript.

This is a local, shared classroom demonstration, not a deployed college system.
All visitors can modify every request. Authentication, staff roles, audit trails,
attachments and notifications are future work. Do not expose it publicly or
enter personal information. The development server binds only to localhost.
Set a persistent SECRET_KEY environment variable if sessions must survive restarts.

Suggested allocation (confirm actual contributions before submission):
Siddharth: dashboard and request submission.
Aditya: request board/status management and search/filter/summary module.
The report preserves the supplied institutional/course labels; verify them and
fill in the faculty name before submission. Signatures are intentionally blank.
