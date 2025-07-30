import random
import os
import sys
import importlib.resources
from pyfiglet import Figlet

MAX_TRIES = 6
WORD_LENGTH = 5
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_GRAY = "\033[90m"
COLOR_RESET = "\033[0m"

def load_words(file_name):
    with importlib.resources.files("wordle").joinpath(file_name).open("r") as f:
        words = [word.strip().lower() for word in f if len(word.strip()) == WORD_LENGTH]
    return words

def choose_secret_word(words):
    return random.choice(words)

def get_feedback(secret, guess):
    feedback = []
    secret_temp = list(secret)
    guess_temp = list(guess)

    for i in range(WORD_LENGTH):
        if guess[i] == secret[i]:
            feedback.append(f"{COLOR_GREEN}{guess[i]}{COLOR_RESET}")
            secret_temp[i] = None
            guess_temp[i] = None
        else:
            feedback.append(None)

    for i in range(WORD_LENGTH):
        if guess_temp[i] is None:
            continue
        elif guess_temp[i] in secret_temp:
            feedback[i] = f"{COLOR_YELLOW}{guess_temp[i]}{COLOR_RESET}"
            secret_temp[secret_temp.index(guess_temp[i])] = None
        else:
            feedback[i] = f"{COLOR_GRAY}{guess_temp[i]}{COLOR_RESET}"
    return ''.join(feedback)

def main():
    try:
        repeat = True
        while repeat:
            words = load_words("words.txt")
            valid_words = load_words("valid.txt")
            secret_word = choose_secret_word(words)

            f = Figlet(font='slant')
            print(f.renderText("wordle-cli!"))
            print("by gautam-4\n\n")
            attempts = []

            for turn in range(1, MAX_TRIES + 1):
                while True:
                    try:
                        guess = input(f"({turn}/{MAX_TRIES}) > ").strip().lower()
                    except KeyboardInterrupt:
                        print("\nexiting...")
                        sys.exit(0)

                    if not guess:
                        print("Enter a 5-letter word.")
                    elif len(guess) != WORD_LENGTH:
                        print("Enter a 5-letter word.")
                    elif guess not in valid_words:
                        print("Not a valid word.")
                    else:
                        break

                feedback = get_feedback(secret_word, guess)
                attempts.append(feedback)

                os.system("clear" if os.name == "posix" else "cls")
                print(f.renderText("wordle-cli"))
                for line in attempts:
                    print(line)

                if guess == secret_word:
                    print("🎉 You guessed it!")
                    sys.exit(0)

            print(f"❌ Out of tries! The word was: {secret_word}")
            
            print("\nDo you want to play again (y/n)")
            play_again = input().strip().lower()
            if play_again != "y":
                repeat = False

    except KeyboardInterrupt:
        print("\nexiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
