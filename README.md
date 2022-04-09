https://medium.com/analytics-vidhya/building-akinator-with-python-using-bayes-theorem-216253c98daa
https://habr.com/ru/post/84364/

[//]: # (TODO learn by errors using users data )

Main things to do

    1. Learn by errors using users data
    2. Choose questions 
    3. People still can have errors

Main function:
    1. Start game and answer questions. 
    2. If we don't your guess is wrong save new data with these questions 
    3. Early stop asking questions if Akinator is really sure of the answer
    4. 

Allow users to add new characters if Akinator got it wrong, and save their answers
Reinforce characters answers if Akinator got it right
Allow users to add new questions
Use a database instead of in-memory to be able to add new characters and questions indefinitely
Instead of randomly choosing questions, select the ones that could untie the top guesses


1. Collection database 
2. Add answer for characters 
3. Translate to english
4. **Change probability to some constant and show only after this probability is more.** 
5. Add changing answer for question. 
6. **Change generating next question. Not use randomly use smart things**
7. Change button for answers and questions for new user. Ask questions from fix guess character.  
8. **Добавить все в docker-compose and heroku**
9. **Add sentry for logging**
10. **Add command to create superuser with password ruslan and ruslan** 