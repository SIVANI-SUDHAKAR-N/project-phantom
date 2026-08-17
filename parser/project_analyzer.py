from pathlib import Path

from .scanner import scan_project
from .analyzer import analyze_python_file

def analyze_project(project_path):
    path = Path(project_path)

    summary = scan_project(project_path)

    python_analysis = []

    for item in path.rglob("*.py"):
        if item.is_file():
            try:
                result = analyze_python_file(item)
                python_analysis.append(result)
            except SyntaxError:
                python_analysis.append({
                    "file": str(item),
                    "error": "Could not parse Python file"
                })

    return {
        "summary": summary,
        "python_files": python_analysis
    }