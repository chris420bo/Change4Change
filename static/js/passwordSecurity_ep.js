//For Edit Profile
let eyeiconO = document.querySelector("img#eyeicon-o");
let eyeiconN = document.querySelector("img#eyeicon-n");
let eyeiconC = document.querySelector("img#eyeicon-c");
let passwordO = document.querySelector("input#old-pass");
let passwordN = document.querySelector("input#new-pass");
let passwordC = document.querySelector("input#confirm-pass");

eyeiconO.addEventListener('click', () => {
	if(passwordO.type == "password"){
		passwordO.type = "test";
		eyeiconO.src = "../static/images/eye-open.png";
	} else{
		passwordO.type = "password";
		eyeiconO.src = "../static/images/eye-close.png";
	}
});

eyeiconN.addEventListener('click', () => {
	if(passwordN.type == "password"){
		passwordN.type = "test";
		eyeiconN.src = "../static/images/eye-open.png";
	} else{
		passwordN.type = "password";
		eyeiconN.src = "../static/images/eye-close.png";
	}
});

eyeiconC.addEventListener('click', () => {
	if(passwordC.type == "password"){
		passwordC.type = "test";
		eyeiconC.src = "../static/images/eye-open.png";
	} else{
		passwordC.type = "password";
		eyeiconC.src = "../static/images/eye-close.png";
	}
});
