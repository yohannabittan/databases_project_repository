#private content sharing
#Programmer : Yohann A Abittan 
#NetID : yaa243

from flask import Flask,render_template,request, redirect, url_for , session
import pymysql.cursors
import hashlib

app = Flask(__name__)

app.secret_key = 'A key that is oh so secret'

conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='Private_content_sharing', charset='utf8mb4', port=3306, cursorclass=pymysql.cursors.DictCursor)

@app.route("/")

def home():
	return render_template("home.html", title="Welcome to the home page")

@app.route("/login", methods=['GET'])

def login():
	return render_template("login.html", title="Login")

@app.route("/register", methods=['GET'])

def register():
	return render_template("register.html", title="Sign up")

@app.route('/registerAuth', methods=['GET','POST'])

def registerAuth():
	username = request.form['username']
	password = request.form['password']

	password = hashlib.md5(password).hexdigest()

	cursor = conn.cursor()

	query = 'SELECT * FROM person WHERE username = %s'
	cursor.execute(query,(username))

	data = cursor.fetchone()

	if (data): 
		error = "This username is already in use"
		cursor.close()
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO person VALUES(%s,%s,NULL,NULL)'
		cursor.execute(ins,(username,password))
		conn.commit()
		cursor.close()
		return render_template('home.html', title="Sign up succeeded")

@app.route('/loginAuth', methods = ['GET','POST'])

def loginAuth():
	username = request.form['username']
	password = request.form['password']

	password = hashlib.md5(password).hexdigest()

	cursor = conn.cursor()

	query = 'SELECT * FROM person WHERE username =%s  and password =%s '
	cursor.execute(query, (username, password))
	
	data = cursor.fetchone()
	
	cursor.close()
	
	if(data):
		session['username'] = username 
		return render_template('homePage.html', title="Login succeeded")
	else:
		error = "The username and password combination is incorrect"
		return render_template('login.html',error = error)



@app.route('/homePage', methods=['GET'])

def homePage():
	
	cursor = conn.cursor()
	query = 'SELECT content_name, timest, username FROM content WHERE public = 1'
	cursor.execute(query)
	content = cursor.fetchall()
	cursor.close()
	return render_template('homePage.html', content=content)
	#else :
	#	error = "You must be logged in to access this page !"
	#	return render_template('login.html',error = error)

@app.route('/prePost', methods=['GET'])

def prePost():

	return render_template("prePost.html", title="Here you can post your content")

@app.route('/postPost', methods=['GET','POST'])

def postPost():

	filepath = request.form['filepath']
	contentname = request.form['contentname']
	public = form.public.data
	username = session['username']

	cursor = conn.cursor()
	ins = 'INSERT INTO content VALUES(NULL,%s,current_timestamp,%s,%s,%s)'
	
	if public == "True":
		cursor.execute(ins,(username,filepath,contentname,True))
		conn.commit()
	else:
		cursor.execute(ins,(username,filepath,contentname,False))
		conn.commit()

	cursor.close()

	return render_template('homePage.html', title="successful post")


@app.route('/logout',methods=['GET'])

def logout():
	session.pop('username')
	return render_template('logout.html')

if __name__ == "__main__":
	app.run('127.0.0.1',5000, debug = True)

