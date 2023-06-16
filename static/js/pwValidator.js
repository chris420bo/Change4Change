var pw = document.getElementById("password");
var validateMessage = document.getElementById("pw-valid");

pw.onfocus = function() {
    validateMessage.style.visibility = "visible";
}

pw.onblur = function() {
    validateMessage.style.visibility = "hidden";
}

pw.onkeyup = function() {
    var lowercase = document.getElementById("lower");
    var uppercase = document.getElementById("upper");
    var num = document.getElementById("number");
    var spChar = document.getElementById("specialChar");
    var len = document.getElementById("length");

    if(pw.value.length >= 8 && pw.value.length <= 15){
        len.classList.remove("invalid");
        len.classList.add("valid");
    }
    else{
        len.classList.remove("valid");
        len.classList.add("invalid");
    }

    var lcLetters = /[a-z]/g;
    if(pw.value.match(lcLetters)){
        lowercase.classList.remove("invalid");
        lowercase.classList.add("valid");
    }
    else{
        lowercase.classList.remove("valid");
        lowercase.classList.add("invalid");
    }

    var ucLetters = /[A-Z]/g;
    if(pw.value.match(ucLetters)){
        uppercase.classList.remove("invalid");
        uppercase.classList.add("valid");
    }
    else{
        uppercase.classList.remove("valid");
        uppercase.classList.add("invalid");
    }

    var validNum = /[0-9]/g;
    if(pw.value.match(validNum)){
        num.classList.remove("invalid");
        num.classList.add("valid");
    }
    else{
        num.classList.remove("valid");
        num.classList.add("invalid");
    }

    var schar1 = /[ -/]/g;
    var schar2 = /[:-@]/g;
    if(pw.value.match(schar1) || pw.value.match(schar2)){
        spChar.classList.remove("invalid");
        spChar.classList.add("valid");
    }
    else{
        spChar.classList.remove("valid");
        spChar.classList.add("invalid");
    }
}