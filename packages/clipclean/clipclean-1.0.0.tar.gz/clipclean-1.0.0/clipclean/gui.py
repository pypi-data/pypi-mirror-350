import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyperclip
import platform
import json
import os
from .cleaner import LLMTextCleaner
from .themes import ThemeManager


class ClipCleanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ClipClean - LLM Output Cleaner")
        self.root.geometry("900x700")
        self.root.minsize(700, 500)
        
        # Initialize components
        self.cleaner = LLMTextCleaner()
        self.theme_manager = ThemeManager()
        self.config_file = os.path.expanduser("~/.clipclean_config.json")
        
        # Load configuration
        self.load_config()
        
        # Apply theme
        self.current_theme = self.theme_manager.apply_theme(self.root, self.config.get("theme", "auto"))
        
        # Setup UI
        self.setup_ui()
        self.setup_bindings()
        
        # Auto-paste on startup if enabled
        if self.config.get("auto_paste", True):
            self.root.after(100, self.auto_paste)
        
        # Setup periodic theme checking for auto mode
        if self.config.get("theme", "auto") == "auto":
            self.root.after(5000, self.check_theme_change)
    
    def load_config(self):
        """Load user configuration"""
        default_config = {
            "theme": "auto",
            "auto_paste": True,
            "auto_clean": True,
            "window_geometry": "900x700"
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = {**default_config, **json.load(f)}
            else:
                self.config = default_config
        except:
            self.config = default_config
    
    def save_config(self):
        """Save user configuration"""
        try:
            self.config["window_geometry"] = self.root.geometry()
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass
    
    def setup_ui(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Header
        self.setup_header(main_frame)
        
        # Settings bar
        self.setup_settings_bar(main_frame)
        
        # Input area
        self.setup_input_area(main_frame)
        
        # Control buttons
        self.setup_controls(main_frame)
        
        # Output area
        self.setup_output_area(main_frame)
        
        # Status bar
        self.setup_status_bar(main_frame)
    
    def setup_header(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        header_frame.columnconfigure(1, weight=1)
        
        # Title with icon
        title_frame = ttk.Frame(header_frame)
        title_frame.grid(row=0, column=0, sticky="w")
        
        title_label = ttk.Label(title_frame, text="🧹 ClipClean", 
                               font=("Helvetica", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = ttk.Label(title_frame, text="LLM Output Cleaner", 
                                  font=("Helvetica", 10), 
                                  foreground=self.current_theme["accent"])
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Theme selector and quick actions
        controls_frame = ttk.Frame(header_frame)
        controls_frame.grid(row=0, column=2, sticky="e")
        
        # Theme selector
        theme_frame = ttk.Frame(controls_frame)
        theme_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(theme_frame, text="Theme:", font=("Helvetica", 9)).pack(side=tk.LEFT)
        
        self.theme_var = tk.StringVar(value=self.config.get("theme", "auto"))
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var,
                                  values=["auto", "light", "dark"], 
                                  state="readonly", width=8)
        theme_combo.pack(side=tk.LEFT, padx=(5, 0))
        theme_combo.bind("<<ComboboxSelected>>", self.on_theme_change)
        
        # Quick action buttons
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.pack(side=tk.LEFT)
        
        ttk.Button(buttons_frame, text="📋 Paste", 
                  command=self.paste_text, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="🧹 Clean", 
                  command=self.clean_text, width=8,
                  style="Primary.TButton").pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="📄 Copy", 
                  command=self.copy_cleaned, width=8).pack(side=tk.LEFT, padx=2)
    
    def setup_settings_bar(self, parent):
        settings_frame = ttk.Frame(parent)
        settings_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # Auto-paste setting
        self.auto_paste_var = tk.BooleanVar(value=self.config.get("auto_paste", True))
        auto_paste_cb = ttk.Checkbutton(settings_frame, text="Auto-paste on startup", 
                                       variable=self.auto_paste_var,
                                       command=self.on_setting_change)
        auto_paste_cb.pack(side=tk.LEFT, padx=(0, 20))
        
        # Auto-clean setting
        self.auto_clean_var = tk.BooleanVar(value=self.config.get("auto_clean", True))
        auto_clean_cb = ttk.Checkbutton(settings_frame, text="Auto-clean on paste", 
                                       variable=self.auto_clean_var,
                                       command=self.on_setting_change)
        auto_clean_cb.pack(side=tk.LEFT)
    
    def setup_input_area(self, parent):
        # Input section
        input_frame = ttk.LabelFrame(parent, text="📝 Original Text", padding="10")
        input_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(1, weight=1)
        
        # Input toolbar
        input_toolbar = ttk.Frame(input_frame)
        input_toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        input_toolbar.columnconfigure(1, weight=1)
        
        # Character count
        self.input_count_var = tk.StringVar(value="0 characters")
        count_label = ttk.Label(input_toolbar, textvariable=self.input_count_var,
                               font=("Helvetica", 9))
        count_label.grid(row=0, column=0, sticky="w")
        
        # Clear button
        clear_btn = ttk.Button(input_toolbar, text="🗑️ Clear", 
                              command=self.clear_input, width=8)
        clear_btn.grid(row=0, column=2, sticky="e")
        
        # Text area with custom styling
        text_frame = ttk.Frame(input_frame)
        text_frame.grid(row=1, column=0, sticky="nsew")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.input_text = scrolledtext.ScrolledText(
            text_frame, height=10, wrap=tk.WORD, 
            font=("Consolas", 11),
            bg=self.current_theme["text_bg"],
            fg=self.current_theme["text_fg"],
            selectbackground=self.current_theme["text_select_bg"],
            selectforeground=self.current_theme["text_select_fg"],
            insertbackground=self.current_theme["accent"],
            relief="flat", borderwidth=2
        )
        self.input_text.grid(row=0, column=0, sticky="nsew")
        self.input_text.bind('<KeyRelease>', self.on_text_change)
        self.input_text.bind('<Button-1>', self.on_text_change)
    
    def setup_controls(self, parent):
        controls_frame = ttk.Frame(parent)
        controls_frame.grid(row=3, column=0, pady=15)
        
        # Main action button with enhanced styling
        clean_btn = ttk.Button(controls_frame, text="🔄 Clean Text", 
                              command=self.clean_text,
                              style="Primary.TButton")
        clean_btn.pack(side=tk.LEFT, padx=5)
        
        # Additional actions
        ttk.Button(controls_frame, text="↔️ Swap", 
                  command=self.swap_texts,
                  width=8).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(controls_frame, text="🗑️ Clear All", 
                  command=self.clear_all,
                  style="Warning.TButton",
                  width=10).pack(side=tk.LEFT, padx=5)
    
    def setup_output_area(self, parent):
        # Output section
        output_frame = ttk.LabelFrame(parent, text="✨ Cleaned Text", padding="10")
        output_frame.grid(row=4, column=0, sticky="nsew", pady=(10, 0))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(1, weight=1)
        
        # Output toolbar
        output_toolbar = ttk.Frame(output_frame)
        output_toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        output_toolbar.columnconfigure(1, weight=1)
        
        # Character count and reduction
        self.output_count_var = tk.StringVar(value="0 characters")
        output_count_label = ttk.Label(output_toolbar, textvariable=self.output_count_var,
                                      font=("Helvetica", 9))
        output_count_label.grid(row=0, column=0, sticky="w")
        
        self.reduction_var = tk.StringVar()
        reduction_label = ttk.Label(output_toolbar, textvariable=self.reduction_var,
                                   font=("Helvetica", 9),
                                   foreground=self.current_theme["success"])
        reduction_label.grid(row=0, column=1, sticky="e", padx=(0, 10))
        
        # Copy button
        copy_btn = ttk.Button(output_toolbar, text="📄 Copy", 
                             command=self.copy_cleaned,
                             style="Success.TButton", width=8)
        copy_btn.grid(row=0, column=2, sticky="e")
        
        # Text area
        text_frame = ttk.Frame(output_frame)
        text_frame.grid(row=1, column=0, sticky="nsew")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(
            text_frame, height=10, wrap=tk.WORD,
            font=("Consolas", 11),
            bg=self.current_theme["text_bg"],
            fg=self.current_theme["text_fg"],
            selectbackground=self.current_theme["text_select_bg"],
            selectforeground=self.current_theme["text_select_fg"],
            insertbackground=self.current_theme["accent"],
            relief="flat", borderwidth=2
        )
        self.output_text.grid(row=0, column=0, sticky="nsew")
    
    def setup_status_bar(self, parent):
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=5, column=0, sticky="ew", pady=(15, 0))
        status_frame.columnconfigure(0, weight=1)
        
        # Status with icon
        self.status_var = tk.StringVar(value="Ready - Paste LLM output to clean")
        self.status_icon_var = tk.StringVar(value="🟢")
        
        status_content = ttk.Frame(status_frame)
        status_content.grid(row=0, column=0, sticky="w")
        
        status_icon = ttk.Label(status_content, textvariable=self.status_icon_var,
                               font=("Helvetica", 10))
        status_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        status_label = ttk.Label(status_content, textvariable=self.status_var,
                                font=("Helvetica", 9))
        status_label.pack(side=tk.LEFT)
    
    def setup_bindings(self):
        # Keyboard shortcuts
        self.root.bind('<Control-v>', lambda e: self.paste_text())
        self.root.bind('<Control-c>', lambda e: self.copy_cleaned())
        self.root.bind('<Control-l>', lambda e: self.clear_all())
        self.root.bind('<F5>', lambda e: self.clean_text())
        self.root.bind('<Control-Return>', lambda e: self.clean_text())
        self.root.bind('<Escape>', lambda e: self.clear_all())
        
        # Window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_theme_change(self, event=None):
        """Handle theme change"""
        new_theme = self.theme_var.get()
        self.config["theme"] = new_theme
        self.save_config()
        
        # Apply new theme
        self.current_theme = self.theme_manager.apply_theme(self.root, new_theme)
        
        # Update text widget colors
        self.update_text_colors()
        
        self.set_status("🎨 Theme changed to " + new_theme, "success")
    
    def on_setting_change(self):
        """Handle setting changes"""
        self.config["auto_paste"] = self.auto_paste_var.get()
        self.config["auto_clean"] = self.auto_clean_var.get()
        self.save_config()
    
    def update_text_colors(self):
        """Update text widget colors after theme change"""
        for widget in [self.input_text, self.output_text]:
            widget.configure(
                bg=self.current_theme["text_bg"],
                fg=self.current_theme["text_fg"],
                selectbackground=self.current_theme["text_select_bg"],
                selectforeground=self.current_theme["text_select_fg"],
                insertbackground=self.current_theme["accent"]
            )
    
    def check_theme_change(self):
        """Check for system theme changes in auto mode"""
        if self.config.get("theme", "auto") == "auto":
            current_system_theme = self.theme_manager.detect_system_theme()
            if hasattr(self, '_last_system_theme') and self._last_system_theme != current_system_theme:
                self.current_theme = self.theme_manager.apply_theme(self.root, "auto")
                self.update_text_colors()
            self._last_system_theme = current_system_theme
            
        # Schedule next check
        self.root.after(5000, self.check_theme_change)
    
    def auto_paste(self):
        """Auto-paste clipboard content on startup"""
        try:
            clipboard_content = pyperclip.paste()
            if clipboard_content and clipboard_content.strip():
                self.input_text.insert('1.0', clipboard_content)
                self.update_counts()
                self.set_status("📋 Auto-pasted from clipboard", "info")
                if self.auto_clean_var.get():
                    self.root.after(500, self.clean_text)
        except Exception:
            pass
    
    def paste_text(self):
        """Paste from clipboard"""
        try:
            clipboard_content = pyperclip.paste()
            if clipboard_content:
                self.input_text.delete('1.0', tk.END)
                self.input_text.insert('1.0', clipboard_content)
                self.set_status("📋 Text pasted from clipboard", "success")
                self.update_counts()
                
                if self.auto_clean_var.get():
                    self.root.after(300, self.clean_text)
            else:
                self.set_status("❌ Clipboard is empty", "warning")
        except Exception as e:
            self.set_status(f"❌ Failed to paste: {str(e)}", "error")
    
    def clean_text(self):
        """Clean the input text with visual feedback"""
        input_content = self.input_text.get('1.0', tk.END).strip()
        
        if not input_content:
            self.set_status("❌ No text to clean", "warning")
            return
        
        try:
            # Show processing status
            self.set_status("🔄 Cleaning text...", "info")
            self.root.update_idletasks()
            
            # Clean the text
            cleaned_text = self.cleaner.clean(input_content)
            
            # Display cleaned text
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert('1.0', cleaned_text)
            
            # Update counts and show results
            self.update_counts()
            
            original_len = len(input_content)
            cleaned_len = len(cleaned_text)
            reduction = original_len - cleaned_len
            
            if reduction > 0:
                self.set_status(f"✨ Cleaned: {reduction} characters removed", "success")
            else:
                self.set_status("✅ Text was already clean", "success")
                
        except Exception as e:
            self.set_status(f"❌ Cleaning failed: {str(e)}", "error")
    
    def copy_cleaned(self):
        """Copy cleaned text to clipboard"""
        content = self.output_text.get('1.0', tk.END).strip()
        
        if not content:
            self.set_status("❌ No cleaned text to copy", "warning")
            return
        
        try:
            pyperclip.copy(content)
            self.set_status("📄 Cleaned text copied to clipboard", "success")
        except Exception as e:
            self.set_status(f"❌ Copy failed: {str(e)}", "error")
    
    def swap_texts(self):
        """Swap input and output texts"""
        input_content = self.input_text.get('1.0', tk.END).strip()
        output_content = self.output_text.get('1.0', tk.END).strip()
        
        if not output_content:
            self.set_status("❌ No cleaned text to swap", "warning")
            return
        
        self.input_text.delete('1.0', tk.END)
        self.input_text.insert('1.0', output_content)
        
        self.output_text.delete('1.0', tk.END)
        if input_content:
            self.output_text.insert('1.0', input_content)
        
        self.update_counts()
        self.set_status("↔️ Texts swapped", "info")
    
    def clear_input(self):
        """Clear input text only"""
        self.input_text.delete('1.0', tk.END)
        self.update_counts()
        self.set_status("🗑️ Input cleared", "info")
    
    def clear_all(self):
        """Clear both text areas"""
        self.input_text.delete('1.0', tk.END)
        self.output_text.delete('1.0', tk.END)
        self.update_counts()
        self.set_status("🗑️ All text cleared", "info")
    
    def on_text_change(self, event=None):
        """Handle text changes in input area"""
        self.update_counts()
    
    def update_counts(self):
        """Update character counts and reduction percentage"""
        input_count = len(self.input_text.get('1.0', tk.END)) - 1
        output_count = len(self.output_text.get('1.0', tk.END)) - 1
        
        self.input_count_var.set(f"{input_count:,} characters")
        self.output_count_var.set(f"{output_count:,} characters")
        
        if input_count > 0 and output_count > 0:
            reduction = ((input_count - output_count) / input_count) * 100
            if reduction > 0:
                self.reduction_var.set(f"↓ {reduction:.1f}% reduction")
            else:
                self.reduction_var.set("")
        else:
            self.reduction_var.set("")
    
    def set_status(self, message, status_type="info"):
        """Set status message with appropriate icon"""
        icons = {
            "info": "🔵",
            "success": "🟢", 
            "warning": "🟡",
            "error": "🔴"
        }
        
        self.status_icon_var.set(icons.get(status_type, "🔵"))
        self.status_var.set(message)
        
        # Auto-clear status after some time for non-error messages
        if status_type != "error":
            self.root.after(3000, lambda: self.set_status("Ready - Paste LLM output to clean"))
    
    def on_closing(self):
        """Handle application closing"""
        self.save_config()
        self.root.destroy()


def main():
    root = tk.Tk()
    
    # Set window icon if available
    try:
        if platform.system() == "Windows":
            root.iconbitmap(default="icon.ico")
    except:
        pass
    
    app = ClipCleanGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()