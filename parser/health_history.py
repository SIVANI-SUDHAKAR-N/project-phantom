from pathlib import Path
import json
from datetime import datetime


HISTORY_FILE = ".phantom_history.json"


def _history_path(project_path):
    return Path(project_path).resolve() / HISTORY_FILE


def _safe_number(value, default=0):
    return value if isinstance(value, (int, float)) else default


def create_snapshot(project_path="."):
    """
    Run PHANTOM intelligence and create a historical snapshot.
    """

    from .phantom_intelligence import analyze_phantom

    project_path = Path(project_path).resolve()

    intelligence = analyze_phantom(str(project_path))

    phantom = intelligence.get("phantom", {})

    metrics = phantom.get("metrics", {})
    architecture_score = phantom.get("architecture_score", {})
    cycles = phantom.get("cycles", {})
    code_smells = phantom.get("code_smells", {})

    snapshot = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),

        "project": project_path.name,

        "metrics": {
            "total_files": _safe_number(
                metrics.get("total_files")
            ),
            "python_files": _safe_number(
                metrics.get("python_files")
            ),
            "lines_of_code": _safe_number(
                metrics.get("lines_of_code")
            ),
            "functions": _safe_number(
                metrics.get("functions")
            ),
            "classes": _safe_number(
                metrics.get("classes")
            ),
            "average_complexity": _safe_number(
                metrics.get("average_complexity")
            ),
            "maximum_complexity": _safe_number(
                metrics.get("maximum_complexity")
            ),
            "internal_dependency_edges": _safe_number(
                metrics.get("internal_dependency_edges")
            ),
            "external_dependencies": _safe_number(
                metrics.get("external_dependencies")
            ),
        },

        "architecture": {
            "score": _safe_number(
                architecture_score.get("score")
            ),
            "grade": architecture_score.get(
                "grade",
                "UNKNOWN"
            ),
            "circular_dependencies": _safe_number(
                cycles.get("count")
            ),
            "main_contributor": architecture_score.get(
                "main_contributor"
            ),
        },

        "code_smells": {
            "total": _safe_number(
                code_smells.get("total_smells")
            ),
            "severity_counts": code_smells.get(
                "severity_counts",
                {}
            ),
        },
    }

    history = load_history(project_path)

    history.append(snapshot)

    save_history(project_path, history)

    return snapshot


def load_history(project_path="."):
    """
    Load all previously stored PHANTOM snapshots.
    """

    history_file = _history_path(project_path)

    if not history_file.exists():
        return []

    try:
        with open(
            history_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

    except (
        json.JSONDecodeError,
        OSError,
    ):
        pass

    return []


def save_history(project_path, history):
    """
    Save PHANTOM snapshot history.
    """

    history_file = _history_path(project_path)

    with open(
        history_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=2
        )


def calculate_trend(history, metric_path):
    """
    Calculate change between the first and latest
    snapshot for a metric.

    Example:
        calculate_trend(
            history,
            "metrics.lines_of_code"
        )
    """

    if len(history) < 2:
        return {
            "available": False,
            "change": 0,
            "percentage": 0,
        }

    def get_value(snapshot):
        value = snapshot

        for part in metric_path.split("."):
            if not isinstance(value, dict):
                return 0

            value = value.get(part, 0)

        return _safe_number(value)

    first = get_value(history[0])
    latest = get_value(history[-1])

    change = latest - first

    if first == 0:
        percentage = 0
    else:
        percentage = round(
            (change / first) * 100,
            2
        )

    return {
        "available": True,
        "first": first,
        "latest": latest,
        "change": change,
        "percentage": percentage,
    }


def analyze_health_history(project_path="."):
    """
    Return PHANTOM health history and major trends.
    """

    project_path = Path(project_path).resolve()

    history = load_history(project_path)

    trends = {
        "lines_of_code": calculate_trend(
            history,
            "metrics.lines_of_code"
        ),

        "functions": calculate_trend(
            history,
            "metrics.functions"
        ),

        "average_complexity": calculate_trend(
            history,
            "metrics.average_complexity"
        ),

        "maximum_complexity": calculate_trend(
            history,
            "metrics.maximum_complexity"
        ),

        "architecture_score": calculate_trend(
            history,
            "architecture.score"
        ),

        "code_smells": calculate_trend(
            history,
            "code_smells.total"
        ),

        "circular_dependencies": calculate_trend(
            history,
            "architecture.circular_dependencies"
        ),
    }

    return {
        "project": project_path.name,
        "snapshot_count": len(history),
        "snapshots": history,
        "trends": trends,
    }