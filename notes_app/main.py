import os
import argparse
import sys
import subprocess
from notes_app.utils import get_note_actual_title
from notes_app.note_operations import (
    create_note_file, _list_notes_internal, NOTES_STORAGE_DIR, get_note_content
)
from notes_app.menu import run_menu
from notes_app.intro import play_intro # Import the intro function
from notes_app.utils import get_note_actual_title, load_settings

def main():
    # If no arguments are provided, run the menu.
    if len(sys.argv) == 1:
        settings = load_settings()
        if settings.get("play_intro", True):
            play_intro() # Play the intro animation first
        run_menu()
    else:
        parser = argparse.ArgumentParser(description="A simple CLI notes app.")
        parser.add_argument("command", choices=["add", "list", "view", "delete", "edit"], help="Command to execute")
        parser.add_argument("--title", help="Title of the note")

        args = parser.parse_args()

        # For direct commands, ensure we use the provided --title rather than prompting
        if args.title:
            target_filename = None
            if os.path.exists(NOTES_STORAGE_DIR):
                for filename in os.listdir(NOTES_STORAGE_DIR):
                    if filename.endswith(".txt") and get_note_actual_title(filename) == args.title:
                        target_filename = filename
                        break

            if not target_filename and args.command in ["view", "delete", "edit"]:
                print(f"Error: Note '{args.title}' not found.")
                sys.exit(1)
        else:
            if args.command in ["view", "delete", "edit"]:
                print(f"Error: --title is required for the '{args.command}' command when not using menu.")
                sys.exit(1)

        if args.command == "add":
            title = args.title if args.title else input("Enter note title: ")
            print("Enter note content (type 'EOF' on a new line to finish):")
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
        elif args.command == "list":
            _list_notes_internal(include_numbers=False)
        elif args.command == "view":
            content = get_note_content(args.title)
            print(f"\n--- {args.title} ---")
            print(content)
            print(f"--- End of {args.title} ---")
        elif args.command == "delete":
            file_path = os.path.join(NOTES_STORAGE_DIR, target_filename)
            os.remove(file_path)
            print(f"Note '{args.title}' deleted.")
        elif args.command == "edit":
            file_path = os.path.join(NOTES_STORAGE_DIR, target_filename)
            editor = os.environ.get('EDITOR')
            if editor is None:
                try:
                    subprocess.run(['micro', '-version'], check=True, capture_output=True)
                    editor = 'micro'
                except (FileNotFoundError, subprocess.CalledProcessError):
                    editor = 'nano'
            try:
                print(f"Opening '{args.title}' in {editor}...")
                subprocess.run([editor, file_path])
            except FileNotFoundError:
                print(f"Error: Editor '{editor}' not found. Please set your EDITOR environment variable or install micro/nano/vi.")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
