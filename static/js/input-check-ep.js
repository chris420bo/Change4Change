var lcLetters = /[a-z]/g;
var ucLetters = /[A-Z]/g;
var validNum = /[0-9]/g;
var schar1 = /[ -/]/g;
var schar2 = /[:-@]/g;

//Change Username Form
let buttonUser = document.querySelector("button#user-button");
let oUserInUser = document.querySelector("input#old_user");
let nUserInUser = document.querySelector("input#new_user");
let loginFormUser = document.querySelector("#change_username");

loginFormUser.addEventListener('input', () => {
	if ((nUserInUser.value.length >= 1 && nUserInUser.value.length <= 8)
		&& (nUserInUser.value.match(lcLetters) || nUserInUser.value.match(ucLetters))
		&& (nUserInUser.value.match(validNum))
		&& (oUserInUser.value.length > 0)) {
		buttonUser.removeAttribute('disabled');
	}else{
		buttonUser.setAttribute('disabled', 'disabled');
	}
});

//Change Password Form
let buttonPass = document.querySelector("button#pass-button");
let oPassInPass = document.querySelector("input#old-pass");
let nPassInPass = document.querySelector("input#new-pass");
let cPassInPass = document.querySelector("input#confirm-pass");
let loginFormPass = document.querySelector("#change_password");

loginFormPass.addEventListener('input', () => {
	if ((nPassInPass.value.length >= 8 && nPassInPass.value.length <= 15)
		&& (nPassInPass.value.match(lcLetters) || nPassInPass.value.match(ucLetters))
		&& (nPassInPass.value.match(validNum))
		&& (nPassInPass.value.match(schar1) || nPassInPass.value.match(schar2))
		&& (oPassInPass.value.length > 0) && (nPassInPass.value == cPassInPass.value)) {
		buttonPass.removeAttribute('disabled');
	}else{
		buttonPass.setAttribute('disabled', 'disabled');
	}
});

//Change Address Form
let buttonAddr = document.querySelector("button#addr-button");
let addrInAddr = document.querySelector("input#street_address");
let cityInAddr = document.querySelector("input#city");
let zipInAddr = document.querySelector("input#new_zip");
let loginFormAddr = document.querySelector("#change_address");

loginFormAddr.addEventListener('input', () => {
	if ((addrInAddr.value.length > 0)
		&& (cityInAddr.value.length > 0)
		&& (zipInAddr.value.length > 0)) {
		buttonAddr.removeAttribute('disabled');
	}else{
		buttonAddr.setAttribute('disabled', 'disabled');
	}
});