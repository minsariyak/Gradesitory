import stripe
import smtplib, ssl
from flask import Flask, redirect, request, render_template, session
from cs50 import SQL
from functools import wraps
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

db = SQL("sqlite:///gpa.db")

#calculate gpa
def calculate_gpa(scale, gpaType):
	#calculate cummulative gpa for 9 point scale
	if scale == 9 and gpaType == 'cgpa':
		#get course credits
		credits = db.execute("SELECT courseCredit FROM gpa WHERE user_id = :id", id=session["user_id"])

		#get total credits
		totalCredits = 0
		for i in range(len(credits)):
			totalCredits += credits[i]["courseCredit"]

		#get grade points
		points = {
		"A+": 9,
		"A": 8,
		"B+": 7,
		"B": 6,
		"C+": 5,
		"C": 4,
		"D+": 3,
		"D": 2,
		"E": 1,
		"F": 0
		}

		#get course grades
		grades = db.execute("SELECT courseGrade FROM gpa WHERE user_id = :id", id=session["user_id"])

		#multiply points by credits and store in accumulating variable
		cumGpa = 0

		for x in range(len(credits)):
			i = grades[x]["courseGrade"]
			totalPoints = credits[x]["courseCredit"] * points[i]
			cumGpa += totalPoints

		#if no courses exist, gpa = 0, else return calculated gpa.
		if totalCredits == 0:
			overallGpa = 0
			return overallGpa
		else:
			overallGpa = cumGpa/totalCredits
			return overallGpa

	#Calculate major gpa for 9 point scale
	elif scale == 9 and gpaType == 'mgpa':
		#get course credits
		credits = db.execute("SELECT courseCredit FROM gpa WHERE user_id = :id AND category = :category", id=session["user_id"], category='Major')

		#get total credits
		totalCredits = 0
		for i in range(len(credits)):
			totalCredits += credits[i]["courseCredit"]

		#get grade points
		points = {
		"A+": 9,
		"A": 8,
		"B+": 7,
		"B": 6,
		"C+": 5,
		"C": 4,
		"D+": 3,
		"D": 2,
		"E": 1,
		"F": 0
		}

		#get course grades
		grades = db.execute("SELECT courseGrade FROM gpa WHERE user_id = :id AND category = :category", id=session["user_id"], category='Major')

		#multiply points by credits and store in accumulating variable
		cumGpa = 0

		for x in range(len(credits)):
			i = grades[x]["courseGrade"]
			totalPoints = credits[x]["courseCredit"] * points[i]
			cumGpa += totalPoints

		#if no courses exist, gpa = 0, else return calculated gpa.
		if totalCredits == 0:
			overallGpa = 0
			return overallGpa
		else:
			overallGpa = cumGpa/totalCredits
			return overallGpa

	#Calculate non major gpa for 9 point scale
	elif scale == 9 and gpaType == 'nmgpa':
		#get course credits
		credits = db.execute("SELECT courseCredit FROM gpa WHERE user_id = :id AND category = :category", id=session["user_id"], category='Non-Major')

		#get total credits
		totalCredits = 0
		for i in range(len(credits)):
			totalCredits += credits[i]["courseCredit"]

		#get grade points
		points = {
		"A+": 9,
		"A": 8,
		"B+": 7,
		"B": 6,
		"C+": 5,
		"C": 4,
		"D+": 3,
		"D": 2,
		"E": 1,
		"F": 0
		}

		#get course grades
		grades = db.execute("SELECT courseGrade FROM gpa WHERE user_id = :id AND category = :category", id=session["user_id"], category='Non-Major')

		#multiply points by credits and store in accumulating variable
		cumGpa = 0

		for x in range(len(credits)):
			i = grades[x]["courseGrade"]
			totalPoints = credits[x]["courseCredit"] * points[i]
			cumGpa += totalPoints

		#if no courses exist, gpa = 0, else return calculated gpa.
		if totalCredits == 0:
			overallGpa = 0
			return overallGpa
		else:
			overallGpa = cumGpa/totalCredits
			return overallGpa

	#calculate cummulative gpa for 4 point scale
	elif scale == 4 and gpaType == 'cgpa':
		#get course credits
		credits = db.execute("SELECT courseCredit FROM gpa WHERE user_id = :id", id=session["user_id"])

		#get total credits
		totalCredits = 0
		for i in range(len(credits)):
			totalCredits += credits[i]["courseCredit"]

		#get grade points
		points = {
		"A+": 4,
		"A": 4,
		"A-": 3.7,
		"B+": 3.3,
		"B": 3,
		"B-": 2.7,
		"C+": 2.3,
		"C": 2,
		"C-": 1.7,
		"D+": 1.3,
		"D": 1,
		"D-": 0.7,
		"F": 0
		}

		#get course grades
		grades = db.execute("SELECT courseGrade FROM gpa WHERE user_id = :id", id=session["user_id"])

		#multiply points by credits and store in accumulating variable
		cumGpa = 0

		for x in range(len(credits)):
			i = grades[x]["courseGrade"]
			totalPoints = credits[x]["courseCredit"] * points[i]
			cumGpa += totalPoints

		#if no courses exist, gpa = 0, else return calculated gpa.
		if totalCredits == 0:
			overallGpa = 0
			return overallGpa
		else:
			overallGpa = cumGpa/totalCredits
			return overallGpa

	#Calculate major gpa for 4 point scale
	elif scale == 4 and gpaType == 'mgpa':
		#get course credits
		credits = db.execute("SELECT courseCredit FROM gpa WHERE user_id = :id AND category = :category", id=session["user_id"], category='Major')

		#get total credits
		totalCredits = 0
		for i in range(len(credits)):
			totalCredits += credits[i]["courseCredit"]

		#get grade points
		points = {
		"A+": 4,
		"A": 4,
		"A-": 3.7,
		"B+": 3.3,
		"B": 3,
		"B-": 2.7,
		"C+": 2.3,
		"C": 2,
		"C-": 1.7,
		"D+": 1.3,
		"D": 1,
		"D-": 0.7,
		"F": 0
		}

		#get course grades
		grades = db.execute("SELECT courseGrade FROM gpa WHERE user_id = :id AND category = :category", id=session["user_id"], category='Major')

		#multiply points by credits and store in accumulating variable
		cumGpa = 0

		for x in range(len(credits)):
			i = grades[x]["courseGrade"]
			totalPoints = credits[x]["courseCredit"] * points[i]
			cumGpa += totalPoints

		#if no courses exist, gpa = 0, else return calculated gpa.
		if totalCredits == 0:
			overallGpa = 0
			return overallGpa
		else:
			overallGpa = cumGpa/totalCredits
			return overallGpa

	#Calculate non major gpa for 4 point scale
	elif scale == 4 and gpaType == 'nmgpa':
		#get course credits
		credits = db.execute("SELECT courseCredit FROM gpa WHERE user_id = :id AND category = :category", id=session["user_id"], category='Non-Major')

		#get total credits
		totalCredits = 0
		for i in range(len(credits)):
			totalCredits += credits[i]["courseCredit"]

		#get grade points
		points = {
		"A+": 4,
		"A": 4,
		"A-": 3.7,
		"B+": 3.3,
		"B": 3,
		"B-": 2.7,
		"C+": 2.3,
		"C": 2,
		"C-": 1.7,
		"D+": 1.3,
		"D": 1,
		"D-": 0.7,
		"F": 0
		}

		#get course grades
		grades = db.execute("SELECT courseGrade FROM gpa WHERE user_id = :id AND category = :category", id=session["user_id"], category='Non-Major')

		#multiply points by credits and store in accumulating variable
		cumGpa = 0

		for x in range(len(credits)):
			i = grades[x]["courseGrade"]
			totalPoints = credits[x]["courseCredit"] * points[i]
			cumGpa += totalPoints

		#if no courses exist, gpa = 0, else return calculated gpa.
		if totalCredits == 0:
			overallGpa = 0
			return overallGpa
		else:
			overallGpa = cumGpa/totalCredits
			return overallGpa

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if session.get("user_id") is None:
			return redirect("/login")
		return f(*args, **kwargs)
	return decorated_function

def subscription_check(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		sub_id = db.execute("SELECT sub_id FROM users WHERE id = :id", id=session["user_id"])
		subscription = stripe.Subscription.retrieve(sub_id[0]['sub_id'])

		if subscription['status'] != "active" and subscription['status'] != "trialing":
			return render_template("register.html", message="Your subscription is not active")
		return f(*args, **kwargs)
	return decorated_function

#function that adds users to stripe dashboard to process payments
def create_stripe_details(user_name,user_email, number, exp_month, exp_year, cvc):

	#create a payment method for the new user
	payment = stripe.PaymentMethod.create(
		type="card",
		card={
			"number": number,
			"exp_month": exp_month,
			"exp_year": exp_year,
			"cvc": cvc
		}
	)

	#create a new user object
	new_user = stripe.Customer.create(
		name=user_name,
		email=user_email,
	)

	#attach payment method to user object
	stripe.PaymentMethod.attach(payment['id'], customer=new_user['id'])

	#create subscription and charge user
	subscription = stripe.Subscription.create(
		customer=new_user['id'],
		items=[{"price": "price_1KCpqNH1uNVbbRvANiT61gpY"}],
		default_payment_method= payment['id'],
	)

	return payment['id'], subscription['id'], new_user['id']

def update_payment(pm_id, cus_id, update_number, update_exp_month, update_exp_year, update_cvc):

	updated_card = stripe.PaymentMethod.create(
		type="card",
		card={
			"number": update_number,
			"exp_month": update_exp_month,
			"exp_year": update_exp_year,
			"cvc": update_cvc
		}
	)

	stripe.PaymentMethod.detach(pm_id)

	stripe.PaymentMethod.attach(updated_card['id'], customer=cus_id)

	return updated_card['id']

def cancel_subscription(sub_id):
	stripe.Subscription.delete(sub_id)

def settings_data():
	#get the current user's stripe IDs from users DB
	user_IDs = db.execute("SELECT cus_id, pm_id, sub_id FROM users WHERE id = :id", id=session['user_id'])

	#using the cus_id from above, get all the PaymentIntents for that user
	transaction = stripe.PaymentIntent.list(customer=user_IDs[0]['cus_id'])

	#create an Intent object which stores formatted amount and date of each PaymentIntent
	class Intent:
		def __init__(self, amount, date):
			self.amount = amount
			self.date = date

	#the history array stores all the formatted PaymentIntents and it's passed on when template is rendered
	history = []

	#the loop that formats the PaymentIntents. Convert cents to dollars and Unix timestamp to actual datetime
	for payment in transaction:
		amount = payment['amount']/100
		date = datetime.fromtimestamp(payment['created'])
		p = Intent(amount, date)
		history.append(p)

	#get the user's current PaymentMethod on file
	current_card = stripe.PaymentMethod.retrieve(user_IDs[0]['pm_id'])

	#get the user's current sub_id to get next payment date
	subscription = stripe.Subscription.retrieve(user_IDs[0]['sub_id'])

	#convert timestamp tp date
	next_billing_date = datetime.fromtimestamp(subscription['current_period_end'])

	#get the user's details from DB to show on settings page
	user = db.execute("SELECT username, email, gpa_scale FROM users WHERE id = :id", id=session['user_id'])

	return user, history, current_card, next_billing_date

def send_verification_email(receiver, digest, username):
	sender_email = "myprojects2512@gmail.com"
	receiver_email = receiver
	password = "HelloWorld"

	message = MIMEMultipart("alternative")
	message["Subject"] = "Gradesitory | Email Verification"
	message["From"] = sender_email
	message["To"] = receiver_email

	text = """\
	Hello """ + username + """, your email verification code is """ + digest + """."""
	html = """\
	<!DOCTYPE html>
	<html>
		<body style="margin: 0; padding: 0;">
		<script src="https://kit.fontawesome.com/e7ff852a3e.js" crossorigin="anonymous"></script>
			<div style="background-color: white; margin: 0; padding: 5%; text-align: center; height: 100%;">
				<img src="cid:image1" style="width: 10%;">
				<div style="background-color: #F0F8FF; text-align: center; width: 50%; margin: auto; padding: 3%; border-radius: 10px;">
					<h1>Hello, """ + username + """</h1>
					<p>Your email verification code is as below:
					<span style="font-weight: bold; display: block; margin-top: 5%;">""" + digest + """</span></p>
				</div>
				<h5 style="margin-top: 1%;"><a href="https://www.gradesitory.com/terms_of_service">Terms of Use</a> | <a href="https://www.gradesitory.com/privacy_policy">Privacy Policy</a> | <a href="https://www.gradesitory.com/contact">Contact</a></h5>
				<p><i class="far fa-copyright" style="font-size: 80%;"></i> 2021 Gradesitory. All rights reserved.</p>
			</div>
		</body>
	</html>
	"""
	part1 = MIMEText(text, "plain")
	part2 = MIMEText(html, "html")

	message.attach(part1)
	message.attach(part2)

	img = open('static/img/logo.png', 'rb')
	msgImage = MIMEImage(img.read())
	img.close()

	msgImage.add_header('Content-ID', '<image1>')
	message.attach(msgImage)

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
	    server.login(sender_email, password)
	    server.sendmail(
	        sender_email, receiver_email, message.as_string()
	    )

def send_recovery_email(receiver, digest, username):
	sender_email = "myprojects2512@gmail.com"
	receiver_email = receiver
	password = "HelloWorld"

	message = MIMEMultipart("alternative")
	message["Subject"] = "Gradesitory | Password Recovery"
	message["From"] = sender_email
	message["To"] = receiver_email

	text = """\
	Hello """ + username + """, your password recovery code is """ + digest + """."""
	html = """\
	<!DOCTYPE html>
	<html>
		<body style="margin: 0; padding: 0;">
			<div style="background-color: white; margin: 0; padding: 5%; text-align: center; height: 100%;">
				<img src="cid:image1" style="width: 10%;">
				<div style="background-color: #F0F8FF; text-align: center; width: 50%; margin: auto; padding: 3%; border-radius: 10px;">
					<h1>Hello, """ + username + """</h1>
					<p>Your password recovery code is as below:
					<span style="font-weight: bold; display: block; margin-top: 5%;">""" + digest + """</span></p>
				</div>
				<h5 style="margin-top: 1%;"><a href="https://www.gradesitory.com/terms_of_service">Terms of Use</a> | <a href="https://www.gradesitory.com/privacy_policy">Privacy Policy</a> | <a href="https://www.gradesitory.com/contact">Contact</a></h5>
				<p><i class="far fa-copyright" style="font-size: 80%;"></i> 2021 Gradesitory. All rights reserved.</p>
			</div>
		</body>
	</html>
	"""
	part1 = MIMEText(text, "plain")
	part2 = MIMEText(html, "html")

	message.attach(part1)
	message.attach(part2)

	img = open('static/img/logo.png', 'rb')
	msgImage = MIMEImage(img.read())
	img.close()

	msgImage.add_header('Content-ID', '<image1>')
	message.attach(msgImage)

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
	    server.login(sender_email, password)
	    server.sendmail(
	        sender_email, receiver_email, message.as_string()
	    )

def send_contact_email(name, email, message):
	sender_email = "myprojects2512@gmail.com"
	password = "HelloWorld"
	user_name = name
	user_email = email
	user_message = message

	message = MIMEMultipart("alternative")
	message["Subject"] = "Gradesitory | Contact"
	message["From"] = user_email
	message["To"] = sender_email

	text = """\
	\nName: """ + user_name + """\nEmail: """ + user_email + """\nMessage: """ + user_message

	part1 = MIMEText(text, "plain")
	message.attach(part1)

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
	    server.login(sender_email, password)
	    server.sendmail(sender_email, sender_email, message.as_string())


