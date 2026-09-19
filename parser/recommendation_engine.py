from pathlib import Path


def _priority_from_score(score):
    """Convert a numeric risk score into a recommendation priority."""

    if score >= 75:
        return "high"

    if score >= 40:
        return "medium"

    return "low"


def _add_recommendation(
    recommendations,
    title,
    reason,
    action,
    priority="medium",
    category="general",
):
    """Add a structured recommendation."""

    recommendations.append(
        {
            "title": title,
            "priority": priority,
            "category": category,
            "reason": reason,
            "action": action,
        }
    )


def recommend_from_metrics(metrics, recommendations):
    """Generate recommendations from project metrics."""

    if not isinstance(metrics, dict):
        return

    average_complexity = metrics.get(
        "average_complexity",
        0
    )

    maximum_complexity = metrics.get(
        "maximum_complexity",
        0
    )

    external_dependencies = metrics.get(
        "external_dependencies",
        0
    )

    internal_edges = metrics.get(
        "internal_dependency_edges",
        0
    )

    most_complex_function = metrics.get(
        "most_complex_function"
    )

    most_connected_file = metrics.get(
        "most_connected_file"
    )

    # ---------------------------------------------------------
    # HIGH COMPLEXITY
    # ---------------------------------------------------------

    if maximum_complexity >= 11:

        function_name = "the most complex functions"

        if isinstance(
            most_complex_function,
            dict
        ):
            function_name = most_complex_function.get(
                "name",
                function_name
            )

        _add_recommendation(
            recommendations,
            "Refactor highly complex functions",
            (
                f"Maximum function complexity is "
                f"{maximum_complexity}."
            ),
            (
                f"Break {function_name} into smaller "
                f"single-purpose functions and reduce "
                f"nested control flow."
            ),
            "high",
            "complexity",
        )

    elif maximum_complexity >= 6:

        _add_recommendation(
            recommendations,
            "Review moderately complex functions",
            (
                f"Maximum function complexity is "
                f"{maximum_complexity}."
            ),
            (
                "Review functions with elevated complexity "
                "and simplify branching where possible."
            ),
            "medium",
            "complexity",
        )

    # ---------------------------------------------------------
    # AVERAGE COMPLEXITY
    # ---------------------------------------------------------

    if average_complexity >= 6:

        _add_recommendation(
            recommendations,
            "Reduce overall code complexity",
            (
                f"Average project complexity is "
                f"{average_complexity}."
            ),
            (
                "Prioritize complex modules and simplify "
                "conditional and control-flow logic."
            ),
            "high",
            "complexity",
        )

    # ---------------------------------------------------------
    # EXTERNAL DEPENDENCIES
    # ---------------------------------------------------------

    if external_dependencies >= 15:

        _add_recommendation(
            recommendations,
            "Review external dependency load",
            (
                f"The project uses "
                f"{external_dependencies} external "
                f"dependencies."
            ),
            (
                "Review whether all external dependencies "
                "are necessary, actively maintained, and "
                "appropriately isolated."
            ),
            "high",
            "dependencies",
        )

    elif external_dependencies >= 8:

        _add_recommendation(
            recommendations,
            "Review external dependencies",
            (
                f"The project uses "
                f"{external_dependencies} external "
                f"dependencies."
            ),
            (
                "Check dependency necessity, maintenance, "
                "and version management."
            ),
            "medium",
            "dependencies",
        )

    # ---------------------------------------------------------
    # HIGHLY CONNECTED FILE
    # ---------------------------------------------------------

    if internal_edges >= 8:

        file_name = (
            str(most_connected_file)
            if most_connected_file
            else "the most connected file"
        )

        _add_recommendation(
            recommendations,
            "Review highly connected modules",
            (
                f"The project contains "
                f"{internal_edges} internal dependency edges."
            ),
            (
                f"Inspect {file_name} and consider reducing "
                "responsibilities or introducing clearer "
                "module boundaries."
            ),
            "medium",
            "architecture",
        )


def recommend_from_architecture(
    architecture,
    recommendations,
):
    """Generate recommendations from architecture analysis."""

    if not isinstance(architecture, dict):
        return

    score = architecture.get(
        "score",
        100
    )

    grade = architecture.get(
        "grade",
        "UNKNOWN"
    )

    circular_dependencies = architecture.get(
        "circular_dependencies",
        0
    )

    main_contributor = architecture.get(
        "main_contributor"
    )

    # ---------------------------------------------------------
    # ARCHITECTURE SCORE
    # ---------------------------------------------------------

    if score < 60:

        _add_recommendation(
            recommendations,
            "Prioritize architecture improvement",
            (
                f"Architecture score is {score}/100 "
                f"({grade})."
            ),
            (
                "Review coupling, dependency concentration, "
                "complexity, and dependency load before "
                "adding further features."
            ),
            "high",
            "architecture",
        )

    elif score < 75:

        _add_recommendation(
            recommendations,
            "Improve architectural health",
            (
                f"Architecture score is {score}/100 "
                f"({grade})."
            ),
            (
                "Focus refactoring efforts on the largest "
                "contributors to architectural risk."
            ),
            "medium",
            "architecture",
        )

    # ---------------------------------------------------------
    # CIRCULAR DEPENDENCIES
    # ---------------------------------------------------------

    if circular_dependencies > 0:

        _add_recommendation(
            recommendations,
            "Break circular dependencies",
            (
                f"{circular_dependencies} circular "
                "dependency cycle(s) were detected."
            ),
            (
                "Identify the modules involved in each cycle "
                "and introduce clearer dependency boundaries."
            ),
            "high",
            "dependencies",
        )

    # ---------------------------------------------------------
    # MAIN CONTRIBUTOR
    # ---------------------------------------------------------

    contributor_messages = {
        "coupling": (
            "Reduce unnecessary relationships between "
            "modules and separate tightly coupled "
            "responsibilities."
        ),

        "circular_dependencies": (
            "Break dependency cycles and establish a "
            "clearer direction of dependencies."
        ),

        "dependency_concentration": (
            "Distribute responsibilities across modules "
            "instead of concentrating dependencies around "
            "one module."
        ),

        "complexity": (
            "Prioritize refactoring of complex functions "
            "and simplify control flow."
        ),

        "external_dependencies": (
            "Review external libraries and reduce "
            "unnecessary dependency load."
        ),
    }

    if main_contributor in contributor_messages:

        _add_recommendation(
            recommendations,
            "Address the primary architecture risk",
            (
                f"The primary architecture risk contributor "
                f"is {main_contributor}."
            ),
            contributor_messages[main_contributor],
            "high" if score < 60 else "medium",
            "architecture",
        )


def recommend_from_smells(
    code_smells,
    recommendations,
):
    """Generate recommendations from detected code smells."""

    if not isinstance(code_smells, dict):
        return

    total_smells = code_smells.get(
        "total_smells",
        0
    )

    severity_counts = code_smells.get(
        "severity_counts",
        {}
    )

    high_smells = severity_counts.get(
        "high",
        0
    )

    medium_smells = severity_counts.get(
        "medium",
        0
    )

    # ---------------------------------------------------------
    # HIGH SEVERITY
    # ---------------------------------------------------------

    if high_smells > 0:

        _add_recommendation(
            recommendations,
            "Resolve high-severity code smells",
            (
                f"{high_smells} high-severity code smell(s) "
                "were detected."
            ),
            (
                "Inspect the affected files and address "
                "high-severity findings before lower-priority "
                "cleanup."
            ),
            "high",
            "code_smells",
        )

    # ---------------------------------------------------------
    # MEDIUM SEVERITY
    # ---------------------------------------------------------

    if medium_smells >= 5:

        _add_recommendation(
            recommendations,
            "Reduce accumulated code smells",
            (
                f"{medium_smells} medium-severity code "
                "smell(s) were detected."
            ),
            (
                "Create a cleanup/refactoring pass and "
                "address the largest files, dependency "
                "issues, and branching problems."
            ),
            "medium",
            "code_smells",
        )

    elif total_smells > 0:

        _add_recommendation(
            recommendations,
            "Review detected code smells",
            (
                f"{total_smells} code smell(s) were detected."
            ),
            (
                "Review the smell findings and address "
                "the highest-impact issues."
            ),
            "low",
            "code_smells",
        )


def generate_recommendations(
    intelligence
):
    """
    Generate explainable recommendations from PHANTOM data.
    """

    recommendations = []

    if not isinstance(intelligence, dict):
        return {
            "count": 0,
            "recommendations": [],
        }

    metrics = intelligence.get(
        "metrics",
        {}
    )

    architecture_score = intelligence.get(
        "architecture_score",
        {}
    )

    cycles = intelligence.get(
        "cycles",
        {}
    )

    code_smells = intelligence.get(
        "code_smells",
        {}
    )

    # ---------------------------------------------------------
    # Normalize architecture data
    # ---------------------------------------------------------

    architecture = dict(
        architecture_score
        if isinstance(
            architecture_score,
            dict
        )
        else {}
    )

    if isinstance(cycles, dict):

        architecture[
            "circular_dependencies"
        ] = cycles.get(
            "count",
            architecture.get(
                "circular_dependencies",
                0
            )
        )

    # ---------------------------------------------------------
    # Generate recommendations
    # ---------------------------------------------------------

    recommend_from_metrics(
        metrics,
        recommendations,
    )

    recommend_from_architecture(
        architecture,
        recommendations,
    )

    recommend_from_smells(
        code_smells,
        recommendations,
    )

    # ---------------------------------------------------------
    # Sort by priority
    # ---------------------------------------------------------

    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2,
    }

    recommendations.sort(
        key=lambda item: priority_order.get(
            item["priority"],
            3
        )
    )

    # ---------------------------------------------------------
    # Add IDs
    # ---------------------------------------------------------

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):
        recommendation["id"] = index

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    priority_counts = {
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for recommendation in recommendations:

        priority = recommendation["priority"]

        if priority in priority_counts:
            priority_counts[priority] += 1

    return {
        "count": len(recommendations),
        "priority_counts": priority_counts,
        "recommendations": recommendations,
    }

def analyze_recommendations(
    project_path="."
):
    """
    Run PHANTOM intelligence and generate recommendations.
    """

    from .phantom_intelligence import analyze_phantom

    project_path = Path(
        project_path
    ).resolve()

    intelligence = analyze_phantom(
        str(project_path)
    )

    phantom = intelligence.get(
        "phantom",
        intelligence
    )

    result = generate_recommendations(
        phantom
    )

    result["project"] = project_path.name

    return result
def _unwrap_analysis(data):
    """
    Extract the actual analyzer data from a PHANTOM
    {status, data} wrapper when present.
    """

    if not isinstance(data, dict):
        return {}

    if "data" in data and isinstance(data["data"], dict):
        return data["data"]

    return data


def generate_recommendations(
    intelligence
):
    """
    Generate explainable recommendations from PHANTOM data.
    """

    recommendations = []

    if not isinstance(intelligence, dict):
        return {
            "count": 0,
            "priority_counts": {
                "high": 0,
                "medium": 0,
                "low": 0,
            },
            "recommendations": [],
        }

    # ---------------------------------------------------------
    # UNWRAP PHANTOM ANALYZER RESULTS
    # ---------------------------------------------------------

    metrics = _unwrap_analysis(
        intelligence.get(
            "metrics",
            {}
        )
    )

    architecture_score = _unwrap_analysis(
        intelligence.get(
            "architecture_score",
            {}
        )
    )

    cycles = _unwrap_analysis(
        intelligence.get(
            "cycles",
            {}
        )
    )

    code_smells = _unwrap_analysis(
        intelligence.get(
            "code_smells",
            {}
        )
    )

    # ---------------------------------------------------------
    # NORMALIZE ARCHITECTURE DATA
    # ---------------------------------------------------------

    architecture = dict(
        architecture_score
        if isinstance(
            architecture_score,
            dict
        )
        else {}
    )

    if isinstance(cycles, dict):

        architecture[
            "circular_dependencies"
        ] = cycles.get(
            "count",
            architecture.get(
                "circular_dependencies",
                0
            )
        )

    # ---------------------------------------------------------
    # GENERATE RECOMMENDATIONS
    # ---------------------------------------------------------

    recommend_from_metrics(
        metrics,
        recommendations,
    )

    recommend_from_architecture(
        architecture,
        recommendations,
    )

    recommend_from_smells(
        code_smells,
        recommendations,
    )

    # ---------------------------------------------------------
    # SORT BY PRIORITY
    # ---------------------------------------------------------

    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2,
    }

    recommendations.sort(
        key=lambda item:
            priority_order.get(
                item.get(
                    "priority",
                    "low"
                ),
                3
            )
    )

    # ---------------------------------------------------------
    # ADD IDS
    # ---------------------------------------------------------

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):
        recommendation["id"] = index

    # ---------------------------------------------------------
    # PRIORITY SUMMARY
    # ---------------------------------------------------------

    priority_counts = {
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for recommendation in recommendations:

        priority = recommendation.get(
            "priority"
        )

        if priority in priority_counts:
            priority_counts[priority] += 1

    return {
        "count": len(recommendations),
        "priority_counts": priority_counts,
        "recommendations": recommendations,
    }