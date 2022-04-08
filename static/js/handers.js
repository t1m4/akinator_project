function logHandler(data) {
    console.log(data)
}

function yesAnswerHandler() {
    hideObject(userFinishAnswerContainer)
    hideObject(characterPredictedYesAnswerContainer)
    hideObject(characterPredictedNoAnswerContainer)
    hideObject(characterPredictedContainer)
    showObject(startGameContainer)
    showObject(continueGameContainer)

    new_game_data = JSON.parse(localStorage.getItem(gameName))
    new_game_data['is_success_predicted'] = true
    new_game_data['is_finished'] = true
    let gameId = localStorage.getItem(gameIdName)
    make_request(`/api/games/${gameId}/`, logHandler, "PUT", new_game_data)

    clearLocalStorage()
    clearRadioButtons()
    clearInput()
}

function saveNewCharacterHandler(data) {
    let gameId = localStorage.getItem(gameIdName)
    let game = JSON.parse(localStorage.getItem(gameName))
    let new_game_data = {game_data}
    new_game_data['user_answer'] = saveCharacterInputContainer.value
    new_game_data['user_character_id'] = data['id']
    new_game_data['is_finished'] = true
    new_game_data['answers'] = game.answers
    make_request(`/api/games/${gameId}/`, logHandler, "PUT", new_game_data)

    clearRadioButtons()
    clearLocalStorage()
    clearInput()

}

function saveCharacterHandler(event) {
    event.preventDefault()
    if (saveCharacterInputContainer.value == null || saveCharacterInputContainer.value === "") {
        alert("Вы должны ввести имя вашего персонажа")
        return
    }

    hideObject(characterPredictedAddButtonsContainer)
    hideObject(userFinishAnswerContainer)
    showObject(startGameContainer)
    showObject(continueGameContainer)

    new_user_data = {
        'name': saveCharacterInputContainer.value,
        'answers': JSON.parse(localStorage.getItem(gameName)).answers

    }
    make_request(`/api/character/`, saveNewCharacterHandler, "POST", new_user_data)


}

function noAnswerHandler() {
    showObject(characterPredictedAddButtonsContainer)
    hideObject(characterPredictedYesAnswerContainer)
    hideObject(characterPredictedNoAnswerContainer)
    hideObject(characterPredictedContainer)
}