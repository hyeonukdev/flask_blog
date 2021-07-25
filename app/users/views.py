from flask import render_template
from app.users import users


@users.route("/users")
def users_test():
    return render_template("users.html")

