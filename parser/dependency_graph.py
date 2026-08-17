from pathlib import Path

from .dependency_analyzer import find_imports


def build_dependency_graph(project_path):
    path = Path(project_path)

    graph = {}

    for file in path.rglob("*.py"):
        if not file.is_file():
            continue

        imports = find_imports(file)

        internal = []
        external = []

        for imported in imports:
            module_path = path / imported.replace(".", "/")

            if (module_path.with_suffix(".py")).exists():
                internal.append(imported)
            else:
                external.append(imported)

        graph[str(file)] = {
            "internal": internal,
            "external": external
        }

    return graph