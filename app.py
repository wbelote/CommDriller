from flask import Flask, render_template, request, redirect, url_for
from database import cases as db_cases, submit as db_submit
import random, time

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
    case_name = f"UFR-{case[1]}-{case[3]} ({case[2]}{case[4]})"
    return render_template("main.html", name=case_name, alg=case[5], case_id=case[0])


@app.route("/submit/<case_id>", methods=["POST", "GET"])
def submit(case_id):
    if request.method == "POST":
        data = dict(request.form.items())
        today = time.localtime()
        date = today.tm_year * 1000 + today.tm_mon * 100 + today.tm_mday
        db_submit(data["time"], date, case_id)
    return redirect(url_for("corners"))


if __name__ == '__main__':
    app.run(debug=True)
