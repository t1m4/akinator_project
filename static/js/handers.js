function yesAnswerHandler() {
    console.log("yes")
    hideObject(userFinishAnswerContainer)
    hideObject(characterPredictedYesAnswerContainer)
    hideObject(characterPredictedNoAnswerContainer)
    hideObject(characterPredictedContainer)
    showObject(startGameContainer)
    //TODO save game info
    clearRadioButtons()
    clearLocalStorage()
}

function saveCharacterHandler() {
    console.log(saveCharacterInputContainer.value)
    hideObject(characterPredictedAddButtonsContainer)
    hideObject(userFinishAnswerContainer)
    showObject(startGameContainer)

    clearRadioButtons()
    //TODO save game info
    clearLocalStorage()

}

function noAnswerHandler() {
    console.log("no")
    showObject(characterPredictedAddButtonsContainer)
    hideObject(characterPredictedYesAnswerContainer)
    hideObject(characterPredictedNoAnswerContainer)
    hideObject(characterPredictedContainer)
    saveCharacterButtonContainer.addEventListener('click', saveCharacterHandler)
}