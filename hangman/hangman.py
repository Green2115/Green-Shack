from colorama import init, Fore, Back, Style
from random import choice
import random
import time
from pathlib import Path
letters = []
init(autoreset=True)

def get_words():
    base_path = Path(__file__).parent
    words_file = base_path / 'words.txt'
    topics_file = base_path / 'topics.txt'
    
    with open(words_file, 'r') as f:
        words = f.readlines()
    words = [word.strip() for word in words]
    word_guessing_num = random.randint(0, len(words) - 1)
    word_guessing = words[word_guessing_num]
    
    with open(topics_file, 'r') as f:
        topics = f.readlines()
    topics = [topic.strip() for topic in topics]
    topic_hint = topics[word_guessing_num]
    return word_guessing, topic_hint


def hangman(word_to_guess):
    letters = list(word_to_guess)
    display = []
    already_guessed = []
    lives = 6
    # lives = 6  # Removed unused variable
    for _ in range(len(letters)):  # Changed 'letter' to '_' to indicate it's unused
        display.append('-')
    print(''.join(display))
    global won  # Declare 'won' as global to avoid UnboundLocalError
    while not won:
        guess = input("Guess a letter: ").lower()
        guess_check = list(guess)
        if len(guess_check) == 1:
            if guess in already_guessed:
                print(Fore.YELLOW+"You already guessed that letter. Try again.")
                time.sleep(1)
                continue
            for pos in range(len(letters)):
                if letters[pos] == guess:
                    display[pos] = guess
                    already_guessed.append(guess)
            if guess not in letters:
                lives -= 1
                print(Fore.RED+f"You guessed {guess}, that's not in the word. You lose a life. \n you have {lives} lives remaining")
                already_guessed.append(guess)
                time.sleep(1)
                

        
        if '-' not in display:
            print(Fore.GREEN + "You win!" + Style.RESET_ALL)
            won = True
            time.sleep(5)
        elif lives == 0:
            print(Fore.RED + "You lose!" + Style.RESET_ALL)
            print(Fore.BLUE + f"The word was: {word_to_guess}" + Style.RESET_ALL)
            won = True
            time.sleep(5)
        else:
            print(f'{''.join(display)} \n already guessed letters: {", ".join(already_guessed)}')


global won
won = False
    
DefaultChoice = input("set word or automatically choose one (1, 2): ")
    

    
if  DefaultChoice == '1':
    while True:
        word_to_guess = input("Enter the word to be guessed: ").strip().lower()
        topic = input("Enter a topic hint for the word: ").strip().lower()
        print(f"The topic is: {topic}")
        hangman(word_to_guess)
else:
    while True:
        won = False
        word_to_guess, topic = get_words()
        print(f"The topic is: {topic}")
        hangman(word_to_guess)