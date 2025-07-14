# ui/main_window.py

import tkinter as tk
from tkinter import ttk
from .compare_tab import CompareTab
from .create_tab import CreateTab

class DatabaseComparisonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Comparison Tool")
        self.root.geometry("1080x1000")
        self.root.resizable(False, False)
        
        self.configure_styles()
        self.create_widgets()
    
    def configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#2c3e50')
        self.style.configure('TLabelframe', font=('Segoe UI', 10, 'bold'), background='#f5f5f5')
        self.style.configure('TLabelframe.Label', font=('Segoe UI', 10, 'bold'), background='#f5f5f5')
        self.style.configure('TNotebook', background='#f5f5f5')
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'), padding=[10, 5])
        
        # Button styles
        button_styles = ['Run', 'Exit', 'Browse', 'Refresh', 'Create']
        for style_name in button_styles:
            self.style.configure(f'{style_name}.TButton', foreground='black', background='white')
            self.style.map(f'{style_name}.TButton',
                        background=[('active', 'lightgray'), ('pressed', 'gray')],
                        foreground=[('pressed', 'black'), ('active', 'black')])
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create Compare tab
        self.compare_tab = CompareTab(self.notebook, self)
        self.notebook.add(self.compare_tab.frame, text='Compare')
        
        # Create Create tab
        self.create_tab = CreateTab(self.notebook, self)
        self.notebook.add(self.create_tab.frame, text='Create')
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, 
                             textvariable=self.status_var, 
                             relief=tk.SUNKEN, 
                             anchor=tk.W,
                             padding=(5, 2))
        status_bar.pack(fill=tk.X)