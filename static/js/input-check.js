//For Log In Check
let button = document.querySelector("button.login-button");
let userIn = document.querySelector("input#username");
let passIn = document.querySelector("input#password");
let loginForm = document.querySelector("form");

loginForm.addEventListener('input', () => {
	if(userIn.value.length > 0 && passIn.value.length > 0){
		button.removeAttribute('disabled');
	} else{
		button.setAttribute('disabled', 'disabled');
	}
});

//For Registration Check
let buttonReg = document.querySelector("button.join-button");
let userInReg = document.querySelector("input#username");
let passInReg = document.querySelector("input#password");
let frstInReg = document.querySelector("input#first_name");
let lastInReg = document.querySelector("input#last_name");
let dobInReg = document.querySelector("input#birthday");
let addrInReg = document.querySelector("input#street_address");
let cityInReg = document.querySelector("input#city");
let zipInReg = document.querySelector("input#zipcode");
let emailInReg = document.querySelector("input#email");
let loginFormReg = document.querySelector("form");

var lcLetters = /[a-z]/g;
var ucLetters = /[A-Z]/g;
var validNum = /[0-9]/g;
var schar1 = /[ -/]/g;
var schar2 = /[:-@]/g;

loginFormReg.addEventListener('input', () => {
	if ((userInReg.value.length >= 1 && userInReg.value.length <= 8)
		&& (userInReg.value.match(lcLetters) || userInReg.value.match(ucLetters))
		&& (userInReg.value.match(validNum))
		&& (passInReg.value.length >= 8 && passInReg.value.length <= 15)
		&& (passInReg.value.match(lcLetters) || passInReg.value.match(ucLetters))
		&& (passInReg.value.match(validNum))
		&& (passInReg.value.match(schar1) || passInReg.value.match(schar2))
		&& (frstInReg.value.length > 1) && (lastInReg.value.length > 1)
		&& (dobInReg.value.length > 1) && (addrInReg.value.length > 1)
		&& (cityInReg.value.length > 1) && (zipInReg.value.length > 1)
		&& (emailInReg.value.length > 1)) {
		buttonReg.removeAttribute('disabled');
	}else{
		buttonReg.setAttribute('disabled', 'disabled');
	}
});

//For Bank Account Linking
let buttonBank = document.querySelector("button.connect-button");
let nameInBank = document.querySelector("input#bank_name");
let acctnInBank = document.querySelector("input#username");
let acctpInBank = document.querySelector("input#password");
let acctdInBank = document.querySelector("input#last_4");
let loginFormBank = document.querySelector("form");

loginFormBank.addEventListener('input', () => {
	if (nameInBank.value.length > 0 && acctnInBank.value.length > 0
		&& acctpInBank.value.length > 0 && acctdInBank.value.length > 0) {
		buttonBank.removeAttribute('disabled');
	}else{
		buttonBank.setAttribute('disabled', 'disabled');
	}
});