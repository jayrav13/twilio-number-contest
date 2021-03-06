# Import statements.
from flask import Flask, request, redirect
import twilio.twiml
from model import db, Contests, Contestants
import random 
import hashlib
import time

# Set up app.
app = Flask(__name__)

# Custom isint function.
def isint(val):
	try:
		x = int(val)
		return True
	except:
		return False

# Primary route for guesses. 
@app.route("/contests", methods=['POST'])
def contests():

	# Get currently active contest, set up Twilio response.
	contest = Contests.query.filter_by(active=1).first()
	resp = twilio.twiml.Response()

	# Check to make sure contest is returned.
	if contest:

		# Make sure text is a number.
		if isint(request.form['Body']):

			# Set up contestant, add to current contest.
			contestant = Contestants(str(request.form['From']).strip(), int(request.form['Body']))
			contest.contestants.append(contestant)

			# If the guess is correct, winner!
			if int(request.form['Body']) == contest.number:

				# Set winner, deactivate contest, create new contest. Repeat!
				contestant.winner = 1
				contest.active = 0
				contest.token = hashlib.md5(str(time.time())).hexdigest()
				new = Contests(random.random() * 50 + 1)
				db.session.add(new)
				resp.message("Winner winner, chicken dinner!")

			# If the guess is incorrect:
			else:
				# Send a hit with if the number is smaller or bigger.
				hint = ""
				if int(request.form['Body']) > contest.number:
					hint = "smaller"
				else:
					hint = "bigger"

				resp.message("Ah, not quite. Try a " + hint + " number!")

			# Add the contestant to SQLite, not a winner yet.
			db.session.add(contestant)

		# Respond with an error if not a number. Record user w/value -1.
		else:
			contestant = Contestants(str(request.form['From']).strip(), -1)
			contest.contestants.append(contestant)
			resp.message("Ah - I was expecting a number! Try again!")

	# This should never execute, but in case there are no active, handle.
	else:
		resp.message("No contests running - try back in a bit!")

	# Commit everything, respond.
	db.session.commit()
	return str(resp)

# Run.
if __name__ == "__main__":
	app.run(host='0.0.0.0')
