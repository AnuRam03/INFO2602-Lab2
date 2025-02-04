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
  print('database intialized')

@app.cli.command("create-user", help="Creates a new user")
@click.argument('username')
@click.argument('email')
@click.argument('password')
def create_user(username, email, password):
  try:
    new_user = User(username, email, password)
    db.session.add(new_user)
    db.session.commit()
  except IntegrityError:
    db.session.rollback()
    print(f'ERROR: Username {username} or Email {email} already exists')
  else:
    print(f'User {username} created')
