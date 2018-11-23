from flask import Flask, jsonify, json, Response
from flask_pymongo import PyMongo
import datetime
from flask_cors import CORS
from flask import request
from flask import Response
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'py_mongo'
app.config['MONGO_URI'] = 'mongodb://tibi:tibitibi1@ds121212.mlab.com:21212/py_mongo'

mongo = PyMongo(app)

@app.route('/')
def welcome():
	return 'welcome'

# ADD
@app.route('/add', methods=['POST'])
def add():
	todos = mongo.db.todos
	data = request.json
	todos.insert(data)
	return Response(str('complete'), status=200, mimetype='application/json');

# FIND-ONE
@app.route('/find-one/<jobname>', methods=['GET'])
def findOne(jobname):
	todos = mongo.db.todos
	todo = todos.find_one_or_404({'name':jobname})
	return jsonify({'name':todo['name'], 'done':todo['done']})

# FIND-ALL
@app.route('/find-all', methods=['GET'])
def findAll():
	todos = mongo.db.todos
	output = []
	for i in todos.find():
		job = todos.find_one_or_404({'name':i['name']})
		id = job['_id']
		output.append({'id':str(id),'name':i['name'], 'done':i['done'], 'description':i['description'], 'date':i['date'], 'time':i['time']})
	response_data = json.dumps(output)
	response = Response(response_data, status=200, mimetype="application/json")
	response.headers['Location'] = '/find-all'
	return response

# UPDATE
@app.route('/update/<jobid>', methods=['PUT'])
def update(jobid):
	todos = mongo.db.todos
	data = request.json
	todo = todos.find_one_or_404({'_id': ObjectId(jobid)})
	if todo:
		todo['description'] = data['description']
		todo['done'] = data['done']
		todo['date'] = data['date']
		todos.save(todo)
		response = Response('Updated', status=200, mimetype="application/json")
		response.headers['Location'] = '/update/' + str(jobid)
		return response
	else:
		error = json.dumps({"error":"Failed to update"})
		response = Response(error, status=400, mimetype="application/json")
		return response

# DELETE
@app.route('/delete/<jobid>', methods=['POST'])
def delete(jobid):
	todos = mongo.db.todos
	# data = request.json
	todo = todos.find_one_or_404({'_id': ObjectId(jobid)})
	if todo:
		todos.remove(todo)
		response = Response('Deleted', status=200, mimetype="application/json")
		response.headers['Location'] = '/delete/' + str(jobid)
		return response
	else:
		error = json.dumps({"error":"Failed to delete"})
		response = Response(error, status=400, mimetype="application/json")
		return response
	

if __name__ == '__main__':
	app.run(debug=True)