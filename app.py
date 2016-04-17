from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

name=None

@app.route('/', methods=['GET', 'POST'])
def login_page():
	error = None
	if request.method=='POST':
		if request.form['username']=='kaitcov' and request.form['password']=='p':
			global name
			name=request.form['username']
			return redirect(url_for('home', name=name))
		else:
			error="Invalid Credentials"
	return render_template('login.html', error=error)

@app.route('/home')
def home():
	return render_template('home.html', name=request.args.get('name'))

@app.route('/about')
def about():
	return render_template('about.html', name=name)

@app.route('/createFood')
def createFood():
	return render_template('createFood.html', name=name)

if __name__ == '__main__':
	app.run(debug = True)


