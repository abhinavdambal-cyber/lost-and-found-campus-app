from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import date

app = Flask(__name__)
app.secret_key = "change-this-before-deployment"
DB_PATH = Path(__file__).with_name("campusfind.db")


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('Lost', 'Found')),
                location TEXT NOT NULL,
                date_reported TEXT NOT NULL,
                contact TEXT NOT NULL
            )
        """)


@app.route("/")
def home():
    with get_db() as db:
        items = db.execute(
            "SELECT * FROM items ORDER BY id DESC LIMIT 6"
        ).fetchall()
        total = db.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        lost_count = db.execute(
            "SELECT COUNT(*) FROM items WHERE status = 'Lost'"
        ).fetchone()[0]
        found_count = db.execute(
            "SELECT COUNT(*) FROM items WHERE status = 'Found'"
        ).fetchone()[0]
    return render_template(
        "index.html", items=items, total=total,
        lost_count=lost_count, found_count=found_count
    )


@app.route("/report/<status>", methods=["GET", "POST"])
def report(status):
    status = status.title()
    if status not in ("Lost", "Found"):
        return redirect(url_for("home"))

    if request.method == "POST":
        item_name = request.form.get("item_name", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()
        location = request.form.get("location", "").strip()
        contact = request.form.get("contact", "").strip()
        reported_date = request.form.get("date_reported") or date.today().isoformat()

        if not all([item_name, description, category, location, contact]):
            flash("Please fill in all the fields.")
            return render_template("report.html", status=status)

        with get_db() as db:
            db.execute("""
                INSERT INTO items
                (item_name, description, category, status, location, date_reported, contact)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (item_name, description, category, status,
                  location, reported_date, contact))

        flash(f"Your {status.lower()} item report was submitted!")
        return redirect(url_for("items"))

    return render_template("report.html", status=status)


@app.route("/items")
def items():
    search = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    category = request.args.get("category", "").strip()

    sql = "SELECT * FROM items WHERE 1=1"
    params = []

    if search:
        sql += " AND (item_name LIKE ? OR description LIKE ? OR location LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])

    if status in ("Lost", "Found"):
        sql += " AND status = ?"
        params.append(status)

    if category:
        sql += " AND category = ?"
        params.append(category)

    sql += " ORDER BY id DESC"

    with get_db() as db:
        results = db.execute(sql, params).fetchall()
        categories = db.execute(
            "SELECT DISTINCT category FROM items ORDER BY category"
        ).fetchall()

    return render_template(
        "items.html", items=results, search=search,
        selected_status=status, selected_category=category,
        categories=categories
    )


@app.route("/item/<int:item_id>")
def item_detail(item_id):
    with get_db() as db:
        item = db.execute(
            "SELECT * FROM items WHERE id = ?", (item_id,)
        ).fetchone()

    if item is None:
        flash("That item report could not be found.")
        return redirect(url_for("items"))

    return render_template("detail.html", item=item)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
