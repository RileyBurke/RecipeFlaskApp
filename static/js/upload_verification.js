"use strict"

const $ = selector => document.querySelector(selector);

document.addEventListener("DOMContentLoaded", () => {
    console.log("loaded");
    $("#submit_recipe").addEventListener("click", submitRecipe);
});

function submitRecipe() {
    console.log("Submitting recipe")
    const validExtensions = ["jpg", "jpeg", "png", "bmp"];
    let isValidName, isValidCategory, isValidSize, isValidFile, isValidIngredients, isValidInstructions;
    let fileExtension = $("#image_upload").value.split('.').pop();

    if($("#image_upload").value === ""){
        $("#image_upload").nextElementSibling.textContent = "Must include an image file.";
        isValidFile = false;
    }else if (!(validExtensions.includes(fileExtension))){
        $("#image_upload").nextElementSibling.textContent = "Invalid image file. Must use a jpg, png, or bmp file.";
        isValidFile = false;
    }else{
        $("#image_upload").nextElementSibling.textContent = "";
        isValidFile = true;
    }

    if ($("#recipe_name").value === ""){
        $("#recipe_name").nextElementSibling.textContent = "Must include a recipe name.";
        isValidName = false;
    }else{
        $("#recipe_name").nextElementSibling.textContent = "";
        isValidName = true;
    }

    if ($("#recipe_category").value === "Choose category"){
        $("#recipe_category").nextElementSibling.textContent = "Must choose a category.";
        isValidCategory = false;
    }else{
        $("#recipe_category").nextElementSibling.textContent = "";
        isValidCategory = true;
    }

    if ($("#serving_size").value === ""){
        $("#serving_size").nextElementSibling.textContent = "Must include a serving size.";
        isValidSize = false;
    }else{
        $("#serving_size").nextElementSibling.textContent = "";
        isValidSize = true;
    }

    if ($("#ingredients").value === "") {
        $("#ingredients").nextElementSibling.textContent = "Must include a list of ingredients.";
        isValidIngredients = false;
    }else{
        $("#ingredients").nextElementSibling.textContent = "";
        isValidIngredients = true;
    }

    if ($("#instructions").value === "") {
        $("#instructions").nextElementSibling.textContent = "Must include cooking instructions.";
        isValidInstructions = false;
    }else{
        $("#instructions").nextElementSibling.textContent = "";
        isValidInstructions = true;
    }

    if (isValidFile && isValidName && isValidCategory && isValidSize && isValidIngredients && isValidInstructions){
        $("#recipe_form").submit();
    }
}

