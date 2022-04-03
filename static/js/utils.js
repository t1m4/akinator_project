"use strict";

function hideObject(element) {
    element.style.visibility = "hidden";
}

function showObject(element) {
    element.style.visibility = "visible";
}

function getCookie(cookieName) {
    let name = cookieName + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function isNullVariable(variable) {
    return variable == null;
}

function make_request(url, handler_function, method = "GET", body = null, headers = null,) {
    if (isNullVariable(headers)) {
        headers = {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie('csrftoken')
        }
    }
    if (body != null) {
        body = JSON.stringify(body)
    }
    fetch(location.origin + url, {
        method: method,
        headers: headers,
        body: body,
    })
        .then(response => response.json())
        .then(data => handler_function(data))
}

function setImageMetaCallback(character_image, width, height) {
    let defauut_size = 400
    if (width > defauut_size || height > defauut_size) {
        character_image.width = defauut_size
        character_image.height = defauut_size
    } else {
        character_image.width = width
        character_image.height = height

    }
}

function setImageMeta(url, callback = setImageMetaCallback) {
    let character_image = characterImageContainer.children[0]
    character_image.src = url;
    character_image.onload = function () {
        callback(character_image, this.width, this.height);
    }
}


function clearRadioButtons() {
    var radioButtonArray = document.getElementsByName('radio');

    console.log("arrag", radioButtonArray)
    for (var i = 0; i < radioButtonArray.length; i++) {
        var radioButton = radioButtonArray[i];
        radioButton.checked = false;
    }
}

function clearLocalStorage(){
    localStorage.removeItem(gameIdName)
    localStorage.removeItem(gameName)
    localStorage.removeItem(currentQuestionName)
}
