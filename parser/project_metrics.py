import ast
from pathlib import Path
from collections import defaultdict

from .dependency_graph import build_dependency_graph


IGNORED_DIRECTORIES = {
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    "node_modules",
}


def should_ignore(path):
    """Return True when a file is inside an ignored directory."""

    return any(
        part in IGNORED_DIRECTORIES
        for part in Path(path).parts
    )


def read_file(file_path):
    """Safely read a source file."""

    try:
        return Path(file_path).read_text(
            encoding="utf-8"
        )
    except (OSError, UnicodeDecodeError):
        return None


def calculate_function_complexity(node):
    """
    Calculate a lightweight cyclomatic complexity value.
    """

    complexity = 1

    branch_nodes = (
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.IfExp,
        ast.ExceptHandler,
    )

    for child in ast.walk(node):

        if isinstance(child, branch_nodes):
            complexity += 1

        elif isinstance(child, ast.BoolOp):
            complexity += max(
                0,
                len(child.values) - 1
            )

    return complexity


def analyze_python_file(file_path):
    """
    Extract metrics from one Python file.
    """

    code = read_file(file_path)

    if code is None:
        return None

    lines = len(code.splitlines())

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {
            "lines": lines,
            "functions": 0,
            "classes": 0,
            "complexities": [],
            "parse_error": True,
        }

    functions = []
    classes = []
    complexities = []

    for node in ast.walk(tree):

        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            complexity = calculate_function_complexity(
                node
            )

            functions.append(node.name)

            complexities.append({
                "name": node.name,
                "complexity": complexity,
                "line": getattr(
                    node,
                    "lineno",
                    None
                ),
            })

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return {
        "lines": lines,
        "functions": len(functions),
        "classes": len(classes),
        "complexities": complexities,
        "parse_error": False,
    }


def calculate_metrics(project_path="."):
    """
    Calculate complete project-level metrics.
    """

    project_path = Path(project_path).resolve()

    graph = build_dependency_graph(
        project_path
    )

    total_files = 0
    python_files = 0
    total_lines = 0
    total_functions = 0
    total_classes = 0

    internal_edges = 0
    external_dependencies = set()

    all_complexities = []

    file_dependency_counts = {}

    most_connected_file = None
    highest_file_dependencies = -1

    most_complex_function = None

    file_metrics = {}

    for file_path, dependency_data in graph.items():

        if should_ignore(file_path):
            continue

        total_files += 1
        python_files += 1

        internal = dependency_data.get(
            "internal",
            []
        )

        external = dependency_data.get(
            "external",
            []
        )

        internal_edges += len(internal)

        external_dependencies.update(
            external
        )

        dependency_count = (
            len(internal)
            + len(external)
        )

        file_dependency_counts[
            file_path
        ] = dependency_count

        if dependency_count > highest_file_dependencies:

            highest_file_dependencies = (
                dependency_count
            )

            most_connected_file = file_path

        metrics = analyze_python_file(
            file_path
        )

        if metrics is None:
            continue

        file_metrics[file_path] = metrics

        total_lines += metrics["lines"]
        total_functions += metrics["functions"]
        total_classes += metrics["classes"]

        all_complexities.extend(
            metrics["complexities"]
        )

    # ----------------------------------------------
    # Complexity statistics
    # ----------------------------------------------

    complexity_values = [
        item["complexity"]
        for item in all_complexities
    ]

    if complexity_values:

        average_complexity = (
            sum(complexity_values)
            / len(complexity_values)
        )

        maximum_complexity = max(
            complexity_values
        )

        most_complex_function = max(
            all_complexities,
            key=lambda item:
            item["complexity"]
        )

    else:

        average_complexity = 0
        maximum_complexity = 0

    # ----------------------------------------------
    # Average dependencies
    # ----------------------------------------------

    if python_files:

        average_dependencies = (
            sum(
                file_dependency_counts.values()
            )
            / python_files
        )

    else:

        average_dependencies = 0

    return {
        "total_files": total_files,
        "python_files": python_files,
        "lines_of_code": total_lines,
        "functions": total_functions,
        "classes": total_classes,

        "internal_dependency_edges":
            internal_edges,

        "external_dependencies":
            len(external_dependencies),

        "external_dependency_names":
            sorted(external_dependencies),

        "average_complexity":
            round(average_complexity, 2),

        "maximum_complexity":
            maximum_complexity,

        "average_dependencies":
            round(average_dependencies, 2),

        "most_connected_file":
            most_connected_file,

        "most_connected_file_dependencies":
            max(
                highest_file_dependencies,
                0
            ),

        "most_complex_function":
            most_complex_function,

        "file_metrics":
            file_metrics,
    }


def analyze_project_metrics(project_path="."):
    """
    Public entry point for Phantom's project metrics engine.
    """

    return calculate_metrics(project_path)