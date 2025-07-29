# Recommended Codebase Structure for Discord Translation Bot

## Overview
To keep the codebase clean, maintainable, and scalable, split logic into focused modules and directories. This structure is ideal for collaborative work and future feature expansion.

---

## Directory Layout
```
src/
  main.py
  db.py
  utils.py
  constants.py
  commands/
    __init__.py
    user_commands.py
    admin_commands.py
    misc_commands.py
```

---

## File Responsibilities

### `main.py`
- Bot instantiation
- Event hooks (`on_ready`, `on_message`, etc.)
- Imports and registers commands from the `commands/` package
- Main entrypoint

### `db.py`
- All database logic (CRUD operations, schema setup, etc.)

### `utils.py`
- Helper functions (e.g., `preserve_user_mentions`, `restore_mentions`, `translate_message`, `detect_language`)

### `constants.py`
- Constants like `SUPPORTED_LANGUAGES` and any other global config

### `commands/` package
- **`user_commands.py`**: User-facing commands (e.g., `setlang`, `mylang`, `languages`, `ping`)
- **`admin_commands.py`**: Admin-only commands (e.g., `settranschannel`, `addtranschannel`, `removetranschannel`, `listtranschannels`, `setchannellang`, `debugdb`)
- **`misc_commands.py`**: Miscellaneous or meta commands (e.g., custom `help`)
- Each file exports a `setup(bot)` function to register its commands

---

## Example: Registering Commands in `main.py`
```python
from commands import user_commands, admin_commands, misc_commands

user_commands.setup(bot)
admin_commands.setup(bot)
misc_commands.setup(bot)
```

---

## Benefits
- **Separation of concerns**: Each file has a clear purpose
- **Scalability**: Easy to add new features or commands
- **Testability**: Smaller, focused modules are easier to test
- **Readability**: No more scrolling through a massive `main.py`

---

_Stick to this structure and your future self (and teammates) will thank you!_ 