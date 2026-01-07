import sys
from notes_app.utils import (
    clear_screen, show_selection_menu, load_settings, save_settings,
    Colors, apply_theme, THEMES
)
from notes_app.note_operations import (
    add_note, list_notes, view_note, delete_note, edit_note
)

def run_settings_menu():
    """Runs the settings submenu."""
    while True:
        settings = load_settings()
        intro_status = "ON" if settings.get("play_intro", True) else "OFF"
        current_editor = settings.get("preferred_editor", "Auto")
        current_theme = settings.get("theme", "Default")
        
        options = [
            (f"Toggle Intro (Current: {intro_status})", "toggle_intro"),
            (f"Select Editor (Current: {current_editor})", "select_editor"),
            (f"Change Theme (Current: {current_theme})", "change_theme"),
            ("Back", "back")
        ]
        
        choice = show_selection_menu(options, title="Settings")
        
        if choice == "toggle_intro":
            settings["play_intro"] = not settings.get("play_intro", True)
            save_settings(settings)
        elif choice == "select_editor":
            editor_options = [
                ("Auto (micro -> $EDITOR -> nano -> vi)", "Auto"),
                ("micro", "micro"),
                ("nano", "nano"),
                ("vi", "vi"),
                ("vim", "vim"),
                ("Cancel", None)
            ]
            selected_editor = show_selection_menu(editor_options, title="Select Preferred Editor")
            if selected_editor:
                settings["preferred_editor"] = selected_editor
                save_settings(settings)
        elif choice == "change_theme":
            theme_options = [(theme, theme) for theme in THEMES.keys()]
            theme_options.append(("Cancel", None))
            
            selected_theme = show_selection_menu(theme_options, title="Select Theme")
            if selected_theme:
                settings["theme"] = selected_theme
                save_settings(settings)
                apply_theme(selected_theme)
        elif choice == "back":
            break

def run_menu():
    """Runs the main menu loop for the notes app using an interactive selection."""
    
    while True:
        options = [
            ("Add Note", "1"),
            ("Edit Note", "2"),
            ("View Note", "3"),
            ("List Note Properties", "4"),
            ("Delete Note", "5"),
            ("Settings", "7"),
            ("Exit", "6")
        ]
        
        choice = show_selection_menu(options, title=f"noteBoi CLI\n{Colors.YELLOW}v1.1.0{Colors.RESET}")

        if choice == '1':
            clear_screen()
            add_note()
        elif choice == '2':
            edit_note()
        elif choice == '3':
            view_note()
        elif choice == '4':
            clear_screen()
            list_notes()
        elif choice == '5':
            clear_screen()
            delete_note()
        elif choice == '7':
            run_settings_menu()
        elif choice == '6':
            print(f"{Colors.BLUE}Exiting noteBoi CLI. Goodbye!{Colors.RESET}")
            sys.exit(0)