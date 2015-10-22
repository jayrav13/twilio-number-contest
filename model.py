# Imports
# flask
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.script import Manager
#from flask.ext.migrate import Migrate, MigrateCommand

# sqlalchemy
from sqlalchemy import Integer, ForeignKey, String, Column, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

# other
import time
import hashlib

# set up app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///contests.db" 

# set up database
db = SQLAlchemy(app)

# set up migration
#migrate = Migrate(app, db)
#manager = Manager(app)
#manager.add_command('contests', MigrateCommand)

class Contests(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	active = db.Column(db.Integer)
	number = db.Column(db.Integer)
	token = db.Column(db.String)
	contestants = relationship("Contestants", backref="contests", primaryjoin=("Contests.id==Contestants.contest"))

	def __init__(self, number):
		self.active = 1
		self.number = int(number)
		self.token = None

class Contestants(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	contest = db.Column(db.Integer, ForeignKey('contests.id'))
	number = db.Column(db.String)
	guess = db.Column(db.Integer)
	winner = db.Column(db.Integer)

	def __init__(self, number, guess):
		self.number = number
		self.guess = guess
		self.winner = 0

if __name__ == "__main__":
	manager.run()
