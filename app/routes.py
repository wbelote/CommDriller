import time

from flask import redirect, render_template, request, url_for, make_response

from app import app, data


@app.route("/")
def home():
    return redirect(f"corners")


@app.route("/corners")
def corners():
    return redirect(f"corners/{data.next_case()}")


@app.route("/corners/<case_id>")
def corners_id(case_id):
    case = data.case_for_id(case_id)
    return render_template("main.html", case=case, history=data.history(), stats=[])


@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "POST":

        form_data = dict(request.form.items())
        if not form_data["time"].strip():
            print("DATA NOT SUBMITTED")
            return redirect(f"corners/{form_data['case_id']}")
        form_data['date'] = int(time.time())

        # data.submit(form_data)
        res = make_response(redirect(f"corners/{form_data['case_id']}"))
        cookie = request.cookies.get('times')
        res.set_cookie(
            'times',
            f"{cookie}i{round(float(form_data['time']), 3)}i{int(form_data['date'])}i{int(form_data['case_id'])}n"
        )
        return res

    return redirect(url_for("corners"))

# @app.route("/table")
# def table():
#     grid = db.time_grid()
#     return render_template("grid.html", grid=grid)


# @app.route("/delete/<time_corner>")
# def delete(time_corner):
#     time_id, case_id = time_corner.split("-")
#     db.delete_time(time_id)
#     return redirect(f"/corners/{case_id}")
