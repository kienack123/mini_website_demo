
from bson.objectid import ObjectId
from bson.json_util import dumps
import api
from flask import request, json , jsonify


def create_todo_list():
    if request.method == "POST":
        _json = request.json
        title = _json["title"]
        description = _json["description"]
        completed = _json["completed"]
        api.todo_list.insert_one({
            "title":title,
            "description":description,
            "completed":completed
        })
        resp = jsonify("created successfully !")
        resp.status_code = 200
        return resp
    else:
        return not_found()

def not_found(error = None):
    message = {
        'status': 404,
        'messege':'Not found' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

def get_todo_list():
    todo = api.todo_list.find()
    resp = dumps(todo)
    return resp

def delete_todo_list(id):
    api.todo_list.delete_one({'id':ObjectId(id)})
    resp = jsonify("Delete Todo successfully !")
    resp.status_code = 200 
    return resp

def update_todo_list(id):
    if request.method == "PUT":
        _json = request.json
        id = id
        title = _json["title"]
        description = _json["description"]
        completed = _json["completed"]
        api.account.update_one({'_id': ObjectId(id)},{'$set':{
            'title':title,
            'description':description,
            'completed':completed
        }})
        resp = jsonify("Update Todo successfully !")
        resp.status_code = 200

        return resp
    