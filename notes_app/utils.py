import os
import sys
import tty
import termios
import json
import subprocess

# ANSI Colors
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    MAGENTA = "\033[95m"

# Theme Definitions
THEMES = {
    "Default": {
        "BLUE": "\033[94m",
        "CYAN": "\033[96m",
        "WHITE": "\033[97m",
        "YELLOW": "\033[93m"
    },
    "Dracula": {
        "BLUE": "\033[38;5;61m",  # Purple/Blue
        "CYAN": "\033[38;5;117m", # Light Blue
        "WHITE": "\033[38;5;231m", # White
        "YELLOW": "\033[38;5;84m"  # Greenish
    },
    "Matrix": {
        "BLUE": "\033[32m",       # Green
        "CYAN": "\033[92m",       # Bright Green
        "WHITE": "\033[37m",      # Light Gray
        "YELLOW": "\033[33m"      # Yellow (keep for variety or make green?)
    },
    "Fire": {
        "BLUE": "\033[91m",       # Red
        "CYAN": "\033[93m",       # Yellow
        "WHITE": "\033[97m",      # White
        "YELLOW": "\033[31m"      # Dark Red
    }
}

def apply_theme(theme_name):
    """Updates Colors class attributes based on the selected theme."""
    theme = THEMES.get(theme_name, THEMES["Default"])
    Colors.BLUE = theme.get("BLUE", "\033[94m")
    Colors.CYAN = theme.get("CYAN", "\033[96m")
    Colors.WHITE = theme.get("WHITE", "\033[97m")
    Colors.YELLOW = theme.get("YELLOW", "\033[93m")

# Deprecated: Backwards compatibility aliases (static, won't update with theme)
RESET = Colors.RESET
BOLD = Colors.BOLD
BLUE = Colors.BLUE
CYAN = Colors.CYAN
WHITE = Colors.WHITE
YELLOW = Colors.YELLOW

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
        print(f"{Colors.CYAN}{Colors.BOLD}{title}{Colors.RESET}")
        print(f"{Colors.BLUE}-------------------{Colors.RESET}")
        
        for idx, (label, _) in enumerate(normalized_options):
            if idx == current_row:
                print(f"{Colors.BLUE}> {Colors.CYAN}{Colors.BOLD}{label}{Colors.RESET}")
            else:
                print(f"  {Colors.WHITE}{label}{Colors.RESET}")
                
        print(f"{Colors.BLUE}-------------------{Colors.RESET}")
        print(f"{Colors.WHITE}(Use Arrow Keys to Navigate, Enter to Select){Colors.RESET}")

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
    settings = {"play_intro": True, "theme": "Default", "preferred_editor": "Auto"}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                loaded = json.load(f)
                settings.update(loaded)
        except:
            pass
    
    apply_theme(settings.get("theme", "Default"))
    return settings

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def get_preferred_editor_command():
    """
    Determines the best editor command based on settings and availability.
    Priority: Settings > micro > $EDITOR > nano > vi
    """
    settings = load_settings()
    preferred = settings.get("preferred_editor", "Auto")
    
    if preferred != "Auto":
        return preferred

    # Check for micro
    try:
        subprocess.run(['micro', '-version'], check=True, capture_output=True)
        return 'micro'
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    # Check for $EDITOR
    env_editor = os.environ.get('EDITOR')
    if env_editor:
        return env_editor

    # Check for nano
    try:
        subprocess.run(['nano', '--version'], check=True, capture_output=True)
        return 'nano'
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    
    # Fallback
    return 'vi'
