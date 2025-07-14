# ui/compare_tab.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from business_logic.database_operations import DatabaseOperations
from business_logic.comparison_logic import ComparisonLogic
from business_logic.report_generator import ReportGenerator
from dotenv import load_dotenv

load_dotenv() 

db_server = os.getenv('DB_SERVER', 'MARS-2016')
db_username = os.getenv('DB_USERNAME', 'sa')
db_password = os.getenv('DB_PASSWORD', 'mars@123')

class CompareTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent, padding=(20, 15))
        self.common_tables = []
        self.table_vars = {}
        self.create_widgets()
        self.setup_styles()
    
    def setup_styles(self):
        style = ttk.Style()
        
        # Custom theme colors
        style.theme_create("custom_theme", parent="clam", settings={
            "TFrame": {"configure": {"background": "#f5f7fa"}},
            "TLabel": {"configure": {"background": "#f5f7fa", "font": ("Segoe UI", 10)}},
            "TButton": {
                "configure": {
                    "padding": 6,
                    "font": ("Segoe UI", 9, "bold"),
                    "background": "#4a6fa5",
                    "foreground": "white"
                },
                "map": {
                    "background": [("active", "#3a5a80"), ("disabled", "#cccccc")],
                    "foreground": [("disabled", "#888888")]
                }
            },
            "TEntry": {"configure": {"fieldbackground": "white"}},
            "TCombobox": {"configure": {"fieldbackground": "white"}},
            "TCheckbutton": {"configure": {"background": "#f5f7fa"}},
            "TLabelframe": {
                "configure": {
                    "background": "#f5f7fa",
                    "relief": "groove",
                    "borderwidth": 2
                }
            },
            "TLabelframe.Label": {
                "configure": {
                    "background": "#f5f7fa",
                    "font": ("Segoe UI", 10, "bold"),
                    "foreground": "#2c3e50"
                }
            }
        })
        style.theme_use("custom_theme")
        
        # Custom styles
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#2c3e50")
        style.configure("Primary.TButton", background="#3498db")
        style.configure("Secondary.TButton", background="#95a5a6")
        style.configure("Accent.TButton", background="#e74c3c")
        style.configure("Table.TCheckbutton", font=("Segoe UI", 9), padding=5)
        style.configure("Progress.TLabel", font=("Segoe UI", 9), foreground="#2c3e50")
    
    def create_widgets(self):
        # Main container with subtle background
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Header with logo placeholder
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Logo placeholder (you can replace with actual image)
        ttk.Label(header_frame, 
                 text="🔍 Database Comparison Tool", 
                 style='Header.TLabel').pack(side=tk.LEFT)
        
        # Connection frame with modern styling
        conn_frame = ttk.LabelFrame(main_container, 
                                  text=" SERVER CONNECTION ",
                                  padding=(20, 15))
        conn_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Server entry with icon placeholder
        server_frame = ttk.Frame(conn_frame)
        server_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(server_frame, text="Server Host:").pack(side=tk.LEFT, padx=(0, 10))
        self.server_entry = ttk.Entry(server_frame, font=("Segoe UI", 10))
        self.server_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.server_entry.insert(0, db_server)
        
        # Credentials frame with improved layout
        cred_frame = ttk.Frame(conn_frame)
        cred_frame.pack(fill=tk.X, pady=10)
        
        # Username
        user_frame = ttk.Frame(cred_frame)
        user_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        ttk.Label(user_frame, text="Username:").pack(side=tk.LEFT, padx=(0, 10))
        self.user_entry = ttk.Entry(user_frame, font=("Segoe UI", 10))
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.user_entry.insert(0, db_username)
        
        # Password with show/hide toggle
        pass_frame = ttk.Frame(cred_frame)
        pass_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(pass_frame, text="Password:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.password_entry = ttk.Entry(pass_frame, show="•", font=("Segoe UI", 10))
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.password_entry.insert(0, db_password)
        
        # Show/hide password button
        self.show_pass_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(pass_frame, 
                       text="👁️", 
                       style='Toolbutton',
                       variable=self.show_pass_var,
                       command=self.toggle_password_visibility).pack(side=tk.LEFT, padx=(5, 0))
        
        # Action buttons with better visual hierarchy
        action_frame = ttk.Frame(conn_frame)
        action_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Button(action_frame, 
                  text="🔄 Refresh Databases", 
                  style='Secondary.TButton',
                  command=self.refresh_databases).pack(side=tk.RIGHT)
        
        # Database selection frame
        db_frame = ttk.LabelFrame(main_container, 
                                text=" DATABASE SELECTION ",
                                padding=(20, 15))
        db_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Source DB with improved layout
        db1_frame = ttk.Frame(db_frame)
        db1_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(db1_frame, text="Source Database:").pack(side=tk.LEFT, padx=(0, 10))
        self.db1_var = tk.StringVar()
        self.db1_combobox = ttk.Combobox(db1_frame, 
                                        textvariable=self.db1_var, 
                                        state="readonly",
                                        font=("Segoe UI", 10))
        self.db1_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Target DB
        db2_frame = ttk.Frame(db_frame)
        db2_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(db2_frame, text="Target Database:").pack(side=tk.LEFT, padx=(0, 10))
        self.db2_var = tk.StringVar()
        self.db2_combobox = ttk.Combobox(db2_frame, 
                                        textvariable=self.db2_var, 
                                        state="readonly",
                                        font=("Segoe UI", 10))
        self.db2_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Get Tables button with icon and primary style
        ttk.Button(db_frame, 
                  text="📋 GET TABLES", 
                  style='Primary.TButton',
                  command=self.get_common_tables_list).pack(pady=(10, 0))
        
        # Tables comparison frame with modern card styling
        self.tables_frame = ttk.LabelFrame(main_container, 
                                         text=" TABLES SELECTION ",
                                         padding=(20, 15))
        self.tables_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Container with scrollable canvas and modern styling
        container = ttk.Frame(self.tables_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas with scrollbar
        self.canvas = tk.Canvas(container, bg='white', bd=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Mousewheel bindings
        self.scrollable_frame.bind("<Enter>", self._bind_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_mousewheel)
        
        # Options frame with modern styling
        options_frame = ttk.LabelFrame(main_container, 
                                     text=" COMPARISON OPTIONS ",
                                     padding=(20, 15))
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Data comparison checkbox with better layout
        self.compare_data_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, 
                       text="Compare table data (enable for detailed comparison)",
                       variable=self.compare_data_var,
                       style='TCheckbutton').pack(anchor=tk.W, pady=5)
        
        # Output location with improved layout
        output_frame = ttk.Frame(options_frame)
        output_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(output_frame, text="Report Location:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.output_entry = ttk.Entry(output_frame, font=("Segoe UI", 10))
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.output_entry.insert(0, os.path.abspath('./comparison_report.html'))
        
        ttk.Button(output_frame, 
                  text="📂 Browse...", 
                  style='Secondary.TButton',
                  command=self.browse_output).pack(side=tk.LEFT)
        
        # Progress frame with modern styling
        self.progress_frame = ttk.Frame(main_container)
        self.progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_label = ttk.Label(self.progress_frame, 
                                      text="Ready to compare databases...", 
                                      style='Progress.TLabel',
                                      wraplength=750)
        self.progress_label.pack(fill=tk.X)
        
        # Action buttons with improved visual hierarchy
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, 
                  text="▶️ Run Comparison", 
                  style='Primary.TButton',
                  command=self.run_comparison).pack(side=tk.LEFT, padx=5, expand=True)
        
        ttk.Button(button_frame, 
                  text="❌ Exit", 
                  style='Accent.TButton',
                  command=self.app.root.quit).pack(side=tk.RIGHT, padx=5, expand=True)
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_pass_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")
    
    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def browse_output(self):
        initial_file = self.output_entry.get()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            initialfile=os.path.basename(initial_file),
            initialdir=os.path.dirname(initial_file)
        )
        if file_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)

    def refresh_databases(self):
        self.app.status_var.set("Fetching databases...")
        self.progress_label.config(text="Connecting to server to fetch database list...")
        self.app.root.update()
        
        try:
            databases = DatabaseOperations.get_databases(
                self.server_entry.get(),
                self.user_entry.get(),
                self.password_entry.get()
            )
            
            if databases:
                self.db1_combobox['values'] = databases
                self.db2_combobox['values'] = databases
                
                if len(databases) >= 1:
                    self.db1_var.set(databases[0])
                if len(databases) >= 2:
                    self.db2_var.set(databases[1])
                
                self.app.status_var.set(f"Found {len(databases)} databases")
                self.progress_label.config(text=f"Successfully fetched {len(databases)} databases from server.")
            else:
                self.db1_combobox['values'] = []
                self.db2_combobox['values'] = []
                self.db1_var.set('')
                self.db2_var.set('')
                self.app.status_var.set("No databases found")
                self.progress_label.config(text="No databases found or connection failed.")
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            self.db1_combobox['values'] = []
            self.db2_combobox['values'] = []
            self.db1_var.set('')
            self.db2_var.set('')
            self.app.status_var.set("Connection failed")
            self.progress_label.config(text="Failed to connect to server.")

    def get_common_tables_list(self):
        """Get list of common tables and display in grid layout with checkboxes"""
        if not self.db1_var.get() or not self.db2_var.get():
            messagebox.showerror("Error", "Please select both databases first")
            return
            
        try:
            # Clear previous tables list
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            self.common_tables = []
            self.table_vars = {}
            
            # Get connections and common tables
            conn1 = DatabaseOperations.get_connection(
                self.server_entry.get(),
                self.db1_var.get(),
                self.user_entry.get(),
                self.password_entry.get()
            )
            conn2 = DatabaseOperations.get_connection(
                self.server_entry.get(),
                self.db2_var.get(),
                self.user_entry.get(),
                self.password_entry.get()
            )
            
            cursor1 = conn1.cursor()
            cursor2 = conn2.cursor()
            self.common_tables = sorted(ComparisonLogic.get_common_tables(cursor1, cursor2))
            conn1.close()
            conn2.close()
            
            if not self.common_tables:
                ttk.Label(self.scrollable_frame, 
                         text="No common tables found between databases",
                         style='Info.TLabel').pack(pady=10)
                return
            
            # Add "Select All" checkbox
            all_var = tk.BooleanVar(value=True)
            select_all_cb = ttk.Checkbutton(
                self.scrollable_frame,
                text="Select All Tables",
                variable=all_var,
                command=lambda: self.toggle_all_tables(all_var.get()),
                style='Bold.TCheckbutton'  # Use a bold style for the header
            )
            select_all_cb.grid(row=0, column=0, columnspan=5, sticky='w', pady=10, padx=5)
            
            # Configure grid layout - 5 columns now
            columns = 4
            for i, table in enumerate(self.common_tables):
                var = tk.BooleanVar(value=True)
                self.table_vars[table] = var
                
                row = (i // columns) + 1  # +1 because row 0 is "Select All"
                col = i % columns
                
                # Create a frame for each table to better control layout
                table_frame = ttk.Frame(self.scrollable_frame)
                table_frame.grid(row=row, column=col, sticky='w', padx=5, pady=2)
                
                # Checkbutton with larger font and proper text wrapping
                cb = ttk.Checkbutton(
                    table_frame,
                    text=table,
                    variable=var,
                    width=37,  # Increased width
                    style='Table.TCheckbutton'  # Custom style for tables
                )
                cb.pack(fill='x', expand=True)
            
            # Configure column weights and minimum sizes
            for i in range(columns):
                self.scrollable_frame.columnconfigure(i, weight=1, minsize=150)  # Wider minimum column size
            
            # Update canvas scroll region after widgets are added
            self.scrollable_frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            
            # Set minimum height for the canvas
            self.canvas.config(height=150)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get tables: {str(e)}")
    
    def toggle_all_tables(self, select_all):
        """Toggle all table checkboxes"""
        for table, var in self.table_vars.items():
            var.set(select_all)


    def run_comparison(self):
        if not self.db1_var.get() or not self.db2_var.get():
            messagebox.showerror("Error", "Please select both source and target databases")
            return
        
        selected_tables = [table for table, var in self.table_vars.items() if var.get()]
        if not selected_tables and self.compare_data_var.get():
            messagebox.showerror("Error", "No tables selected for comparison")
            return
            
        self.app.status_var.set("Connecting to databases...")
        self.progress_label.config(text="Initializing comparison...")
        self.app.root.update()
        
        try:
            conn1 = DatabaseOperations.get_connection(
                self.server_entry.get(),
                self.db1_var.get(),
                self.user_entry.get(),
                self.password_entry.get()
            )
            conn2 = DatabaseOperations.get_connection(
                self.server_entry.get(),
                self.db2_var.get(),
                self.user_entry.get(),
                self.password_entry.get()
            )
            cursor1 = conn1.cursor()
            cursor2 = conn2.cursor()

            # Compare schema
            self.app.status_var.set("Comparing schemas...")
            self.progress_label.config(text="Comparing database schemas...")
            self.app.root.update()
            
            schema1 = ComparisonLogic.get_schema(cursor1)
            schema2 = ComparisonLogic.get_schema(cursor2)
            schema_diff = ComparisonLogic.compare_schemas(schema1, schema2)

            data_results = None
            differences_found = 0
            if self.compare_data_var.get():
                self.app.status_var.set("Comparing table data...")
                self.app.root.update()
                
                common_tables = sorted(selected_tables) if self.compare_data_var.get() else []
                total_tables = len(common_tables)
                data_results = []
                
                self.progress_label.config(
                    text=f"Starting data comparison for {total_tables} tables... | Differences found: 0"
                )
                self.app.root.update()
                
                for i, table in enumerate(common_tables, 1):
                    result = ComparisonLogic.compare_table_data(
                        conn1, conn2, table, self.db1_var.get(), self.db2_var.get()
                    )
                    if result['status'] == 'Different':
                        differences_found += 1
                    data_results.append(result)
                    self.progress_label.config(
                        text=f"Comparing data: Table {i}/{total_tables} ({table}) | Differences found: {differences_found}"
                    )
                    self.app.root.update_idletasks()

            self.app.status_var.set("Generating report...")
            self.progress_label.config(text="Generating final report...")
            self.app.root.update()
            
            # Get the path to the template (assuming it's in a templates directory)
            template_path = os.path.join(os.path.dirname(__file__), '../templates/report_template.html')
            output_path = self.output_entry.get()
            
            ReportGenerator.render_html_report(
                template_path,
                output_path,
                self.db1_var.get(),
                self.db2_var.get(),
                schema_diff,
                data_results
            )

            conn1.close()
            conn2.close()

            self.app.status_var.set("Comparison complete")
            self.progress_label.config(
                text=f"Comparison completed successfully!\n"
                     f"Report generated at: {output_path}\n"
                     f"Total tables compared: {len(data_results) if data_results else 0}\n"
                     f"Tables with differences: {differences_found}"
            )
        except Exception as e:
            self.app.status_var.set("Error occurred")
            self.progress_label.config(text=f"Error during comparison: {str(e)}")
            messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")
        finally:
            self.app.root.update_idletasks()