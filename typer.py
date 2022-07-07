from curses import wrapper
import curses
import random
import time

sentences = [
    "The miniature pet elephant became the envy of the neighborhood.",
    "He decided to live his life by the big beats manifesto.",
    "The light in his life was actually a fire burning all around him.",
    "There aren't enough towels in the world to stop the sewage flowing from his mouth.",
    "It's a skateboarding penguin with a sunhat!",
    "Purple is the best city in the forest.",
    "Kevin embraced his ability to be at the wrong place at the wrong time.",
    "This book is sure to liquefy your brain.",
    "My Mum tries to be cool by saying that she likes all the same things that I do.",
    "Sarah ran from the serial killer holding a jug of milk.",
    "Everything was going so well until I was accosted by a purple giraffe.",
    "In the end, he realized he could see sound and hear words.",
    "They got there early, and they got really good seats.",
    "Seek success, but always be prepared for random cats.",
    "He was an introvert that extroverts seemed to love.",
    "Blue sounded too cold at the time and yet it seemed to work for gin.",
    "It's always a good idea to seek shelter from the evil gaze of the sun.",
    "He picked up trash in his spare time to dump in his neighbor's yard.",
    "They throw cabbage that turns your brain into emotional baggage.",
    "The lyrics of the song sounded like fingernails on a chalkboard.",
    "Bill ran from the giraffe toward the dolphin.",
    "Today arrived with a crash of my car through the garage door.",
    "I would have gotten the promotion, but my attendance wasn’t good enough.",
    "The crowd yells and screams for more memes.",
    "The irony of the situation wasn't lost on anyone in the room.",
    "I ate a sock because people on the Internet told me to.",
    "She saw the brake lights, but not in time.",
    "I’m working on a sweet potato farm.",
    "the simplest sentence here"
]


def position_cursor(stdscr, target_text, current_text):
    ''' Cursor is meaningless, but for ease of use and aesthetics
        the cursor has to be manually moved to the letter/word that
        the user is currently typing'''
    stdscr.move(curses.LINES // 2, (curses.COLS // 2 - len(target_text) // 2) + len(current_text) + 1)


def print_ending(stdscr, wpm):
    '''clears the screen, outputs results
        waits for enter, else it quits the game'''
    stdscr.clear()
    stdscr.addstr(
        curses.LINES // 2 - 2,
        curses.COLS // 2 - len("Your scored:") // 2,
        "Your scored:",
    )
    stdscr.addstr(
        curses.LINES // 2,
        curses.COLS // 2 - len(f"{wpm} WPM") // 2,
        f"{wpm} WPM",
        curses.color_pair(1)
    )
    stdscr.addstr(
        curses.LINES // 2 + 2,
        curses.COLS // 2 - len("Press enter to play again") // 2,
        "Press enter to play again"
    )
    while True:
        try:
            key = stdscr.getkey()
            if ord(key) == 10: ## 10 is enter
                stdscr.clear()
                wrapper(main) ## run game again
            else:
                break ## if enter is not pressed, quit the loop / quit the game
        except:
            pass ## as getkey is not blocking, it will throw an exception every time a user does not press a key


def print_correct_word(stdscr, current_text: list[str], target_text: str):
    ''' checks for correct location to print the green, red and grey characters
        returns TRUE if the user has successfully finished and the sentences match'''
    if "".join(current_text) == target_text:
        return True

    for index, char in enumerate(current_text):
        color = curses.color_pair(2) ## add red if they are wrong
        char_to_show = target_text[index]
        if len(current_text) > len(target_text):
            pass
        elif char == target_text[index]:
            color = curses.color_pair(1) ## add green if char both sentences match
            char_to_show = char
        stdscr.addstr(
            curses.LINES // 2,
            curses.COLS // 2 - len(target_text) // 2 + index + 1,
            char_to_show,
            color
        )

    position_cursor(stdscr, target_text, current_text)
    #stdscr.move(curses.LINES // 2, ((curses.COLS // 2 - len(target_text)) + len(current_text)) + 5)
    stdscr.addstr(target_text[len(current_text):], curses.color_pair(3)) ## fill in what is not written with grey

    return False

 

def wpm_test(stdscr, target_text):
    '''Main loop of the game, calls all the functions above'''
    current_text = []
    start_time = time.time()
    stdscr.nodelay(True)
    stdscr.clear()

    welcome_message = "Below is the sentence you will have to type:"
    start_message = "Begin typing the sentence above to start."

    stdscr.addstr(
        (curses.LINES // 2) - 2,
        (curses.COLS // 2) - len(welcome_message) // 2,
        welcome_message
    )
    stdscr.addstr(
        (curses.LINES // 2),
        (curses.COLS // 2) - len(target_text) // 2,
        target_text,
        curses.color_pair(1)
    )
    stdscr.addstr(
        (curses.LINES // 2) + 2,
        (curses.COLS // 2) - len(start_message) // 2,
        start_message
    )
    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
        
        if len(current_text) > 0:
            wpm_text = f"WPM: {wpm}"

            stdscr.addstr(
                (curses.LINES // 2) - 2,
                (curses.COLS // 2) - len(wpm_text) // 2,
                wpm_text
            )

            position_cursor(stdscr, target_text, current_text)
        try:
            key = stdscr.getkey()
        except:
            continue
        
        try:
            ord(key) ## if the key is KEY_DOWN, for example, it will be changed to 0
        except:
            key = 0

        if ord(key) == 27:
            break
        elif ord(key) == 8 and len(current_text) > 0:
            current_text.pop()
        elif len(current_text) +1 <= len(target_text):
            current_text.append(key)
   
        stdscr.clear()
    
        if print_correct_word(stdscr, current_text, target_text):
            print_ending(stdscr, wpm)
            break

        position_cursor(stdscr, target_text, current_text)
    
        stdscr.refresh()

    
def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(3, 8, -1) ## grey

    wpm_test(stdscr, target_text=random.choice(sentences)) ## starts the game

wrapper(main)
