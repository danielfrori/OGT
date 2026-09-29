# OGT

A system tray app in Python that provides a customizable menu with links, commands, and actions.

## Features

- Create and customize your own system tray menu
- Open webpages from the tray
- Execute terminal commands (with optional confirmation dialogs)
- Run scripts

## Requirements

- Python 3.8 or newer
- `pystray` and `Pillow` (see `requirements.txt`)
- `tkinter` (used for confirmation and error dialogs).

## Installation

```bash
git clone https://github.com/danielfrori/OGT.git
cd OGT
pip install -r requirements.txt
```

## Usage

**Linux/macOS:** `python main.py` or use `ogt.sh`

**Windows:** Run `main.py` directly or double-click `OGT.bat`

## Config Location

- **Linux**: `~/.config/ogt/config.json`
- **Windows**: `%APPDATA%\OGT\config.json`

## Configuration

Edit your config file with JSON:

```json
[
    {
        "name": "Web Links",
        "submenu": [
            {"name": "GitHub", "type": "webpage", "url": "https://github.com"},
            {"name": "Google", "type": "webpage", "url": "https://google.com"}
        ]
    },
    {
        "name": "System",
        "submenu": [
            {"name": "Restart PC", "type": "command", "command": ["shutdown", "/r", "/t", "0"], "confirm": true, "confirm_message": "Restart?"},
            {"name": "Quit", "type": "function", "function": "quit"}
        ]
    }
]
```

### Notes

- Commands should be lists, like `["echo", "test"]`. Use full paths where you can, especially on Windows.
- `webpage` only opens `http://` and `https://` links. Other schemes (such as `file://`) are blocked.
- If a menu entry is invalid (missing `name`, unknown `type`, missing `url`/`command`/`function`, and so on), it is skipped and the reason is printed to the console. The rest of the menu still loads.
- If the config file can't be read, contains invalid JSON, or has no valid entries, OGT shows an error dialog and exits.

### Item Types

| Type | Description | Example |
|------|-------------|---------|
| `webpage` | Opens a URL | `"url": "https://example.com"` |
| `command` | Runs terminal command | `"command": ["echo", "test"]` |
| `separator` | Visual divider | `"type": "separator"` |
| `submenu` | Nested menu items | `"submenu": [...]` |
| `function` | App actions | `"function": "quit"` or `"restart"` |

### Commands with Confirmation

Add `confirm: true` and `confirm_message` to require user approval:

```json
{
    "name": "Shutdown",
    "type": "command",
    "command": ["shutdown", "/s"],
    "confirm": true,
    "confirm_message": "Shut down?"
}
```

### Icon

Replace `icon.ico` with your own .ico file for custom tray icon.

### Presets

The app auto-generates your config using the provided presets:

- `presets/linux_config.json` — Linux preset with links and Steam shortcuts
- `presets/win_config.json` — Windows preset with system commands

These are used when you don't have a config file yet.

---

OGT is released under the [MIT License](LICENSE).