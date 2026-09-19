from pathlib import Path

from .dependency_analyzer import find_imports


IGNORED_DIRS = {
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    "node_modules",
}


def should_ignore(path):
    return any(
        part in IGNORED_DIRS
        for part in Path(path).parts
    )


def module_name_from_file(file_path, project_path):
    """
    Convert:

        parser/foo.py

    into:

        parser.foo
    """

    file_path = Path(file_path).resolve()
    project_path = Path(project_path).resolve()

    relative = file_path.relative_to(project_path)

    parts = list(relative.parts)

    if not parts:
        return ""

    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = Path(parts[-1]).stem

    return ".".join(parts)


def build_module_index(project_path):
    """
    Build:

        module name -> actual Python file
    """

    project_path = Path(project_path).resolve()

    index = {}

    for file_path in project_path.rglob("*.py"):

        if not file_path.is_file():
            continue

        if should_ignore(file_path):
            continue

        module_name = module_name_from_file(
            file_path,
            project_path
        )

        if module_name:
            index[module_name] = file_path

    return index


def resolve_absolute_import(
    imported,
    module_index
):
    """
    Resolve an absolute Python import.

    Example:

        parser.foo
        parser.foo.bar
        fastapi
    """

    imported = imported.strip()

    if not imported:
        return None

    # Exact match first
    if imported in module_index:
        return module_index[imported]

    # Try progressively shorter module names.
    #
    # Example:
    #
    # parser.foo.something
    #
    # may actually refer to:
    #
    # parser.foo

    parts = imported.split(".")

    for end in range(
        len(parts),
        0,
        -1
    ):

        candidate = ".".join(
            parts[:end]
        )

        if candidate in module_index:
            return module_index[candidate]

    return None


def resolve_relative_import(
    imported,
    source_file,
    project_path,
    module_index
):
    """
    Resolve a relative Python import.

    Examples:

        .foo
        ..foo
        .foo.bar

    The number of leading dots determines how many
    package levels are moved upward.
    """

    imported = imported.strip()

    if not imported.startswith("."):
        return None

    # Count leading dots.
    level = 0

    while (
        level < len(imported)
        and imported[level] == "."
    ):
        level += 1

    module_part = imported[level:]

    source_module = module_name_from_file(
        source_file,
        project_path
    )

    if not source_module:
        return None

    source_parts = source_module.split(".")

    # The source file itself is not a package level.
    #
    # parser.foo
    #
    # belongs to package:
    #
    # parser

    package_parts = source_parts[:-1]

    # Move upward according to the relative level.
    #
    # level 1:
    # from .foo
    #
    # stays inside the current package.
    #
    # level 2:
    # from ..foo
    #
    # moves one package upward.

    if level > len(package_parts):
        return None

    base_parts = package_parts[
        :len(package_parts) - (level - 1)
    ]

    if module_part:
        target_parts = (
            base_parts
            + module_part.split(".")
        )
    else:
        target_parts = base_parts

    candidate = ".".join(
        target_parts
    )

    if candidate in module_index:
        return module_index[candidate]

    # A relative import can refer to a package's
    # __init__.py.
    package_init = candidate

    if package_init in module_index:
        return module_index[package_init]

    return None


def resolve_import(
    imported,
    source_file,
    project_path,
    module_index
):
    """
    Resolve an import to an internal project file.

    Returns:

        Path
        or
        None
    """

    imported = imported.strip()

    if not imported:
        return None

    # ---------------------------------------------------------
    # RELATIVE IMPORT
    # ---------------------------------------------------------

    if imported.startswith("."):

        return resolve_relative_import(
            imported,
            source_file,
            project_path,
            module_index
        )

    # ---------------------------------------------------------
    # ABSOLUTE IMPORT
    # ---------------------------------------------------------

    return resolve_absolute_import(
        imported,
        module_index
    )


def build_dependency_graph(project_path="."):
    """
    Build the complete internal/external dependency graph
    for the project.
    """

    project_path = Path(
        project_path
    ).resolve()

    module_index = build_module_index(
        project_path
    )

    graph = {}

    for file_path in project_path.rglob("*.py"):

        if not file_path.is_file():
            continue

        if should_ignore(file_path):
            continue

        file_key = str(
            file_path.relative_to(
                project_path
            ).as_posix()
        )

        internal = []
        external = []

        try:

            imports = find_imports(
                file_path
            )

        except (
            SyntaxError,
            OSError,
            UnicodeDecodeError
        ):

            graph[file_key] = {
                "module": module_name_from_file(
                    file_path,
                    project_path
                ),
                "internal": [],
                "external": [],
            }

            continue

        for imported in imports:

            target = resolve_import(
                imported,
                file_path,
                project_path,
                module_index
            )

            if target is not None:

                target_key = str(
                    target.relative_to(
                        project_path
                    ).as_posix()
                )

                # Do not create self-dependencies.
                if target_key != file_key:

                    internal.append(
                        target_key
                    )

            else:

                external.append(
                    imported
                )

        graph[file_key] = {
            "module": module_name_from_file(
                file_path,
                project_path
            ),

            "internal": sorted(
                set(internal)
            ),

            "external": sorted(
                set(external)
            ),
        }

    return graph