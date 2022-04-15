"use strict"

const $ = selector => document.querySelector(selector);

function removeRecipe(){
    let isValidOption = false;

    if ($("#recipe_select").value === "Select a recipe to delete"){
        $("#removal_form").nextElementSibling.textContent = "Must choose a category.";
        isValidOption = false;
    }else{
        $("#removal_form").nextElementSibling.textContent = "";
        isValidOption = true;
    }

    if (isValidOption){
        $("#removal_form").submit();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("loaded");
    $("#remove_recipe").addEventListener("click", removeRecipe);
});