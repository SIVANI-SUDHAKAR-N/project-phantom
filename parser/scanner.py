from pathlib import Path


def scan_project(project_path):
    path = Path(project_path)

    total_files = 0
    total_folders = 0
    python_files = 0

    for item in path.rglob("*"):
        if item.is_file():
            total_files += 1

            if item.suffix == ".py":
                python_files += 1

        elif item.is_dir():
            total_folders += 1

    return {
        "total_files": total_files,
        "total_folders": total_folders,
        "python_files": python_files
    }