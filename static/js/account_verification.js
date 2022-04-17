"use strict"

const $ = selector => document.querySelector(selector);

document.addEventListener("DOMContentLoaded", () => {
    $("#submit_account").addEventListener("click", userSubmission);
});

function userSubmission() {
    let validUsername, validPassword, passwordsMatch;

    if ($("#username").value.length > 16 || $("#username").value.length < 8  || $("#username").value === ""){
            $("#username").nextElementSibling.textContent = "Username must be between 8 and 16 characters long.";
            validUsername = false;
        }else{
            $("#username").nextElementSibling.textContent = "";
            validUsername = true;
        }

    if ($("#password_1").value.length > 20 || $("#password_1").value.length < 8 ||
        $("#password_1").value === ""){
        $("#password_1").nextElementSibling.textContent = "Passwords must be between 8 and 20 characters long.";
        validPassword = false;
    }else {
        $("#password_1").nextElementSibling.textContent = "";
        validPassword = true;
    }

    if ($("#password_2") !== null){
        if ($("#password_1").value !== $("#password_2").value) {
            $("#password_2").nextElementSibling.textContent = "Passwords must match.";
            passwordsMatch = false;
        }else{
            $("#password_2").nextElementSibling.textContent = "";
            passwordsMatch = true;
        }
    }

    if (validUsername && validPassword){
        if ($("#password_2") !== null && passwordsMatch || $("#password_2") == null){
            $("#user_account_form").submit();
        }
    }
}