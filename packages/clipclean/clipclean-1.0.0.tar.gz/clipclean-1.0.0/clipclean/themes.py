"""Theme management for ClipClean GUI"""

import tkinter as tk
from tkinter import ttk
import platform
import subprocess


class ThemeManager:
    """Manages light and dark themes for the application"""
    
    def __init__(self):
        self.current_theme = "auto"
        self.themes = {
            "light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "select_bg": "#0078d4",
                "select_fg": "#ffffff",
                "entry_bg": "#ffffff",
                "entry_fg": "#000000",
                "button_bg": "#f0f0f0",
                "button_fg": "#000000",
                "frame_bg": "#f8f9fa",
                "accent": "#0078d4",
                "success": "#107c10",
                "warning": "#ff8c00",
                "error": "#d13438",
                "border": "#d1d1d1",
                "text_bg": "#ffffff",
                "text_fg": "#000000",
                "text_select_bg": "#0078d4",
                "text_select_fg": "#ffffff"
            },
            "dark": {
                "bg": "#2d2d30",
                "fg": "#cccccc",
                "select_bg": "#3794ff",
                "select_fg": "#ffffff",
                "entry_bg": "#3c3c3c",
                "entry_fg": "#cccccc",
                "button_bg": "#404040",
                "button_fg": "#cccccc",
                "frame_bg": "#252526",
                "accent": "#3794ff",
                "success": "#4ec9b0",
                "warning": "#ffcc02",
                "error": "#f44747",
                "border": "#464647",
                "text_bg": "#1e1e1e",
                "text_fg": "#cccccc",
                "text_select_bg": "#3794ff",
                "text_select_fg": "#ffffff"
            }
        }
    
    def detect_system_theme(self):
        """Detect system theme preference"""
        try:
            system = platform.system()
            
            if system == "Darwin":  # macOS
                result = subprocess.run(
                    ["defaults", "read", "-g", "AppleInterfaceStyle"],
                    capture_output=True, text=True, timeout=2
                )
                return "dark" if result.returncode == 0 and "Dark" in result.stdout else "light"
            
            elif system == "Windows":
                try:
                    import winreg
                    key = winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER,
                        r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
                    )
                    value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                    winreg.CloseKey(key)
                    return "light" if value else "dark"
                except:
                    return "light"
            
            # Linux and others - try to detect from environment
            elif system == "Linux":
                # Check for common dark theme indicators
                dark_indicators = [
                    "GNOME_DESKTOP_SESSION_ID",
                    "KDE_FULL_SESSION"
                ]
                # This is a simplified detection - could be enhanced
                return "light"
                
        except:
            pass
        
        return "light"  # Default fallback
    
    def get_theme(self, theme_name=None):
        """Get theme colors"""
        if theme_name is None:
            theme_name = self.current_theme
        
        if theme_name == "auto":
            theme_name = self.detect_system_theme()
        
        return self.themes.get(theme_name, self.themes["light"])
    
    def apply_theme(self, root, theme_name="auto"):
        """Apply theme to the root window and all widgets"""
        self.current_theme = theme_name
        theme = self.get_theme()
        
        # Configure ttk style
        style = ttk.Style()
        
        # Set theme based on platform
        if platform.system() == "Darwin":
            style.theme_use('aqua')
        elif platform.system() == "Windows":
            style.theme_use('vista')
        else:
            style.theme_use('clam')
        
        # Configure custom styles
        style.configure("Title.TLabel", 
                       font=("Helvetica", 16, "bold"),
                       foreground=theme["fg"],
                       background=theme["bg"])
        
        style.configure("Heading.TLabel",
                       font=("Helvetica", 11, "bold"),
                       foreground=theme["fg"],
                       background=theme["bg"])
        
        style.configure("Custom.TFrame",
                       background=theme["frame_bg"],
                       relief="flat",
                       borderwidth=1)
        
        # Configure labelframe - use map for proper theme support
        style.configure("Custom.TLabelFrame",
                       background=theme["frame_bg"],
                       foreground=theme["fg"],
                       borderwidth=1)
        
        style.configure("Custom.TLabelFrame.Label",
                       background=theme["frame_bg"],
                       foreground=theme["accent"],
                       font=("Helvetica", 10, "bold"))
        
        style.configure("Primary.TButton",
                       font=("Helvetica", 10, "bold"))
        
        style.configure("Success.TButton",
                       foreground=theme["success"])
        
        style.configure("Warning.TButton",
                       foreground=theme["warning"])
        
        style.configure("Danger.TButton",
                       foreground=theme["error"])
        
        # Configure root window
        root.configure(bg=theme["bg"])
        
        return theme