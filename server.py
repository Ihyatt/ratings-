"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/sign-in")
def sign_in():
    """Sign in."""

    
    return render_template("sign_in.html")

@app.route("/user-repeat-check", methods = ['POST'])
def user_repeat_check():
    """Checking if user exists."""
  
    email = request.form.get("email")
    password = request.form.get("password")
    session["email"] = email

    if User.query.filter(User.email == email).all():
        flash('You are already a user!')
    else:
        
        flash('You were successfully logged in')
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

    return render_template("sign_in.html", email=email, password=password)

@app.route("/log-in")
def log_in():
    """log in."""

    
    return render_template("log_in.html")


@app.route("/log-in-check", methods = ['POST'])
def log_in_check():
    """Checking if user exists."""

    email = request.form.get("email")
    password = request.form.get("password")

    session["email"] = email
    
    if User.query.filter(User.email == email).all():
        if User.query.filter(User.password == password).all():
            flash('You are logged in!')
    else:
        
        flash("You are not a user, you're a loser")
        return render_template("sign_in.html")

    return render_template("homepage.html")

@app.route("/user-list")
def details():
    """Take User to details page."""

        
    return render_template("user_list.html")

@app.route("/log-out")
def log_out():
    """Log user out. Take user id out of session."""

    flash("You are now logged out!")
    del session["email"]

    return render_template("homepage.html")
        



@app.route("/users/<int:user_id>")
def details(user_id):
    """Take User to details page."""

    user_check = User.query.filter(user_id == user_id).first()

    rating_check = Rating.query.filter(user_id == user_id).all()

    return render_template("user_details.html", user_check=user_check, rating_check=rating_check)
        


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
