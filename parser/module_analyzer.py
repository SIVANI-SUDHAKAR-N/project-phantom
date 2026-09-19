from pathlib import Path
from collections import defaultdict

from .architecture_analyzer import detect_modules
from .dependency_graph import build_dependency_graph


def get_module(file_path, project_path):
    """
    Determine which architectural module a file belongs to.
    """

    file_path = Path(file_path).resolve()
    project_path = Path(project_path).resolve()

    try:
        relative = file_path.relative_to(project_path)
    except ValueError:
        return "external"

    if len(relative.parts) == 1:
        return "root"

    return relative.parts[0]


def build_module_relationships(project_path="."):
    """
    Convert the file-level dependency graph into a module-level graph.
    """

    project_path = Path(project_path).resolve()

    file_graph = build_dependency_graph(project_path)
    modules = detect_modules(project_path)

    relationships = defaultdict(
        lambda: {
            "depends_on": set(),
            "depended_by": set(),
            "edge_count": 0,
        }
    )

    for file_path, dependency_data in file_graph.items():

        source_module = get_module(
            file_path,
            project_path
        )

        if source_module not in modules:
            continue

        for dependency in dependency_data.get(
            "internal",
            []
        ):

            # The dependency graph now returns
            # relative file paths such as:
            # parser/analyzer.py

            dependency_path = (
                project_path / dependency
            )

            candidate_files = [
                dependency_path,
                dependency_path / "__init__.py",
            ]

            target_file = None

            for candidate in candidate_files:

                if candidate.exists():
                    target_file = candidate
                    break

            if target_file is None:
                continue

            target_module = get_module(
                target_file,
                project_path
            )

            if target_module == source_module:
                continue

            relationships[source_module][
                "depends_on"
            ].add(target_module)

            relationships[target_module][
                "depended_by"
            ].add(source_module)

            relationships[source_module][
                "edge_count"
            ] += 1

    result = {}

    for module in sorted(modules):

        relationship = relationships[module]

        result[module] = {
            "depends_on": sorted(
                relationship["depends_on"]
            ),
            "depended_by": sorted(
                relationship["depended_by"]
            ),
            "fan_out": len(
                relationship["depends_on"]
            ),
            "fan_in": len(
                relationship["depended_by"]
            ),
            "edge_count": relationship[
                "edge_count"
            ],
        }

    return result


def calculate_module_coupling(relationships):
    """
    Calculate module coupling.
    """

    result = {}

    for module, data in relationships.items():

        fan_in = data["fan_in"]
        fan_out = data["fan_out"]

        coupling = fan_in + fan_out

        result[module] = {
            **data,
            "coupling_score": coupling,
        }

    return result


def detect_highly_connected_modules(
    modules,
    threshold=3
):
    """
    Identify modules whose coupling score is
    greater than or equal to the threshold.
    """

    highly_connected = []

    for module, data in modules.items():

        score = data.get(
            "coupling_score",
            0
        )

        if score >= threshold:

            highly_connected.append({
                "module": module,
                "coupling_score": score,
                "fan_in": data.get(
                    "fan_in",
                    0
                ),
                "fan_out": data.get(
                    "fan_out",
                    0
                ),
            })

    highly_connected.sort(
        key=lambda item: item["coupling_score"],
        reverse=True
    )

    return highly_connected


def calculate_dependency_concentration(
    modules
):
    """
    Measure how concentrated module connections are.

    A higher percentage means a larger share of the
    architecture's connections is concentrated around
    one module.
    """

    if not modules:
        return {
            "score": 0,
            "percentage": 0,
            "dominant_module": None,
            "total_connections": 0,
        }

    connection_counts = {}

    for module, data in modules.items():

        connection_counts[module] = (
            data.get("fan_in", 0)
            + data.get("fan_out", 0)
        )

    total_connections = sum(
        connection_counts.values()
    )

    if total_connections == 0:

        return {
            "score": 0,
            "percentage": 0,
            "dominant_module": None,
            "total_connections": 0,
        }

    dominant_module = max(
        connection_counts,
        key=connection_counts.get
    )

    dominant_connections = connection_counts[
        dominant_module
    ]

    percentage = (
        dominant_connections
        / total_connections
    ) * 100

    return {
        "score": round(percentage),
        "percentage": round(
            percentage,
            2
        ),
        "dominant_module": dominant_module,
        "total_connections": total_connections,
    }


def analyze_modules(project_path="."):
    """
    Main Module Intelligence entry point.
    """

    relationships = build_module_relationships(
        project_path
    )

    modules = calculate_module_coupling(
        relationships
    )

    highly_connected = (
        detect_highly_connected_modules(
            modules
        )
    )

    concentration = (
        calculate_dependency_concentration(
            modules
        )
    )

    most_connected = None

    if modules:

        most_connected = max(
            modules,
            key=lambda name:
            modules[name]["coupling_score"]
        )

    return {
        "module_count": len(modules),
        "modules": modules,
        "most_connected_module": most_connected,
        "highly_connected_modules":
            highly_connected,
        "dependency_concentration":
            concentration,
    }