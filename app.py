
import os
from flask import Flask, request, redirect, url_for

app = Flask(__name__)
APP_VERSION = os.getenv("APP_VERSION", "v1")
contacts = []
next_id = 1


@app.route("/")
def home():
    rows = ""
    for c in contacts:
        rows += (
            f"<li>{c['id']} - {c['name']} | {c['phone']} | "
            f"{c['email']} "
            f"<a href='/edit/{c['id']}'>Edit</a> "
            f"<a href='/delete/{c['id']}'>Delete</a></li>"
        )

    search = ""
    if APP_VERSION == "v3":
        search = """
        <form action="/search">
        <input name="q" placeholder="Search by name">
        <button>Search</button>
        </form>
        """

    form = """
    <h3>Add Contact</h3>
    <form method="post" action="/add">
    <input name="name" placeholder="Name" required>
    <input name="phone" placeholder="Phone" required>
    <input name="email" placeholder="Email" required>
    <button type="submit">Add Contact</button>
    </form>
    """

    return f"""
    <h1>Contact Management System - {APP_VERSION.upper()}</h1>
    {form}
    {search}
    <h3>Contacts</h3>
    <ul>{rows}</ul>
    """


@app.route("/add", methods=["POST"])
def add():
    global next_id
    contacts.append({
        "id": next_id,
        "name": request.form["name"],
        "phone": request.form["phone"],
        "email": request.form["email"]
    })
    next_id += 1
    return redirect(url_for("home"))


@app.route("/edit/<int:contact_id>", methods=["GET", "POST"])
def edit(contact_id):
    if APP_VERSION == "v1":
        return "Edit is available in V2 and V3 only", 404

    c = next((x for x in contacts if x["id"] == contact_id), None)
    if not c:
        return "Contact not found", 404

    if request.method == "POST":
        c["name"] = request.form["name"]
        c["phone"] = request.form["phone"]
        c["email"] = request.form["email"]
        return redirect(url_for("home"))

    return f"""
    <h2>Edit Contact</h2>
    <form method="post">
    <input name="name" value="{c['name']}" required>
    <input name="phone" value="{c['phone']}" required>
    <input name="email" value="{c['email']}" required>
    <button>Save Changes</button>
    </form>
    """


@app.route("/delete/<int:contact_id>")
def delete(contact_id):
    if APP_VERSION == "v1":
        return "Delete is available in V2 and V3 only", 404

    contacts[:] = [c for c in contacts if c["id"] != contact_id]
    return redirect(url_for("home"))


@app.route("/search")
def search():
    if APP_VERSION != "v3":
        return "Search is available in V3 only", 404

    q = request.args.get("q", "").lower()
    matches = [c for c in contacts if q in c["name"].lower()]
    return "<h2>Search Results</h2><ul>" + "".join(
        f"<li>{c['name']} - {c['phone']} - {c['email']}</li>"
        for c in matches
    ) + "</ul><a href='/'>Back</a>"


@app.route("/health")
def health():
    return {"status": "healthy", "version": APP_VERSION}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
