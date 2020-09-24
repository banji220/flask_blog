from flask import render_template, url_for, flash, redirect
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user

posts = [
    {
        "author": "@Banji",
        "title": "Blog Post 1",
        "content": "My first blog post in Flask",
        "date" : "Sep 1, 2020"
    },
    {
        "author": "@mirdarx",
        "title": "Blog Post 2",
        "content": "My Second blog post in Flask",
        "date": "Sep 4, 2020"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title = "About")


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account has been created for with ❤️! You are now able to log in", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title = "Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for("home"))
            else:
                 flash(f"Login Was Unsuccessful 😕, Please check your username and password!", "danger")
        
    return render_template("login.html", title = "Login", form=form)
