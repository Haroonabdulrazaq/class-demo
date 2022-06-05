from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
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
  if request.method == 'POST':
    description = request.form.get('description', '')
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))
  else:
     user = request.args.get('description')
     return render_template('index.html')

@app.route("/")
def index():
    return render_template('index.html', data=Todo.query.all())

