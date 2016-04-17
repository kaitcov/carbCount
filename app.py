from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client.ccDatabase
foods = db.foods
people = db.people
meals = db.meals

name=None

@app.route('/', methods=['GET', 'POST'])
def login_page():
	error = None
	if request.method=='POST':
		if request.form['username']=='kaitcov' and request.form['password']=='p':
			global name
			name=request.form['username']
			post = {"name": name}
			user_id = people.insert_one(post).inserted_id
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

@app.route('/createFood', methods=['GET', 'POST'])
def createFood():
	if request.method == 'POST':
		foodName = request.form['foodName']
		foodSize = request.form['foodSize']
		foodCarbs = request.form['foodCarbs']
		foodFiber = request.form['foodFiber']
		foodCalories = request.form['foodCalories']
		post = {"user":name, "foodName":foodName, "foodSize":foodSize, "foodCarbs":foodCarbs, "foodFiber":foodFiber, "foodCalories":foodCalories}
		food_id = foods.insert_one(post).inserted_id
		for item in foods.find({"name":name}):
			print item

	return render_template('createFood.html', name=name)

@app.route('/diary')
def diary():
	return render_template('diary.html', name=name)

if __name__ == '__main__':
	app.run(debug = True)


