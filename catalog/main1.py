from flask import Flask,redirect,url_for,render_template,request,flash
from flask_mail import Mail,Message
from random import randint
from db import Register,Base,User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager,current_user,login_user,logout_user,login_required

engine=create_engine('sqlite:///LIST.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)
session=DBSession()

app=Flask(__name__)
app.secret_key='ss'

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

@login_manager.user_loader
def load_user(user_id):
	return session.query(User).get(int(user_id))

@app.route('/index')

def index():
	return render_template('index.html')
'''
@app.route('/hi')
def hiData():
	return render_template('hi.html')'''

@app.route('/show', methods=['POST','GET'])
def showData():
	register=session.query(Register).all()
	return render_template('show.html',reg=register)

@app.route('/add',methods=['POST','GET'])
def addData():
	if request.method=='POST':
		newData=Register(name=request.form['name'],email=request.form['email'],des=request.form['des'],password=request.form['password'])
		session.add(newData)
		session.commit()
		flash("New data is added")
		return redirect(url_for('showData'))
	else:
		return render_template('add.html')
@app.route('/edit/<int:register_id>',methods=['POST','GET'])
def editData(register_id):
	editeddata=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		editeddata.name=request.form['name']
		editeddata.email=request.form['email']
		editeddata.des=request.form['des']
		session.add(editeddata)
		session.commit()
		flash("Successfully Edited %s" %(editedData.name))
		return redirect(url_for('showData'))
	else:
		return render_template('edit.html',register=editeddata)

@app.route('/delete/<int:register_id>',methods=['POST','GET'])
def deleteData(register_id):
	deletedata=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		session.delete(deletedata)
		session.commit()
		return redirect(url_for('showData',register_id=register_id))
	else:
		return render_template('delete.html',register=deletedata)

@app.route("/account",methods=['GET','POST'])
@login_required
def account():
	return render_template('account.html')

@app.route('/register',methods=['POST','GET'])
def registerData():
	if request.method=='POST':
		userdata=User(name=request.form['name'],email=request.form['email'],password=request.form['password'],des=request.form['des'])
		session.add(userdata)
		session.commit()
		return redirect(url_for('index'))
	else:
		return render_template('register.html')


@login_required
@app.route("/login",methods=['POST','GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('showData'))
	try:
		if request.method=='POST':
			user=session.query(User).filter_by(email=request.form['email'],password=request.form['password']).first()
			if user:
				login_user(user)
				return redirect(url_for('showData'))
			else:
				flash('Login failed')
		else:
			return render_template('login.html',title="login")
	except Exception as e:
		flash("login failed")
	else:
		return render_template('login.html',title="login")

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
	return session.query(User).get(int(user_id))

if __name__=='__main__':
	app.run(debug=True)