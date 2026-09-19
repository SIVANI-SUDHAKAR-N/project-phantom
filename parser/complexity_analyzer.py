import ast
from pathlib import Path


# ==========================================
# CYCLOMATIC COMPLEXITY
# ==========================================

class ComplexityVisitor(ast.NodeVisitor):

    def __init__(self):
        self.complexity = 1

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_IfExp(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        # and / or introduce additional paths
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)


# ==========================================
# FUNCTION ANALYSIS
# ==========================================

def calculate_function_complexity(node):

    visitor = ComplexityVisitor()

    for child in node.body:
        visitor.visit(child)

    return visitor.complexity


# ==========================================
# FILE ANALYSIS
# ==========================================

def analyze_file_complexity(file_path, project_path=None):

    try:

        file_path = Path(file_path)

        source = file_path.read_text(
            encoding="utf-8"
        )

        tree = ast.parse(source)

    except Exception as error:

        return {
            "file": str(file_path),
            "functions": [],
            "error": str(error)
        }


    functions = []


    for node in ast.walk(tree):

        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef)
        ):

            complexity = calculate_function_complexity(node)

            functions.append({

                "name": node.name,

                "complexity":
                    complexity,

                "line":
                    node.lineno

            })


    # ==========================================
    # NORMALIZE FILE PATH
    # ==========================================

    if project_path is not None:

        try:

            relative_path = (
                file_path
                .resolve()
                .relative_to(
                    Path(project_path).resolve()
                )
                .as_posix()
            )

        except ValueError:

            relative_path = file_path.as_posix()

    else:

        relative_path = file_path.as_posix()


    return {

        "file":
            relative_path,

        "functions":
            functions

    }


# ==========================================
# PROJECT ANALYSIS
# ==========================================

def analyze_complexity(project_path):

    project_path = Path(project_path).resolve()

    results = []


    for file in project_path.rglob("*.py"):

        # Ignore virtual environments
        if ".venv" in file.parts:
            continue

        if "venv" in file.parts:
            continue

        # Ignore cache
        if "__pycache__" in file.parts:
            continue

        # Ignore Git
        if ".git" in file.parts:
            continue

        # Ignore Node modules
        if "node_modules" in file.parts:
            continue

        results.append(
            analyze_file_complexity(
                file,
                project_path
            )
        )


    return results