import ast


def analyze_python_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()

    tree = ast.parse(code)

    functions = 0
    classes = 0
    imports = 0

    for node in ast.walk(tree):

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions += 1

        elif isinstance(node, ast.ClassDef):
            classes += 1

        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            imports += 1

    return {
        "file": str(file_path),
        "functions": functions,
        "classes": classes,
        "imports": imports
    }