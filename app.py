from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import UserForm, LoginForm, Delete, FeedbackForm
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()
connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "SMOKEY"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404, 401

@app.errorhandler(401)
def page_not_authorized(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 401


@app.route("/")
def redirecting():
    """Redirects to /register"""

    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register():
    """Show register form and post user info"""

    if 'username'  in session:
        return redirect(f"/users/{session['username']}")
    
    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, pwd, email, first_name, last_name)
        
        db.session.commit()
        session["username"] = user.username

        return redirect(f"/users/{session['username']}")
    
    return render_template('user/register.html', form = form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Show login form and authenticate user"""

    if 'username'  in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data

        user =  User.authenticate(username, pwd)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        
        else:
            form.username.errors = ["Invalid username/password"]

    return render_template('user/login.html', form = form)
    

@app.route('/logout')
def logout():
    """Logs user out and redirects to homepage"""

    session.pop('username')

    return redirect("/")

@app.route('/users/<username>')
def show_user(username):
    if 'username' not in session or username != session['username']:
        flash("You are not authorized to view this page")
        return redirect("/")
    
        # alternatively, can return HTTP Unauthorized status:
        #
        # from werkzeug.exceptions import Unauthorized
        # raise Unauthorized()

    user = User.query.get_or_404(username)
    form = Delete()
    return render_template('user/show.html', user=user, form=form)


@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Deletes user off the database"""

    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username')

    return redirect("/")

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """Shows feedback add form and post into database"""
    if 'username' not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get_or_404(username)
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)
        
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{user.username}")
    
    else:
        return render_template('feedback/new.html', form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """Show update-feedback form and post it"""
    feedback = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized()
    

    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        flash(f"Update Feedback-{feedback.title}")
        return redirect(f"/users/{feedback.username}")
    
    return render_template("feedback/edit.html", form=form, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Deletes feedback"""

    feedback = Feedback.query.get_or_404(feedback_id)
    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f"/users/{feedback.username}")


