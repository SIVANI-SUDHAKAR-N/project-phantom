from pathlib import Path
from collections import defaultdict


def detect_modules(project_path="."):
    """
    Detect architectural modules based on top-level directories.

    Returns:
        {
            "module_name": {
                "files": [...],
                "file_count": int
            }
        }
    """

    project_path = Path(project_path).resolve()

    modules = defaultdict(list)

    for file in project_path.rglob("*.py"):

        if not file.is_file():
            continue

        relative = file.relative_to(project_path)

        # Ignore common virtual/environment directories
        if any(
            part in {
                ".venv",
                "venv",
                "__pycache__",
                ".git",
                "node_modules"
            }
            for part in relative.parts
        ):
            continue

        # First directory becomes the architectural module
        if len(relative.parts) > 1:
            module = relative.parts[0]
        else:
            module = "root"

        modules[module].append(str(relative))

    return {
        module: {
            "files": sorted(files),
            "file_count": len(files)
        }
        for module, files in sorted(modules.items())
    }


def build_architecture_map(project_path="."):
    """
    Build a high-level architecture map from project modules.
    """

    project_path = Path(project_path).resolve()

    modules = detect_modules(project_path)

    architecture = {
        "project": project_path.name,
        "modules": modules,
        "module_count": len(modules)
    }

    return architecture


def analyze_architecture(project_path="."):
    """
    Main Architecture Intelligence entry point.
    """

    architecture = build_architecture_map(project_path)

    return architecture