function logHandler(data) {
    console.log(data)
}

function yesAnswerHandler() {
    hideObject(characterImageContainer)
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
    hideObject(characterImageContainer)
}

function handleCreateNewQuestion(data) {
    let questionId = data['id']

    let probabilities = {
        1: 0,
        2: 0.25,
        3: 0.5,
        4: 0.75,
        5: 1,
    }
    let answerValue = parseInt(newQuestionAnswer.value)
    let probability_of_question = probabilities[answerValue]

    let current_game = JSON.parse(localStorage.getItem(gameName))
    current_game.answers.push({
        "id": questionId,
        "answer": probability_of_question
    })
    localStorage.setItem(gameName, JSON.stringify(current_game));
    newQuestion.value = ""
    newQuestionAnswer.value = ""

}

function addNewQuestion(event) {
    event.preventDefault()
    let questionNameValue = newQuestion.value
    if (questionNameValue == null || questionNameValue === "") {
        alert("Вы должны ввести вопрос")
        return
    }
    let answerValue = parseInt(newQuestionAnswer.value)
    if (answerValue == null || isNaN(answerValue) || answerValue === "" || answerValue < 1 || answerValue > 5) {
        alert("Вы должны ввести ответ от 1 до 5")
        return
    }

    make_request(`/api/questions/`, handleCreateNewQuestion, "POST", {'name': questionNameValue})

}