from pathlib import Path


IGNORED_DIRS = {
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    "node_modules",
}


def should_ignore(path):
    """Return True if the path belongs to an ignored directory."""
    path = Path(path)

    return any(
        part in IGNORED_DIRS
        for part in path.parts
    )


def search_files(
    project_path=".",
    query="",
    risk="all",
    complexity_filter="all",
    highly_coupled=False,
):
    """
    Search and filter Python files using PHANTOM's
    real intelligence data.
    """

    project_path = Path(
        project_path
    ).resolve()

    # ---------------------------------------------------------
    # PHANTOM INTELLIGENCE
    # ---------------------------------------------------------

    from .dependency_graph import (
        build_dependency_graph,
    )

    from .complexity_analyzer import (
        analyze_complexity,
    )

    from .hotspot_analyzer import (
        analyze_hotspots,
    )

    from .risk_analyzer import (
        analyze_risks,
    )

    graph = build_dependency_graph(
        project_path
    )

    complexity_data = analyze_complexity(
        str(project_path)
    )

    hotspot_data = analyze_hotspots(
        str(project_path)
    )

    risk_data = analyze_risks(
        str(project_path)
    )

    # ---------------------------------------------------------
    # COMPLEXITY LOOKUP
    # ---------------------------------------------------------

    complexity_lookup = {}

    if isinstance(complexity_data, list):

        for file_data in complexity_data:

            if not isinstance(
                file_data,
                dict,
            ):
                continue

            file_name = file_data.get(
                "file"
            )

            if not file_name:
                continue

            functions = file_data.get(
                "functions",
                [],
            )

            total_complexity = 0

            for function in functions:

                if not isinstance(
                    function,
                    dict,
                ):
                    continue

                value = function.get(
                    "complexity",
                    1,
                )

                if isinstance(
                    value,
                    (int, float),
                ):
                    total_complexity += value

            if not functions:
                total_complexity = 1

            normalized = str(
                Path(file_name).as_posix()
            )

            complexity_lookup[
                normalized
            ] = total_complexity

    # ---------------------------------------------------------
    # HOTSPOT LOOKUP
    # ---------------------------------------------------------

    hotspot_lookup = {}

    if isinstance(
        hotspot_data,
        dict,
    ):

        for hotspot in hotspot_data.get(
            "hotspots",
            [],
        ):

            if not isinstance(
                hotspot,
                dict,
            ):
                continue

            file_name = hotspot.get(
                "file"
            )

            if file_name:

                hotspot_lookup[
                    str(
                        Path(file_name).as_posix()
                    )
                ] = hotspot.get(
                    "score",
                    0,
                )

    # ---------------------------------------------------------
    # RISK LOOKUP
    # ---------------------------------------------------------

    risk_lookup = {}

    if isinstance(
        risk_data,
        dict,
    ):

        for risk_item in risk_data.get(
            "risks",
            [],
        ):

            if not isinstance(
                risk_item,
                dict,
            ):
                continue

            file_name = risk_item.get(
                "file"
            )

            if file_name:

                risk_lookup[
                    str(
                        Path(file_name).as_posix()
                    )
                ] = risk_item

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------

    results = []

    for file_path, dependency_data in graph.items():

        normalized_file = str(
            Path(file_path).as_posix()
        )

        # -----------------------------------------------------
        # QUERY FILTER
        # -----------------------------------------------------

        if query:

            query_lower = query.lower()

            if query_lower not in normalized_file.lower():
                continue

        # -----------------------------------------------------
        # DEPENDENCIES
        # -----------------------------------------------------

        internal = dependency_data.get(
            "internal",
            [],
        )

        external = dependency_data.get(
            "external",
            [],
        )

        dependency_count = (
            len(internal)
            + len(external)
        )

        # -----------------------------------------------------
        # REAL COMPLEXITY
        # -----------------------------------------------------

        complexity = complexity_lookup.get(
            normalized_file,
            1,
        )

        if complexity >= 11:
            complexity_level = "high"

        elif complexity >= 6:
            complexity_level = "medium"

        else:
            complexity_level = "low"

        # -----------------------------------------------------
        # REAL RISK
        # -----------------------------------------------------

        risk_item = risk_lookup.get(
            normalized_file,
            {},
        )

        risk_level = risk_item.get(
            "level",
            "low",
        )

        risk_score = risk_item.get(
            "score",
            0,
        )

        # -----------------------------------------------------
        # REAL HOTSPOT
        # -----------------------------------------------------

        hotspot_score = hotspot_lookup.get(
            normalized_file,
            0,
        )

        highly_connected = (
            len(internal) >= 5
        )

        # -----------------------------------------------------
        # RISK FILTER
        # -----------------------------------------------------

        if risk.lower() != "all":

            if risk.lower() != risk_level:
                continue

        # -----------------------------------------------------
        # COMPLEXITY FILTER
        # -----------------------------------------------------

        if (
            complexity_filter.lower()
            != "all"
        ):

            if (
                complexity_filter.lower()
                != complexity_level
            ):
                continue

        # -----------------------------------------------------
        # COUPLING FILTER
        # -----------------------------------------------------

        if (
            highly_coupled
            and not highly_connected
        ):
            continue

        # -----------------------------------------------------
        # FILE METRICS
        # -----------------------------------------------------

        try:

            full_path = (
                project_path
                / file_path
            )

            lines = full_path.read_text(
                encoding="utf-8"
            ).splitlines()

            line_count = len(lines)

        except (
            UnicodeDecodeError,
            OSError,
        ):

            line_count = 0

        # -----------------------------------------------------
        # RESULT
        # -----------------------------------------------------

        results.append(
            {
                "file": normalized_file,
                "lines": line_count,
                "dependencies": dependency_count,
                "internal_dependencies": len(
                    internal
                ),
                "external_dependencies": len(
                    external
                ),
                "complexity": complexity,
                "complexity_level": complexity_level,
                "risk": risk_level,
                "risk_score": risk_score,
                "hotspot_score": hotspot_score,
                "highly_coupled": highly_connected,
            }
        )

    # ---------------------------------------------------------
    # SORT
    # ---------------------------------------------------------

    risk_order = {
        "high": 0,
        "medium": 1,
        "low": 2,
    }

    results.sort(
        key=lambda item: (
            risk_order.get(
                item["risk"],
                3,
            ),
            -item["risk_score"],
            -item["hotspot_score"],
            -item["complexity"],
        )
    )

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    return {
        "query": query,
        "filters": {
            "risk": risk,
            "complexity": complexity_filter,
            "highly_coupled": highly_coupled,
        },
        "count": len(results),
        "results": results,
    }