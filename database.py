import sqlite3
import os

from flask import current_app, g

def get_db(app):
    with app.app_context():
        if "db" not in g:
            g.db = sqlite3.connect(os.path.join(app.instance_path, "sqlite_database.sqlite"))
            g.db.row_factory = sqlite3.Row
        return g.db

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db(app):
    db = get_db(app)

    with app.app_context():
        with current_app.open_resource("schema.sql") as f:
            db.executescript(f.read().decode("utf8"))
