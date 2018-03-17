######### REMEMBRALL ############
''' a web application/API to take notes and make to do list '''
import flask_login
from flask import Flask, render_template, request, url_for, session, redirect
from pymongo import MongoClient
import bcrypt
import time
from mako.template import Template
from flask_session import Session

MONGODB_URI = "mongodb://mmm:qazwsx123@ds251827.mlab.com:51827/log_in_details"
client = MongoClient(MONGODB_URI)
db = client.get_database("log_in_details")
login_details =db.log_in_details


notes = Flask(__name__)
#login_manager = flask_login.LoginManager()
#login_manager.init_app(notes)

@notes.route("/")
def app_home():
	if 'email' in session:
		template = Template(filename="main.html" ) 
		#print(template.render(x="Hello World!")		
		return template.render(x = session['email'])
		#time.sleep(5)
		#return 'you are logged in as ' + session['email'] + '<br>' + '<b><a href = "/logout">click here to log out</a></b>'
	return render_template("home.html")

@notes.route("/login_page", methods=['POST','GET'])
def login_page():
	if request.method=='POST':
		email = login_details.db.users
		login_user = email.find_one({'email': request.form['Lemail']})
		if login_user:
			if bcrypt.hashpw(request.form['password'].encode('UTF-8'), login_user['password']) == login_user['password']:
				session['email'] = request.form['Lemail']
				return redirect(url_for('app_home'))
				#return "does it work fine?"
		return 'Invalid username/password combination'
	return render_template('login_page.html')	

	#return render_template("login_page.html")



@notes.route('/logout', methods=['GET',])
def logout():
    if request.method =='GET':
    	#return render_template('home.html')
    	session.pop('email', None)
    #flash('You were logged out')
    	return redirect(url_for('app_home'))
    
'''@login_manager.user_reloader
def user_reloader(email):
	if email not in login_details[email]:
		return'''
    
@notes.route("/sign_up", methods=['POST','GET'])
def sign_up():
	if request.method =='POST':
		email = login_details.db.users
		existing_user =email.find_one({'email': request.form['email']})#changed
		user = {}
		user['email']= request.form['email'] #changed
		if existing_user is None:
			hashpass = bcrypt.hashpw(request.form['set_password'].encode('UTF-8'), bcrypt.gensalt())
			email.insert({'email': request.form['email'], 'password': hashpass})
			session['email'] = request.form['email']
			#session['logged_in'] = True
			#flash('you were logged in')	
			return redirect(url_for('app_home'))
		return 'an account with that email already exists'
	return render_template('sign_up.html')

@notes.route("/new_note", methods=['POST', 'GET'])
def new_note():
	if 'email' in session:
		if request.method =='POST':
			store_notes = login_details.db.store_notes
			header=store_notes.find({"header": request.form['header']})
			
			if header:
				user={}
				user['header']= request.form.get('header')
				user['note']= request.form.get('notes')

				store_notes.insert(user)
				return 'your note has been saved!'
			return 'that title already exists. Choose a new one.'

#@notes.route("/change", methods=['GET','POST','PATCH','DELETE'])
		# if request.method =='PATCH':
		# 	store_notes.find_one({'header':request.form['header']})
		# 	store_notes.update_one({'note': request.form['notes']},{'$set':request.form})
		# 	return 'your note has been modified!'
		# elif request.method =='DELETE':
		# 	store_notes.delete_one({})





if __name__ == '__main__':
	notes.secret_key = 'mysecret'
	notes.run(port=2222, use_reloader =True, debug =True)
