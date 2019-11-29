import time

from flask import Flask, render_template, request, redirect, url_for

import database as db

"""
App for tracking times and algs for 3-style comms

Timer view:
- Shows a case, enter time with typing or timer [DONE]
- Option to show/hide/edit alg for that case
- Next button for next case [DONE]
- Prioritizes times based on:
    - Amount drilled, less first
    - Average time, slower first
    - Time since drilled, longer first
View time history, for case or for all [PARTIAL]
"""

app = Flask(__name__)


@app.route("/")
def home():
    return redirect(f"corners")


@app.route("/corners")
def corners():
    case = db.next_case()
    return redirect(f"corners/{case[0]}")


@app.route("/corners/<case_id>")
def corners_id(case_id):
    case = db.case_for_id(case_id)
    case_name = f"UFR-{case[1]}-{case[2]} ({case[3]}{case[4]})"
    return render_template("main.html",
                           case=[case[0], case_name, case[5]], history=db.history(), stats=db.stats())


@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        data = dict(request.form.items())
        if not data["time"].strip():
            print("DATA NOT SUBMITTED")
            return redirect(f"corners/{data['case_id']}")
        date = int(time.time())
        db.submit((data["time"], date, data["case_id"]))
        return redirect(f"corners/{data['case_id']}")
    return redirect(url_for(f"corners"))


@app.route("/table")
def table():
    grid = db.time_grid()
    return render_template("grid.html", grid=grid)


@app.route("/delete/<time_corner>")
def delete(time_corner):
    time_id, case_id = time_corner.split("-")
    db.delete_time(time_id)
    return redirect(f"/corners/{case_id}")


if __name__ == '__main__':
    app.run(debug=True)
