"use strict"

const $ = selector => document.querySelector(selector);

document.addEventListener("DOMContentLoaded", () => {
    $("#submit_account").addEventListener("click", userSubmission);
});

function userSubmission() {
    let validUsername = true;
    let validPassword = true;

    if ($("#password").value.length > 20 || $("#password").value.length < 8){
        $("#password").nextElementSibling.textContent = "Passwords must be between 8 and 20 characters long.";
        validPassword = false;
    }else {
        $("#password").nextElementSibling.textContent = "";
        validPassword = true;
    }

    if ($("#password_2") !== null){
        if ($("#password").value !== $("#password_2").value) {
            $("#password_2").nextElementSibling.textContent = "Passwords must match.";
            validPassword = false;
        }else{
            $("#password").nextElementSibling.textContent = "";
            validPassword = true;
        }
    }

    if ($("#username").value.length > 16 || $("#username").value.length < 8){
        $("#username").nextElementSibling.textContent = "Username must be between 8 and 16 characters long.";
        validUsername = false;
    }else{
        $("#username").nextElementSibling.textContent = "";
        validUsername = true;
    }

    if (validUsername && validPassword){
        $("#user_account_form").submit();
    }
}