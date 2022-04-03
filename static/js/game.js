"use strict";

function handleFinishGameRequest(character_data) {
    console.log(character_data)
    setImageMeta(character_data['image_url']);
    hideObject(answerContainer)
    showObject(userFinishAnswerContainer)

    showObject(characterPredictedYesAnswerContainer)
    showObject(characterPredictedNoAnswerContainer)
    showObject(characterPredictedContainer)

    characterPredictedContainer.textContent = "Ваш персонаж: " + character_data['name']
}

function handleNextQuestionRequest(next_question) {
    console.log('handleNextQuestionRequest', next_question)
    if (isNullVariable(next_question['is_finished'])) {
        localStorage.setItem(currentQuestionName, JSON.stringify(next_question))
        let questionHeader = document.querySelector('.question-text');
        questionHeader.textContent = "Question: " + next_question['name']
    } else {
        localStorage.removeItem(currentQuestionName)
        let guess_character_id = next_question['id']
        make_request(`/api/character/${guess_character_id}/`, handleFinishGameRequest)
    }
}


function nextQuestionEventListener(event) {
    event.preventDefault()
    let user_answer = parseFloat(event.target.elements.answer.value)
    let gameId = localStorage.getItem(gameIdName)
    let currentQuestion = JSON.parse(localStorage.getItem(currentQuestionName))
    if (isNullVariable(user_answer) || isNullVariable(gameId) || isNullVariable(currentQuestion)) {
        alert("You must begin new game!")
        return
    }
    game_data['answers'] = [
        {
            'id': currentQuestion["id"],
            'answer': user_answer,
        }
    ]
    if (isNullVariable(game_data['id'])) {
        game_data['id'] = parseInt(localStorage.getItem(gameIdName))
    }
    make_request(`/api/games/${gameId}/add_answers/`, handleNextQuestionRequest, "POST", game_data)
}

function handleFirstQuestionRequest(data) {
    let question = data['results'][Math.floor(Math.random() * data['results'].length)];
    console.log(question)
    question = {
        'id': 1,
        'name': 'Is your character yellow?'
    }
    let questionHeader = document.querySelector('.question-text');
    localStorage.setItem(currentQuestionName, JSON.stringify(question))
    questionHeader.textContent = "Question: " + question['name']
}

function showFirstQuestion() {
    hideObject(startGameContainer)
    let gameId = localStorage.getItem(gameIdName)
    let game = localStorage.getItem(gameName)
    if (isNullVariable(gameId)) {
        alert("You must begin new game!")
    }
    make_request('/api/questions/', handleFirstQuestionRequest)

}

function main() {
    console.log(JSON.parse(localStorage.getItem(gameName)))
    // showFirstQuestion()

    let question = localStorage.getItem(currentQuestionName)
    let questionHeader = document.querySelector('.question-text');
    if (!isNullVariable(question)) {
        questionHeader.textContent = "Question: " + question['name']
    }

}

(function () {
    main()
})();