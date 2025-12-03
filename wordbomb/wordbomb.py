import random
import time
import asyncio
from inputimeout import inputimeout, TimeoutOccurred
easy=r"C:\\Users\\marol\\OneDrive\\Pulpit\\Marcel\\Programming\\wordbomb\\Easy.txt"
hard=r"C:\\Users\\marol\\OneDrive\\Pulpit\\Marcel\\Programming\\wordbomb\\hard.txt"
medium=r"C:\\Users\\marol\\OneDrive\\Pulpit\\Marcel\\Programming\\wordbomb\\medium.txt"
difficulties = [easy, medium, hard]
won = False
timer_time = 10
completed = False
default_timer_time = timer_time

def see_if_in_dictionary(word):
    dictionary = r"C:\Users\marol\OneDrive\Pulpit\Marcel\Programming\wordbomb\words.txt"
    word = word.lower()
    with open(dictionary, 'r', encoding="utf-8") as f:
        words = [line.strip().lower() for line in f if line.strip()]
        return word in words
    

def Give_chunk(dictionary):
    with open(dictionary, 'r', encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    random_line = random.choice(lines).strip()
    print(f"Your chunk is: {random_line}")
    return random_line  # return full line, not a random word
            


start = input("start? ")

if start.lower() == "yes":
    mode = input("mode (normal/forever): ")
    lives=2
    level = 0
    to_next_level = 0
    guessed_words = []
    while not won:
        
        chunk = Give_chunk(difficulties[level])

        try:
            user_word = inputimeout(prompt=f"You have {timer_time} seconds to enter a word using the chunk: ", timeout=timer_time)
        except TimeoutOccurred:
            print("Time's up! You failed to enter a word in time.")
            if lives == 0:
                print("You have no lives left! Game over!")
                won = True
            else:
                print(f"You have {lives} lives left.")
                lives -= 1
            time.sleep(1)
            continue
        user_word_clean = user_word.strip().lower()
        if see_if_in_dictionary(user_word_clean) and chunk.lower() in user_word_clean:
            print("correct!")
            guessed_words.append(user_word_clean)
            time.sleep(1)
            timer_time = round(timer_time * 0.99, 4)
            to_next_level += 1
        else:
            if lives == 0:
                print("You have no lives left! Game over!")
                won = True
            else:
                print(f"incorrect! You have {lives} lives left.")
                lives -= 1
                timer_time = default_timer_time
                time.sleep(1)
        if to_next_level == 5:
            if level == 2 and mode.lower() != "forever":
                print("You have completed the game! Congratulations!")
                won = True
            else:
                if level < 2:
                    level += 1
                    to_next_level = 0
                    print("You advanced to the next level!")
                    time.sleep(1)


            
        