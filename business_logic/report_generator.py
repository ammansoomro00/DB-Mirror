# business_logic/report_generator.py

from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import webbrowser
import os

class ReportGenerator:
    @staticmethod
    def render_html_report(template_path, output_path, db1, db2, schema_diff, data_results=None):
        env = Environment(loader=FileSystemLoader(searchpath=os.path.dirname(template_path)))
        with open(template_path, 'r') as f:
            template_str = f.read()
        
        template = env.from_string(template_str)
        
        html = template.render(
            db1=db1,
            db2=db2,
            schema_diff={
                "only_in_db1": [f"{item[0]}.{item[1]} ({item[2]})" for item in schema_diff[0]],
                "only_in_db2": [f"{item[0]}.{item[1]} ({item[2]})" for item in schema_diff[1]]
            },
            data_results=data_results,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        webbrowser.open(f"file://{os.path.abspath(output_path)}")
        return output_path