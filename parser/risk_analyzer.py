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
    return any(part in IGNORED_DIRS for part in path.parts)


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, value))


def get_risk_level(score):
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def calculate_file_risk(
    complexity,
    internal_dependencies,
    external_dependencies,
    hotspot_score=0,
    smell_count=0,
):
    complexity_penalty = min(complexity * 3, 30)
    internal_penalty = min(internal_dependencies * 4, 20)
    external_penalty = min(external_dependencies * 2, 10)
    hotspot_penalty = min(hotspot_score * 0.25, 25)
    smell_penalty = min(smell_count * 3, 15)

    score = (
        complexity_penalty
        + internal_penalty
        + external_penalty
        + hotspot_penalty
        + smell_penalty
    )

    return clamp(round(score))


def build_risk_reasons(
    complexity,
    internal_dependencies,
    external_dependencies,
    hotspot_score,
    smell_count,
):
    reasons = []

    if complexity >= 11:
        reasons.append("High cyclomatic complexity")
    elif complexity >= 6:
        reasons.append("Moderate cyclomatic complexity")

    if internal_dependencies >= 5:
        reasons.append("High internal coupling")
    elif internal_dependencies >= 3:
        reasons.append("Moderate internal coupling")

    if external_dependencies >= 5:
        reasons.append("Many external dependencies")
    elif external_dependencies >= 3:
        reasons.append("Several external dependencies")

    if hotspot_score >= 70:
        reasons.append("High hotspot pressure")
    elif hotspot_score >= 40:
        reasons.append("Moderate hotspot pressure")

    if smell_count > 0:
        reasons.append(
            f"{smell_count} code smell(s) detected"
        )

    if not reasons:
        reasons.append(
            "No major risk contributors detected"
        )

    return reasons


# ---------------------------------------------------------
# COMPLEXITY LOOKUP
# ---------------------------------------------------------

def build_complexity_lookup(complexity_data):
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
                (int, float)
            ):
                total_complexity += complexity

        # Files without functions still get
        # a baseline complexity.
        if not functions:
            total_complexity = 1

        # Normalize Windows/Linux path separators.
        normalized_file = str(
            Path(file_name).as_posix()
        )

        lookup[normalized_file] = (
            total_complexity
        )

    return lookup


# ---------------------------------------------------------
# HOTSPOT LOOKUP
# ---------------------------------------------------------

def build_hotspot_lookup(hotspot_data):
    lookup = {}

    if not isinstance(
        hotspot_data,
        dict
    ):
        return lookup

    hotspots = hotspot_data.get(
        "hotspots",
        []
    )

    for hotspot in hotspots:

        if not isinstance(
            hotspot,
            dict
        ):
            continue

        file_name = hotspot.get(
            "file"
        )

        if not file_name:
            continue

        score = hotspot.get(
            "score",
            0
        )

        normalized_file = str(
            Path(file_name).as_posix()
        )

        lookup[normalized_file] = score

    return lookup


# ---------------------------------------------------------
# CODE SMELL LOOKUP
# ---------------------------------------------------------

def build_smell_lookup(smell_data):
    lookup = {}

    if not isinstance(
        smell_data,
        dict
    ):
        return lookup

    files = smell_data.get(
        "files",
        {}
    )

    if not isinstance(
        files,
        dict
    ):
        return lookup

    for file_name, file_data in files.items():

        if not isinstance(
            file_data,
            dict
        ):
            continue

        smell_count = file_data.get(
            "smell_count",
            0
        )

        normalized_file = str(
            Path(file_name).as_posix()
        )

        lookup[normalized_file] = (
            smell_count
        )

    return lookup


# ---------------------------------------------------------
# MAIN RISK ANALYSIS
# ---------------------------------------------------------

def analyze_risks(project_path="."):

    project_path = Path(
        project_path
    ).resolve()

    from .dependency_graph import (
        build_dependency_graph
    )

    from .complexity_analyzer import (
        analyze_complexity
    )

    from .hotspot_analyzer import (
        analyze_hotspots
    )

    from .code_smell_analyzer import (
        analyze_code_smells
    )

    # -----------------------------------------------------
    # Build intelligence sources
    # -----------------------------------------------------

    graph = build_dependency_graph(
        project_path
    )

    complexity_data = analyze_complexity(
        str(project_path)
    )

    hotspot_data = analyze_hotspots(
        str(project_path)
    )

    smell_data = analyze_code_smells(
        str(project_path)
    )

    # -----------------------------------------------------
    # Build lookup tables
    # -----------------------------------------------------

    complexity_lookup = (
        build_complexity_lookup(
            complexity_data
        )
    )

    hotspot_lookup = (
        build_hotspot_lookup(
            hotspot_data
        )
    )

    smell_lookup = (
        build_smell_lookup(
            smell_data
        )
    )

    # -----------------------------------------------------
    # Calculate risks
    # -----------------------------------------------------

    risks = []

    for file_path, dependency_data in graph.items():

        # Normalize file path so every analyzer
        # uses the same representation.
        normalized_file = str(
            Path(file_path).as_posix()
        )

        internal = dependency_data.get(
            "internal",
            []
        )

        external = dependency_data.get(
            "external",
            []
        )

        # -------------------------------------------------
        # Get REAL complexity
        # -------------------------------------------------

        complexity = complexity_lookup.get(
            normalized_file,
            1
        )

        # -------------------------------------------------
        # Get hotspot score
        # -------------------------------------------------

        hotspot_score = hotspot_lookup.get(
            normalized_file,
            0
        )

        # -------------------------------------------------
        # Get code smell count
        # -------------------------------------------------

        smell_count = smell_lookup.get(
            normalized_file,
            0
        )

        # -------------------------------------------------
        # Calculate risk score
        # -------------------------------------------------

        score = calculate_file_risk(
            complexity=complexity,
            internal_dependencies=len(
                internal
            ),
            external_dependencies=len(
                external
            ),
            hotspot_score=hotspot_score,
            smell_count=smell_count,
        )

        level = get_risk_level(
            score
        )

        reasons = build_risk_reasons(
            complexity=complexity,
            internal_dependencies=len(
                internal
            ),
            external_dependencies=len(
                external
            ),
            hotspot_score=hotspot_score,
            smell_count=smell_count,
        )

        risks.append(
            {
                "file": normalized_file,
                "score": score,
                "level": level,
                "complexity": complexity,
                "internal_dependencies": len(
                    internal
                ),
                "external_dependencies": len(
                    external
                ),
                "hotspot_score": hotspot_score,
                "code_smells": smell_count,
                "reasons": reasons,
            }
        )

    # -----------------------------------------------------
    # Highest risk first
    # -----------------------------------------------------

    risks.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    # -----------------------------------------------------
    # Severity statistics
    # -----------------------------------------------------

    severity_counts = {
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for risk in risks:

        level = risk.get(
            "level"
        )

        if level in severity_counts:
            severity_counts[level] += 1

    # -----------------------------------------------------
    # Final result
    # -----------------------------------------------------

    return {
        "project": project_path.name,
        "risk_count": len(risks),
        "severity_counts": severity_counts,
        "risks": risks,
        "top_risk": (
            risks[0]
            if risks
            else None
        ),
    }