from flask import Flask, render_template, request, redirect, url_for
from database import cases as db_cases
import random

app = Flask(__name__)

"""
App for tracking times and algs for 3-style comms

Timer view:
- Shows a case, enter time with typing or timer
- Option to show/hide/edit alg for that case
- Next button for next case
- Prioritizes times based on:
    - Amount drilled, less first
    - Average time, slower first
    - Time since drilled, longer first
View time history, for case or for all
"""


@app.route("/")
def home():
    return redirect(url_for("corners"))


@app.route("/corners")
def corners():
    case = random.choice(db_cases())
    case_name = f"UFR-{case[0]}-{case[2]} ({case[1]}{case[3]})"
    return render_template("main.html", name=case_name, alg=case[4])


@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        data = dict(request.form.items())
        return render_template("submitted.html", time=data["time"])


if __name__ == '__main__':
    app.run(debug=True)
