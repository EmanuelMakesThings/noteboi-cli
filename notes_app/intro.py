import time
import sys
from notes_app.utils import clear_screen, Colors

def typewriter_print(text, delay=0.05, color=None, newline=True):
    """Prints text character by character with a delay and optional color."""
    if color:
        sys.stdout.write(color)
    
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    
    if color:
        sys.stdout.write(Colors.RESET)
    
    if newline:
        print() 

def play_intro():
    clear_screen()
    
    time.sleep(1) # Initial pause

    # Line 1: Welcome to noteBoi CLI
    sys.stdout.write("         ")
    typewriter_print("Welcome to ", delay=0.05, color=Colors.WHITE, newline=False)
    typewriter_print("noteBoi CLI", delay=0.07, color=Colors.CYAN + Colors.BOLD, newline=True)
    time.sleep(0.5)

    # Line 2: Organize your thoughts
    sys.stdout.write("         ")
    typewriter_print("Organize your thoughts", delay=0.05, color=Colors.WHITE, newline=True)
    time.sleep(0.5)

    # Space for visual separation
    print()

    # Line 3: Designed by...
    sys.stdout.write("         ")
    typewriter_print("Designed by Jonah Cecil", delay=0.05, color=Colors.BLUE, newline=True)
    time.sleep(0.5)

    print("\n")
    sys.stdout.write("         ") # Indent prompt
    typewriter_print("READY > ", delay=0.05, color=Colors.CYAN + Colors.BOLD, newline=False)
    input() # Wait for user to press Enter
    clear_screen()

if __name__ == "__main__":
    play_intro()
