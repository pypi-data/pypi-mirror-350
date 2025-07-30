# ClipClean 🧹

A simple GUI tool for cleaning text copied from LLM (Large Language Model) outputs. Removes problematic Unicode characters, fixes formatting issues, and makes text ready for use in documents or other applications.

## Features

- **Simple Interface**: Clean, focused GUI designed for quick text cleaning
- **LLM-Optimized**: Specifically targets common issues in AI-generated text
- **Dark/Light Mode**: Automatic theme detection based on system settings
- **Auto-Paste**: Automatically loads clipboard content when opened
- **Smart Cleaning**: Handles Unicode normalization, smart quotes, special dashes, and more
- **Real-time Stats**: Shows character count and reduction percentage
- **Settings Persistence**: Remembers your preferences between sessions
- **Enhanced UX**: Visual feedback, status indicators, and smooth interactions

## Common Issues It Fixes

- Smart quotes (`"` → `"`)
- Special dashes (`–`, `—` → `-`)
- Non-breaking spaces and other invisible characters
- Excessive whitespace and line breaks
- Unicode characters that don't display properly
- Markdown formatting artifacts

## Installation

### From PyPI (recommended)
```bash
pip install clipclean
```

### Standalone Executables
Download pre-built executables from the [Releases](https://github.com/kevinobytes/clipclean/releases) page:
- **Windows**: `clipclean-windows.exe`
- **macOS**: `clipclean-macos`

### From Source
```bash
git clone https://github.com/kevinobytes/clipclean.git
cd clipclean
pip install -e .
```

## Usage

Simply run the application:
```bash
clipclean
```

### Quick Workflow
1. Copy text from your LLM (ChatGPT, Claude, etc.)
2. Open ClipClean (it auto-pastes)
3. Click "Clean" or let auto-clean do it
4. Copy the cleaned text

### Keyboard Shortcuts
- `Ctrl+V` - Paste from clipboard
- `Ctrl+C` - Copy cleaned text
- `F5` or `Ctrl+Return` - Clean text
- `Ctrl+L` - Clear all
- `Escape` - Clear all

### Theme Options
- **Auto**: Automatically detects system theme (default)
- **Light**: Light theme for all environments
- **Dark**: Dark theme for all environments

### Settings
- **Auto-paste on startup**: Automatically pastes clipboard content when the app opens
- **Auto-clean on paste**: Automatically cleans text when pasted
- **Theme preference**: Saved between sessions

## Requirements

- Python 3.8+
- tkinter (included with Python)
- pyperclip

## Development

```bash
# Clone and set up development environment
git clone https://github.com/yourusername/clipclean.git
cd clipclean
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .

# Run from source
python -m clipclean.gui
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.