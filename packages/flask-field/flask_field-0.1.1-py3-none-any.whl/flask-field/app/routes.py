from flask import Blueprint, flash, redirect, render_template, url_for, session
from app.modules.templates_classes.auth import *
from app.modules.db_manager import *

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/")
def index():
    return render_template("index.html", title="Maxim Industies")

@routes_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data).first()
        if user != None:
            session["user_id"] = user.user_id
            session["username"] = user.login

            isClient = user.role == "user"

            if isClient != None:
                session["role"] = "user"
            else:
                session["role"] = "admin"

            if session["role"] == "admin":
                return redirect(url_for("routes.admin"))
            else:
                return redirect(url_for("routes.user"))
        else: 
            flash("Неверный пароль!", "danger")
    return render_template("login.html", title="Вход", form=form)

@routes_bp.route("/registration", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            login=form.username.data,
            password_hash=form.confirm_password.data
        )

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.user_id
        session["username"] = new_user.login
        session["role"] = "client"

        return redirect(url_for("routes.client"))

    return render_template("register.html", form=form)

@routes_bp.route("/user", methods=["GET", "POST"])
def client():
    if session["role"] != "pharmaceft":
        flash("Недостаточно привелегий", "danger")
        return redirect(url_for("routes.login"))
    return render_template("user.html")

@routes_bp.route("/admin", methods=["GET", "POST"])
def manager():
    if session["role"] != "manager":
        flash("Недостаточно привелегий", "danger")
        return redirect(url_for("routes.login"))
    return render_template("admin.html")