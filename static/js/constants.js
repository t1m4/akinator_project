"use strict";


let gameIdName = 'gameId'
let gameName = 'game'
let currentQuestionName = 'currentQuestion'
let predictedCharacterIdName = 'predictedCharacterId'

let game_data = {
    "answers": [],
    "is_success_predicted": false,
    "is_finished": false,
    "user_answer": "",
    "user_character_id": null,
}

let startGameContainer = document.querySelector('.start-game')
let answerContainer = document.querySelector('.answer-container')
let userFinishAnswerContainer = document.querySelector('.user-finish-answer-container')
let characterImageContainer = document.querySelector('.character-image')

let characterPredictedContainer = document.querySelector('.user-predicted-character-name')
let characterPredictedYesAnswerContainer = document.querySelector('.user-predicted-yes')
let characterPredictedNoAnswerContainer = document.querySelector('.user-predicted-no')
let characterPredictedAddButtonsContainer = document.querySelector('.user-predicted-no-add-buttons')

let saveCharacterButtonContainer = document.querySelector('.save-user-character-button')
let saveCharacterInputContainer = document.querySelector('.user-character-name-input')

characterPredictedYesAnswerContainer.addEventListener("change", () => yesAnswerHandler());
characterPredictedNoAnswerContainer.addEventListener("change", () => noAnswerHandler());

