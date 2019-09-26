from flask import Flask,redirect,url_for,render_template,request,flash
from flask_mail import Mail,Message
from random import randint

app=Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='ganiraju100@gmail.com'
app.config['MAIL_PASSWORD']='*******'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True


mail=Mail(app)
otp=randint(000000,999999)
app.secret_key='gg'

@app.route('/email')
def email():
	return render_template('email.html')
@app.route('/email_verify',methods=['POST','GET'])
def email_verify():
	email=request.form['mail']
	msg=Message('OTP for verification',sender='ganiraju100@gmail.com',recipients=[email])
	msg.body=str(otp)
	mail.send(msg)
	return render_template('email_verify.html')
@app.route('/validation',methods=['POST','GET'])
def validation():
	user_otp=request.form['otpvalue']
	if otp==int(user_otp):
		return "OTP verification is done"
	else:
		return "Invalid OTP"





@app.route('/home/<name>')
def index(name):
	return "<h1> Good Evening Gani </h1>" +name
@app.route('/index/<int:age>')
def index1(age):
	return "<h1> RamaniGani </h1>  {}" .format(age)

@app.route('/user/<float:age>')
def index2(age):
	return " %f" %age
#function mapping
@app.route('/adminurl')
def admin():
	return "<h1> This is admin page </h1>"
@app.route('/studenturl')
def student():
	return "<h1> This is student page</h1>"
@app.route('/user/<name>')
def home(name):
	if name=='adimin':
		return redirect(url_for('admin'))
	if name=='student':
		return redirect(url_for('student'))		
@app.route('/login')
def login():
	return render_template('login.html')
@app.route('/loginpage/<name>')
def loginpage(name):
	return render_template('login page.html',username=name)
@app.route('/table/<int:value>')
def table(value):
	return render_template('table.html',n=value)
	 
@app.route('/upload')
def upload():
	return render_template('upload.html')
@app.route('/success',methods=['POST','GET'])
def success():
	if request.method=="POST":
		f=request.files['image']
		f.save(f.filename)
		return render_template('success.html',name=f.filename)
	else:
		return "Please check code"
if __name__=='__main__':
	app.run(debug=True)
