from flask import Flask, render_template, request
import datetime as dt
from pymongo import MongoClient

with open('db_connection_string.txt','r') as f:
    connection_string = f.read()

app = Flask(__name__)
client = MongoClient(connection_string)
app.db = client.microblog

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        entry_content = request.form.get("content")
        formatted_date = dt.datetime.now().strftime("%Y-%m-%d")
        app.db.entries.insert_one({"content": entry_content, "date":formatted_date})
        

    entries_with_date = [
        (
        entry["content"],
        entry["date"],
        dt.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
        )
        for entry in app.db.entries.find({})
    ]
    return render_template("home.html", entries=entries_with_date)
