from email.policy import default
from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import sys

from sqlalchemy import false
# from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://haroon:haroon@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     description = db.Column(db.String, nullable=False)
     completed = db.Column(db.String, nullable=False, default=False)

     def __repr__(self):
        return f'<Todo ID: {self.id}, name: {self.description}>'

# db.create_all()


@app.route('/todos/create', methods=['POST', 'GET']) 
def create_todo():
  body ={}
  error = False
  try:
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    body['description']= todo.description
  except:
    error =True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if not error:
      return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST','GET'])
def set_completed_todo(todo_id):
  body={}
  error =False
  try: 
    completed = request.get_json()['completed']
    todo = Todo(completed= completed)
    db.session.add(todo)
    db.session.commit()
    body['completed'] = todo.completed
  except:
    error =True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    return (url_for('index.html'))


@app.route("/")
def index():
    return render_template('index.html', data=Todo.query.all())

