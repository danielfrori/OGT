# OGT

A simple system tray app in Python that provides a customizable menu with links, commands, and actions.

## Features

- Create and customize your own system tray menu
- Open webpages from the tray
- Execute terminal commands (with optional confirmation dialogs)
- Run scripts

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

## Item Types

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

## Presets

The app auto-generates your config using the provided presets:

- `presets/linux_config.json` — Linux preset with links and Steam shortcuts
- `presets/win_config.json` — Windows preset with system commands

These are used when you don't have a config file yet.

## Icon

Replace `icon.ico` with your own .ico file for custom tray icon.