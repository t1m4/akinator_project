import random
from pprint import pprint

import numpy as np

questions = {
    1: "Is your character yellow?",
    2: "Is your character bald?",
    3: "Is your character a man?",
    4: "Is your character short?",
}

characters = [
    {"name": "Homer Simpson", "answers": {1: 1, 2: 1, 3: 1, 4: 0}},
    {"name": "SpongeBob SquarePants", "answers": {1: 1, 2: 1, 3: 1, 4: 0.75}},
    {"name": "Sandy Cheeks", "answers": {1: 0, 2: 0, 3: 0}},
]

questions_so_far = []
answers_so_far = []


def index(request):
    global questions_so_far, answers_so_far

    # question = request.args.get("question")
    # answer = request.args.get("answer")
    question = request.get("question")
    answer = request.get("answer")
    # TODO save after start game id of this game, add questions and answers for game. Create each game model.
    if question and answer:
        questions_so_far.append(int(question))
        answers_so_far.append(float(answer))
    probabilities = calculate_probabilites(questions_so_far, answers_so_far)
    print("probabilities", probabilities)

    questions_left = list(set(questions.keys()) - set(questions_so_far))
    if len(questions_left) == 0:
        result = sorted(probabilities, key=lambda p: p["probability"], reverse=True)[0]
        print(f"You got winner. This is your guess {result}")
    else:
        print(
            f"LEft questions {questions_left} ,{questions_so_far}, {len(answers_so_far)}"
        )
        # next_question = random.choice(questions_left)
        next_question = question + 1
        return next_question
        # return render_template('index.html', question=next_question, question_text=questions[next_question])


def calculate_probabilites(questions_so_far, answers_so_far):
    probabilities = []
    for character in characters:
        probabilities.append(
            {
                "name": character["name"],
                "probability": calculate_character_probability(
                    character, questions_so_far, answers_so_far
                ),
            }
        )

    return probabilities


def calculate_character_probability(character, questions_so_far, answers_so_far):
    # Prior
    P_character = 1 / len(characters)

    # Likelihood
    P_answers_given_character = 1
    P_answers_given_not_character = 1
    for question, answer in zip(questions_so_far, answers_so_far):
        P_answers_given_character *= max(
            1 - abs(answer - character_answer(character, question)), 0.01
        )

        P_answer_not_character = np.mean(
            [
                1 - abs(answer - character_answer(not_character, question))
                for not_character in characters
                if not_character["name"] != character["name"]
            ]
        )
        P_answers_given_not_character *= max(P_answer_not_character, 0.01)
        print(
            "result {:30} {:20} {:20}".format(
                character["name"],
                P_answers_given_character,
                P_answers_given_not_character,
            )
        )

    # Evidence
    P_answers = (
        P_character * P_answers_given_character
        + (1 - P_character) * P_answers_given_not_character
    )

    # Bayes Theorem
    P_character_given_answers = (P_answers_given_character * P_character) / P_answers
    return P_character_given_answers


def character_answer(character, question):
    if question in character["answers"]:
        return character["answers"][question]
    return 0.5


def ready_akinator():

    aki = akinator.Akinator()

    q = aki.start_game()

    while aki.progression <= 80:
        a = input(q + "\n\t")
        if a == "b":
            try:
                q = aki.back()
            except akinator.CantGoBackAnyFurther:
                pass
        else:
            q = aki.answer(a)
    aki.win()

    correct = input(
        f"It's {aki.first_guess['name']} ({aki.first_guess['description']})! Was I correct?\n{aki.first_guess['absolute_picture_path']}\n\t")
    if correct.lower() == "yes" or correct.lower() == "y":
        print("Yay\n")
    else:
        print("Oof\n")

if __name__ == "__main__":
    # question = random.choice(questions)
    # question = questions[1]
    # answer = input(question)
    # question_index = [k for k, v in questions.items() if v == question][0]
    # print(question_index)
    # while question_index:
    #     next_question = index({"question": question_index, "answer": answer})
    #     if not next_question:
    #         break
    #     # if next_question:
    #     answer = input(
    #         f"Question number {next_question} and question: {questions[next_question]}"
    #     )
    #     question_index = next_question
    #     # print('seocnd questin', next_question)

    n = 5
    a = [[0]*n]*n
    for i in range(n):
        for j in range(n):
            # a[i][j] = (random.randint(1, 10) + i) + j
            a[i][j] = (i + j)
    pprint(a)

    k = a[0][0]
    result = []
    for i in range(n):
        # for j in range(n-i):
        for j in range(n - i):
            print(i, j , a[i][j])
            # if i == j and j<n-1 and a[i][j+1] > k:
            #     k = a[i][j+1]
            #     result.append({
            #         'i': i,
            #         'j': j+1,
            #         'k': k,
            #     })

    print("max", k)
    print("max", result)