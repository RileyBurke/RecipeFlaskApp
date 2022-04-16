"use strict"

const $ = selector => document.querySelector(selector);

function removeRecipe(){
    let isValidOption;

    if ($("#recipe_select").value === ""){
        $("#remove_recipe").nextElementSibling.textContent = "Must choose a recipe.";
        isValidOption = false;
    }else{
        $("#remove_recipe").nextElementSibling.textContent = "";
        isValidOption = true;
    }

    if (isValidOption){
        if (confirm("Are you sure you want to delete these recipes?") === true){
            $("#removal_form").submit();
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("loaded");
    $("#remove_recipe").addEventListener("click", removeRecipe);
});