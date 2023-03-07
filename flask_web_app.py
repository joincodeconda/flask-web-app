from flask import Flask, render_template, request, flash, redirect, url_for
from database import get_db, init_db
import os

app = Flask(__name__)

@app.route("/", methods=("POST", "GET"))
def index():
    db = get_db(app)
    list_of_posts = db.execute(
        "SELECT p.id, title, body, created"
        " FROM post p"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template('index.html', posts=list_of_posts)

@app.route("/create", methods=("POST", "GET"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db(app)
            db.execute(
                "INSERT INTO post (title, body) VALUES (?, ?)",
                (title, body),
            )
            db.commit()
            return redirect(url_for("index"))
    else:
        return render_template("create.html")

def get_post(id):
    post = (
        get_db(app).execute(
            "SELECT p.id, title, body, created"
            " FROM post p"
            " WHERE p.id = ?",
            (id,),
        ).fetchone()
    )

    if post is None:
        return redirect(url_for("index"))

    return post

@app.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    our_post = get_post(id)

    if request.method == "POST":
        title = request["title"]
        body = request["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            return redirect(url_for("index"))
        else:
            db = get_db(app)
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("index"))

    return render_template("update.html", post=our_post)

if __name__ == '__main__':
    init_db(app)
    app.run(port=3333)
