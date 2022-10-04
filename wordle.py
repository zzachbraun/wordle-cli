import mmap
from random import randint

# for setting flags
CORRECT = 1
CLOSE = 2

WORD_LIST_LENGTH = 2314
WORD_LIST = "wordlist.txt"
GUESS_LIST = "valid-words.txt"

# If you want the answer printed before input
DEBUG = False

# Colors for printing to terminal
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    ENDC = "\033[0m"


# Checks if a word is on the list of guessable words
def validWord(word) -> bool:
    if guessableWords.find(bytes(word, "utf-8")) != -1:
        return True
    return False


# Makes sure a word is 5 letters long
def validWordLength(word) -> bool:
    if len(word) != 5:
        return False
    return True


# Gets a random word from the list of possible words
def getRandomWord() -> str:
    # Generate a value divisible by 6 within the size of the bytes of the mmap
    rnd = randint(0, WORD_LIST_LENGTH - 1) * 6
    # Finds the first index of any given word and slices the word out to return it
    word = possibleWords[rnd : rnd + 5]
    return word.decode("utf-8")


# Gets the number of letters in a word and stores them in a dictionary
def getLetterCounts(word) -> dict:
    newDict = dict()
    for letter in word:
        if letter in newDict:
            newDict[letter] += 1
        else:
            newDict[letter] = 1
    return newDict


# Prints a word to the console with correct colors
def printWord(word, flags):
    for idx, letter in enumerate(word):
        if flags[idx] == CORRECT:
            print(f"{Colors.GREEN}{letter}{Colors.ENDC}", end="")
        elif flags[idx] == CLOSE:
            print(f"{Colors.YELLOW}{letter}{Colors.ENDC}", end="")
        else:
            print(letter, end="")
    print("")


if __name__ == "__main__":
    # Save the word lists as memory maps
    with open(WORD_LIST, "rb", 0) as words:
        possibleWords = mmap.mmap(words.fileno(), 0, access=mmap.ACCESS_READ)

    with open(GUESS_LIST, "rb", 0) as words:
        guessableWords = mmap.mmap(words.fileno(), 0, access=mmap.ACCESS_READ)

    secretWord = getRandomWord()  # The word to be guessed
    guessList = []
    guesses = 6
    correct = False

    while guesses > 0:
        if DEBUG:
            print(secretWord)
        guess = input("\nGuess a word: ")
        if validWord(guess) and validWordLength(guess):  # Check for validity
            if guess == secretWord:  # Check for victory
                correct = True
                break

            guessList.append(guess)  # Add the guess to the list

            """
            for each word
            go through correct letters first, setting flag in a list
            then go through close letters, setting flag in list
            then print based on set flags
            """

            # Loop through each word in the list
            for idx, word in enumerate(guessList):
                letterCounts = getLetterCounts(secretWord)
                flags = [0 for _ in range(5)]
                # Check all correctly placed letters first,
                # then set a flag for correct and lower the
                # allowed number of uses of the letter
                for letter in range(5):
                    if word[letter] == secretWord[letter]:
                        if letterCounts[word[letter]] > 0:
                            flags[letter] = CORRECT
                            letterCounts[word[letter]] -= 1
                # Check all closely placed lettters next,
                # then set a flag for close and lower the
                # allowed number of uses of the letter
                for letter in range(5):
                    if word[letter] in secretWord:
                        if letterCounts[word[letter]] > 0:
                            flags[letter] = CLOSE
                            letterCounts[word[letter]] -= 1
                printWord(word, flags)  # Print the word with correct formatting

            guesses -= 1

        else:
            print("Invalid word!")

    if correct:
        print(f"Congratulations! The word was {secretWord}!")
    else:
        print(f"You lose! The word was {secretWord}.")
