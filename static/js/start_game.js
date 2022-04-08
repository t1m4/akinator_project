"use strict";


function handleStartGameRequest(data) {
    localStorage.setItem(gameIdName, data['id']);
    localStorage.setItem(gameName, JSON.stringify(data));
    showFirstQuestion()
}


function startGame() {
    hideObject(answerContainer)
    hideObject(userFinishAnswerContainer)
    hideObject(characterPredictedYesAnswerContainer)
    hideObject(characterPredictedNoAnswerContainer)
    hideObject(characterPredictedContainer)
    hideObject(startGameContainer)
    hideObject(continueGameContainer)

    let gameId = localStorage.getItem(gameIdName)
    showObject(answerContainer)
    console.log('Start new game!!!')
    make_request('/api/games/', handleStartGameRequest, "POST", game_data)
}

function continueGame() {
    let gameId = localStorage.getItem(gameIdName)
    if (!isNullVariable(gameId)) {
        hideObject(answerContainer)
        hideObject(userFinishAnswerContainer)
        hideObject(characterPredictedYesAnswerContainer)
        hideObject(characterPredictedNoAnswerContainer)
        hideObject(characterPredictedContainer)
        hideObject(startGameContainer)
        hideObject(continueGameContainer)
        showObject(answerContainer)
        let question = JSON.parse(localStorage.getItem(currentQuestionName))
        let questionHeader = document.querySelector('.question-text');
        if (!isNullVariable(question)) {
            questionHeader.textContent = questionText + question['name']
        } else {
            clearLocalStorage()
        }
        console.log('Continue the old game!!!')
    } else {
        alert('Нет игры для продолжения. Начните новую игру')
    }
}


function main() {
    let gameId = localStorage.getItem(gameIdName)
    if (!isNullVariable(gameId)) {

    }
    let nextQuestionForm = document.querySelector('.question-form');
    startGameContainer.addEventListener("click", () => startGame());
    continueGameContainer.addEventListener("click", () => continueGame());
    nextQuestionForm.addEventListener("submit", (e) => nextQuestionEventListener(e));
}

(function () {
    main()
})();