var un = document.getElementById("username");
var userValidate = document.getElementById("user-valid");

un.onfocus = function() {
    userValidate.style.visibility = "visible";
}

un.onblur = function() {
    userValidate.style.visibility = "hidden";
}

un.onkeyup = function() {
    var letter = document.getElementById("letter");
    var num = document.getElementById("unNum");
    var len = document.getElementById("unLen");

    if(un.value.length >= 1 && un.value.length <= 8){
        len.classList.remove("invalid");
        len.classList.add("valid");
    }
    else{
        len.classList.remove("valid");
        len.classList.add("invalid");
    }

    var lcLetters = /[a-z]/g;
    var ucLetters = /[A-Z]/g;
    if(un.value.match(lcLetters) || un.value.match(ucLetters)){
        letter.classList.remove("invalid");
        letter.classList.add("valid");
    }
    else{
        letter.classList.remove("valid");
        letter.classList.add("invalid");
    }

    var validNum = /[0-9]/g;
    if(un.value.match(validNum)){
        num.classList.remove("invalid");
        num.classList.add("valid");
    }
    else{
        num.classList.remove("valid");
        num.classList.add("invalid");
    }
}