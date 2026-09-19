from pathlib import Path

from .dependency_graph import build_dependency_graph
from .module_analyzer import analyze_modules
from .cycle_detector import analyze_cycles


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, value))


def calculate_coupling_penalty(module_data):
    """
    Calculate an architecture coupling penalty.

    Highly connected modules contribute more to architectural risk.
    """

    modules = module_data.get("modules", {})

    if not modules:
        return 0

    scores = [
        data.get("coupling_score", 0)
        for data in modules.values()
    ]

    average_coupling = sum(scores) / len(scores)

    # Keep this contribution between 0 and 20.
    return clamp(round(average_coupling * 4), 0, 20)


def calculate_concentration_penalty(module_data):
    """
    Detect dependency concentration.

    If a small number of modules handle most of the connections,
    the architecture becomes more concentrated.
    """

    modules = module_data.get("modules", {})

    if len(modules) <= 1:
        return 0

    total_connections = sum(
        data.get("fan_in", 0) + data.get("fan_out", 0)
        for data in modules.values()
    )

    if total_connections == 0:
        return 0

    maximum_connections = max(
        data.get("fan_in", 0) + data.get("fan_out", 0)
        for data in modules.values()
    )

    concentration = maximum_connections / total_connections

    return clamp(round(concentration * 15), 0, 15)


def calculate_external_dependency_penalty(graph):
    """
    Estimate architectural pressure caused by external dependencies.
    """

    if not graph:
        return 0

    external_counts = [
        len(data.get("external", []))
        for data in graph.values()
    ]

    total_external = sum(external_counts)

    if total_external == 0:
        return 0

    # Keep contribution between 0 and 20.
    return clamp(round(total_external * 2), 0, 20)


def calculate_complexity_penalty(project_path):
    """
    Calculate a complexity contribution.

    Uses the existing complexity analyzer when available.
    """

    try:
        from .complexity_analyzer import analyze_complexity

        results = analyze_complexity(project_path)

        if isinstance(results, dict):
            complexity_values = []

            for value in results.values():
                if isinstance(value, (int, float)):
                    complexity_values.append(value)

                elif isinstance(value, dict):
                    complexity = value.get("complexity")

                    if isinstance(complexity, (int, float)):
                        complexity_values.append(complexity)

            if complexity_values:
                average = sum(complexity_values) / len(complexity_values)

                return clamp(round(average * 2), 0, 20)

    except Exception:
        # Architecture scoring should not crash the entire analysis
        # if the complexity engine has an incompatible result format.
        pass

    return 0


def calculate_cycle_penalty(cycle_data):
    """
    Circular dependencies are a strong architectural risk.
    """

    count = cycle_data.get("count", 0)

    return clamp(count * 25, 0, 25)


def get_grade(score):
    if score >= 90:
        return "EXCELLENT"

    if score >= 75:
        return "GOOD"

    if score >= 60:
        return "MODERATE"

    if score >= 40:
        return "RISKY"

    return "CRITICAL"


def analyze_architecture_score(project_path="."):
    """
    Main Architecture Score engine.

    Starts from 100 and subtracts explainable architectural penalties.
    """

    project_path = Path(project_path)

    graph = build_dependency_graph(project_path)

    module_data = analyze_modules(project_path)

    cycle_data = analyze_cycles(project_path)

    coupling_penalty = calculate_coupling_penalty(module_data)

    concentration_penalty = calculate_concentration_penalty(
        module_data
    )

    external_penalty = calculate_external_dependency_penalty(
        graph
    )

    complexity_penalty = calculate_complexity_penalty(
        project_path
    )

    cycle_penalty = calculate_cycle_penalty(
        cycle_data
    )

    total_penalty = (
        coupling_penalty
        + concentration_penalty
        + external_penalty
        + complexity_penalty
        + cycle_penalty
    )

    score = clamp(100 - total_penalty)

    contributors = {
        "coupling": coupling_penalty,
        "circular_dependencies": cycle_penalty,
        "dependency_concentration": concentration_penalty,
        "complexity": complexity_penalty,
        "external_dependencies": external_penalty,
    }

    main_contributor = max(
        contributors,
        key=contributors.get
    )

    return {
        "score": score,
        "grade": get_grade(score),
        "total_penalty": total_penalty,
        "contributors": contributors,
        "main_contributor": main_contributor,
        "circular_dependency_count": cycle_data.get("count", 0),
        "most_connected_module": module_data.get(
            "most_connected_module"
        ),
    }