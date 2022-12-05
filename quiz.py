import sqlite3, re
import difflib as dl

def main():

    num, difficulty = getInput()
    questions = getQuestions(num, difficulty)
    play(questions)

def getInput():

    # two infinite loops take user input. Break out as soon as input is valid

    MIN = 1
    MAX = 11 # max = 10 because range goes up to but doesn't include its upper limit

    while True:

        num = input("\nHow many questions do you want? ")

        if num.isnumeric() and int(num) in range(MIN,MAX*10):

            break

    while True:

        difficulty = input("\nHow difficult do you want the questions to be (1-10)? Hit enter to get questions from all difficulty levels. ")

        if not difficulty or (difficulty.isnumeric() and int(difficulty) in range(MIN,MAX)):

            break

    return int(num), difficulty

def getQuestions(num, difficulty):

    # connect to sql database
    con = sqlite3.connect("jeopardy.db")
    cur = con.cursor()

    # query the database for data --> categories, questions and answer. Select random difficulty levels if nothing is entered by the user
    if difficulty == "":
        questions = [question for question in cur.execute(
                """SELECT category, question, answer FROM jeopardy ORDER BY RANDOM() LIMIT (?)""", (num,))]
    else:
        questions = [question for question in cur.execute(
                """SELECT category, question, answer FROM jeopardy WHERE value = (?) ORDER BY RANDOM() LIMIT (?)""", (int(difficulty) * 100, num))]

    # only for debugging   
    # questions = [question for question in cur.execute(
    #             """SELECT category, question, answer FROM jeopardy WHERE id = (?) ORDER BY RANDOM() LIMIT (?)""", (int(difficulty), num))]

    # return the list of tuples that each hold the data pertaining to a specific question
    return questions

def play(questions):

    # store number of correct guesses
    correct = 0

    # loop over each question in [questions]
    for i in range(len(questions)):

        # print question number, category and the question itself
        print(f"\nQUESTION {i+1}/{len(questions)}\nCategory: {questions[i][0]}\nQuestion: {questions[i][1]}.")

        # receive guess from user and convert it to upper case
        guess = input("\nYour guess: ").upper()

        # check whether guess is correct or not
        if guessed(guess, questions[i][2]):

            print(f"\nCorrect, the answer is: {questions[i][2]}.")
            correct += 1

        else:

            print(f"\nWrong, the correct answer is: {questions[i][2]}.")

        print("\n-------------------------------------------------------")

    print(f"\nYou answered correctly on {correct}/{len(questions)} questions.\n")

    return

def guessed(guess, answer):

    # [fillers] is used to ignore general words, [signs] is used to split answer and guess on spaces and punctuation
    fillers = ["the", "of", "and", "then", "that", "when", "what", "why", "a", "to"]
    punc = r"[\s\(\)\-\,\/]"

    # if guess and answer are exactly the same, return true
    if answer.upper() == guess:
        return True

    # if no guess is given, return false
    if not guess:
        return False

    if guess.isnumeric() and answer.isnumeric() and guess != answer:
        return False

    # convert answer and guess to lists created by splitting on spaces and various signs
    guessList = re.split(punc, guess)
    answerList = re.split(punc, answer)

    # loop over the words in the answerList
    for word in answerList:

        # if the current word is in [fillers], skip it
        if word.lower() in fillers:
            continue

        # if there is just a single match between a word in guessList and a word in answerList, return true
        match = dl.get_close_matches(word.upper(), guessList)
        if match != []:
            return True

    # if the answer is a single word, but the user has typed it as two words, this code will return true
    return ("".join(guessList) == answer.upper())

if __name__ == "__main__":
    main()


# below code is for debugging - with this code the difficulty level is instead the id, so I can access specific questions
# questions = [question for question in cur.execute(
#         "SELECT category, question, answer, id FROM jeopardy WHERE id = (?) LIMIT (?)", (difficulty, num))]