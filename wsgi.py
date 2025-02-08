import click, sys
from models import db, User
from app import app
from sqlalchemy.exc import IntegrityError


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.init_app(app)
  db.create_all()
  bob = User('bob', 'bob@mail.com', 'bobpass')
  print(bob)
  db.session.add(bob)
  db.session.commit()
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