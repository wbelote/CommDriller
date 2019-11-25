from flask import Flask, render_template, request, redirect, url_for
import database as db
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
    case = random.choice(db.cases())
    return redirect(f"corners/{next(case)}")


@app.route("/corners")
def corners():
    case = random.choice(db.cases())
    return redirect(f"corners/{case[0]}")


@app.route("/corners/<case_id>")
def corners_id(case_id):
    case = db.case_for_id(case_id)
    case_name = f"UFR-{case[1]}-{case[2]} ({case[3]}{case[4]})"
    return render_template("main.html", name=case_name, alg=case[5], case_id=case[0], history=db.history())


@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        data = dict(request.form.items())
        today = time.localtime()
        date = today.tm_year * 10000 + today.tm_mon * 100 + today.tm_mday
        db.submit((data["time"], date, data["case_id"]))
        return redirect(f"corners/{data['case_id']}")
    return redirect(url_for(f"corners"))


if __name__ == '__main__':
    app.run(debug=True)
