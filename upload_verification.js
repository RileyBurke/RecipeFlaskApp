"use strict"

const $ = selector => document.querySelector(selector);

const validExtensions = ["jpg", "jpeg", "png", "bmp"];

let isValidFile;
let fileSplit = $("image_upload").textContent.split(".");
let fileExtension = fileSplit[-1].toLowerCase();


if (!(fileExtension in validExtensions)){
    isValidFile = false;
    $("image_upload").nextElementSibling.textContent = "Invalid image file.";
}else{
    isValidFile = true;
}

