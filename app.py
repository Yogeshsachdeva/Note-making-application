######### REMEMBRALL ############
''' a web application/API to take notes and make to do list '''
import flask_login
from flask import Flask, render_template, request, url_for, session, redirect
from pymongo import MongoClient
import bcrypt
import time
from mako.template import Template
from flask_session import Session
from bson import json_util

MONGODB_URI = "mongodb://mmm:qazwsx123@ds251827.mlab.com:51827/log_in_details"
client = MongoClient(MONGODB_URI)
db = client.get_database("log_in_details")
login_details =db.log_in_details
store_notes = login_details.db.store_notes

app = Flask(__name__)
app.secret_key = 'mysecret'

@app.route("/")
def app_home():
	if 'email' in session:
		template = Template(filename="main.html" ) 		
		return template.render(x = session['email'])
	return render_template("home.html")

@app.route("/login_page", methods=['POST','GET'])
def login_page():
	if request.method=='POST':
		email = login_details.db.users
		login_user = email.find_one({'email': request.form['Lemail']})
		if login_user:
			if bcrypt.hashpw(request.form['password'].encode('UTF-8'), login_user['password']) == login_user['password']:
				session['email'] = request.form['Lemail']
				return redirect(url_for('app_home'))
		return 'Invalid username/password combination'
	return render_template('login_page.html')	

	



@app.route('/logout', methods=['GET',])
def logout():
    if request.method =='GET':

    	session.pop('email', None)
    
    	return redirect(url_for('app_home'))
    

@app.route("/sign_up", methods=['POST','GET'])
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
				
			return redirect(url_for('app_home'))
		return 'an account with that email already exists'
	return render_template('sign_up.html')

@app.route("/new_note", methods=['POST', 'GET', 'DELETE'])
def new_note():
	if 'email' in session:
		if request.method =='POST':
			#store_notes = login_details.db.store_notes
			header=store_notes.find({"header": request.form['header']})
			
			if header:
				user={}
				user['header']= request.form.get('header')
				user['note']= request.form.get('notes')

				store_notes.insert(user)
				return 'your note has been saved!'
			return 'that title already exists. Choose a new one.'
		

@app.route("/notes/<header>/", methods=['GET','PATCH','DELETE'])
def get_notes(header):
	notes=store_notes.find_one({"header":header})
	if not notes:
		return jsonify({"that note doesn't exist"})
	if request.method=='GET':
		return json_util.dumps(notes)
	elif request.method=='PATCH':
		store_notes.update_one({"header":header},{'$set':request.form})
		return jsonify({"result":"note was successfully updated"})	
	elif request.method=="DELETE":
		store_notes.delete_one({"header":header})
		return jsonify({"the note was successfully deleted!"})







if __name__ == '__main__':
	
	app.run(port=2222, use_reloader =True, debug =True)
