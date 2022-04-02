"use strict";


function handleStartGameRequest(data) {
    localStorage.setItem(gameIdName, data['id']);
    localStorage.setItem(gameName, JSON.stringify(data));
}


function startGame(startGameButton) {
    // hideObject(startGameButton
    let gameId = localStorage.getItem(gameIdName)
    if (gameId != null) {
        console.log('Continue the old game!!!')
    } else {
        console.log('Start new game!!!')
        make_request('/api/games/', handleStartGameRequest, "POST", game_data)
    }
}


function main() {
    let startGameButton = document.querySelector('.start-game');
    let nextQuestionButton = document.querySelector('.next-question');
    let nextQuestionForm = document.querySelector('.question-form');
    startGameButton.addEventListener("click", () => startGame(startGameButton));
    // nextQuestionButton.addEventListener("click", () => nextQuestionEventListener());
    nextQuestionForm.addEventListener("submit", (e) => nextQuestionEventListener(e));
}

(function () {
    main()
})();