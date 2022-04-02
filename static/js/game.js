"use strict";

function handleNextQuestionrequest(data) {
    console.log(data)
    // TODO change question to new question and repeat it again
//    TODO if you got winner you must send data to API and suggest user to answer again or not

}


function nextQuestionEventListener(event) {
    event.preventDefault()
    console.log(event.target)
    let user_answer = parseFloat(event.target.elements.answer.value)
    let gameId = localStorage.getItem(gameIdName)
    let currentQuestionId = localStorage.getItem(currentQuestionIdName)
    if (isNullVariable(user_answer) || isNullVariable(gameId) || isNullVariable(currentQuestionId) )
    console.log("hello worls", gameId, currentQuestionId, user_answer)
    let current_game_data = game_data
    current_game_data['answers'] = [
        {
            'id': currentQuestionId,
            'answer': user_answer,
        }
    ]
    make_request(`/api/games/${gameId}/`, handleNextQuestionrequest, "PUT", game_data)
}

function handleFirstQuestionRequest(data) {
    let question = data['results'][Math.floor(Math.random() * data['results'].length)];
    console.log(question)
    let questionHeader = document.querySelector('.question-text');
    let questionForm = document.querySelector('.question-form');
    console.log(questionHeader, questionForm)
    localStorage.setItem(currentQuestionIdName, question['id'])
    questionHeader.textContent = "Question: " + question['name']
}

function showFirstQuestion() {
    let gameId = localStorage.getItem(gameIdName)
    let game = localStorage.getItem(gameName)
    if (isNullVariable(gameId)) {
        alert("You must begin new game!")
    }
    make_request('/api/questions/', handleFirstQuestionRequest)

}

function main() {
    let startGameButton = document.querySelector('.start-game');
    let gameIdFromStorage = localStorage.getItem(gameIdName)
    console.log(JSON.parse(localStorage.getItem(gameName)))
    showFirstQuestion()
}

(function () {
    main()
})();