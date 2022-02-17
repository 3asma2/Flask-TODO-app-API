from flask import Flask,request,jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

DATABASE_URI = 'sqlite:///todoapp.db'
# DATABASE_URI = 'postgres://postgres:asmaa@localhost:5432/flaskapp'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Task("{self.title}")'

@app.route('/',methods=['GET'])
def getall():
    todoapp = Task.query.all()
    result =[]
    for task in todoapp :
        dict= {}
        dict["id"] = task.id
        dict["title"] = task.title
        dict["created_at"] = task.created_at
        result.append(dict)
    return jsonify({
        'data':result
    })

@app.route('/add',methods=['GET','POST'])
def addnew():
    data = json.loads(request.data)
    todotittle = data['title']
    addnew = Task(
        title = todotittle,
    )
    db.session.add(addnew)
    db.session.commit()
    return jsonify({
        'data':f'{todotittle} is done'
    })

@app.route('/todo/<int:id>',methods=['PUT', 'GET', 'DELETE'])
def mod_task(id):
    todo = Task.query.filter_by(id=id).first()
    if request.method == 'GET':
        dict = {}
        dict['id'] = todo.id
        dict['title'] = todo.title

        return jsonify({
            "data": dict
        })
    if request.method == 'PUT':
        data = json.loads(request.data)
        todo.title = data['title']

        db.session.commit()
        return jsonify({
            'data':'updating is done'
        })
    if request.method == 'DELETE':
        db.session.delete(todo)
        db.session.commit()

        return jsonify({
            "data": "deleting is done"
        })


db.create_all()
app.run(host='127.0.0.1',port=5000,debug=True)