function addCourse() {
	document.getElementById("add-course").style.display = "block";
	document.getElementById("overlay").style.display = "block";
	// document.getElementById("main-div").style.filter = "blur(15px)";
	// document.getElementById("sidenav").style.filter = "blur(15px)";
	// document.getElementById("button").style.filter = "blur(15px)";
}

function revert() {
	document.getElementById("add-course").style.display = "none";
	document.getElementById("edit-course").style.display = "none";
	document.getElementById("overlay").style.display = "none";
	// document.getElementById("main-div").style.filter = "none";
	// document.getElementById("sidenav").style.filter = "none";
	// document.getElementById("button").style.filter = "none";
}

function loadData(x) {
	var row_num = x;
	var courseName = document.getElementById(row_num).cells[0].innerHTML;
	var courseCredit = document.getElementById(row_num).cells[1].innerHTML;
	var courseGrade = document.getElementById(row_num).cells[2].innerHTML;
	var category = document.getElementById(row_num).cells[3].innerHTML;

	//Get ID 
	var ID = document.getElementById(row_num).cells[4].innerHTML;
	document.getElementById("ecID").value = ID;

	//Preset course name
	document.getElementById("courseName").value = courseName;

	//Check which credit to select
	document.getElementById("courseCredit").value = courseCredit;
	// if (courseCredit == 3) {
	// 	document.getElementById("three").checked = true;
	// }
	// if (courseCredit == 6) {
	// 	document.getElementById("six").checked = true;
	// }
	// if (courseCredit == 9) {
	// 	document.getElementById("nine").checked = true;
	// }


	//Check which grade to select
	if (courseGrade === "A+") {
		document.getElementById("A+").selected = "true";
	}
	if (courseGrade === "A") {
		document.getElementById("A").selected = "true";
	}
	if (courseGrade === "A-") {
		document.getElementById("A-").selected = "true";
	}
	if (courseGrade === "B+") {
		document.getElementById("B+").selected = "true";
	}
	if (courseGrade === "B") {
		document.getElementById("B").selected = "true";
	}
	if (courseGrade === "B-") {
		document.getElementById("B-").selected = "true";
	}
	if (courseGrade === "C+") {
		document.getElementById("C+").selected = "true";
	}
	if (courseGrade === "C") {
		document.getElementById("C").selected = "true";
	}
	if (courseGrade === "C-") {
		document.getElementById("C-").selected = "true";
	}
	if (courseGrade === "D+") {
		document.getElementById("D+").selected = "true";
	}
	if (courseGrade === "D") {
		document.getElementById("D").selected = "true";
	}
	if (courseGrade === "D-") {
		document.getElementById("D-").selected = "true";
	}
	if (courseGrade === "F") {
		document.getElementById("F").selected = "true";
	}

	//Check which category to select
	if (category === "Major") {
		document.getElementById("Major").selected = "true"
	}

	if (category === "Non-Major") {
		document.getElementById("Non-Major").selected = "true"
	}

	document.getElementById("edit-course").style.display = "block";
	document.getElementById("overlay").style.display = "block";
	// document.getElementById("main-div").style.filter = "blur(15px)";
	// document.getElementById("sidenav").style.filter = "blur(15px)";
	// document.getElementById("button").style.filter = "blur(15px)";
}

function verifyEmail() {
	document.getElementById("verification-form").submit();
}

function showVerify() {
	document.getElementById("verify-email").style.display = "block";
	document.getElementById("overlay").style.display = "block";
	// document.getElementById("main-div").style.filter = "blur(15px)";
}

function displayCourses(category) {

	//clear search input when navigating between categories
	document.getElementById("search-input").value = "";

	if (category === 'all') {

		//Ensure all table rows aren't hidden by a previous search (undoing search filter)
		table = document.getElementById("all-courses-table");
		tr = table.getElementsByTagName("tr");
		for(i = 0; i < tr.length; i++) {
			tr[i].style.display = "";
		}

		document.getElementById('display-major-courses').style.display = "none";
		document.getElementById('display-non-major-courses').style.display = "none";
		document.getElementById('display-all-courses').style.display = "block";
	}

	if (category === 'Major') {

		//Ensure all table rows aren't hidden by a previous search (undoing search filter)
		table = document.getElementById("major-courses-table");
		tr = table.getElementsByTagName("tr");
		for(i = 0; i < tr.length; i++) {
			tr[i].style.display = "";
		}

		document.getElementById('display-non-major-courses').style.display = "none";
		document.getElementById('display-all-courses').style.display = "none";
		document.getElementById('display-major-courses').style.display = "block";
	}

	if (category === 'Non-Major') {

		//Ensure all table rows aren't hidden by a previous search (undoing search filter)
		table = document.getElementById("non-major-courses-table");
		tr = table.getElementsByTagName("tr");
		for(i = 0; i < tr.length; i++) {
			tr[i].style.display = "";
		}

		document.getElementById('display-all-courses').style.display = "none";
		document.getElementById('display-major-courses').style.display = "none";
		document.getElementById('display-non-major-courses').style.display = "block";
	}

	if (category === 'all-mb') {

		//Ensure all table rows aren't hidden by a previous search (undoing search filter)
		table = document.getElementById("all-courses-table");
		tr = table.getElementsByTagName("tr");
		for(i = 0; i < tr.length; i++) {
			tr[i].style.display = "";
		}

		document.getElementById('display-major-courses').style.display = "none";
		document.getElementById('display-non-major-courses').style.display = "none";
		document.getElementById('display-all-courses').style.display = "block";
		document.getElementById('sidenav-mobile').style.display = "none";
	}

	if (category === 'Major-mb') {

		//Ensure all table rows aren't hidden by a previous search (undoing search filter)
		table = document.getElementById("major-courses-table");
		tr = table.getElementsByTagName("tr");
		for(i = 0; i < tr.length; i++) {
			tr[i].style.display = "";
		}

		document.getElementById('display-non-major-courses').style.display = "none";
		document.getElementById('display-all-courses').style.display = "none";
		document.getElementById('display-major-courses').style.display = "block";
		document.getElementById('sidenav-mobile').style.display = "none";
	}

	if (category === 'Non-Major-mb') {

		//Ensure all table rows aren't hidden by a previous search (undoing search filter)
		table = document.getElementById("non-major-courses-table");
		tr = table.getElementsByTagName("tr");
		for(i = 0; i < tr.length; i++) {
			tr[i].style.display = "";
		}

		document.getElementById('display-all-courses').style.display = "none";
		document.getElementById('display-major-courses').style.display = "none";
		document.getElementById('display-non-major-courses').style.display = "block";
		document.getElementById('sidenav-mobile').style.display = "none";
	}
}

function search() {

	var all, major, nonMajor, input, table, tr, i, td;
	all = document.getElementById('display-all-courses');
	major = document.getElementById('display-major-courses');
	nonMajor = document.getElementById('display-non-major-courses');
	
	if (all.style.display == "block") {
		tableOnHand = "all-courses-table";
	} else if (major.style.display == "block") {
		tableOnHand = "major-courses-table";
	} else if (nonMajor.style.display == "block") {
		tableOnHand = "non-major-courses-table";
	}

	input = document.getElementById("search-input").value;
	table = document.getElementById(tableOnHand);
	tr = table.getElementsByTagName("tr");

	for(i = 0; i < tr.length; i++) {

		td = tr[i].getElementsByTagName("td")[0];
	
		if (td) {

			if (td.innerText.indexOf(input) > -1) {
				tr[i].style.display = "";
			} else {
				tr[i].style.display = "none";
			}
		}
	}
}

function toggleSearchBar() {
	var search = document.getElementById("search");
	if (search.className == "search-bar") {
		search.classList.remove("search-bar");
		search.classList.add("search-bar-active");
	}
	else {
		search.classList.remove("search-bar-active");
		search.classList.add("search-bar");
	}
}

function showSidenav() {
	document.getElementById('sidenav-mobile').style.display = "block";
}

function hideSidenav() {
	document.getElementById('sidenav-mobile').style.display = "none";
}