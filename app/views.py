from app import app
from flask import render_template, flash, redirect
from .forms import LoginForm

@app.route('/')
@app.route('/index')
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
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login Request for OpenID="%s", remember="%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form)

