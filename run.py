#!/usr/bin/env python3
import sys
import os

# Add the current directory to sys.path so we can import notes_app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from notes_app.main import main

if __name__ == "__main__":
    main()
