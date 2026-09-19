from pathlib import Path


def find_cycles(graph):
    """
    Detect circular dependencies in a directed dependency graph.

    Graph format:
    {
        "file_a.py": {
            "internal": ["file_b.py"],
            "external": []
        }
    }
    """

    cycles = []
    visited = set()
    recursion_stack = []

    def dfs(node):
        if node in recursion_stack:
            start = recursion_stack.index(node)
            cycle = recursion_stack[start:] + [node]

            # Normalize cycle to prevent duplicates
            normalized = tuple(sorted(cycle))

            existing = {
                tuple(sorted(existing_cycle))
                for existing_cycle in cycles
            }

            if normalized not in existing:
                cycles.append(cycle)

            return

        if node in visited:
            return

        recursion_stack.append(node)

        dependencies = graph.get(node, {}).get("internal", [])

        for dependency in dependencies:
            dfs(dependency)

        recursion_stack.pop()
        visited.add(node)

    for node in graph:
        dfs(node)

    return cycles


def analyze_cycles(project_path="."):
    """
    Build the project's dependency graph and detect circular dependencies.
    """

    from parser.dependency_graph import build_dependency_graph

    project_path = Path(project_path)

    graph = build_dependency_graph(project_path)

    cycles = find_cycles(graph)

    return {
        "count": len(cycles),
        "cycles": cycles
    }