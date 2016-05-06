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



@app.route("/log-out")
def log_out():
    """Log user out. Take user id out of session."""

    flash("You are now logged out!")
    del session["email"]

    return render_template("homepage.html")
        


@app.route("/users/<int:user_id>")
def details(user_id):
    """Take User to details page."""

    user = User.query.get(user_id) #returns an object: such as row of user info 

    ratings = user.ratings



    return render_template("user_details.html", user=user, ratings=ratings)


@app.route("/movie-list")
def movie_list():
    """Take user to a listing of all movies """

    movies = Movie.query.order_by(Movie.title).all()
    return render_template("movie_list.html", movies=movies)


@app.route("/movie-details/<int:movie_id>", methods=["GET"])
def movie_details(movie_id):
    """Take user to a profile of a movie."""
    movie = Movie.query.get(movie_id)
    user_id = session.get("user_id")

    
    if user_id:
        user_rating = Rating.query.filter_by(
            movie_id=movie_id, user_id=user_id).first()

    else:
        user_rating = None

    return render_template("movie_details.html",
                           movie=movie,
                           user_rating=user_rating)



@app.route("/movie-details/<int:movie_id>", methods = ['POST'])
def submit_rating(movie_id):
    """Submit user rating"""
    
    score = int(request.form["score"])

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("No user logged in.")

    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

    if rating:
        rating.score = score
        flash("Rating updated.")

    else:
        rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
        flash("Rating added.")
        db.session.add(rating)

    db.session.commit()

    return redirect("/movie-details/%s" % movie_id)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
