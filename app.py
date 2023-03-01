from flask import Flask, render_template, redirect, session, url_for
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

app = Flask(__name__)
app.secret_key = 'mubashar123'
app.config["MONGO_URI"] = "mongodb://localhost:27017/login1st"
mongo = PyMongo(app)

class SignupForm(FlaskForm):
    full_name = StringField('Full Name', validators=[validators.DataRequired()])
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({'username': form.username.data})
        if user is None:
            mongo.db.users.insert_one({'full_name': form.full_name.data, 'username': form.username.data, 'password': form.password.data})
            return redirect(url_for('login'))
        else:
            form.username.errors.append('Username already exists')
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({'username': form.username.data, 'password': form.password.data})
        if user is not None:
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            form.username.errors.append('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = mongo.db.users.find_one({'username': session['username']})
    return render_template('home.html', full_name=user['full_name'], username=session['username'])
    # return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)