import os
import datetime
import subprocess
import sys
from notes_app.utils import (
    get_note_actual_title, show_selection_menu, clear_screen,
    NOTES_STORAGE_DIR, Colors, load_settings, get_preferred_editor_command
)

def _ensure_notes_dir_exists():
    if not os.path.exists(NOTES_STORAGE_DIR):
        os.makedirs(NOTES_STORAGE_DIR)

def _get_file_info(filename):
    file_path = os.path.join(NOTES_STORAGE_DIR, filename)
    if os.path.exists(file_path):
        size_bytes = os.path.getsize(file_path)
        size_str = f"{size_bytes} B" if size_bytes < 1024 else f"{size_bytes / 1024:.2f} KB"
        timestamp = os.path.getmtime(file_path)
        last_modified = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return size_str, last_modified
    return "N/A", "N/A"

def create_note_file(title, content):
    _ensure_notes_dir_exists()
    sanitized_title = "".join(c for c in title if c.isalnum() or c in (' ', '.', '_')).rstrip()
    filename = f"{sanitized_title}.txt"
    file_path = os.path.join(NOTES_STORAGE_DIR, filename)
    with open(file_path, "w") as f:
        f.write(content)
    size, last_mod = _get_file_info(filename)
    return {"title": sanitized_title, "size": size, "last_modified": last_mod}

def list_notes_for_api():
    if not os.path.exists(NOTES_STORAGE_DIR):
        return []
    notes = []
    for filename in sorted(os.listdir(NOTES_STORAGE_DIR)):
        if filename.endswith(".txt"):
            size, last_mod = _get_file_info(filename)
            notes.append({
                "title": get_note_actual_title(filename),
                "size": size,
                "last_modified": last_mod
            })
    return notes

def get_note_content(title):
    filename = f"{title}.txt"
    file_path = os.path.join(NOTES_STORAGE_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return None

def delete_note_by_title(title):
    filename = f"{title}.txt"
    file_path = os.path.join(NOTES_STORAGE_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

# --- CLI Interactive Functions ---

def _get_sorted_notes_files():
    _ensure_notes_dir_exists()
    return sorted([f for f in os.listdir(NOTES_STORAGE_DIR) if f.endswith(".txt")])

def add_note():
    print(f"{Colors.CYAN}{Colors.BOLD}Add New Note{Colors.RESET}")
    print(f"{Colors.BLUE}-------------------{Colors.RESET}")
    title = input(f"{Colors.WHITE}Enter note title: {Colors.RESET}").strip()
    if not title:
        print(f"{Colors.WHITE}Error: Title cannot be empty.{Colors.RESET}")
        return
    print(f"{Colors.WHITE}Enter note content (type 'EOF' on a new line to finish):{Colors.RESET}")
    content_lines = []
    while True:
        try:
            line = sys.stdin.readline().strip()
        except KeyboardInterrupt:
            print("\nNote creation cancelled.")
            return
        if line == "EOF":
            break
        content_lines.append(line)
    content = "\n".join(content_lines)
    create_note_file(title, content)
    print(f"{Colors.CYAN}Note '{title}' added successfully.{Colors.RESET}")
    input(f"\n{Colors.BLUE}Press Enter to return to menu...{Colors.RESET}")

def _list_notes_internal(include_numbers=True):
    notes = _get_sorted_notes_files()
    if not notes:
        print(f"{Colors.WHITE}No notes found.{Colors.RESET}")
        return []
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}--- Current Notes ---{Colors.RESET}")
    for i, filename in enumerate(notes, 1):
        title = get_note_actual_title(filename)
        size, last_mod = _get_file_info(filename)
        prefix = f"{i}. " if include_numbers else "- "
        print(f"{Colors.WHITE}{prefix}{title} {Colors.BLUE}(Size: {size}, Modified: {last_mod}){Colors.RESET}")
    return notes

def list_notes():
    _list_notes_internal(include_numbers=False)
    input(f"\n{Colors.BLUE}Press Enter to return to menu...{Colors.RESET}")

def view_note():
    notes = _get_sorted_notes_files()
    if not notes:
        print(f"{Colors.WHITE}No notes found to view.{Colors.RESET}")
        input(f"\n{Colors.BLUE}Press Enter to return to menu...{Colors.RESET}")
        return
    
    options = []
    for filename in notes:
        title = get_note_actual_title(filename)
        options.append((title, title))
    
    options.append(("Cancel", None))

    selected_title = show_selection_menu(options, title="Select Note to View")
    
    if selected_title:
        clear_screen()
        content = get_note_content(selected_title)
        print(f"{Colors.CYAN}{Colors.BOLD}--- {selected_title} ---{Colors.RESET}")
        print(f"{Colors.WHITE}{content}{Colors.RESET}")
        print(f"{Colors.BLUE}" + "-" * (len(selected_title) + 8) + f"{Colors.RESET}")
        input(f"\n{Colors.BLUE}Press Enter to return to menu...{Colors.RESET}")

def edit_note():
    notes = _get_sorted_notes_files()
    if not notes:
        print(f"{Colors.WHITE}No notes found to edit.{Colors.RESET}")
        input(f"\n{Colors.BLUE}Press Enter to return to menu...{Colors.RESET}")
        return
    
    options = []
    for filename in notes:
        title = get_note_actual_title(filename)
        options.append((title, title))
    
    options.append(("Cancel", None))

    selected_title = show_selection_menu(options, title="Select Note to Edit")

    if selected_title:
        filename = f"{selected_title}.txt"
        file_path = os.path.join(NOTES_STORAGE_DIR, filename)
        
        editor = get_preferred_editor_command()
        
        print(f"{Colors.WHITE}Opening '{selected_title}' in {editor}...{Colors.RESET}")
        try:
            subprocess.run([editor, file_path])
        except FileNotFoundError:
             print(f"{Colors.WHITE}Error: Editor '{editor}' not found. Please check your settings or installation.{Colors.RESET}")
             input(f"\n{Colors.BLUE}Press Enter to return to menu...{Colors.RESET}")

def delete_note():
    # Explicitly NOT using a selection menu for safety, as requested.
    # User must type the exact name.
    
    _list_notes_internal(include_numbers=False)
    print(f"\n{Colors.BLUE}-------------------{Colors.RESET}")
    
    notes = _get_sorted_notes_files()
    if not notes:
        input(f"\n{Colors.BLUE}Press Enter to return to menu...{Colors.RESET}")
        return

    try:
        print(f"{Colors.WHITE}To delete a note, please type its {Colors.BOLD}EXACT{Colors.RESET}{Colors.WHITE} name.{Colors.RESET}")
        target_title = input(f"{Colors.CYAN}Note Name > {Colors.RESET}").strip()
        
        if not target_title:
            return

        # Check if note exists
        found = False
        for filename in notes:
            if get_note_actual_title(filename) == target_title:
                found = True
                break
        
        if found:
            confirm = input(f"{Colors.WHITE}Are you sure you want to delete '{target_title}'? (y/N): {Colors.RESET}").lower()
            if confirm == 'y':
                if delete_note_by_title(target_title):
                    print(f"{Colors.CYAN}Note '{target_title}' deleted.{Colors.RESET}")
                else:
                    print(f"{Colors.WHITE}Failed to delete note.{Colors.RESET}")
            else:
                print(f"{Colors.WHITE}Deletion cancelled.{Colors.RESET}")
        else:
            print(f"{Colors.WHITE}Note '{target_title}' not found.{Colors.RESET}")

    except KeyboardInterrupt:
        print(f"\n{Colors.WHITE}Operation cancelled.{Colors.RESET}")

    input(f"\n{Colors.BLUE}Press Enter to return to menu...{Colors.RESET}")