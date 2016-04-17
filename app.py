from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
import datetime

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
	food_id = None
	if request.method == 'POST':
		foodName = request.form['foodName']
		foodSize = request.form['foodSize']
		foodCarbs = request.form['foodCarbs']
		foodFiber = request.form['foodFiber']
		foodCalories = request.form['foodCalories']
		post = {"user":name, "foodName":foodName, "foodSize":foodSize, "foodCarbs":foodCarbs, "foodFiber":foodFiber, "foodCalories":foodCalories}
		food_id = foods.insert_one(post).inserted_id

	return render_template('createFood.html', name=name, food_id=food_id)

@app.route('/diary', methods=['GET', 'POST'])
def diary():
	now = datetime.datetime.now()
	day = str(now.month) + "/" + str(now.day) + "/" + str(now.year)
	if request.method == "POST":
		selectedFood = request.form.get('userFoods')
		selectedFood = selectedFood.split(',')
		print selectedFood[1]
		post = {'user':name, 'date':day, selectedFood[1]:[]}
		meal_response = meals.insert_one(post).inserted_id
		result = meals.update_one({'user':name, 'date':day}, { '$push': {selectedFood[1]: {'foodID': selectedFood[0]}}})
		print result.matched_count
		breakfastList = []
		lunchList = []
		dinnerList = []
		snackList = []
		if result.matched_count != 0:
			meal = meals.find_one({'user':name, 'date':day})
			for item in meal['breakfast']:
				breakfastList.append(item)
			for item in meal['lunch']:
				lunchList.append(item)
			for item in meal['dinner']:
				dinnerList.append(item)
			for item in meal['snack']:
				snackList.append(item)
	foodResponse = foods.find({"user":name})
	foodList = []
	for food in foodResponse:
		foodList.append(food)
	return render_template('diary.html', name=name, foodList=foodList, day=day, breakfastList=breakfastList, lunchList=lunchList, dinnerList=dinnerList, snackList=snackList)

if __name__ == '__main__':
	app.run(debug = True)


