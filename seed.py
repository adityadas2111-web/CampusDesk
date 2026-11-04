from app import create_app
import sqlite3
app = create_app()
with sqlite3.connect(app.config['DATABASE']) as db:
    if db.execute('SELECT COUNT(*) FROM requests').fetchone()[0] == 0:
        db.executemany('INSERT INTO requests(title,location,category,priority,description,status) VALUES(?,?,?,?,?,?)', [
            ('Projector display flickers', 'Academic Block - Room 204', 'Electrical', 'High', 'Display flickers during presentations. Please inspect the connection.', 'Open'),
            ('Water tap leaking', 'Library - Ground floor', 'Plumbing', 'Medium', 'Tap continues dripping after it is closed.', 'In Progress'),
            ('Loose chair repaired', 'Computer Lab 2', 'Furniture', 'Low', 'The chair near workstation 12 was unstable.', 'Resolved')])
        print('Three sample requests added.')
    else:
        print('Database already contains requests; no changes made.')
