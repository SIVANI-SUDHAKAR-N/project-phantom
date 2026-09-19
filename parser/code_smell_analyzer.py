import ast
from pathlib import Path

from .dependency_graph import build_dependency_graph


IGNORED_DIRECTORIES = {
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    "node_modules",
}


# Thresholds are intentionally simple and explainable.
LARGE_FILE_LINES = 300
HIGH_DEPENDENCY_COUNT = 10
HIGH_BRANCH_COUNT = 10
COMPLEX_FUNCTION = 10


def should_ignore(path):
    """Check whether a path belongs to an ignored directory."""

    return any(
        part in IGNORED_DIRECTORIES
        for part in Path(path).parts
    )


def read_python_file(file_path):
    """Read a Python file safely."""

    try:
        return Path(file_path).read_text(
            encoding="utf-8"
        )
    except (OSError, UnicodeDecodeError):
        return None


def count_lines(code):
    """Count physical lines in a source file."""

    if not code:
        return 0

    return len(code.splitlines())


def count_branches(tree):
    """
    Count branching/control-flow constructs.
    """

    branch_nodes = (
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.IfExp,
        ast.Try,
        ast.ExceptHandler,
    )

    return sum(
        isinstance(node, branch_nodes)
        for node in ast.walk(tree)
    )


def find_duplicate_imports(tree):
    """
    Detect duplicate import statements.
    """

    imports = []
    duplicates = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for alias in node.names:

                name = alias.name

                if name in imports:
                    duplicates.append(name)
                else:
                    imports.append(name)

        elif isinstance(node, ast.ImportFrom):

            if node.module:

                name = node.module

                if name in imports:
                    duplicates.append(name)
                else:
                    imports.append(name)

    return sorted(set(duplicates))


def calculate_function_complexity(node):
    """
    Calculate a lightweight cyclomatic complexity estimate
    for an individual function.
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


def find_complex_functions(tree):
    """
    Find functions whose estimated complexity exceeds
    the configured threshold.
    """

    smells = []

    for node in ast.walk(tree):

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            )
        ):

            complexity = calculate_function_complexity(
                node
            )

            if complexity > COMPLEX_FUNCTION:

                smells.append({
                    "name": node.name,
                    "line": getattr(
                        node,
                        "lineno",
                        None
                    ),
                    "complexity": complexity,
                    "reason": (
                        f"Function complexity is "
                        f"{complexity}, above the "
                        f"threshold of "
                        f"{COMPLEX_FUNCTION}."
                    ),
                })

    return smells


def analyze_file(
    file_path,
    dependency_data=None
):
    """
    Analyze one Python file for structural code smells.
    """

    file_path = Path(file_path).resolve()

    code = read_python_file(
        file_path
    )

    if code is None:
        return []

    # --------------------------------------------------
    # PARSE SAFELY
    # --------------------------------------------------

    try:

        tree = ast.parse(code)

    except SyntaxError as error:

        return [{
            "type": "parse_warning",
            "severity": "warning",
            "line": getattr(
                error,
                "lineno",
                None
            ),
            "message": (
                "File could not be parsed, "
                "so complete smell analysis "
                "was skipped."
            ),
        }]

    smells = []

    lines = count_lines(code)

    # --------------------------------------------------
    # LARGE FILE
    # --------------------------------------------------

    if lines > LARGE_FILE_LINES:

        smells.append({
            "type": "large_file",
            "severity": "medium",
            "message": (
                f"File contains {lines} lines, "
                f"exceeding the threshold of "
                f"{LARGE_FILE_LINES}."
            ),
            "value": lines,
        })

    # --------------------------------------------------
    # EXCESSIVE DEPENDENCIES
    # --------------------------------------------------

    if dependency_data:

        internal = dependency_data.get(
            "internal",
            []
        )

        external = dependency_data.get(
            "external",
            []
        )

        total_dependencies = (
            len(internal)
            + len(external)
        )

        if total_dependencies > HIGH_DEPENDENCY_COUNT:

            smells.append({
                "type": "excessive_dependencies",
                "severity": "high",
                "message": (
                    f"File has "
                    f"{total_dependencies} "
                    f"dependencies, exceeding "
                    f"the threshold of "
                    f"{HIGH_DEPENDENCY_COUNT}."
                ),
                "value": total_dependencies,
                "internal": len(internal),
                "external": len(external),
            })

    # --------------------------------------------------
    # EXCESSIVE BRANCHING
    # --------------------------------------------------

    branches = count_branches(tree)

    if branches > HIGH_BRANCH_COUNT:

        smells.append({
            "type": "excessive_branching",
            "severity": "medium",
            "message": (
                f"File contains {branches} "
                f"branching/control-flow "
                f"constructs, exceeding the "
                f"threshold of "
                f"{HIGH_BRANCH_COUNT}."
            ),
            "value": branches,
        })

    # --------------------------------------------------
    # COMPLEX FUNCTIONS
    # --------------------------------------------------

    complex_functions = find_complex_functions(
        tree
    )

    for function in complex_functions:

        smells.append({
            "type": "complex_function",
            "severity": "high",
            "message": function["reason"],
            "function": function["name"],
            "line": function["line"],
            "complexity": function["complexity"],
        })

    # --------------------------------------------------
    # DUPLICATE IMPORTS
    # --------------------------------------------------

    duplicates = find_duplicate_imports(
        tree
    )

    if duplicates:

        smells.append({
            "type": "duplicate_imports",
            "severity": "low",
            "message": (
                "The file imports the same "
                "module more than once."
            ),
            "modules": duplicates,
        })

    return smells


def analyze_code_smells(project_path="."):
    """
    Analyze all Python files in a project.
    """

    project_path = Path(
        project_path
    ).resolve()

    graph = build_dependency_graph(
        project_path
    )

    files = {}
    total_smells = 0

    for file_path, dependency_data in graph.items():

        if should_ignore(file_path):
            continue

        # --------------------------------------------------
        # IMPORTANT:
        # The dependency graph stores relative paths.
        # Convert them into an absolute path before
        # passing them to analyze_file().
        # --------------------------------------------------

        full_file_path = (
            project_path / file_path
        ).resolve()

        smells = analyze_file(
            full_file_path,
            dependency_data
        )

        files[file_path] = {
            "smell_count": len(smells),
            "smells": smells,
        }

        total_smells += len(smells)

    # --------------------------------------------------
    # SEVERITY COUNTS
    # --------------------------------------------------

    severity_counts = {
        "high": 0,
        "medium": 0,
        "low": 0,
        "warning": 0,
    }

    for file_data in files.values():

        for smell in file_data["smells"]:

            severity = smell.get(
                "severity"
            )

            if severity in severity_counts:
                severity_counts[severity] += 1

    # --------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------

    return {
        "total_smells": total_smells,
        "severity_counts": severity_counts,
        "file_count": len(files),
        "files": files,
    }