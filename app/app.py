import os
import psycopg2
from flask import Flask, request, redirect, render_template

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


def run_query(sql, params=None, fetch=False):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                if fetch:
                    return cur.fetchall()
    finally:
        conn.close()


def init_db():
    run_query(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
        """
    )


init_db()


@app.route("/")
def index():
    rows = run_query(
        "SELECT id, text, created_at FROM notes ORDER BY id DESC", fetch=True
    )
    notes = [
        {"id": r[0], "text": r[1], "created": r[2].strftime("%d %b %Y, %H:%M")}
        for r in rows
    ]
    return render_template("index.html", notes=notes)


@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("text", "").strip()[:500]
    if text:
        run_query("INSERT INTO notes (text) VALUES (%s)", (text,))
    return redirect("/")


@app.route("/delete/<int:note_id>", methods=["POST"])
def delete(note_id):
    run_query("DELETE FROM notes WHERE id = %s", (note_id,))
    return redirect("/")


@app.route("/health")
def health():
    try:
        run_query("SELECT 1")
        return "ok", 200
    except Exception:
        return "database not reachable", 500