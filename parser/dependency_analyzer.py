import ast


def find_imports(file_path):
    """
    Extract imported module names from a Python file.

    Absolute imports are returned normally.

    Relative imports are converted into a dotted representation
    while preserving the relative-import level so that the
    dependency graph can resolve them correctly.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()

    tree = ast.parse(code)

    imports = []

    for node in ast.walk(tree):

        # -----------------------------------------------------
        # NORMAL IMPORT
        # -----------------------------------------------------

        if isinstance(node, ast.Import):

            for name in node.names:

                imports.append(
                    name.name
                )

        # -----------------------------------------------------
        # FROM IMPORT
        # -----------------------------------------------------

        elif isinstance(node, ast.ImportFrom):

            module = node.module or ""

            # ast.ImportFrom.level:
            #
            # 0 -> absolute import
            # 1 -> .
            # 2 -> ..
            # etc.
            #
            # Preserve the dots so dependency_graph.py can
            # identify that this is a relative import.

            relative_prefix = "." * node.level

            imported_module = (
                relative_prefix + module
            )

            # Avoid storing an empty import for unusual cases
            # such as "from . import something".

            if imported_module:

                imports.append(
                    imported_module
                )

    return imports