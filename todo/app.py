from email.policy import default
from flask import Flask, jsonify, render_template, request, url_for, redirect, abort
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



class TodoList(db.Model):
  __tablename__ = 'todolist'
  id= db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  todo = db.relationship('Todo', backref='list', lazy=True)

def __repr__(self):
    return f'<TodoList {self.id} {self.name}>'


class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String, nullable=False)
  completed = db.Column(db.String, nullable=False, default=False)
  list_id = db.Column(db.Integer, db.ForeignKey('todolist.id'), nullable= False)

  def __repr__(self):
    return f'<Todo ID: {self.id}, name: {self.description}>'


# db.create_all()

@app.route('/todos/<todo_id>/delete', methods=['DELETE'])
def delete_todo(todo_id):
  error=False
  try:
    print('Todo ID', todo_id)
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
  except:
    error =True
    db.session.rollback()
    print(sys.exc_info())
  finally: 
    db.session.close()
    return jsonify({ 'success': True })

@app.route('/todos/<todo_id>/set-completed', methods=['POST','GET'])
def set_completed_todo(todo_id):
  error =False
  try: 
    completed = request.get_json()['completed']
    print('completed', completed)
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
  except:
    error =True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    return (url_for('index'))



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


@app.route("/lists/<list_id>")
def  get_list_todos(list_id):
    return render_template('index.html',
    lists = TodoList.query.all(),
    active_list = TodoList.query.get(list_id),
    data=Todo.query.filter_by(list_id=list_id).order_by('id').all())


@app.route("/")
def  index():
    return redirect(url_for('get_list_todos', list_id=1))

@app.route('/lists/create', methods=['POST'])
def create_list():
    error = False
    body = {}
    try:
      name = request.get_json()['name']
      print('Goaning I am here', name)
      todolist = TodoList(name=name)
      db.session.add(todolist)
      db.session.commit()
      body['id'] = todolist.id
      body['name'] = todolist.name
      print('I am here', body)
    except:
      db.session.rollback()
      error = True
      print(sys.exc_info)
    finally:
      db.session.close()
    if error:
      abort(500)
    else:
      return jsonify(body)

@app.route('/lists/<list_id>/delete', methods=['DELETE'])
def delete_list(list_id):
    error = False
    try:
      list = TodoList.query.get(list_id)
      for todo in list.todos:
        db.session.delete(todo)

      db.session.delete(list)
      db.session.commit()
    except:
      db.session.rollback()
      error = True
    finally:
        db.session.close()
    if error:
      abort(500)
    else:
      return jsonify({'success': True})


@app.route('/lists/<list_id>/set-completed', methods=['POST'])
def set_completed_list(list_id):
  error = False

  try:
    list = TodoList.query.get(list_id)

    for todo in list.todos:
        todo.completed = True

    db.session.commit()
  except:
    db.session.rollback()

    error = True
  finally:
        db.session.close()

  if error:
    abort(500)
  else:
    return '', 200
