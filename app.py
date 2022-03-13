
from ast import dump
from unicodedata import name
from flask import Flask,render_template,flash,request,session, request,g,json,jsonify
from matplotlib.pyplot import title
from flask.helpers import flash, url_for
from flask_login import LoginManager,login_user ,login_required ,logout_user,current_user
from flask_pymongo import PyMongo, pymongo
import pymongo
from bson.json_util import dumps
from sqlalchemy import not_
from model import User
from datetime import timedelta
from werkzeug.utils import redirect,secure_filename
from werkzeug.security import check_password_hash ,generate_password_hash
from flask_paginate import Pagination, get_page_parameter
from bson.objectid import ObjectId
import api  
import settings

# myclient = pymongo.MongoClient('mongodb://localhost:27017/')
# mydb = myclient['mydatabase']
  
app = Flask(__name__)
app.secret_key='ASDASDASDASDASDSA-4d536a7-fdd1-45db-9be7-49524a23495d'
app.config['MONGO_URI']='mongodb://localhost:27017/mydatabase'
mongo = PyMongo(app)
app.permanent_session_lifetime = timedelta(minutes=30)

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    user = api.find_account_by_id(userid)
    if user:
        g.user = user
    else:
        pass
    return User(userid)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("login"))

@app.route('/')
def loadPage():
    return render_template('loadpage.html')

@app.route('/success_register')
def success_register():
    return render_template("success_register.html")

@app.route('/home')
def home():
    return render_template('home.html')
    

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        err_msg = "Khong Dang Nhap Thanh Cong ! "
        email = request.form.get("email")
        password= request.form.get("password")
        user = api.find_account_by_mail(email)
        if user :
            if User.validate_login(user['password'], password):
                session.permanent = True
                user_obj = User(str(user['_id']))
                g.user = user
                login_user(user_obj)
                return redirect(url_for("account"))
        return redirect(url_for("login",err_msg = err_msg))
    return render_template("login.html")

@app.route('/register',methods=['POST','GET'])
def register(): 
    if request.method == 'POST':
        name = request.form.get('name')
        job = request.form.get('job')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        country = request.form.get('country')
        region = request.form.get('region')
        api.create_account(name,job,email,password,phone,country,region)
        return redirect('/success_register')
    return render_template("register.html")


@app.route('/index',methods=['POST','GET'])
@login_required
def index():
    user = g.user
    khachhang = api.customers.find()
    if request.method == 'POST':
        add_user = {"name":request.form["Name_add"],"address":request.form["Address_add"]}
        find_delete = request.form.get('Name_add')
        find = request.args.get('search_name')
        if find:
            khachhang = api.customers.find({'name': {'$regex': '.*'+find+'.*','$options':'i'}})
        if find_delete:
            api.customers.delete_one({'name': {'$regex': '.*'+find_delete+'.*','$options':'i'}})
        api.customers.insert_one(add_user)
        # ITEMS_PER_PAGE = 8
        # filter = {
            
        # }
        # count_logs = api.account.count_documents(filter)
        # page = int(request.args.get('page', 1))
        # pagination = Pagination(
        #     page=page,
        #     total=count_logs,
        #     per_page=ITEMS_PER_PAGE,
        #     css_framework='bootstrap3')
        # recs = api.customers.find(filter).sort("created_at", pymongo.DESCENDING).skip(
        #     ITEMS_PER_PAGE * (page - 1)).limit(ITEMS_PER_PAGE)
        # pagination = pagination
    return render_template("index.html", 
                            khachhang = khachhang ,user = user)


app.route("/update_todolist/<id_todo>", methods =["GET","POST"])
def update_todolist(id_todo):
    if request.method == 'POST':
        title = request.form.get["title"]
        description = request.form.get["description"]
        completed = request.form.get["completed"]
        new_data = {"$set":{"title":title,
                            "description":description,
                            "completed":completed
        }}
        api.todo_list.update_one({'_id': ObjectId(id_todo)},new_data)
        return redirect(url_for("to_do_list"))
    return redirect(url_for("to_do_list"))

app.route("/delete_todolist/<todo_id>", methods =["POST","GET"])
@login_required
def delete_todolist(todo_id):
    api.todo_list.delete_one({'_id': ObjectId(todo_id)})
    return redirect(url_for("to_do_list"))







@app.route('/list_people',methods =['POST','GET'])
@login_required
def list_people():
    user = g.user
    data_user = api.list_people.find()
    filter = {
    }
    count_logs = api.account.count_documents(filter)
    page = int(request.args.get('page', 1))
    pagination = Pagination(
        page=page,
        total=count_logs,
        per_page= settings.ITEMS_PER_PAGE,
        css_framework='bootstrap3')
    recs = api.list_people.find(filter).sort("created_at", pymongo.DESCENDING).skip(
        settings.ITEMS_PER_PAGE * (page - 1)).limit(settings.ITEMS_PER_PAGE)
    if request.method == 'POST':
        name_people = request.form.get('name_people')
        address_people = request.form.get('address_people')
        phone_people = request.form.get('phone_people')
        position_people = request.form.get('position_people')
        api.insert_people(name_people,address_people,phone_people,position_people)
        return render_template("list_people.html",data_user = data_user,user=user)
    return render_template("list_people.html",data_user = recs,user = user,pagination = pagination)

@app.route('/list_project',methods =['POST','GET'])
@login_required
def list_project():
    user = g.user
    list_project = api.list_project.find()
    filter = {
    }
    count_logs = api.account.count_documents(filter)
    page = int(request.args.get('page', 1))
    pagination = Pagination(
        page=page,
        total=count_logs,
        per_page= settings.ITEMS_PER_PAGE,
        css_framework='bootstrap3')
    recs = api.list_project.find(filter).sort("created_at", pymongo.DESCENDING).skip(
        settings.ITEMS_PER_PAGE * (page - 1)).limit(settings.ITEMS_PER_PAGE)
    if request.method == 'POST':
        name_project = request.form.get('name_project')
        time_begin = request.form.get('time_begin')
        time_finish = request.form.get('time_finish')
        description_project = request.form.get('description_project')
        api.insert_project(name_project,time_begin,time_finish,description_project)
        return render_template("list_project.html",list_project =list_project,user = user)
    return render_template("list_project.html",list_project = recs,user=user ,pagination = pagination)


@app.route('/list_team',methods =['POST','GET'])
@login_required
def list_team():
    user = g.user
    list_team = api.list_team.find()
    filter = {
    }
    count_logs = api.account.count_documents(filter)
    page = int(request.args.get('page', 1))
    pagination = Pagination(
        page=page,
        total=count_logs,
        per_page= settings.ITEMS_PER_PAGE,
        css_framework='bootstrap3')
    recs = api.list_team.find(filter).sort("created_at", pymongo.DESCENDING).skip(
        settings.ITEMS_PER_PAGE * (page - 1)).limit(settings.ITEMS_PER_PAGE)
    if request.method == 'POST':
        job = request.form.get('job')
        name = request.form.get('name')
        number_team = request.form.get('number_team')
        api.insert_team(job,name,number_team)
        return render_template("list_team.html",list_team =list_team,user = user ,pagination = pagination)
    return render_template("list_team.html",list_team = recs,user = user ,pagination = pagination)


@app.route('/create_user',methods=['POST','GET'])
@login_required
def create_user():
   data_user = api.user.find()
   if request.method == 'POST':
            create_user = {"username":request.form["name_user"],"password":request.form["password_user"]}
            api.user.insert_one(create_user)
   return render_template('user.html',data_user = data_user)

@app.route('/delete_user',methods=['POST','GET'])
@login_required
def delete_user():
   data_user = api.user.find()
   if request.method == 'POST':
            delete_one_user = request.form.get('delete_user')
            if delete_one_user:
               api.user.delete_one({'username': {'$regex': '.*'+delete_one_user+'.*','$options':'i'}})
               return render_template('delete_user.html',data_user = data_user)
                     
   return render_template('delete_user.html',data_user = data_user)


@app.route('/update_user',methods=['POST','GET'])
@login_required
def update_user():
    if request.method == 'POST':
        id = request.form.get('update_id')
        name = request.form["update_user"]
        password = request.form["update_password"]
        new_data = {"$set":{"username":name,"password":password}}
        api.user.update_one({'_id': ObjectId(id)},new_data)
        return 'Updated success !'
    data_user = api.user.find()
    return render_template('update_user.html',data_user = data_user)

@app.route('/search',methods=['POST','GET'])
@login_required
def search():
    khachhang = api.customers.find()
    if request.method == 'POST':
        find_data = request.args.get('searchname')
        if find_data:
            khachhang = api.customers.find_one( { '$text': {' $search': find_data }})
    return render_template('abc.html',khachhang = khachhang)


@app.route('/find', methods=['POST', 'GET'])
@login_required
def find():
    name = request.args.get('find_name')
    find_data = {'name': name}
    if name:
        user_list = api.list_people.find(find_data)
    else:
        user_list = api.list_people.find()
    return render_template('list_user.html', user_list=user_list)

@app.route('/employee')
def employee():
    return render_template("employee.html")

@app.route('/list_project/find_project_by_id', methods=['POST', 'GET'])
@login_required
def find_project_by_id():
    user = g.user
    name_project = request.args.get('find_name_project')
    find_data = {'name': name_project}
    if name_project:
        list_project = api.list_project.find(find_data)
    else:
        list_project = api.list_project.find()

    return render_template('list_project.html',list_project = list_project,user = user)

@app.route('/list_people/find_people_by_id', methods=['POST', 'GET'])
@login_required
def find_people_by_id():
    user = g.user
    name_people = request.args.get('find_name_people')
    find_data = {'name': name_people}
    if name_people:
        data_user = api.list_people.find(find_data)
    else:
        data_user = api.list_people.find()
    return render_template('list_people.html',data_user = data_user,user = user)

@app.route('/list_team/find_team_by_id', methods=['POST', 'GET'])
@login_required
def find_team_by_id():
    user = g.user
    name_team = request.args.get('find_name_team')
    find_data = {'job': name_team}
    if name_team:
        list_team = api.list_team.find(find_data)
    else:
        list_team = api.list_team.find()
    return render_template('list_team.html',list_team = list_team,user = user)

@app.route('/delete_people/<people_id>')
@login_required
def delete_user_by_id(people_id):
    user = g.user
    api.list_people.delete_one({'_id': ObjectId(people_id)})
    return redirect(url_for('list_people'))

@app.route('/delete_team/<team_id>')
@login_required
def delete_team_by_id(team_id):
    user = g.user
    api.list_team.delete_one({'_id': ObjectId(team_id)})
    return redirect(url_for('list_team'))

@app.route('/delete_project/<project_id>')
@login_required
def delete_project_by_id(project_id):
    user = g.user
    api.list_project.delete_one({'_id': ObjectId(project_id)})
    return redirect(url_for('list_project'))

@app.route('/project_card')
@login_required
def project_card():
    user = g.user
    return render_template("project_card.html",user = user)

@app.route('/account',methods = ["POST","GET"])
@login_required
def account():
    user = g.user
    if request.method == "POST":
        current_user_id = user.get('_id')
        name = request.form.get('name')
        nickname = request.form.get('nick_name')
        phone = request.form.get('phone')
        country = request.form.get('country')
        region = request.form.get('region')
        icon = request.form.get('filename')
        icon = str(icon)
        account_item = {"$set": {"name":name,
                                "phone":phone,
                                "country":country,
                                "region":region,
                                "nickname":nickname,
                                "icon": icon
                        }}
        api.account.update_one({'_id': current_user_id},account_item)
        return render_template('account.html',user = user)
    return render_template('account.html',user = user)




@app.route('/to_do_list',methods=["POST","GET"])
@login_required
def to_do_list():
    user = g.user
    todo =  api.todo_list.find()
    if request.method == 'POST':
        title = request.form.get("title")
        description = request.form.get("description")
        completed = request.form.get("completed")
        api.create_todo(title,description,completed)
        return render_template("to_do_list.html",user = user ,todo = todo)
    return render_template("to_do_list.html",user = user ,todo = todo)

@app.route('/setting')
@login_required
def setting():
    user = g.user
    return render_template("setting.html",user = user)

@app.route('/log_out')
@login_required
def log_out():
    g.pop('user', None)
    logout_user()
    return redirect(url_for("home"))

@app.route("/create_todo",methods = ["POST"])
def create_todo():
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

@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status': 404,
        'messege':'Not found' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route("/get_todo",methods = ["GET"])
def get_todo():
    todo = api.todo_list.find()
    resp = dumps(todo)
    return resp

@app.route("/delete_todo/<id>",methods = ["DELETE"])
def delete_todo(id):
    api.todo_list.delete_one({'id':ObjectId(id)})
    resp = jsonify("Delete Todo successfully !")
    resp.status_code = 200 
    return resp

@app.route("/update_todo/<id>",methods = ["PUT"])
def update_todo(id):
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
    else:
        return not_found()
    

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='127.0.0.1', port=5000, debug=True)