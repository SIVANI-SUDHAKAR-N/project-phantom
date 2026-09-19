from pathlib import Path
import sys

from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles


# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Allow:
#     uvicorn backend.main:app
# and:
#     uvicorn main:app
# from the backend directory.
#
# This keeps the top-level parser package available.
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# =========================================================
# PHANTOM ANALYZERS
# =========================================================

from parser.project_analyzer import analyze_project
from parser.complexity_analyzer import analyze_complexity
from parser.cycle_detector import analyze_cycles
from parser.architecture_analyzer import analyze_architecture
from parser.module_analyzer import analyze_modules
from parser.phantom_intelligence import analyze_phantom
from parser.search_engine import search_files

from parser.health_history import (
    create_snapshot,
    analyze_health_history,
)

from parser.recommendation_engine import (
    analyze_recommendations,
)

from parser.report_engine import (
    build_report,
    generate_text_report,
    export_json,
    export_csv,
)

from parser.dependency_graph import (
    build_dependency_graph,
)

from parser.project_metrics import (
    analyze_project_metrics,
)

from parser.code_smell_analyzer import (
    analyze_code_smells,
)

from parser.hotspot_analyzer import (
    analyze_hotspots,
)

from parser.risk_analyzer import (
    analyze_risks,
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="PROJECT-PHANTOM"
)


# =========================================================
# SELECTED PROJECT
# =========================================================
#
# PHANTOM itself lives at PROJECT_ROOT.
#
# The selected project can be changed at runtime.
#
# Example:
#
# PHANTOM:
# C:/Users/IND1/Desktop/PROJECT-PHANTOM
#
# Then select:
# C:/Users/IND1/Desktop/MyJavaProject
#
# Every analyzer will use MyJavaProject.
#
# The PHANTOM frontend will STILL be served from
# PROJECT_ROOT/frontend.
# =========================================================

CURRENT_PROJECT = PROJECT_ROOT


def get_current_project():
    """
    Return the project currently selected for analysis.
    """

    return CURRENT_PROJECT


def set_current_project(project_path):
    """
    Change the project currently being analyzed.
    """

    global CURRENT_PROJECT

    if project_path is None:
        raise ValueError(
            "Project path is required."
        )

    path = (
        Path(
            str(project_path)
        )
        .expanduser()
        .resolve()
    )

    if not path.exists():
        raise ValueError(
            "Project folder does not exist."
        )

    if not path.is_dir():
        raise ValueError(
            "Selected path is not a folder."
        )

    CURRENT_PROJECT = path

    return CURRENT_PROJECT


# =========================================================
# FRONTEND ROOT
# =========================================================
#
# IMPORTANT:
#
# Do NOT change this when another project is selected.
#
# PHANTOM's own dashboard must always come from:
#
# PROJECT_ROOT/frontend
#
# =========================================================

FRONTEND_ROOT = PROJECT_ROOT / "frontend"


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def home():

    current_project = get_current_project()

    return {
        "message": "👽 PHANTOM is alive!",
        "project": current_project.name,
        "project_path": str(current_project),
    }


# =========================================================
# CURRENT PROJECT
# =========================================================

@app.get("/current-project")
def current_project():

    project = get_current_project()

    return {
        "status": "success",
        "project": project.name,
        "path": str(project),
    }


# =========================================================
# SELECT PROJECT
# =========================================================

@app.post("/select-project")
async def select_project(
    request: Request
):
    """
    Select a local project folder for PHANTOM analysis.

    Supports both:

    1. JSON:
       {
           "path": "C:/Users/.../Project"
       }

    2. Query parameter:
       /select-project?path=C:/Users/.../Project
    """

    path = request.query_params.get(
        "path"
    )

    # -----------------------------------------------------
    # Try JSON body if query parameter was not supplied.
    # -----------------------------------------------------

    if not path:

        try:

            body = await request.json()

            if isinstance(
                body,
                dict
            ):
                path = body.get(
                    "path"
                )

        except Exception:
            pass

    # -----------------------------------------------------
    # Validate path input.
    # -----------------------------------------------------

    if not path:

        return {
            "status": "error",
            "error": "Project path is required.",
        }

    # -----------------------------------------------------
    # Select project.
    # -----------------------------------------------------

    try:

        selected = set_current_project(
            path
        )

        return {
            "status": "success",
            "project": selected.name,
            "path": str(selected),
            "message": (
                "👽 Project selected successfully."
            ),
        }

    except Exception as error:

        return {
            "status": "error",
            "error": str(error),
        }


# =========================================================
# BASIC PROJECT ANALYSIS
# =========================================================

@app.get("/analyze")
def analyze():

    project = get_current_project()

    return analyze_project(
        str(project)
    )


# =========================================================
# COMPLEXITY
# =========================================================

@app.get("/complexity")
def complexity():

    project = get_current_project()

    results = analyze_complexity(
        str(project)
    )

    return {
        "complexity": results,
        "project": project.name,
    }


# =========================================================
# CIRCULAR DEPENDENCIES
# =========================================================

@app.get("/cycles")
def cycles():

    project = get_current_project()

    results = analyze_cycles(
        str(project)
    )

    return {
        "cycles": results,
        "project": project.name,
    }


# =========================================================
# ARCHITECTURE
# =========================================================

@app.get("/architecture")
def architecture():

    project = get_current_project()

    architecture_data = analyze_architecture(
        str(project)
    )

    module_data = analyze_modules(
        str(project)
    )

    return {
        "architecture": architecture_data,
        "modules": module_data,
        "project": project.name,
    }


# =========================================================
# PHANTOM INTELLIGENCE
# =========================================================

@app.get("/intelligence")
def intelligence():

    project = get_current_project()

    result = analyze_phantom(
        str(project)
    )

    wrapped_data = result.get(
        "phantom",
        {}
    )

    intelligence_data = {}

    # -----------------------------------------------------
    # Unwrap analyzer results.
    # -----------------------------------------------------

    for key, value in wrapped_data.items():

        if (
            isinstance(value, dict)
            and value.get("status") == "success"
        ):

            intelligence_data[key] = (
                value.get("data")
            )

        elif (
            isinstance(value, dict)
            and value.get("status") == "error"
        ):

            intelligence_data[key] = {
                "error": value.get(
                    "error",
                    "Analyzer failed"
                )
            }

        else:

            intelligence_data[key] = value

    # -----------------------------------------------------
    # Always report the CURRENT selected project.
    # -----------------------------------------------------

    intelligence_data["project"] = (
        project.name
    )

    intelligence_data["project_path"] = (
        str(project)
    )

    intelligence_data["pipeline"] = (
        result.get(
            "pipeline",
            {}
        )
    )

    return intelligence_data


# =========================================================
# SEARCH
# =========================================================

@app.get("/search")
def search(
    query: str = "",
    risk: str = "all",
    complexity: str = "all",
    highly_coupled: bool = False,
):

    project = get_current_project()

    return search_files(
        project_path=str(
            project
        ),
        query=query,
        risk=risk,
        complexity_filter=complexity,
        highly_coupled=highly_coupled,
    )


# =========================================================
# HEALTH SNAPSHOT
# =========================================================

@app.get("/snapshot")
def snapshot():

    project = get_current_project()

    return create_snapshot(
        str(project)
    )


# =========================================================
# HEALTH HISTORY
# =========================================================

@app.get("/health-history")
def health_history():

    project = get_current_project()

    return analyze_health_history(
        str(project)
    )


# =========================================================
# RECOMMENDATIONS
# =========================================================

@app.get("/recommendations")
def recommendations():

    project = get_current_project()

    return analyze_recommendations(
        str(project)
    )


# =========================================================
# FULL REPORT
# =========================================================

@app.get("/report")
def report():

    project = get_current_project()

    return build_report(
        str(project)
    )


# =========================================================
# TEXT REPORT
# =========================================================

@app.get("/report/txt")
def report_txt():

    project = get_current_project()

    report = generate_text_report(
        str(project)
    )

    filename = (
        f"PROJECT-PHANTOM-"
        f"{project.name}-Report.txt"
    )

    return Response(
        content=report,
        media_type="text/plain",
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}"'
        },
    )


# =========================================================
# JSON REPORT
# =========================================================

@app.get("/report/json")
def report_json():

    project = get_current_project()

    report = export_json(
        str(project)
    )

    filename = (
        f"PROJECT-PHANTOM-"
        f"{project.name}-Report.json"
    )

    return Response(
        content=report,
        media_type="application/json",
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}"'
        },
    )


# =========================================================
# CSV REPORT
# =========================================================

@app.get("/report/csv")
def report_csv():

    project = get_current_project()

    report = export_csv(
        str(project)
    )

    filename = (
        f"PROJECT-PHANTOM-"
        f"{project.name}-Metrics.csv"
    )

    return Response(
        content=report,
        media_type="text/csv",
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}"'
        },
    )


# =========================================================
# FILE INTELLIGENCE INSPECTOR
# =========================================================

@app.get("/file-inspector")
def file_inspector(
    file: str
):

    project_path = get_current_project()

    requested_file = Path(
        file
    )

    # -----------------------------------------------------
    # SECURITY:
    # Prevent paths from escaping the selected project.
    # -----------------------------------------------------

    try:

        file_path = (
            project_path
            / requested_file
        ).resolve()

        file_path.relative_to(
            project_path.resolve()
        )

    except ValueError:

        return {
            "error": "Invalid file path"
        }

    # -----------------------------------------------------
    # FILE EXISTENCE
    # -----------------------------------------------------

    if not file_path.is_file():

        return {
            "error": "File not found",
            "file": file,
        }

    # -----------------------------------------------------
    # RELATIVE FILE PATH
    # -----------------------------------------------------

    relative_file = (
        file_path
        .relative_to(
            project_path.resolve()
        )
        .as_posix()
    )

    # -----------------------------------------------------
    # DEPENDENCY INFORMATION
    # -----------------------------------------------------

    graph = build_dependency_graph(
        project_path
    )

    dependency_data = graph.get(
        relative_file,
        {
            "module": None,
            "internal": [],
            "external": [],
        },
    )

    # -----------------------------------------------------
    # PROJECT METRICS
    # -----------------------------------------------------

    metrics = analyze_project_metrics(
        str(project_path)
    )

    file_metrics = metrics.get(
        "file_metrics",
        {}
    )

    current_metrics = file_metrics.get(
        relative_file,
        {}
    )

    # -----------------------------------------------------
    # CODE SMELLS
    # -----------------------------------------------------

    smell_data = analyze_code_smells(
        str(project_path)
    )

    smell_info = (
        smell_data
        .get(
            "files",
            {}
        )
        .get(
            relative_file,
            {
                "smell_count": 0,
                "smells": [],
            },
        )
    )

    # -----------------------------------------------------
    # HOTSPOT INFORMATION
    # -----------------------------------------------------

    hotspot_data = analyze_hotspots(
        str(project_path)
    )

    hotspot_info = next(
        (
            item
            for item in hotspot_data.get(
                "hotspots",
                []
            )
            if item.get(
                "file"
            ) == relative_file
        ),
        None,
    )

    # -----------------------------------------------------
    # RISK INFORMATION
    # -----------------------------------------------------

    risk_data = analyze_risks(
        str(project_path)
    )

    risk_info = next(
        (
            item
            for item in risk_data.get(
                "risks",
                []
            )
            if item.get(
                "file"
            ) == relative_file
        ),
        None,
    )

    # -----------------------------------------------------
    # FINAL INSPECTOR RESPONSE
    # -----------------------------------------------------

    return {

        "project": project_path.name,

        "project_path":
            str(project_path),

        "file":
            relative_file,

        "module":
            dependency_data.get(
                "module"
            ),

        "metrics": {

            "lines":
                current_metrics.get(
                    "lines",
                    0
                ),

            "functions":
                current_metrics.get(
                    "functions",
                    0
                ),

            "classes":
                current_metrics.get(
                    "classes",
                    0
                ),

            "complexity":
                current_metrics.get(
                    "complexity",
                    0
                ),
        },

        "dependencies": {

            "internal":
                dependency_data.get(
                    "internal",
                    []
                ),

            "external":
                dependency_data.get(
                    "external",
                    []
                ),

            "internal_count":
                len(
                    dependency_data.get(
                        "internal",
                        []
                    )
                ),

            "external_count":
                len(
                    dependency_data.get(
                        "external",
                        []
                    )
                ),
        },

        "hotspot":
            hotspot_info
            or {
                "score": 0,
                "level": "low",
            },

        "risk":
            risk_info
            or {
                "score": 0,
                "level": "low",
                "reasons": [],
            },

        "code_smells":
            smell_info,
    }


# =========================================================
# FRONTEND / DASHBOARD
# =========================================================
#
# IMPORTANT:
# The dashboard ALWAYS belongs to PHANTOM.
#
# Selecting another project changes the ANALYSIS target,
# NOT the location of the dashboard.
# =========================================================

app.mount(
    "/dashboard",
    StaticFiles(
        directory=FRONTEND_ROOT,
        html=True
    ),
    name="frontend",
)