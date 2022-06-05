from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import sys
# from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://haroon:haroon@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# migrate = Migrate(db, app)


class Todo(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     description = db.Column(db.String, nullable=False)

     def __repr__(self):
        return f'<Todo ID: {self.id}, name: {self.description}>'

db.create_all()


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


@app.route("/")
def index():
    return render_template('index.html', data=Todo.query.all())

