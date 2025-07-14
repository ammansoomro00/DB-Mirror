# ui/create_tab.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from business_logic.database_operations import DatabaseOperations
from dotenv import load_dotenv
import os

load_dotenv() 

db_server = os.getenv('DB_SERVER', 'MARS-2016')
db_username = os.getenv('DB_USERNAME', 'sa')
db_password = os.getenv('DB_PASSWORD', 'mars@123')
class CreateTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent)
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, pady=(10, 20))
        
        ttk.Label(header_frame, 
                 text="Create Databases and Execute Scripts", 
                 style='Header.TLabel').pack(side=tk.LEFT)
        
        # Connection frame (same as compare tab)
        conn_frame = ttk.LabelFrame(self.frame, text="Connection Settings", padding=(15, 10))
        conn_frame.pack(fill=tk.X, pady=5)
        
        # Server
        server_frame = ttk.Frame(conn_frame)
        server_frame.pack(fill=tk.X, pady=5)
        ttk.Label(server_frame, text="Server:").pack(side=tk.LEFT, padx=(0, 10))
        self.server_entry = ttk.Entry(server_frame)
        self.server_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.server_entry.insert(0, db_server)
        
        # Username/Password
        auth_frame = ttk.Frame(conn_frame)
        auth_frame.pack(fill=tk.X, pady=5)
        
        user_frame = ttk.Frame(auth_frame)
        user_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Label(user_frame, text="Username:").pack(side=tk.LEFT, padx=(0, 10))
        self.user_entry = ttk.Entry(user_frame)
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.user_entry.insert(0, db_username)
        
        pass_frame = ttk.Frame(auth_frame)
        pass_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(pass_frame, text="Password:").pack(side=tk.LEFT, padx=(0, 10))
        self.password_entry = ttk.Entry(pass_frame, show="*")
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.password_entry.insert(0, db_password)
        
        pass_frame = ttk.Frame(auth_frame)
        pass_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(pass_frame, text="Password:").pack(side=tk.LEFT, padx=(0, 10))
        self.password_entry = ttk.Entry(pass_frame, show="*")
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.password_entry.insert(0, 'mars@123')
        
        # Database creation frame
        db_create_frame = ttk.LabelFrame(self.frame, text="Database Creation", padding=(15, 10))
        db_create_frame.pack(fill=tk.X, pady=5)
        
        # Database 1
        db1_frame = ttk.Frame(db_create_frame)
        db1_frame.pack(fill=tk.X, pady=5)
        ttk.Label(db1_frame, text="Database 1 Name:").pack(side=tk.LEFT, padx=(0, 10))
        self.db1_name_entry = ttk.Entry(db1_frame)
        self.db1_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Database 2
        db2_frame = ttk.Frame(db_create_frame)
        db2_frame.pack(fill=tk.X, pady=5)
        ttk.Label(db2_frame, text="Database 2 Name:").pack(side=tk.LEFT, padx=(0, 10))
        self.db2_name_entry = ttk.Entry(db2_frame)
        self.db2_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Script selection frame
        script_frame = ttk.LabelFrame(self.frame, text="Script Execution", padding=(15, 10))
        script_frame.pack(fill=tk.X, pady=5)
        
        # N-1 Complete Script
        script1_frame = ttk.Frame(script_frame)
        script1_frame.pack(fill=tk.X, pady=5)
        ttk.Label(script1_frame, text="N-1 Complete Script:").pack(side=tk.LEFT, padx=(0, 10))
        self.script1_entry = ttk.Entry(script1_frame)
        self.script1_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(script1_frame, 
                  text="Browse...", 
                  style='Browse.TButton',
                  command=lambda: self.browse_script(self.script1_entry)).pack(side=tk.LEFT)
        
        # Incremental Script
        script2_frame = ttk.Frame(script_frame)
        script2_frame.pack(fill=tk.X, pady=5)
        ttk.Label(script2_frame, text="Incremental Script:").pack(side=tk.LEFT, padx=(0, 10))
        self.script2_entry = ttk.Entry(script2_frame)
        self.script2_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(script2_frame, 
                  text="Browse...", 
                  style='Browse.TButton',
                  command=lambda: self.browse_script(self.script2_entry)).pack(side=tk.LEFT)
        
        # N Complete Script
        script3_frame = ttk.Frame(script_frame)
        script3_frame.pack(fill=tk.X, pady=5)
        ttk.Label(script3_frame, text="N Complete Script:").pack(side=tk.LEFT, padx=(0, 10))
        self.script3_entry = ttk.Entry(script3_frame)
        self.script3_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(script3_frame, 
                  text="Browse...", 
                  style='Browse.TButton',
                  command=lambda: self.browse_script(self.script3_entry)).pack(side=tk.LEFT)
        
        # Progress frame for create tab
        self.progress_frame = ttk.Frame(self.frame)
        self.progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_label = ttk.Label(self.progress_frame, text="", wraplength=750)
        self.progress_label.pack(fill=tk.X)
        
        # Button frame
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, 
                  text="Create Databases & Execute Scripts", 
                  style='Create.TButton',
                  command=self.create_and_execute).pack(side=tk.LEFT, padx=5, expand=True)
        
        ttk.Button(button_frame, 
                  text="Exit", 
                  style='Exit.TButton',
                  command=self.app.root.quit).pack(side=tk.RIGHT, padx=5, expand=True)
    
    def browse_script(self, entry_widget):
        file_path = filedialog.askopenfilename(
            filetypes=[("SQL files", "*.sql"), ("All files", "*.*")]
        )
        if file_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)
    
    def create_and_execute(self):
        db1_name = self.db1_name_entry.get().strip()
        db2_name = self.db2_name_entry.get().strip()
        
        if not db1_name or not db2_name:
            messagebox.showerror("Error", "Please enter names for both databases")
            return
        
        script1_path = self.script1_entry.get().strip()
        script2_path = self.script2_entry.get().strip()
        script3_path = self.script3_entry.get().strip()
        
        if not all([script1_path, script2_path, script3_path]):
            messagebox.showerror("Error", "Please select all three SQL script files")
            return
        
        self.app.status_var.set("Creating databases...")
        self.progress_label.config(text="Starting database creation...")
        self.app.root.update()
        
        try:
            # Create databases
            if not DatabaseOperations.create_database(
                self.server_entry.get(),
                self.user_entry.get(),
                self.password_entry.get(),
                db1_name
            ):
                return
            self.progress_label.config(text=f"Database '{db1_name}' created successfully")
            self.app.root.update()
            
            if not DatabaseOperations.create_database(
                self.server_entry.get(),
                self.user_entry.get(),
                self.password_entry.get(),
                db2_name
            ):
                return
            self.progress_label.config(text=f"Database '{db2_name}' created successfully")
            self.app.root.update()
            
            # Execute scripts
            self.app.status_var.set("Executing scripts...")
            self.progress_label.config(text="Executing N-1 Complete script on Database 1...")
            self.app.root.update()
            
            if not DatabaseOperations.execute_sql_file(
                self.server_entry.get(),
                db1_name,
                self.user_entry.get(),
                self.password_entry.get(),
                script1_path
            ):
                return
            self.progress_label.config(text="N-1 Complete script executed successfully on Database 1")
            self.app.root.update()
            
            self.progress_label.config(text="Executing Incremental script on Database 1...")
            self.app.root.update()
            
            if not DatabaseOperations.execute_sql_file(
                self.server_entry.get(),
                db1_name,
                self.user_entry.get(),
                self.password_entry.get(),
                script2_path
            ):
                return
            self.progress_label.config(text="Incremental script executed successfully on Database 1")
            self.app.root.update()
            
            self.progress_label.config(text="Executing N Complete script on Database 2...")
            self.app.root.update()
            
            if not DatabaseOperations.execute_sql_file(
                self.server_entry.get(),
                db2_name,
                self.user_entry.get(),
                self.password_entry.get(),
                script3_path
            ):
                return
            self.progress_label.config(text="N Complete script executed successfully on Database 2")
            self.app.root.update()
            
            self.app.status_var.set("Operation completed successfully")
            self.progress_label.config(
                text=f"All operations completed successfully!\n"
                     f"Database 1: {db1_name} (N-1 Complete and Incremental scripts executed)\n"
                     f"Database 2: {db2_name} (N Complete script executed)"
            )
            
            # Update the compare tab dropdowns with the new databases
            self.app.compare_tab.refresh_databases()
            self.app.compare_tab.db1_var.set(db1_name)
            self.app.compare_tab.db2_var.set(db2_name)
        except Exception as e:
            self.app.status_var.set("Error occurred")
            self.progress_label.config(text=f"Error during operation: {str(e)}")
            messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")