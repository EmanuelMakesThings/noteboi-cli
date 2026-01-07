# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-01-07

### Added
- **Unified Settings Integration:** The `edit` command in the CLI now respects your `preferred_editor` setting from `settings.json`, ensuring a consistent experience whether you use the menu or direct commands.
- **Smart Editor Detection:** Added a robust `get_preferred_editor_command` utility that intelligently falls back from your settings -> `micro` -> `$EDITOR` -> `nano` -> `vi`.

### Fixed
- Removed a duplicate execution block in `main.py` that could cause the application to initialize incorrectly.
- Fixed inconsistent editor opening logic between the main menu and CLI arguments.

## [1.0.0] - 2026-01-01
- Initial release of noteBoi CLI.
- Basic note management (Add, Edit, View, Delete, List).
- Interactive Menu and CLI arguments support.
