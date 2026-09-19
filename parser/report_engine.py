from pathlib import Path
from datetime import datetime
import json
import csv
import io


def _safe(value, default=0):
    return value if value is not None else default


def _get_phantom_data(project_path="."):
    """Run the complete PHANTOM intelligence pipeline."""

    from .phantom_intelligence import analyze_phantom

    result = analyze_phantom(
        str(Path(project_path).resolve())
    )

    return result.get("phantom", {})


def build_report(project_path="."):
    """
    Build a complete structured PROJECT-PHANTOM report.
    """

    project_path = Path(project_path).resolve()

    data = _get_phantom_data(project_path)

    metrics = data.get("metrics", {})
    architecture = data.get("architecture_score", {})
    cycles = data.get("cycles", {})
    smells = data.get("code_smells", {})
    modules = data.get("modules", {})
    hotspots = data.get("hotspots", {})
    risks = data.get("risks", {})
    health = data.get("health_history", {})

    report = {
        "report": {
            "title": "PROJECT-PHANTOM Engineering Analysis Report",
            "version": "1.0",
            "generated_at": datetime.now().isoformat(
                timespec="seconds"
            ),
            "project": project_path.name,
        },

        # -----------------------------------------------------
        # EXECUTIVE OVERVIEW
        # -----------------------------------------------------

        "overview": {
            "architecture_score": _safe(
                architecture.get("score")
            ),
            "architecture_grade": architecture.get(
                "grade",
                "UNKNOWN"
            ),
            "circular_dependencies": _safe(
                cycles.get("count")
            ),
            "code_smells": _safe(
                smells.get("total_smells")
            ),
            "hotspots": _safe(
                hotspots.get("hotspot_count")
            ),
            "risks": _safe(
                risks.get("risk_count")
            ),
        },

        # -----------------------------------------------------
        # PROJECT METRICS
        # -----------------------------------------------------

        "metrics": metrics,

        # -----------------------------------------------------
        # ARCHITECTURE
        # -----------------------------------------------------

        "architecture": {
            "score": _safe(
                architecture.get("score")
            ),
            "grade": architecture.get(
                "grade",
                "UNKNOWN"
            ),
            "main_contributor": architecture.get(
                "main_contributor"
            ),
            "most_connected_module": architecture.get(
                "most_connected_module"
            ),
            "circular_dependencies": _safe(
                cycles.get("count")
            ),
            "module_count": _safe(
                modules.get("module_count")
            ),
            "contributors": architecture.get(
                "contributors",
                {}
            ),
        },

        # -----------------------------------------------------
        # DEPENDENCIES
        # -----------------------------------------------------

        "dependencies": {
            "internal_edges": _safe(
                metrics.get(
                    "internal_dependency_edges"
                )
            ),
            "external_dependencies": _safe(
                metrics.get(
                    "external_dependencies"
                )
            ),
            "external_dependency_names": metrics.get(
                "external_dependency_names",
                []
            ),
        },

        # -----------------------------------------------------
        # COMPLEXITY
        # -----------------------------------------------------

        "complexity": {
            "average": _safe(
                metrics.get(
                    "average_complexity"
                )
            ),
            "maximum": _safe(
                metrics.get(
                    "maximum_complexity"
                )
            ),
            "most_complex_function": metrics.get(
                "most_complex_function"
            ),
        },

        # -----------------------------------------------------
        # HOTSPOTS
        # -----------------------------------------------------

        "hotspots": hotspots,

        # -----------------------------------------------------
        # RISK INTELLIGENCE
        # -----------------------------------------------------

        "risks": risks,

        # -----------------------------------------------------
        # CODE SMELLS
        # -----------------------------------------------------

        "code_smells": smells,

        # -----------------------------------------------------
        # HEALTH HISTORY
        # -----------------------------------------------------

        "health_history": health,

        # -----------------------------------------------------
        # RECOMMENDATIONS
        # -----------------------------------------------------

        "recommendations": [],
    }

    # ---------------------------------------------------------
    # RECOMMENDATIONS
    # ---------------------------------------------------------

    try:

        from .recommendation_engine import (
            generate_recommendations
        )

        recommendation_data = generate_recommendations(
            data
        )

        report["recommendations"] = (
            recommendation_data.get(
                "recommendations",
                []
            )
        )

    except Exception as error:

        report["recommendations"] = [
            {
                "title": "Recommendation engine unavailable",
                "priority": "medium",
                "category": "system",
                "reason": str(error),
                "action": (
                    "Check the recommendation engine."
                ),
            }
        ]

    return report


def generate_text_report(project_path="."):
    """
    Generate a professional human-readable TXT report.
    """

    report = build_report(project_path)

    output = []

    # =========================================================
    # HEADER
    # =========================================================

    output.append("=" * 72)
    output.append("                    PROJECT-PHANTOM 👽")
    output.append("             ENGINEERING ANALYSIS REPORT")
    output.append("=" * 72)

    metadata = report["report"]

    output.append(
        f"Project       : {metadata['project']}"
    )

    output.append(
        f"Report Version: {metadata['version']}"
    )

    output.append(
        f"Generated     : {metadata['generated_at']}"
    )

    output.append("")

    # =========================================================
    # EXECUTIVE SUMMARY
    # =========================================================

    output.append("-" * 72)
    output.append("EXECUTIVE SUMMARY")
    output.append("-" * 72)

    overview = report["overview"]

    output.append(
        f"Architecture Score      : "
        f"{overview['architecture_score']}/100"
    )

    output.append(
        f"Architecture Grade      : "
        f"{overview['architecture_grade']}"
    )

    output.append(
        f"Circular Dependencies   : "
        f"{overview['circular_dependencies']}"
    )

    output.append(
        f"Code Smells             : "
        f"{overview['code_smells']}"
    )

    output.append(
        f"Hotspots                : "
        f"{overview['hotspots']}"
    )

    output.append(
        f"Risky Files             : "
        f"{overview['risks']}"
    )

    output.append("")

    # =========================================================
    # PROJECT METRICS
    # =========================================================

    output.append("-" * 72)
    output.append("PROJECT METRICS")
    output.append("-" * 72)

    metrics = report["metrics"]

    metric_labels = {
        "total_files": "Total Files",
        "python_files": "Python Files",
        "lines_of_code": "Lines of Code",
        "functions": "Functions",
        "classes": "Classes",
        "internal_dependency_edges":
            "Internal Dependency Edges",
        "external_dependencies":
            "External Dependencies",
        "average_complexity":
            "Average Complexity",
        "maximum_complexity":
            "Maximum Complexity",
    }

    for key, label in metric_labels.items():

        if key in metrics:

            output.append(
                f"{label:<28}: {metrics[key]}"
            )

    output.append("")

    # =========================================================
    # ARCHITECTURE INTELLIGENCE
    # =========================================================

    output.append("-" * 72)
    output.append("ARCHITECTURE INTELLIGENCE")
    output.append("-" * 72)

    architecture = report["architecture"]

    output.append(
        f"Architecture Score       : "
        f"{architecture['score']}/100"
    )

    output.append(
        f"Architecture Grade       : "
        f"{architecture['grade']}"
    )

    output.append(
        f"Modules                  : "
        f"{architecture['module_count']}"
    )

    output.append(
        f"Most Connected Module    : "
        f"{architecture['most_connected_module']}"
    )

    output.append(
        f"Main Risk Contributor    : "
        f"{architecture['main_contributor']}"
    )

    output.append(
        f"Circular Dependencies    : "
        f"{architecture['circular_dependencies']}"
    )

    output.append("")

    # =========================================================
    # COMPLEXITY
    # =========================================================

    output.append("-" * 72)
    output.append("COMPLEXITY INTELLIGENCE")
    output.append("-" * 72)

    complexity = report["complexity"]

    output.append(
        f"Average Complexity       : "
        f"{complexity['average']}"
    )

    output.append(
        f"Maximum Complexity       : "
        f"{complexity['maximum']}"
    )

    most_complex = complexity.get(
        "most_complex_function"
    )

    if isinstance(most_complex, dict):

        output.append(
            f"Most Complex Function    : "
            f"{most_complex.get('name')}"
        )

        output.append(
            f"Function Complexity      : "
            f"{most_complex.get('complexity')}"
        )

    output.append("")

    # =========================================================
    # DEPENDENCY INTELLIGENCE
    # =========================================================

    output.append("-" * 72)
    output.append("DEPENDENCY INTELLIGENCE")
    output.append("-" * 72)

    dependencies = report["dependencies"]

    output.append(
        f"Internal Dependency Edges: "
        f"{dependencies['internal_edges']}"
    )

    output.append(
        f"External Dependencies    : "
        f"{dependencies['external_dependencies']}"
    )

    external_names = dependencies.get(
        "external_dependency_names",
        []
    )

    if external_names:

        output.append(
            "External Dependency Names:"
        )

        for name in external_names:

            output.append(
                f"  - {name}"
            )

    output.append("")

    # =========================================================
    # HOTSPOTS
    # =========================================================

    output.append("-" * 72)
    output.append("HOTSPOT INTELLIGENCE")
    output.append("-" * 72)

    hotspot_data = report["hotspots"]

    output.append(
        f"Total Hotspots: "
        f"{hotspot_data.get('hotspot_count', 0)}"
    )

    severity_counts = hotspot_data.get(
        "severity_counts",
        {}
    )

    output.append(
        f"High   : {severity_counts.get('high', 0)}"
    )

    output.append(
        f"Medium : {severity_counts.get('medium', 0)}"
    )

    output.append(
        f"Low    : {severity_counts.get('low', 0)}"
    )

    top_hotspot = hotspot_data.get(
        "top_hotspot"
    )

    if isinstance(top_hotspot, dict):

        output.append("")
        output.append("Top Hotspot:")

        output.append(
            f"  File       : "
            f"{top_hotspot.get('file')}"
        )

        output.append(
            f"  Score      : "
            f"{top_hotspot.get('score')}"
        )

        output.append(
            f"  Level      : "
            f"{top_hotspot.get('level')}"
        )

        output.append(
            f"  Complexity : "
            f"{top_hotspot.get('complexity')}"
        )

    output.append("")

    # =========================================================
    # RISK INTELLIGENCE
    # =========================================================

    output.append("-" * 72)
    output.append("RISK INTELLIGENCE")
    output.append("-" * 72)

    risk_data = report["risks"]

    output.append(
        f"Total Risk Entries: "
        f"{risk_data.get('risk_count', 0)}"
    )

    risk_counts = risk_data.get(
        "severity_counts",
        {}
    )

    output.append(
        f"High   : {risk_counts.get('high', 0)}"
    )

    output.append(
        f"Medium : {risk_counts.get('medium', 0)}"
    )

    output.append(
        f"Low    : {risk_counts.get('low', 0)}"
    )

    top_risk = risk_data.get(
        "top_risk"
    )

    if isinstance(top_risk, dict):

        output.append("")
        output.append("Top Risk:")

        output.append(
            f"  File   : {top_risk.get('file')}"
        )

        output.append(
            f"  Score  : {top_risk.get('score')}"
        )

        output.append(
            f"  Level  : {top_risk.get('level')}"
        )

        reasons = top_risk.get(
            "reasons",
            []
        )

        if reasons:

            output.append("  Reasons:")

            for reason in reasons:

                output.append(
                    f"    - {reason}"
                )

    output.append("")

    # =========================================================
    # CODE SMELLS
    # =========================================================

    output.append("-" * 72)
    output.append("CODE SMELL INTELLIGENCE")
    output.append("-" * 72)

    smells = report["code_smells"]

    output.append(
        f"Total Smells: "
        f"{smells.get('total_smells', 0)}"
    )

    severity_counts = smells.get(
        "severity_counts",
        {}
    )

    for severity in [
        "high",
        "medium",
        "low",
        "warning",
    ]:

        output.append(
            f"{severity.title():<8}: "
            f"{severity_counts.get(severity, 0)}"
        )

    output.append("")

    # =========================================================
    # RECOMMENDATIONS
    # =========================================================

    output.append("-" * 72)
    output.append("PHANTOM RECOMMENDATIONS")
    output.append("-" * 72)

    recommendations = report[
        "recommendations"
    ]

    if not recommendations:

        output.append(
            "No recommendations generated."
        )

    else:

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):

            output.append(
                f"{index}. "
                f"{recommendation.get('title')}"
            )

            output.append(
                f"   Priority : "
                f"{recommendation.get('priority')}"
            )

            output.append(
                f"   Category : "
                f"{recommendation.get('category')}"
            )

            output.append(
                f"   Reason   : "
                f"{recommendation.get('reason')}"
            )

            output.append(
                f"   Action   : "
                f"{recommendation.get('action')}"
            )

            output.append("")

    # =========================================================
    # HEALTH HISTORY
    # =========================================================

    output.append("-" * 72)
    output.append("HEALTH HISTORY")
    output.append("-" * 72)

    if health:

        output.append(
            "Health history data is available "
            "in the structured report."
        )

        if isinstance(health, dict):

            snapshots = health.get(
                "snapshots",
                []
            )

            if isinstance(snapshots, list):

                output.append(
                    f"Snapshots Available: "
                    f"{len(snapshots)}"
                )

    else:

        output.append(
            "No health history information available."
        )

    output.append("")

    # =========================================================
    # FOOTER
    # =========================================================

    output.append("=" * 72)
    output.append(
        "Generated by PROJECT-PHANTOM 👽"
    )
    output.append(
        "Static Code Intelligence • Architecture • Risk • Quality"
    )
    output.append("=" * 72)

    return "\n".join(output)


def export_json(project_path="."):
    """
    Return the complete PHANTOM report as JSON text.
    """

    report = build_report(project_path)

    return json.dumps(
        report,
        indent=2,
        default=str
    )


def export_csv(project_path="."):
    """
    Export important PHANTOM metrics and intelligence
    as CSV text.
    """

    report = build_report(project_path)

    rows = []

    fields = [
        "category",
        "metric",
        "value",
    ]

    def add_row(category, metric, value):
        rows.append(
            {
                "category": category,
                "metric": metric,
                "value": value,
            }
        )

    # ---------------------------------------------------------
    # PROJECT METRICS
    # ---------------------------------------------------------

    metrics = report.get(
        "metrics",
        {}
    )

    for key, value in metrics.items():

        if isinstance(
            value,
            (str, int, float)
        ):

            add_row(
                "metrics",
                key,
                value
            )

    # ---------------------------------------------------------
    # ARCHITECTURE
    # ---------------------------------------------------------

    architecture = report.get(
        "architecture",
        {}
    )

    add_row(
        "architecture",
        "architecture_score",
        architecture.get("score", 0)
    )

    add_row(
        "architecture",
        "architecture_grade",
        architecture.get(
            "grade",
            "UNKNOWN"
        )
    )

    add_row(
        "architecture",
        "module_count",
        architecture.get(
            "module_count",
            0
        )
    )

    add_row(
        "architecture",
        "circular_dependencies",
        architecture.get(
            "circular_dependencies",
            0
        )
    )

    # ---------------------------------------------------------
    # HOTSPOTS
    # ---------------------------------------------------------

    hotspot_data = report.get(
        "hotspots",
        {}
    )

    add_row(
        "hotspots",
        "hotspot_count",
        hotspot_data.get(
            "hotspot_count",
            0
        )
    )

    hotspot_counts = hotspot_data.get(
        "severity_counts",
        {}
    )

    for level, count in hotspot_counts.items():

        add_row(
            "hotspots",
            f"{level}_hotspots",
            count
        )

    # ---------------------------------------------------------
    # RISKS
    # ---------------------------------------------------------

    risk_data = report.get(
        "risks",
        {}
    )

    add_row(
        "risks",
        "risk_count",
        risk_data.get(
            "risk_count",
            0
        )
    )

    risk_counts = risk_data.get(
        "severity_counts",
        {}
    )

    for level, count in risk_counts.items():

        add_row(
            "risks",
            f"{level}_risks",
            count
        )

    # ---------------------------------------------------------
    # CODE SMELLS
    # ---------------------------------------------------------

    smell_data = report.get(
        "code_smells",
        {}
    )

    add_row(
        "code_smells",
        "total_smells",
        smell_data.get(
            "total_smells",
            0
        )
    )

    smell_counts = smell_data.get(
        "severity_counts",
        {}
    )

    for level, count in smell_counts.items():

        add_row(
            "code_smells",
            f"{level}_smells",
            count
        )

    # ---------------------------------------------------------
    # RECOMMENDATIONS
    # ---------------------------------------------------------

    recommendations = report.get(
        "recommendations",
        []
    )

    add_row(
        "recommendations",
        "recommendation_count",
        len(recommendations)
    )

    # ---------------------------------------------------------
    # CSV GENERATION
    # ---------------------------------------------------------

    buffer = io.StringIO()

    writer = csv.DictWriter(
        buffer,
        fieldnames=fields
    )

    writer.writeheader()

    writer.writerows(rows)

    return buffer.getvalue()