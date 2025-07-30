# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ClipClean is a modern Python GUI application designed specifically for cleaning text copied from LLM outputs. It features automatic dark/light mode detection, enhanced user experience, and sophisticated text processing optimized for AI-generated content.

## Architecture

- **Package Structure**: Proper Python package with `clipclean/` directory
- **Main Components**:
  - `clipclean/gui.py` - Modern Tkinter GUI with dual-pane interface, theme support, and enhanced UX
  - `clipclean/cleaner.py` - LLM-focused text cleaning engine
  - `clipclean/themes.py` - System theme detection and management
  - `clipclean/__init__.py` - Package initialization
- **Text Processing**: Specialized for LLM output issues (smart quotes, Unicode normalization, markdown artifacts)
- **Theme System**: Automatic detection of system dark/light mode with manual override
- **Dependencies**: Minimal - only `pyperclip` for clipboard operations

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Running the Application
```bash
# Run as module
python -m clipclean.gui

# Or after installation
clipclean
```

### Testing and Building
```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
python test_cleaning.py

# Build package
python -m build

# Build executable (requires PyInstaller)
pyinstaller clipclean.spec
```

## Key Components

- **LLMTextCleaner class** (`cleaner.py`): Core cleaning logic targeting LLM-specific issues
  - Character replacement for smart quotes, dashes, spaces
  - Unicode normalization to ASCII equivalents
  - Formatting fixes for common LLM artifacts
  - Whitespace normalization
- **ClipCleanGUI class** (`gui.py`): Modern two-pane interface
  - Auto-paste functionality
  - Real-time character counting and reduction stats
  - Enhanced keyboard shortcuts
  - Visual feedback and status indicators
  - Settings persistence
  - Professional, focused UI
- **ThemeManager class** (`themes.py`): Theme detection and management
  - System theme detection (macOS, Windows, Linux)
  - Automatic theme switching
  - Manual theme override

## Python Requirements

- Python 3.8+ (broad compatibility)
- Cross-platform compatibility (Windows, macOS, Linux)
- GUI framework: Tkinter (included with Python)
- External dependencies: pyperclip only

## Design Principles

- **Simplicity**: Single-purpose tool focused on LLM text cleaning
- **Speed**: Fast startup and processing for quick workflows
- **Usability**: Auto-paste and one-click cleaning for efficiency
- **Accessibility**: Automatic theme detection for better visibility
- **Persistence**: Remembers user preferences between sessions

## Production Features

- **GitHub Actions**: Automated PyPI publishing and executable building
- **Cross-platform**: Windows, macOS, and Linux executables
- **Professional Packaging**: Proper Python packaging with `pyproject.toml`
- **Release Management**: Automated version tagging and distribution