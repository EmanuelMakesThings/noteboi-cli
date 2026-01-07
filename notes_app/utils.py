import os
import sys
import tty
import termios
import json

# ANSI Colors
RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[94m"
CYAN = "\033[96m"
WHITE = "\033[97m"
YELLOW = "\033[93m"

# Absolute path to the project root's data directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES_STORAGE_DIR = os.path.join(PROJECT_ROOT, "data")
SETTINGS_FILE = os.path.join(PROJECT_ROOT, "settings.json")

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_note_actual_title(filename):
    """Extracts the actual title from a filename (e.g., 'My Note.txt' -> 'My Note')."""
    return os.path.splitext(filename)[0]

def get_note_file_path(filename):
    """Returns the full path for a given filename."""
    return os.path.join(NOTES_STORAGE_DIR, filename)

def get_key():
    """Reads a single keypress from stdin."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch += sys.stdin.read(2) # Read arrow keys
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def show_selection_menu(options, title="Select an option:"):
    """
    Displays an interactive selection menu.
    
    Args:
        options: List of strings or tuples (label, value). If strings, value is same as label.
        title: Title to display above menu.
        
    Returns:
        The selected value, or None if cancelled (if 'Exit' or 'Back' logic is handled by caller, 
        but here we generally return the index or value).
    """
    current_row = 0
    
    # Normalize options to (label, value)
    normalized_options = []
    for opt in options:
        if isinstance(opt, tuple):
            normalized_options.append(opt)
        else:
            normalized_options.append((opt, opt))
            
    while True:
        clear_screen()
        print(f"{CYAN}{BOLD}{title}{RESET}")
        print(f"{BLUE}-------------------{RESET}")
        
        for idx, (label, _) in enumerate(normalized_options):
            if idx == current_row:
                print(f"{BLUE}> {CYAN}{BOLD}{label}{RESET}")
            else:
                print(f"  {WHITE}{label}{RESET}")
                
        print(f"{BLUE}-------------------{RESET}")
        print(f"{WHITE}(Use Arrow Keys to Navigate, Enter to Select){RESET}")

        key = get_key()
        
        if key == '\x1b[A': # Up arrow
            current_row = (current_row - 1) % len(normalized_options)
        elif key == '\x1b[B': # Down arrow
            current_row = (current_row + 1) % len(normalized_options)
        elif key == '\r': # Enter key
            return normalized_options[current_row][1]
        elif key == '\x03': # Ctrl+C
            sys.exit(0)

# Settings Management
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"play_intro": True}
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"play_intro": True}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)