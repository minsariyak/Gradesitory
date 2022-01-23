function showProfile() {
	document.getElementById("subscription-content").style.display = "none";
	document.getElementById("profile-content").style.display = "block";
}

function showSubscription() {
	document.getElementById("subscription-content").style.display = "block";
	document.getElementById("profile-content").style.display = "none";
}

function showSidenav() {
	document.getElementById('sidenav-mobile').style.display = "block";
}

function hideSidenav() {
	document.getElementById('sidenav-mobile').style.display = "none";
}

function showProfileMb() {
	document.getElementById("profile-content").style.display = "block";
	document.getElementById("subscription-content").style.display = "none";
	document.getElementById('sidenav-mobile').style.display = "none";
}

function showSubscriptionMb() {
	document.getElementById("subscription-content").style.display = "block";
	document.getElementById("profile-content").style.display = "none";
	document.getElementById('sidenav-mobile').style.display = "none";
}

function showPassChange() {
	document.getElementById("pass-change").style.display = "block";
	document.getElementById("overlay").style.display = "block";
}

function showEmailChange() {
	document.getElementById("email-change").style.display = "block";
	document.getElementById("overlay").style.display = "block";
}

function showUpdateCard() {
	document.getElementById("update-card").style.display = "block";
	document.getElementById("overlay").style.display = "block";
}

function submitUpdateCard() {
	document.getElementById("update").action = "/subscription_settings_payment_update";
	document.getElementById("update").method = "post";
	document.getElementById("update").submit();
}

function cancelSubscription() {
	document.getElementById("cancellation-form").action = "/subscription_settings_cancel";
	document.getElementById("cancellation-form").submit();
}

function makeSure() {
	document.getElementById("cancellation-form").style.display = "block";
	document.getElementById("overlay").style.display = "block";
}

function revert() {
	document.getElementById("cancellation-form").style.display = "none";
	document.getElementById("update-card").style.display = "none";
	document.getElementById("overlay").style.display = "none";
	document.getElementById("pass-change").style.display = "none";
	document.getElementById("email-change").style.display = "none";
}

function goHome() {
	location.href = "/gpa";				
}

function move(field, target) {
	if (field.value.length == field.maxLength) {
		document.getElementById(target).focus();
	}
}

function validate() {
	var number = document.forms["payment-update"]["card_number"].value;
	var exp_month = document.forms["payment-update"]["card_exp_month"].value;
	var exp_year = document.forms["payment-update"]["card_exp_year"].value;
	var cvc = document.forms["payment-update"]["card_cvc"].value;

	if (number.length < 16) {
		document.getElementById("error-display").innerHTML = "Invalid card number"
		document.getElementById("error-display").style.display = "block";
		revert();
		return;
	}

	if (exp_month.length < 2) {
		document.getElementById("error-display").innerHTML = "Invalid expiry month"
		document.getElementById("error-display").style.display = "block";
		revert();
		return;
	}

	if (exp_year.length < 2) {
		document.getElementById("error-display").innerHTML = "Invalid expiry year"
		document.getElementById("error-display").style.display = "block";
		revert();
		return;
	}

	if (cvc.length < 3) {
		document.getElementById("error-display").innerHTML = "Invalid CVC"
		document.getElementById("error-display").style.display = "block";
		revert();
		return;
	}

	submitUpdateCard();
}



