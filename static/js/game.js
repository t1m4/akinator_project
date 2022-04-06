"use strict";

function handleFinishGameRequest(character_data) {
    if (!isNullVariable(character_data['image_url'])) {
        setImageMeta(character_data['image_url']);

    }
    hideObject(answerContainer)
    showObject(userFinishAnswerContainer)

    showObject(characterPredictedYesAnswerContainer)
    showObject(characterPredictedNoAnswerContainer)
    showObject(characterPredictedContainer)

    characterPredictedContainer.textContent = "Ваш персонаж: " + character_data['name']
}

function handleNextQuestionRequest(next_question) {
    if (isNullVariable(next_question['is_finished'])) {
        localStorage.setItem(currentQuestionName, JSON.stringify(next_question))
        let questionHeader = document.querySelector('.question-text');
        questionHeader.textContent = "Question: " + next_question['name']
    } else {
        localStorage.removeItem(currentQuestionName)
        let guess_character_id = next_question['id']
        localStorage.setItem(predictedCharacterIdName, next_question['id'])
        make_request(`/api/character/${guess_character_id}/`, handleFinishGameRequest)
    }
}


function nextQuestionEventListener(event) {
    event.preventDefault()
    let user_answer = parseFloat(event.target.elements.radio.value)
    let gameId = localStorage.getItem(gameIdName)
    let currentQuestion = JSON.parse(localStorage.getItem(currentQuestionName))
    if (isNullVariable(user_answer) || isNullVariable(gameId) || isNullVariable(currentQuestion)) {
        alert("You must begin new game!")
        return
    }
    let new_answer = {
            'id': currentQuestion["id"],
            'answer': user_answer,
        }
    let new_game_data = {game_data}
    new_game_data['answers'] = [
        new_answer
    ]

    let local_game = JSON.parse(localStorage.getItem(gameName))
    local_game.answers.push(new_answer)
    localStorage.setItem(gameName, JSON.stringify(local_game))
    if (isNullVariable(new_game_data['id'])) {
        new_game_data['id'] = parseInt(localStorage.getItem(gameIdName))
    }
    //TODO uncomment
    // clearRadioButtons()
    make_request(`/api/games/${gameId}/add_answers/`, handleNextQuestionRequest, "POST", new_game_data)
}

function handleFirstQuestionRequest(data) {
    let question = data['results'][Math.floor(Math.random() * data['results'].length)];
    // TODO use random question.
    // question = {
    //     'id': 1,
    //     'name': 'Is your character yellow?'
    // }
    let questionHeader = document.querySelector('.question-text');
    localStorage.setItem(currentQuestionName, JSON.stringify(question))
    questionHeader.textContent = "Question: " + question['name']
}

function showFirstQuestion() {
    hideObject(startGameContainer)
    let gameId = localStorage.getItem(gameIdName)
    if (isNullVariable(gameId)) {
        alert("You must begin new game!")
    }
    make_request('/api/questions/', handleFirstQuestionRequest)

}

function main() {
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