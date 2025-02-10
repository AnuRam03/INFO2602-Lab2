import click, sys
from models import db, User, Todo, Category, TodoCategory
from app import app
from sqlalchemy.exc import IntegrityError

#Task 8.3
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.init_app(app)
  db.create_all()
  bob = User('bob', 'bob@mail.com', 'bobpass')
  #bob.todos.append(Todo('Wash Car')) #before the create_todo function
  #new_todo = bob.create_todo("Wash Car") #with the create_todo function
  bob.create_todo("Wash Car")
  db.session.add(bob)
  #db.session.add(new_todo) #can have either or '.add' line as there is a relationship between these two entities
  db.session.commit()
  print(bob)
  #print(new_todo)
  print('database intialized')

#Task 4.1
@app.cli.command("get-user", help="Retrieves a User")
@click.argument('username', default='bob')
def get_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found!')
    return
  print(bob)

#Task 4.2
@app.cli.command('get-users')
def get_users():
  # gets all objects of a model
  users = User.query.all()
  print(users)

#Original create-user command - Updated in Task 6
#@app.cli.command("create-user", help="Creates a new user")
#@click.argument('username')
#@click.argument('email')
#@click.argument('password')
#def create_user(username, email, password):
#  try:
#    new_user = User(username, email, password)
#    db.session.add(new_user)
#    db.session.commit()
#  except IntegrityError:
#    db.session.rollback()
#    print(f'ERROR: Username {username} or Email {email} already exists')
#  else:
#    print(f'User {username} created')

#Task 5
@app.cli.command("change-email")
@click.argument('username', default='bob')
@click.argument('email', default='bob@mail.com')
def change_email(username, email):
  user = User.query.filter_by(username=username).first()
  if not user:
      print(f'{username} not found!')
      return
  user.email = email
  db.session.add(user)
  db.session.commit()
  print(user)

#Task 6
@app.cli.command('create-user')
@click.argument('username', default='rick')
@click.argument('email', default='rick@mail.com')
@click.argument('password', default='rickpass')
def create_user(username, email, password):
  newuser = User(username, email, password) #create user object then add to db
  message = ""
  try:
    db.session.add(newuser)
    db.session.commit()
  except IntegrityError as e:
    #let's the database undo any previous steps of a transaction
    db.session.rollback()
    # print(e.orig) #optionally print the error raised by the database
    message = "Username or email already taken!" #give the user a useful message
  else:
    message = f'User {username} created' # print the newly created user
  finally: #this is new, it will always run
    print(message)

#Task 7
@app.cli.command('delete-user')
@click.argument('username', default='bob')
def delete_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
      print(f'{username} not found!')
      return
  db.session.delete(bob)
  db.session.commit()
  print(f'{username} deleted')

#Task 8.4
@app.cli.command('get-todos')
@click.argument('username', default='bob')
def get_user_todos(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
      print(f'{username} not found!')
      return
  print(bob.todos)

#Task 9.1
@app.cli.command('add-todo')
@click.argument('username', default='bob')
@click.argument('text', default='Clean Room')
def add_task(username, text):
  user = User.query.filter_by(username=username).first()
  if not user:
      print(f'{username} not found!')
      return
  #new_todo = Todo(text)
  #bob.todos.append(new_todo)
  user.create_todo(text)
  #db.session.add(bob)
  db.session.add(user)
  db.session.commit()

#Lab Code
@app.cli.command('get-todos-all')
def get_todos():
  todos = Todo.query.all()
  print(todos)  

#Task 9.2
@click.argument('todo_id', default=1)
@click.argument('username', default='bob')
@app.cli.command('toggle-todo')
def toggle_todo_command(todo_id, username):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} not found!') #make sure the user exists first
    return
  #filter by id and user_id (these are the variable names in the class) to ensure the task we are looking for is under the (current) user / user in question
  todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()
  if not todo:
    print(f'{username} has no todo id {todo_id}')

  todo.toggle()
  print(f'{todo.text} is {"done" if todo.done else "not done"}!')    