from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient()
db = client.ccDatabase
foods = db.foods
people = db.people
meals = db.meals
goalsColl = db.goals

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
	totalCarbs = 0
	totalFiber = 0
	totalCalories = 0
	goalCarbs = 0
	goalFiber = 0
	goalCalories = 0
	now = datetime.datetime.now()
	day = str(now.month) + "/" + str(now.day) + "/" + str(now.year)
	breakfastList = []
	lunchList = []
	dinnerList = []
	snackList = []
	post = {'user':name, 'date':day, 'breakfast':[], 'lunch':[], 'dinner':[], 'snack':[]}
	meal_response = meals.insert_one(post).inserted_id
	meal = meals.find_one({'user':name, 'date':day})		
	goalFind = goalsColl.find_one({'user':name})
	if goalFind != None:
		goalCarbs = goalFind['goalCarbs']
		goalFiber = goalFind['goalFiber']
		goalCalories = goalFind['goalCalories']
	for item in meal['breakfast']:
		foodResult = foods.find_one({"_id":ObjectId(item['foodID'])})
		totalCarbs += int(foodResult['foodCarbs'])
		totalFiber += int(foodResult['foodFiber'])
		totalCalories += int(foodResult['foodCalories'])
		breakfastList.append(foodResult)
	for item in meal['lunch']:
		foodResult = foods.find_one({"_id":ObjectId(item['foodID'])})
		totalCarbs += int(foodResult['foodCarbs'])
		totalFiber += int(foodResult['foodFiber'])
		totalCalories += int(foodResult['foodCalories'])
		lunchList.append(foodResult)
	for item in meal['dinner']:
		foodResult = foods.find_one({"_id":ObjectId(item['foodID'])})
		totalCarbs += int(foodResult['foodCarbs'])
		totalFiber += int(foodResult['foodFiber'])
		totalCalories += int(foodResult['foodCalories'])
		dinnerList.append(foodResult)
	for item in meal['snack']:
		foodResult = foods.find_one({"_id":ObjectId(item['foodID'])})
		totalCarbs += int(foodResult['foodCarbs'])
		totalFiber += int(foodResult['foodFiber'])
		totalCalories += int(foodResult['foodCalories'])
		snackList.append(foodResult)

	if request.method == "POST":
		selectedFood = request.form.get('userFoods')
		selectedFood = selectedFood.split(',')
		result = meals.update_one({'user':name, 'date':day}, { '$push': {selectedFood[1]: {'foodID': selectedFood[0]}}})
	foodResponse = foods.find({"user":name})
	foodList = []
	for food in foodResponse:
		foodList.append(food)
	return render_template('diary.html', name=name, foodList=foodList, day=day, breakfastList=breakfastList, lunchList=lunchList, dinnerList=dinnerList, snackList=snackList, totalCarbs=totalCarbs, totalFiber=totalFiber, totalCalories=totalCalories, goalCarbs=goalCarbs, goalFiber=goalFiber, goalCalories=goalCalories)

@app.route('/goals', methods=['GET', 'POST'])
def goals():
	goal_response = None
	if request.method == "POST":
		post = {'user':name, 'goalCarbs':request.form['goalCarbs'], 'goalFiber':request.form['goalFiber'], 'goalCalories':request.form['goalCalories']}
		goal_response = goalsColl.insert_one(post).inserted_id
	return render_template('goals.html', name=name, goal_response=goal_response)

if __name__ == '__main__':
	app.run(debug = True)


