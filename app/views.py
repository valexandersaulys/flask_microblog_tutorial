from app import app, db, lm, oid
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from .models import User

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    # the current_user global is set by Flask-Login
    g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'nickname': 'Miguel'} # fake name

    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful Day in Portland!'
            },
        {
            'author': {'nickname': 'Susan'},
            'body': "The Avenger's Movie was so cool!"
            }
        ]
    
    return render_template('index.html',
                           title="Home",
                           user=user,
                           posts=posts)

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler  # This tells Flask-OpenIOd that this is our login view function
def login():
    # Checks to see if the user is logged in
    if g.user is not None and g.user.is_authenticated:
        # g is a global setup by Flask a place to store and share data during
        # the life of a request. Here we'll be storing the logged in user.
        
        return redirect(url_for('index'))  # Using url_for() will enable Flask
                                           # to build the necesary redirect.
    # Get the login form
    form = LoginForm()
    if form.validate_on_submit():
        # Remember the user log in
        # remember_me boolean is stored into the flask session (not db.session)
        # flask.session will store data made during that request and future
        # requests made by the same client. data remains until explicity removed
        session['remember_me'] = form.remember_me.data
        
        # This triggers the user authentication through Flask-OpenID
        # OpenID authentication happens async, after which it'll call oid.after_login
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):  # resp is passed to afte_login with OpenID information
    # First check is to look for validation, we need valid email
    if resp.email is None or resp.email == "":
        flask('Invalid Login, Please Try Again')
        return redirect(url_for('login'))
    
    # Next, search for the user's email and if it isn't in there, we add it
    user = User.query.filter_by(email=resp.email).first()
    # This is just to formally add it to the database
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()

    # Then we load the remember_me value from the Flask session
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    # Then we call Flask-Login's login_user function to register this as valid
    login_user(user, remember = remember_me)

    # Then we redirect to the next page or the index page if a next page was
    # not provided in the request
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
