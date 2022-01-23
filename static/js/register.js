function data() {
	document.getElementsByName("name")[0].value = "{{ name }}";
	document.getElementsByName("email")[0].value = "{{ email }}";
	document.getElementsByName("username")[0].value = "{{ username }}";
	document.getElementsByName("password")[0].value = "{{ password }}";
	document.getElementsByName("confirmation")[0].value = "{{ password }}";
	document.getElementsByName("number")[0].value = "{{ number }}";
	document.getElementsByName("exp_month")[0].value = "{{ exp_month }}";
	document.getElementsByName("exp_year")[0].value = "{{ exp_year }}";
	document.getElementsByName("cvc")[0].value = "{{ cvc }}";
}

function show_payment() {
	document.getElementById("profile").style.display = "none";
	document.getElementById("login").style.display = "none";
	document.getElementById("payment").style.display = "block";
	document.getElementById("payment-button").classList.add("active-button");
	document.getElementById("profile-button").classList.remove("active-button");
}

function show_profile() {
	document.getElementById("profile").style.display = "block";
	document.getElementById("login").style.display = "block";
	document.getElementById("payment").style.display = "none";
	document.getElementById("payment-button").classList.remove("active-button");
	document.getElementById("profile-button").classList.add("active-button");
}

function register() {
	document.getElementById("registration-btn").disabled = "true";
	document.getElementById("register").action = "/register";
	document.getElementById("register").method = "post";
	document.getElementById("register").submit();
}

function validate(section) {

	if (section == "profile") {
		var name = document.forms["registration-form"]["name"].value;
		var email = document.forms["registration-form"]["email"].value;
		var username = document.forms["registration-form"]["username"].value;
		var password = document.forms["registration-form"]["password"].value;
		var confirmation = document.forms["registration-form"]["confirmation"].value;

		if (name == "") {
			document.getElementById("error-display").innerHTML = "Please enter your name"
			document.getElementById("error-display").style.display = "block";
			return;
		}

		if (email == "") {
			document.getElementById("error-display").innerHTML = "Please enter your email"
			document.getElementById("error-display").style.display = "block";
			return;
		}

		if (username == "") {
			document.getElementById("error-display").innerHTML = "Please enter your username"
			document.getElementById("error-display").style.display = "block";
			return;
		}

		if (password == "") {
			document.getElementById("error-display").innerHTML = "Please enter your password"
			document.getElementById("error-display").style.display = "block";
			return;
		}

		if (confirmation == "") {
			document.getElementById("error-display").innerHTML = "Please re-enter your password"
			document.getElementById("error-display").style.display = "block";
			return;
		}

		if (password != confirmation) {
			document.getElementById("error-display").innerHTML = "The passwords donot match"
			document.getElementById("error-display").style.display = "block";
			return;
		}

		var x = document.getElementById("error-display-server")
		if (x) {
			x.style.display = "none";
		}
		document.getElementById("error-display").style.display = "none";
		show_payment();
	}

	if (section == "payment") {
		var number = document.forms["registration-form"]["number"].value;
		var exp_month = document.forms["registration-form"]["exp_month"].value;
		var exp_year = document.forms["registration-form"]["exp_year"].value;
		var cvc = document.forms["registration-form"]["cvc"].value;

		if (number == "") {
			document.getElementById("error-display").innerHTML = "Please enter your card number"
			document.getElementById("error-display").style.display = "block";
			return;
		}

		if (number.length < 16) {
			document.getElementById("error-display").innerHTML = "Invalid card number"
			document.getElementById("error-display").style.display = "block";
			return;
		}

		if (exp_month == "") {
			document.getElementById("error-display").innerHTML = "Please enter your expiry month"
			document.getElementById("error-display").style.display = "block";
			return;
		}

		if (exp_month.length < 2) {
			document.getElementById("error-display").innerHTML = "Invalid expiry month"
			document.getElementById("error-display").style.display = "block";
			return;
		}

		if (exp_year == "") {
			document.getElementById("error-display").innerHTML = "Please enter your expiry year"
			document.getElementById("error-display").style.display = "block";
			return;
		}

		if (exp_year.length < 2) {
			document.getElementById("error-display").innerHTML = "Invalid expiry year"
			document.getElementById("error-display").style.display = "block";
			return;
		}

		if (cvc == "") {
			document.getElementById("error-display").innerHTML = "Please enter your CVC"
			document.getElementById("error-display").style.display = "block";
			return;
		}

		if (cvc.length < 3) {
			document.getElementById("error-display").innerHTML = "Invalid CVC"
			document.getElementById("error-display").style.display = "block";
			return;
		}

		register();
	}	
}

function move(field, target) {
	if (field.value.length == field.maxLength) {
		document.getElementById(target).focus();
	}
}