"use strict"

const $ = selector => document.querySelector(selector);

$("#submit_recipe").addEventListener("click", submitRecipe);

function submitRecipe() {
    const validExtensions = ["jpg", "jpeg", "png", "bmp"];
    let isValidFile;
    let fileSplit = $("image_upload").textContent.split(".");
    let fileExtension = fileSplit[-1].toLowerCase();

    if (!(fileExtension in validExtensions)){
        isValidFile = false;
        $("#image_upload").nextElementSibling.textContent = "Invalid image file. Must use a jpg, png, or bmp file.";
    }else if($("#image_upload").value() === null){
        isValidFile = false;
        $("").nextElementSibling.textContent = "Must include an image file.";
    } else{
        isValidFile = true;
    }

    if ($("#serving_size").value() === ""){
        isValidFile = false;
        $("").nextElementSibling.textContent = "Must include a serving size.";
    }

    if ($("#ingredients").value() === "") {
        isValidFile = false;
        $("").nextElementSibling.textContent = "Must include a list of ingredients.";
    }

    if ($("#instructions").value() === "") {
        isValidFile = false;
        $("").nextElementSibling.textContent = "Must include cooking instructions.";
    }

    if (isValidFile){
        $("#submit_recipe").submit();
    }
}

