import random
import requests
import json
from colored import fg, bg, attr
from english_words import english_words_alpha_set

# Get the random word from a set of english words via module
english_word_list = list(english_words_alpha_set)

game_list = []

for word in english_word_list:
    if(len(word)) == 5:
        game_list.append(word.upper())

word = random.choice(game_list)

# Get the word definition through a simple dictionary API:


def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        response_str = json.dumps(response.json(), sort_keys=True, indent=4)
        response_dict = json.loads(response_str)[0]
        definition = ((response_dict["meanings"][0])[
            "definitions"][0])["definition"]
        print(f'\nPrimary Definition: {definition}\n')
    else:
        print("\n There was a problem getting this definition.")

# Color the letters accordingly based on the guess:


def correct_place(letter):
    color = fg('black') + bg('light_green')
    reset = attr('reset')
    return f'{color}{letter}{reset}'


def correct_letter(letter):
    color = fg('black') + bg('light_yellow')
    reset = attr('reset')
    return f'{color}{letter}{reset}'


def incorrect_letter(letter):
    color = fg('black') + bg('light_gray')
    reset = attr('reset')
    return f'{color}{letter}{reset}'


# Here is where we get the guesses via input:
guesses = []


def get_guess(word):
    guessed = []
    guess = input("Guess the 5 letter word in 6 trys or less: ").upper()
    if len(guess) != 5:
        print("Your guess must be 5 characters.  Try again.\n")
    elif guess not in game_list:
        print("The word is not available or doesn't exist.\n")
    else:
        for index, letter in enumerate(guess):
            if word[index] == guess[index]:
                guessed += correct_place(letter)
            elif letter in word:
                guessed += correct_letter(letter)
            else:
                guessed += incorrect_letter(letter)
        format_guess = ''.join(guessed)
        guesses.append(format_guess)
    return guess

# Here we show a list of guesses that are formatted:


def show_guess(guesses):
    for format_guess in guesses:
        print(format_guess)


# Run the code here:
while True:
    if get_guess(word) == word:
        show_guess(guesses)
        print("You've won the game!")
        break
    elif len(guesses) == 4:
        show_guess(guesses)
        define = input("Would you like the definition to help? Y/N ").upper()
        if define == "Y" or define == "YES":
            get_definition(word)
            show_guess(guesses)
        else:
            print("\nThat's the spirit!  Good luck!\n")
            show_guess(guesses)
            continue
    elif len(guesses) == 5:
        show_guess(guesses)
        hint = input("\nWould you like another hint? Y/N ").upper()
        if hint == "Y" or hint == "YES":
            print(
                f"\n The word begins with {word[0]} and ends with {word[4]}.\n")
            show_guess(guesses)
        else:
            print("\n You can do it!\n")
            show_guess(guesses)
    elif len(guesses) == 6:
        show_guess(guesses)
        print("Sorry you've run out of guesses.  The correct word was " + word + ".")
        break
    else:
        show_guess(guesses)
        print("Please try again.\n")
