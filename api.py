from pymongo import MongoClient
from bson.objectid import ObjectId
import time
import bcrypt
import settings

client = MongoClient('mongodb://localhost:27017/')
mydb = client.mydatabase
account = mydb.account
customers = mydb.customers
list_people = mydb.list_people
list_customer =mydb.list_customer
list_product = mydb.list_product
list_project =mydb.list_project
list_team =mydb.list_team
todo_list =mydb.todo_list




def create_account(name, job, email, password,phone,country,region):
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    account_item = account.insert_one({"name":name,
                          "job":job,
                          "email":email,
                          "password":password,
                          "phone":phone,
                          "country":country,
                          "region":region,
                          })
    return account_item

# def update_account_by_id(account_id,name,nick_name):
#     if not isinstance(account_id, ObjectId):
#         account_id = ObjectId(account_id)
#     new_data = {"name":name,
#                 "nickname":nick_name,
#                 "nickname":nick_name,
#                 "nickname":nick_name,
#                 "nickname":nick_name,
#                 "nickname":nick_name,
#                 "nickname":nick_name,
#                 "nickname":nick_name,
#                 "nickname":nick_name,
#                 }
#     account.update_one({'_id': account_id}, {'$set': new_data})


def create_todo(title,description,completed):
    todo_item = todo_list.insert_one({"title":title,
                          "description":description,
                          "completed":completed})
    return todo_item




def insert_people(name_people,address_people,phone_people,position_people):
    people_item = list_people.insert_one({"name":name_people,
                          "address":address_people,
                          "phone":phone_people,
                          "position":position_people,
                          })
    return people_item

def insert_project(name_project,time_begin,time_finish,description_project):
    project_item = list_project.insert_one({"name":name_project,
                          "time_begin":time_begin,
                          "time_finish":time_finish,
                          "description":description_project,
                          })
    return project_item

def insert_team(job,name,number_team):
    team_item = list_team.insert_one({"job":job,
                          "name":name,
                          "number_team":number_team,
                          })
    return team_item

def find_account_by_id(account_id):
    if not isinstance(account_id, ObjectId):
        account_id = ObjectId(account_id)
    return account.find_one({'_id': account_id})


def find_account_by_mail(email):
    return account.find_one({'email': email})

def check_account_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def delete_user_by_id(people_id):
    if not isinstance(people_id, ObjectId):
        people_id = ObjectId(people_id)
    return list_people.delete_one({'_id':people_id})

def delete_team_by_id(team_id):
    if not isinstance(team_id, ObjectId):
        team_id = ObjectId(team_id)
    return list_team.delete_one({'_id':team_id})


def delete_project_by_id(project_id):
    if not isinstance(project_id, ObjectId):
        project_id = ObjectId(project_id)
    return list_project.delete_one({'_id':project_id})