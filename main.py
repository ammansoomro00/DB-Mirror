# main.py
import tkinter as tk
from ui.main_window import DatabaseComparisonApp

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseComparisonApp(root)
    root.mainloop()