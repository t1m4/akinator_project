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
    // hideObject(startGameButton
    let gameId = localStorage.getItem(gameIdName)
    if (!isNullVariable(gameId)) {
        showObject(answerContainer)
        showFirstQuestion()
        console.log('Continue the old game!!!')
    } else {
        showObject(answerContainer)
        console.log('Start new game!!!')
        make_request('/api/games/', handleStartGameRequest, "POST", game_data)
    }
}


function main() {
    let nextQuestionButton = document.querySelector('.next-question');
    let nextQuestionForm = document.querySelector('.question-form');
    startGameContainer.addEventListener("click", () => startGame());
    // nextQuestionButton.addEventListener("click", () => nextQuestionEventListener());
    nextQuestionForm.addEventListener("submit", (e) => nextQuestionEventListener(e));
}

(function () {
    main()
})();