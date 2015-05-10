from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import (LoginManager, login_user, logout_user, 
							login_required, current_user)

from flask.ext.bootstrap import Bootstrap

import forms
import models
import dropbox
import urllib2

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

#dropbox keys
app_key = 'd7haw01kdn41pu8'
app_secret = 'inngitouy4se0l7'

app = Flask(__name__)
app.secret_key = 'ooogaboogaoooga'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

bootstrap = Bootstrap()

@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None

@app.before_request
def before_request():
	"""Connect to the database before each request"""
	g.db = models.DATABASE 
	g.db.connect()
	g.user = current_user

@app.after_request
def after_request(response):
	"""Close the connection after each request"""
	g.db.close()
	return response

@app.route('/register', methods=('GET', 'POST'))
def register():
	form = forms.RegisterForm()
	if form.validate_on_submit():
		flash("You have registered successfully", "success")
		models.User.create_user(
			username = form.username.data,
			email=form.email.data,
			password=form.password.data
		)
		return redirect(url_for('dfbAuth'))
	return render_template('register.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
	form = forms.LoginForm()
	if form.validate_on_submit():
		try:
			user = models.User.get(models.User.email == form.email.data)
		except models.DoesNotExist:
			flash("Email or Password dosnt match!", "error")
		else:
			if check_password_hash(user.password, form.password.data):
				login_user(user)
				flash("You have been logged in to DfB Explorer", "Success")
				return redirect(url_for('dfbAuth'))
			else:
				flash("Email or Password dosnt match!", "error")
	return render_template('login.html', form=form)

@app.route('/dfbAuth', methods=('GET', 'POST'))
@login_required
def dfbAuth():
	form = forms.DfBAuthForm()
	flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
	authorize_url = flow.start()
	if form.validate_on_submit():
		DfBAuthKey = form.dfbauthcode.data 
		return redirect(url_for('index', a=DfBAuthKey))	
	return render_template('dfbAuth.html', authorize_url=authorize_url, form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You have been logged out", "success")
	return redirect(url_for('login'))

@app.route('/')
@app.route('/<string:a>')
@login_required
def index(a=None):
	if a == None:
		return render_template('main.html', data='{}')
	else:
		#build a urllibrequest to the DfB API
		request = urllib2.Request('https://api.dropbox.com/1/team/get_info')
		request.add_header('Content-type', 'application/json')
		request.add_header('Authorization','Bearer Roti84bECDUAAAAAAAACOhZz6DJtV9g4kWxk2_6gc7GOObK7nrmz1c4ITHm1wlOE')
		body = str('{}')
		request.add_data(body)
		response = urllib2.urlopen(request)
		data = response.read()
		return render_template('main.html', data=data)

if __name__ == '__main__':
	models.initialize()
	bootstrap.init_app(app)
	try:
		models.User.create_user(
			username='chadduffey',
			email='chadduffey@hotmail.com',
			password='password',
			admin=True)
	except ValueError:
		pass

	app.run(debug=DEBUG, host=HOST, port=PORT)