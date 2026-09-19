from pathlib import Path

from .project_analyzer import analyze_project
from .complexity_analyzer import analyze_complexity
from .dependency_graph import build_dependency_graph
from .cycle_detector import analyze_cycles
from .architecture_analyzer import analyze_architecture
from .module_analyzer import analyze_modules
from .architecture_score import analyze_architecture_score
from .code_smell_analyzer import analyze_code_smells
from .project_metrics import analyze_project_metrics
from .hotspot_analyzer import analyze_hotspots
from .risk_analyzer import analyze_risks


def run_analyzer(name, analyzer, project_path):
    """
    Run one PHANTOM analyzer safely.

    If an analyzer fails, the failure is recorded
    instead of stopping the entire intelligence pipeline.
    """

    try:
        data = analyzer(project_path)

        return {
            "status": "success",
            "data": data,
        }

    except Exception as error:

        return {
            "status": "error",
            "analyzer": name,
            "error": str(error),
        }


def analyze_phantom(project_path="."):
    """
    Run the complete PROJECT-PHANTOM intelligence pipeline.

    Pipeline:

    Project
        ↓
    Scanner / AST
        ↓
    Dependencies
        ↓
    Complexity
        ↓
    Architecture
        ↓
    Circular Dependencies
        ↓
    Module Intelligence
        ↓
    Architecture Score
        ↓
    Code Smells
        ↓
    Project Metrics
        ↓
    Hotspots
        ↓
    Risk Intelligence
    """

    project_path = Path(
        project_path
    ).resolve()

    results = {}

    # --------------------------------------------------
    # Project analysis
    # --------------------------------------------------

    results["project"] = run_analyzer(
        "project",
        lambda path: analyze_project(
            str(path)
        ),
        project_path,
    )

    # --------------------------------------------------
    # Complexity
    # --------------------------------------------------

    results["complexity"] = run_analyzer(
        "complexity",
        lambda path: analyze_complexity(
            str(path)
        ),
        project_path,
    )

    # --------------------------------------------------
    # Dependency graph
    # --------------------------------------------------

    results["dependencies"] = run_analyzer(
        "dependencies",
        build_dependency_graph,
        project_path,
    )

    # --------------------------------------------------
    # Circular dependencies
    # --------------------------------------------------

    results["cycles"] = run_analyzer(
        "cycles",
        analyze_cycles,
        project_path,
    )

    # --------------------------------------------------
    # Architecture
    # --------------------------------------------------

    results["architecture"] = run_analyzer(
        "architecture",
        analyze_architecture,
        project_path,
    )

    # --------------------------------------------------
    # Module intelligence
    # --------------------------------------------------

    results["modules"] = run_analyzer(
        "modules",
        analyze_modules,
        project_path,
    )

    # --------------------------------------------------
    # Architecture score
    # --------------------------------------------------

    results["architecture_score"] = run_analyzer(
        "architecture_score",
        analyze_architecture_score,
        project_path,
    )

    # --------------------------------------------------
    # Code smells
    # --------------------------------------------------

    results["code_smells"] = run_analyzer(
        "code_smells",
        analyze_code_smells,
        project_path,
    )

    # --------------------------------------------------
    # Project metrics
    # --------------------------------------------------

    results["metrics"] = run_analyzer(
        "metrics",
        analyze_project_metrics,
        project_path,
    )

    # --------------------------------------------------
    # Hotspots
    # --------------------------------------------------

    results["hotspots"] = run_analyzer(
        "hotspots",
        analyze_hotspots,
        project_path,
    )

    # --------------------------------------------------
    # Risk intelligence
    # --------------------------------------------------

    results["risks"] = run_analyzer(
        "risks",
        analyze_risks,
        project_path,
    )

    # --------------------------------------------------
    # Pipeline status
    # --------------------------------------------------

    successful = 0
    failed = 0

    for result in results.values():

        if result.get("status") == "success":
            successful += 1

        elif result.get("status") == "error":
            failed += 1

    if failed == 0:
        pipeline_status = "healthy"

    elif successful > 0:
        pipeline_status = "partial"

    else:
        pipeline_status = "failed"

    # --------------------------------------------------
    # Final PHANTOM intelligence
    # --------------------------------------------------

    return {
        "project": project_path.name,

        "pipeline": {
            "status": pipeline_status,
            "total_analyzers": len(results),
            "successful": successful,
            "failed": failed,
        },

        "phantom": results,
    }