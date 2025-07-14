
# 🪞 DB Mirror

**DB Mirror** is a GUI-based Python application for comparing two Microsoft SQL Server databases.

It compares both **schema and data** across tables and generates a detailed **HTML report** showing:
- ✅ Identical tables
- ❌ Differences in data
- 🧩 Schema mismatches

---

## 🚀 Features

- 🔐 Enter database credentials securely through a GUI
- 📂 Auto-loads available databases into dropdowns
- ✅ Lists all common tables with **checkboxes to exclude any**
- 📊 Compares selected tables for:
  - Schema (columns, types)
  - Data (row-by-row comparison)
- 📄 Generates a clean HTML report
- 🌐 Automatically opens the report in your browser

---

## 🖥️ GUI Walkthrough

1. **Enter Credentials**
   - Server Name
   - Username & Password

2. **Select Databases**
   - Two dropdowns auto-populated with available DBs

3. **Get Tables**
   - Lists all common tables with exclusion checkboxes

4. **Run Comparison**
   - Compares schemas & data
   - Opens HTML report with results

---

## Command to Generate .exe
` pyinstaller --name=DbCompareTool main.py --add-data "templates/report_template.html;templates" --add-data ".env;." `

## 📦 Requirements

Install required Python libraries:

```bash
pip install pandas pyodbc jinja2
```

---

## 🛠️ Usage

Run the app:

```bash
python main.py
```

---

## 📋 Sample Report Output

- Summary of schema differences
- Table-by-table status
- Sample mismatched rows (for quick debugging)

---

## 🔐 Notes

- Built for Microsoft SQL Server (via ODBC)
- Uses trusted certificate connection (`TrustServerCertificate=yes`)
- Does **not** modify any database content

---

## 📜 License

MIT License – free to use, modify, and distribute.

---

## 🤝 Contribute

Pull requests and feedback are welcome!

---

## 👨‍💻 Author

**Muhammad Amman**  
ammansoomro.com

---
