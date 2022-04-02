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
    if (headers == null) {
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

