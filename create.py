from model import db, Contests
import random

all = Contests.query.filter_by(active=1)

for elem in all:
	elem.active = 0

contest = Contests(random.random() * 1000)
db.session.add(contest)
db.session.commit()
