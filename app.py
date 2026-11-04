import os
from contextlib import contextmanager
import secrets
import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort

STATUSES = ('Open', 'In Progress', 'Resolved')
CATEGORIES = ('Electrical', 'Plumbing', 'Furniture', 'Network', 'Other')

def create_app(database=None):
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    app.config['DATABASE'] = str(database or Path(__file__).with_name('campusdesk.db'))
    @contextmanager
    def connect():
        db = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()
    with connect() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL,
            location TEXT NOT NULL, category TEXT NOT NULL,
            priority TEXT NOT NULL, description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)''')

    @app.before_request
    def csrf():
        session.setdefault('csrf', secrets.token_hex(32))
        if request.method == 'POST' and not secrets.compare_digest(
                session['csrf'], request.form.get('csrf', '')):
            abort(400, 'Invalid form token. Refresh the page and try again.')

    @app.get('/')
    def index():
        status = request.args.get('status', '')
        q = request.args.get('q', '').strip()[:100]
        if status and status not in STATUSES:
            abort(400, 'Invalid status')
        sql, params = 'SELECT * FROM requests WHERE 1=1', []
        if status:
            sql += ' AND status=?'
            params.append(status)
        if q:
            sql += ' AND (instr(lower(title),lower(?))>0 OR instr(lower(location),lower(?))>0)'
            params.extend([q, q])
        with connect() as db:
            rows = db.execute(sql + ' ORDER BY id DESC', params).fetchall()
            counts = {s: db.execute('SELECT COUNT(*) FROM requests WHERE status=?', (s,)).fetchone()[0] for s in STATUSES}
        return render_template('index.html', rows=rows, counts=counts, statuses=STATUSES,
                               categories=CATEGORIES, selected=status, q=q)

    @app.post('/add')
    def add():
        fields = {k: request.form.get(k, '').strip() for k in ('title', 'location', 'category', 'priority', 'description')}
        if not 1 <= len(fields['title']) <= 100 or not 1 <= len(fields['location']) <= 80 or not 1 <= len(fields['description']) <= 1000:
            abort(400, 'Title, location and description are required and must fit the displayed limits.')
        if fields['category'] not in CATEGORIES or fields['priority'] not in ('Low', 'Medium', 'High'):
            abort(400, 'Invalid category or priority')
        with connect() as db:
            db.execute('INSERT INTO requests(title,location,category,priority,description) VALUES(?,?,?,?,?)', tuple(fields.values()))
        flash('Request submitted successfully.')
        return redirect(url_for('index'))

    @app.post('/update/<int:item_id>')
    def update(item_id):
        status = request.form.get('status')
        if status not in STATUSES:
            abort(400, 'Invalid status')
        with connect() as db:
            if db.execute('UPDATE requests SET status=? WHERE id=?', (status, item_id)).rowcount == 0:
                abort(404)
        flash('Request status updated.')
        return redirect(url_for('index'))

    @app.post('/delete/<int:item_id>')
    def delete(item_id):
        with connect() as db:
            if db.execute('DELETE FROM requests WHERE id=?', (item_id,)).rowcount == 0:
                abort(404)
        flash('Request deleted.')
        return redirect(url_for('index'))

    @app.errorhandler(400)
    @app.errorhandler(404)
    def error(exc):
        return render_template('error.html', error=exc), exc.code
    return app

if __name__ == '__main__':
    create_app().run(host='127.0.0.1', port=5000, debug=False)

