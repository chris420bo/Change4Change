let eyeicon = document.querySelector("#eyeicon");
let password = document.querySelector("#password");

eyeicon.addEventListener('click', () => {
	if(password.type == "password"){
		password.type = "test";
		eyeicon.src = "../static/images/eye-open.png";
	} else{
		password.type = "password";
		eyeicon.src = "../static/images/eye-close.png";
	}
});