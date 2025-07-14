# business_logic/database_operations.py

import pyodbc
import os
import pandas as pd

class DatabaseOperations:
    @staticmethod
    def get_connection(server, database, username, password):
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};DATABASE={database};"
            f"UID={username};PWD={password};"
            f"TrustServerCertificate=yes"
        )
        return pyodbc.connect(conn_str)

    @staticmethod
    def get_master_connection(server, username, password):
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"UID={username};PWD={password};"
            f"TrustServerCertificate=yes"
        )
        return pyodbc.connect(conn_str, autocommit=True)

    @staticmethod
    def get_databases(server, username, password):
        try:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"UID={username};PWD={password};"
                f"TrustServerCertificate=yes"
            )
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sys.databases WHERE database_id > 4 ORDER BY name")
            databases = [row[0] for row in cursor.fetchall()]
            conn.close()
            return databases
        except Exception as e:
            raise Exception(f"Failed to fetch databases: {str(e)}")

    @staticmethod
    def create_database(server, username, password, db_name):
        try:
            conn = DatabaseOperations.get_master_connection(server, username, password)
            cursor = conn.cursor()
            cursor.execute(f"SELECT name FROM sys.databases WHERE name = '{db_name}'")
            if cursor.fetchone():
                return True  # Database already exists
            
            cursor.execute(f"CREATE DATABASE [{db_name}]")
            conn.close()
            return True
        except Exception as e:
            raise Exception(f"Failed to create database '{db_name}': {str(e)}")

    @staticmethod
    def execute_sql_file(server, database, username, password, file_path):
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            with open(file_path, 'r') as f:
                sql_script = f.read()
            
            conn = DatabaseOperations.get_connection(server, database, username, password)
            conn.autocommit = True
            cursor = conn.cursor()
            
            for statement in sql_script.split('GO'):
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except pyodbc.Error as e:
                        conn.rollback()
                        continue
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            raise Exception(f"Failed to execute script on database '{database}': {str(e)}")