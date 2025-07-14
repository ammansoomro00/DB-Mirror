# business_logic/comparision_logic.py

import pandas as pd
class ComparisonLogic:
    @staticmethod
    def get_schema(cursor):
        cursor.execute("""
            SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            ORDER BY TABLE_NAME, COLUMN_NAME
        """)
        return set(tuple(row) for row in cursor.fetchall())

    @staticmethod
    def compare_schemas(schema1, schema2):
        only_in_db1 = schema1 - schema2
        only_in_db2 = schema2 - schema1
        return list(only_in_db1), list(only_in_db2)

    @staticmethod
    def get_common_tables(cursor1, cursor2):
        cursor1.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
        cursor2.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
        tables1 = set(row[0] for row in cursor1.fetchall())
        tables2 = set(row[0] for row in cursor2.fetchall())
        return tables1.intersection(tables2)

    @staticmethod
    def compare_table_data(conn1, conn2, table_name, db1_name, db2_name):
        try:
            # Columns to exclude from comparison
            EXCLUDED_COLUMNS = [
                'DOC_CREATE_DATE', 'DOC_LOAD_DATE', 'UPDATE_DATE', 
                'CREATION_TIME', 'AS_OF_DATE', 'CREATE_DATE',
                'LAST_UPDATE_DATE', 'LOAD_TIMESTAMP', 'ETL_DATE',
                'CREATE_TIME','MODIFY_TIME','PASSWORD_MODIFY_DATE',
                'LAST_LOGIN_TIME','LAST_LOGOUT_TIME','CURR_LOGIN_TIME',
                'CREATED_ON','UPDATED_ON',
                'TAB_ORDER', 'DISPLAY_ORDER', 'SORT_ORDER'  
            ]
            
            # Get column information
            columns_query = """
            SELECT COLUMN_NAME, DATA_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = ?
            """
            
            cursor1 = conn1.cursor()
            cursor2 = conn2.cursor()
            
            cursor1.execute(columns_query, table_name)
            db1_columns = {row[0]: row[1] for row in cursor1.fetchall()}
            
            cursor2.execute(columns_query, table_name)
            db2_columns = {row[0]: row[1] for row in cursor2.fetchall()}
            
            # Select columns to compare (excluding timestamp and order columns)
            select_columns = [
                col for col in db1_columns 
                if col in db2_columns and col not in EXCLUDED_COLUMNS
            ]
            
            if not select_columns:
                return {
                    "table": table_name,
                    "status": "Skipped",
                    "diff_sample": "<div class='alert alert-warning'>No comparable columns after exclusions</div>",
                    "diff_count": 0
                }

            # Build and execute queries
            query = f"SELECT {', '.join(f'[{col}]' for col in select_columns)} FROM [{table_name}]"
            
            try:
                df1 = pd.read_sql(query, conn1)
                df2 = pd.read_sql(query, conn2)
            except Exception as e:
                return {
                    "table": table_name,
                    "status": "Error",
                    "diff_sample": f"<div class='alert alert-danger'>Error fetching data: {str(e)}</div>",
                    "diff_count": 0
                }

            # Convert all data to strings for consistent comparison
            df1 = df1.astype(str)
            df2 = df2.astype(str)
            
            # Sort both dataframes by all columns to ignore row order differences
            df1_sorted = df1.sort_values(by=select_columns).reset_index(drop=True)
            df2_sorted = df2.sort_values(by=select_columns).reset_index(drop=True)
            
            # Check if the sorted dataframes are identical
            if df1_sorted.equals(df2_sorted):
                return {
                    "table": table_name,
                    "status": "Identical",
                    "diff_sample": None,
                    "diff_count": 0
                }

            # Find primary key candidates
            pk_candidates = [
                col for col in select_columns 
                if ('id' in col.lower() or 'code' in col.lower() or 'name' in col.lower())
            ]
            if not pk_candidates:
                pk_candidates = select_columns[:1]

            # Mark source for each dataframe
            df1['__source__'] = db1_name
            df2['__source__'] = db2_name
            
            # Combine dataframes
            combined = pd.concat([df1, df2])
            
            # Find rows that exist in only one database (order-independent)
            grouped = combined.groupby(select_columns, dropna=False)['__source__'].agg(list).reset_index()
            db1_only = grouped[grouped['__source__'].apply(lambda x: db1_name in x and db2_name not in x)]
            db2_only = grouped[grouped['__source__'].apply(lambda x: db2_name in x and db1_name not in x)]
            
            # Find changed rows (same PK but different in other columns)
            changed_rows = []
            if pk_candidates:
                # Get common PK values
                pk_values_db1 = df1[pk_candidates].drop_duplicates()
                pk_values_db2 = df2[pk_candidates].drop_duplicates()
                common_pks = pd.merge(pk_values_db1, pk_values_db2, how='inner', on=pk_candidates)
                
                if not common_pks.empty:
                    # Get full rows for common PKs
                    df1_common = pd.merge(df1, common_pks, on=pk_candidates)
                    df2_common = pd.merge(df2, common_pks, on=pk_candidates)
                    
                    # Compare each row
                    for _, pk_row in common_pks.iterrows():
                        row_db1 = df1_common[df1_common[pk_candidates[0]] == pk_row[pk_candidates[0]]].iloc[0]
                        row_db2 = df2_common[df2_common[pk_candidates[0]] == pk_row[pk_candidates[0]]].iloc[0]
                        
                        differences = []
                        for col in select_columns:
                            if col in pk_candidates:
                                continue
                                
                            val1 = row_db1[col]
                            val2 = row_db2[col]
                            
                            # Handle null values
                            if pd.isna(val1) and pd.isna(val2):
                                continue
                                
                            # String comparison with case and whitespace normalization
                            if str(val1).strip().lower() == str(val2).strip().lower():
                                continue
                                
                            differences.append({
                                'column': col,
                                db1_name: val1,
                                db2_name: val2
                            })
                        
                        if differences:
                            changed_rows.append({
                                'pk': {col: row_db1[col] for col in pk_candidates},
                                'differences': differences
                            })

            # Generate report
            html = []
            total_diffs = len(db1_only) + len(db2_only) + len(changed_rows)
            
            # Show excluded columns notice
            excluded_in_table = [col for col in EXCLUDED_COLUMNS if col in db1_columns or col in db2_columns]
            if excluded_in_table:
                html.append("<div class='alert alert-info'>")
                # html.append(f"<p>Excluded columns: {', '.join(excluded_in_table)}</p>") -- COMMENTED OUT
                html.append("</div>")
            
            if total_diffs == 0:
                return {
                    "table": table_name,
                    "status": "Identical",
                    "diff_sample": "".join(html) if excluded_in_table else None,
                    "diff_count": 0
                }

            # Show exclusive rows
            if not db1_only.empty or not db2_only.empty:
                html.append("<h4>Exclusive Rows</h4>")
                if not db1_only.empty:
                    html.append(f"<h5>Only in {db1_name} ({len(db1_only)} rows):</h5>")
                    html.append(db1_only[select_columns].to_html(classes="table table-sm", index=False))
                if not db2_only.empty:
                    html.append(f"<h5>Only in {db2_name} ({len(db2_only)} rows):</h5>")
                    html.append(db2_only[select_columns].to_html(classes="table table-sm", index=False))
            
            # Show changed rows
            if changed_rows:
                html.append("<h4>Changed Rows</h4>")
                html.append("<p>Rows with same keys but different values:</p>")
                for row in changed_rows:
                    html.append("<div class='card mb-3'>")
                    html.append(f"<div class='card-header'>PK: {', '.join(f'{k}={v}' for k,v in row['pk'].items())}</div>")
                    html.append("<div class='card-body'><table class='table table-sm'>")
                    html.append("<thead><tr><th>Column</th>")
                    html.append(f"<th>{db1_name}</th><th>{db2_name}</th></tr></thead><tbody>")
                    for diff in row['differences']:
                        html.append("<tr>")
                        html.append(f"<td>{diff['column']}</td>")
                        html.append(f"<td style='background-color:#ffcccc'>{diff[db1_name]}</td>")
                        html.append(f"<td style='background-color:#ffcccc'>{diff[db2_name]}</td>")
                        html.append("</tr>")
                    html.append("</tbody></table></div></div>")
            
            return {
                "table": table_name,
                "status": "Different",
                "diff_sample": "".join(html),
                "diff_count": total_diffs
            }
                
        except Exception as e:
            return {
                "table": table_name,
                "status": "Error",
                "diff_sample": f"<div class='alert alert-danger'>Error comparing table: {str(e)}</div>",
                "diff_count": 0
            }