from pathlib import Path

IGNORED_DIRS = {
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    "node_modules",
}


def should_ignore(path):
    path = Path(path)

    return any(
        part in IGNORED_DIRS
        for part in path.parts
    )


def calculate_hotspot_score(
    complexity,
    internal_dependencies,
    external_dependencies,
):
    """
    Calculate hotspot pressure for a file.

    Higher complexity and dependency counts
    produce higher hotspot pressure.
    """

    score = (
        complexity * 5
        + internal_dependencies * 3
        + external_dependencies * 2
    )

    return min(round(score), 100)


def get_hotspot_level(score):
    if score >= 70:
        return "high"

    if score >= 40:
        return "medium"

    return "low"


def build_complexity_lookup(complexity_data):
    """
    Convert complexity analyzer output into:

        file path -> total file complexity
    """

    lookup = {}

    if not isinstance(complexity_data, list):
        return lookup

    for file_data in complexity_data:

        if not isinstance(file_data, dict):
            continue

        file_name = file_data.get("file")

        if not file_name:
            continue

        functions = file_data.get(
            "functions",
            []
        )

        total_complexity = 0

        for function in functions:

            if not isinstance(function, dict):
                continue

            complexity = function.get(
                "complexity",
                1
            )

            if isinstance(
                complexity,
                (int, float),
            ):
                total_complexity += complexity

        if not functions:
            total_complexity = 1

        lookup[
            str(
                Path(file_name).as_posix()
            )
        ] = total_complexity

    return lookup


def analyze_hotspots(project_path="."):
    """
    Analyze hotspot pressure for every Python file.
    """

    project_path = Path(
        project_path
    ).resolve()

    from .dependency_graph import (
        build_dependency_graph,
    )

    from .complexity_analyzer import (
        analyze_complexity,
    )

    graph = build_dependency_graph(
        project_path
    )

    complexity_data = analyze_complexity(
        str(project_path)
    )

    complexity_lookup = (
        build_complexity_lookup(
            complexity_data
        )
    )

    hotspots = []

    for file_path, dependency_data in graph.items():

        internal = dependency_data.get(
            "internal",
            [],
        )

        external = dependency_data.get(
            "external",
            [],
        )

        normalized_file = str(
            Path(file_path).as_posix()
        )

        complexity = complexity_lookup.get(
            normalized_file,
            1,
        )

        score = calculate_hotspot_score(
            complexity=complexity,
            internal_dependencies=len(
                internal
            ),
            external_dependencies=len(
                external
            ),
        )

        level = get_hotspot_level(
            score
        )

        hotspots.append(
            {
                "file": file_path,
                "complexity": complexity,
                "internal_dependencies": len(
                    internal
                ),
                "external_dependencies": len(
                    external
                ),
                "score": score,
                "level": level,
            }
        )

    hotspots.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    severity_counts = {
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for hotspot in hotspots:

        level = hotspot.get(
            "level"
        )

        if level in severity_counts:
            severity_counts[level] += 1

    return {
        "project": project_path.name,
        "hotspot_count": len(
            hotspots
        ),
        "severity_counts": severity_counts,
        "hotspots": hotspots,
        "top_hotspot": (
            hotspots[0]
            if hotspots
            else None
        ),
    }