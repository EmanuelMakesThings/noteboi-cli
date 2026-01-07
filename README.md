# noteBoi CLI


<img width="420" height="245" alt="Screenshot 2026-01-07 114350" src="https://github.com/user-attachments/assets/8937ea55-ed5d-4634-ad9a-cc1eec9710cd" />




**Organize your thoughts.**

noteBoi CLI is a stylish, interactive command-line application for managing your notes efficiently. Designed by Jonah Cecil.

## Features
- **Interactive Menu:** Navigate effortlessly with arrow keys.
- **Manage Notes:** Add, Edit, View, List Properties, and Delete notes.
- **Customizable:**
    - Toggle the "noteBoi" intro animation.
    - Select your preferred editor (`micro`, `nano`, `vi`, `vim`, or system default).
- **Persistent Storage:** Notes are safely stored as text files in the `data/` directory.
- **Direct CLI Commands:** Quick actions for power users.

## 🚀 What's New in v1.1.0
- **Unified Settings:** Your preferred editor and theme settings now apply to both the interactive menu and direct CLI commands.
- **Smart Editor Detection:** Improved logic to automatically find the best available editor on your system.
- **Stability Improvements:** Cleaned up internal logic for a smoother startup experience.

## Requirements
- Python 3.6+
- Linux/macOS (uses `tty`/`termios` for interactive inputs)

## Installation
Clone the repository and you're ready to go. No external dependencies required.

```bash
git clone https://github.com/yourusername/notes_cli.git
cd notes_cli
```

## Usage

### Interactive Mode (Recommended)
Launch the full experience:
```bash
python run.py
```
Use the **Arrow Keys** to navigate and **Enter** to select options.

### Command Line Mode
Perform quick operations directly:

**List note properties:**
```bash
python run.py list
```

**Add a note:**
```bash
python run.py add --title "My Idea"
```

**View a note:**
```bash
python run.py view --title "My Idea"
```

**Edit a note:**
```bash
python run.py edit --title "My Idea"
```

**Delete a note:**
```bash
python run.py delete --title "My Idea"
```

## Configuration
Settings are stored locally in `settings.json` and can be modified via the **Settings** menu in the app.

- **Intro:** Toggle the startup animation ON/OFF.
- **Editor:** Choose your preferred text editor for writing notes.

## Data Storage
All notes are stored as `.txt` files in the `data/` directory.

## Changelog
See [CHANGELOG.md](CHANGELOG.md) for a history of changes and updates.
