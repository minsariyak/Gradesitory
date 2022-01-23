import os
import sys
import stripe
import secrets
import smtplib
from cs50 import SQL
from flask import Flask, flash, redirect, request, render_template, session, url_for
from helpers import login_required, create_stripe_details, update_payment, cancel_subscription, subscription_check, calculate_gpa, settings_data, send_verification_email, send_recovery_email, send_contact_email
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from email.message import EmailMessage
from datetime import datetime

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# connecting the database
db = SQL("sqlite:///gpa.db")

# connecting the Stripe API. It is needed to communicate with Stripe's server. 
stripe.api_key = "sk_test_51HwhjjH1uNVbbRvAjk38Cnd305CYmkG4WbNlHM4GhPgzHvK7U63VZlzlMQKdS1BissIqyClAbi0cwg1NMwudb5w400NGIJBbBi"

@app.route("/")
def index():
	return render_template("landing.html")

@app.route("/grading_systems")
def grading_systems():
	return render_template("grading_systems.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
	if request.method == 'GET':
		return render_template("contact.html")
	else:
		name = request.form.get("name")
		email = request.form.get("email")
		message = request.form.get("message")

		send_contact_email(name, email, message)
		msg = "Thank you for contacting us. We'll respond as soon as possible."

		return render_template("contact.html", msg=msg)

@app.route("/terms_of_service")
def termsOfService():
	return render_template("terms_of_service.html")

@app.route("/privacy_policy")
def privacyPolicy():
	return render_template("privacy_policy.html")

@app.route("/gpa")
@login_required
@subscription_check
def gpa_home():
	user = db.execute("SELECT username, gpa_scale, verified FROM users WHERE id = :id", id=session["user_id"])
	all_courses = db.execute("SELECT * FROM gpa WHERE user_id = :id ORDER BY courseName ASC", id=session["user_id"])
	major_courses = db.execute("SELECT * FROM gpa WHERE user_id = :id AND category = :category ORDER BY courseName ASC", id=session["user_id"], category='Major')
	non_major_courses = db.execute("SELECT * FROM gpa WHERE user_id = :id AND category = :category ORDER BY courseName ASC", id=session["user_id"], category='Non-Major')
	if user[0]['gpa_scale'] == 9:
		cgpa = round(calculate_gpa(9, 'cgpa'), 2)
		mgpa = round(calculate_gpa(9, 'mgpa'), 2)
		nmgpa = round(calculate_gpa(9, 'nmgpa'), 2)

		return render_template("home9.html", all_courses=all_courses, major_courses=major_courses, non_major_courses=non_major_courses, cgpa=cgpa, mgpa=mgpa, nmgpa=nmgpa, user=user)
	else:
		cgpa = round(calculate_gpa(4, 'cgpa'), 2)
		mgpa = round(calculate_gpa(4, 'mgpa'), 2)
		nmgpa = round(calculate_gpa(4, 'nmgpa'), 2)

		return render_template("home4.html", all_courses=all_courses, major_courses=major_courses, non_major_courses=non_major_courses, cgpa=cgpa, mgpa=mgpa, nmgpa=nmgpa, user=user)

@app.route("/addCourse")
@login_required
@subscription_check
def addCourse():
	#get form elements
	courseName = request.args.get("courseName")
	try:
		courseCredit = float(request.args.get("credit"))
	except Exception:
		flash('Error! Invalid course credits')
		return redirect("/gpa")
	courseGrade = request.args.get("grades")
	category = request.args.get("category")

	#add to database
	db.execute("INSERT INTO gpa (user_id, courseName, courseCredit, courseGrade, category) VALUES (:id, :courseName, :courseCredit, :courseGrade, :category)", id=session["user_id"], courseName=courseName, courseCredit=courseCredit, courseGrade=courseGrade, category=category)
	flash(f"{courseName} added successfully!")
	return redirect("/gpa")

@app.route("/editCourse", methods=["POST"])
@login_required
@subscription_check
def submitEdit():
	id = request.form.get("courseID")
	courseName = request.form.get("courseName")
	try:
		courseCredit = float(request.form.get("credit"))
	except Exception as e:
		flash('Error! Invalid course credits')
		return redirect("/gpa")
	courseGrade = request.form.get("grades")
	category = request.form.get("category")
	db.execute("UPDATE gpa SET courseName=:courseName, courseCredit=:courseCredit, courseGrade=:courseGrade, category=:category WHERE id=:id", courseName=courseName, courseCredit=courseCredit, courseGrade=courseGrade, category=category, id=id)
	flash(f"{courseName} edited successfully")

	return redirect("/gpa")

@app.route("/deleteCourse", methods=["POST"])
@login_required
@subscription_check
def deleteCourse():
	id = request.args.get("id")
	name = request.args.get("name")

	db.execute("DELETE FROM gpa WHERE id=:id", id=id)
	flash(f"{name} deleted successfully!")

	return redirect("/gpa")

@app.route("/login", methods=["GET", "POST"])
def login():
	session.clear()

	if request.method == "POST":
		if not request.form.get("username"):
			message = "Username/password can't be empty"
			return render_template("login.html", message=message)
		elif not request.form.get("password"):
			message = "Username/password can't be empty"
			return render_template("login.html", message=message)

		rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

		if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
			message = "Invalid username and/or password"
			return render_template("login.html", message=message)

		session["user_id"] = rows[0]["id"]
		return redirect("/gpa")
	else:
		return render_template("login.html")

@app.route("/logout")
def logout():
	session.clear()
	return redirect("/login")


@app.route("/register", methods=["GET","POST"])
def register():
	if request.method == 'GET':
		return render_template("register.html")
	else:
		name = request.form.get("name")
		email = request.form.get("email")
		username = request.form.get("username")
		password = request.form.get("password")
		confirmation = request.form.get("confirmation")
		gpa_scale = int(request.form.get("gpa_scale"))
		number = request.form.get("number")
		exp_month = int(request.form.get("exp_month"))
		exp_year = int(request.form.get("exp_year"))
		cvc = request.form.get("cvc")

		existing_users = db.execute("SELECT username FROM users")
		for i in range(len(existing_users)):
			if username == existing_users[i]['username']:
				message = "Username taken, please choose another one"
				return render_template("register.html", message=message, name=name, email=email, username=username, password=password, gpa_scale=gpa_scale, number=number, exp_month=exp_month, exp_year=exp_year, cvc=cvc)

		hash = generate_password_hash(password)

		try:
			stripe_ids = create_stripe_details(name, email, number, exp_month, exp_year, cvc)
		except stripe.error.CardError as e:
			return render_template("register.html", route="card_error", message=e.user_message, name=name, email=email, username=username, password=password, gpa_scale=gpa_scale, number=number, exp_month=exp_month, exp_year=exp_year, cvc=cvc)

		db.execute("INSERT INTO users (username, hash, pm_id, sub_id, cus_id, gpa_scale, email, verified) VALUES (:username, :hash, :pm_id, :sub_id, :cus_id, :gpa_scale, :email, :verified)", username=username, hash=hash, pm_id=stripe_ids[0], sub_id=stripe_ids[1], cus_id=stripe_ids[2], gpa_scale=gpa_scale, email=email, verified=0)

		#start session for this new user to skip logging in
		new_user = db.execute("SELECT * FROM users WHERE id = last_insert_rowid()")
		session["user_id"] = new_user[0]["id"]

		#add metadata to registered user
		stripe.Customer.modify(new_user[0]['cus_id'], metadata={"user_id": new_user[0]['id']})

		return redirect("/gpa")

@app.route("/settings")
@login_required
@subscription_check
def settings():
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

	#convert timestamp to date
	next_billing_date = datetime.fromtimestamp(subscription['current_period_end'])

	#get the user's details from DB to show on settings page
	user = db.execute("SELECT username, email, gpa_scale FROM users WHERE id = :id", id=session['user_id'])

	return render_template("settings.html", user=user, history=history, current_card=current_card, next_billing_date=next_billing_date)

@app.route("/subscription_settings_payment_update", methods=["GET","POST"])
@login_required
@subscription_check
def subscription_settings_payment_update():
	if request.method == 'POST':
		#get settings data
		settings = settings_data()

		card_number = request.form.get("card_number")
		card_exp_month = int(request.form.get("card_exp_month"))
		card_exp_year = int(request.form.get("card_exp_year"))
		card_cvc = request.form.get("card_cvc")

		current_user = db.execute("SELECT * FROM users WHERE id = :id", id=session['user_id'])
		pm_id = current_user[0]['pm_id']
		cus_id = current_user[0]['cus_id']

		#update card in stripe
		try:
			new_pm_id = update_payment(pm_id, cus_id, card_number, card_exp_month, card_exp_year, card_cvc)
		except stripe.error.CardError as e:
			return render_template("settings.html", view="subscription", error_msg=e.user_message, user=settings[0], history=settings[1], current_card=settings[2], next_billing_date=settings[3])

		#save new pm_id to database
		db.execute("UPDATE users SET pm_id = :pm_id WHERE id = :id", pm_id=new_pm_id, id=session['user_id'])

		card_message = "Payment card successfully updated!"

		return render_template("settings.html", view="subscription", card_message=card_message, user=settings[0], history=settings[1], current_card=settings[2], next_billing_date=settings[3])

@app.route("/subscription_settings_cancel")
@login_required
@subscription_check
def subscription_settings_cancel():

	#stop the subcription cycle on stripe
	current_user = db.execute("SELECT sub_id FROM users WHERE id = :id", id=session['user_id'])
	sub_id = current_user[0]['sub_id']
	cancel_subscription(sub_id)

	#delete user's courses from 'gpa' table in database
	db.execute("DELETE FROM gpa WHERE user_id = :id", id=session['user_id'])
	#delete user's details from 'users' table in databse
	db.execute("DELETE FROM users WHERE id = :id", id=session['user_id'])

	#log user out
	session.clear()

	return render_template("login.html", deactivation_msg="Your account was successfully deactivated.")

@app.route("/change_password", methods=["POST"])
@login_required
@subscription_check
def change_password():
	#get settings data
	settings = settings_data()

	current_password = request.form.get("current_password")
	new_password = request.form.get("new_password")
	confirm_new_password = request.form.get("confirm_new_password")

	if new_password != confirm_new_password:
		password_error = "Passwords do not match"
		return render_template("settings.html", password_error=password_error, view="profile",  user=settings[0], history=settings[1], current_card=settings[2], next_billing_date=settings[3])

	current_user = db.execute("SELECT * FROM users WHERE id = :id", id=session['user_id'])
	if not check_password_hash(current_user[0]['hash'], current_password):
		password_error = "Incorrect current password"
		return render_template("settings.html", password_error=password_error, view="profile",  user=settings[0], history=settings[1], current_card=settings[2], next_billing_date=settings[3])

	hash = generate_password_hash(new_password)
	db.execute("UPDATE users SET hash = :hash WHERE id = :id", hash=hash, id=session['user_id'])
	password_message = "Password updated successfully"

	return render_template("settings.html", view="profile", password_message=password_message, user=settings[0], history=settings[1], current_card=settings[2], next_billing_date=settings[3])

@app.route("/verify_email", methods=["GET","POST"])
@login_required
@subscription_check
def verify_email():
	if request.method == 'GET':
		user = db.execute("SELECT email, username FROM users WHERE id = :id", id=session['user_id'])

		#generate random code
		digest = secrets.token_hex(3)

		#check if code already exists for user in DB
		check_value = db.execute("SELECT * FROM verify WHERE email = :email", email=user[0]['email'])

		#save email and code to 'verify' DB if it is the first time else update existing value
		if not check_value:
			db.execute("INSERT INTO verify (email, digest) VALUES (:email, :digest)", email=user[0]['email'], digest=digest)
		else:
			db.execute("UPDATE verify SET digest = :digest WHERE email = :email", digest=digest, email=user[0]['email'])

		send_verification_email(user[0]['email'], digest, user[0]['username'])

		return render_template("verify.html")
	else:
		verification_code = request.form.get("verification_code")

		user = db.execute("SELECT email, gpa_scale from users WHERE id = :id", id=session['user_id'])
		digest = db.execute("SELECT digest FROM verify WHERE email = :email", email=user[0]['email'])

		if secrets.compare_digest(verification_code, digest[0]['digest']) != True:
			return render_template("verify.html", msg = 'Incorrect code')

		db.execute("UPDATE users SET verified = :true WHERE id = :id", true=1, id=session['user_id'])
		db.execute("DELETE FROM verify WHERE email = :email", email=user[0]['email'])

		return render_template("verify.html", msg = "Email verified successfully. Redirecting to home page...", timeout = True)

@app.route("/resend_email_code", methods=["POST"])
@login_required
@subscription_check
def resend_email_code():
	user = db.execute("SELECT email FROM users WHERE id = :id", id=session['user_id'])

	#generate random code
	digest = secrets.token_hex(3)

	#check if code already exists for user in DB
	check_value = db.execute("SELECT * FROM verify WHERE email = :email", email=user[0]['email'])

	#save email and code to 'verify' DB if it is the first time else update existing value
	if not check_value:
		db.execute("INSERT INTO verify (email, digest) VALUES (:email, :digest)", email=user[0]['email'], digest=digest)
	else:
		db.execute("UPDATE verify SET digest = :digest WHERE email = :email", digest=digest, email=user[0]['email'])

	send_verification_email(user[0]['email'], digest, user[0]['username'])

	return render_template("verify.html", msg="Code was resent")

@app.route("/change_email", methods=["POST"])
@login_required
@subscription_check
def change_email():

	#get settings data
	settings = settings_data()

	current_password = request.form.get("current_password")
	current_email = request.form.get("current_email")
	new_email = request.form.get("new_email")

	current_user = db.execute("SELECT * FROM users WHERE id = :id", id=session['user_id'])
	if not check_password_hash(current_user[0]['hash'], current_password):
		email_error = "Incorrect current password"
		return render_template("settings.html", view="profile", email_error=email_error, user=settings[0], history=settings[1], current_card=settings[2], next_billing_date=settings[3])

	if current_email != current_user[0]['email']:
		email_error = "Incorrect current email"
		return render_template("settings.html", view="profile", email_error=email_error, user=settings[0], history=settings[1], current_card=settings[2], next_billing_date=settings[3])

	db.execute("UPDATE users SET email = :email, verified = :verified WHERE id = :id", email=new_email, verified=0, id=session["user_id"])

	return render_template("settings.html", view="profile", email_message="Email changed successfully", user=settings[0], history=settings[1], current_card=settings[2], next_billing_date=settings[3])

@app.route("/forgot_password", methods=["GET","POST"])
def forgot_password():
	if request.method == "GET":
		return render_template("password.html", status=False) #when status is false, only the form to enter username is displayed
	else:
		#retrieve username from form
		username = request.form.get("username")

		#Validate Data
		if not username:
			error = "Please enter your username"
			return render_template("password.html", status=False, error=error)
		uName = db.execute("SELECT username FROM users WHERE username = :username", username=username)
		if not uName:
			error = "Username not found"
			return render_template("password.html", status=False, error=error)

		#get email from DB based on username
		email = db.execute("SELECT email, verified FROM users WHERE username = :username", username=username)
		if email[0]['verified'] == 0:
			error = "Your email isn't verified"
			return render_template("password.html", status=False, error=error)

		#generate random code
		digest = secrets.token_hex(3)

		#Check if value exists for that username
		check_value = db.execute("SELECT digest FROM reset WHERE username = :username", username=username)

		#save username and code to 'reset' table if no value exists there, else replace it with existing value.
		if not check_value:
			db.execute("INSERT INTO reset (username, digest) VALUES (:username, :digest)", username=username, digest=digest)
		else:
			db.execute("UPDATE reset SET digest = :digest WHERE username = :username", digest=digest, username=username)

		send_recovery_email(email[0]['email'], digest, username)

		#when status is true, the form to accept the reset-code emailed is displayed
		#username retrieved from form is passed on to use it in the route below

		return render_template("password.html", status=True, username=username, msg="Please check your email for the reset code")

@app.route("/resend_password_code", methods=["POST"])
def resend_password_code():
	#retrieve username from form
	username = request.form.get("username")

	#get email from DB based on username
	email = db.execute("SELECT email FROM users WHERE username = :username", username=username)

	#generate random code
	digest = secrets.token_hex(3)

	#update code
	db.execute("UPDATE reset SET digest = :digest WHERE username = :username", digest=digest, username=username)

	send_recovery_email(email[0]['email'], digest, username)

	return render_template("password.html", status=True, username=username, msg="Code was emailed again, please enter new code.")

@app.route("/reset_password", methods=["POST"])
def reset_password():
	password = request.form.get("password")
	confirm_password = request.form.get("confirm_password")
	digest = request.form.get("digest")
	username = request.form.get("username")

	#check if digest matches the one in 'reset' DB
	stored_digest = db.execute("SELECT digest FROM reset WHERE username = :username", username=username)

	if secrets.compare_digest(digest, stored_digest[0]['digest']) != True:
		error = 'Incorrect Code'
		return render_template("password.html", status=True, error=error, username=username)

	#check if both passwords match
	if password != confirm_password:
		error = 'Passwords donot match'
		return render_template("password.html", status=True, error=error, username=username)

	#update password in 'users' DB
	pass_hash = generate_password_hash(password)
	db.execute("UPDATE users SET hash = :pass_hash WHERE username = :username", pass_hash=pass_hash, username=username)
	recovery_message = 'Password updated successfully, please login with new password'

	#clear 'reset' DB
	db.execute("DELETE FROM reset WHERE username = :username", username=username)

	return render_template("login.html", recovery_message=recovery_message)