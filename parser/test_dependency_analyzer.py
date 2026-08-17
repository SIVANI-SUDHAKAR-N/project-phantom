from dependency_graph import build_dependency_graph

result = build_dependency_graph(".")

for file, dependencies in result.items():
    print("\nFile:", file)
    print("Internal:", dependencies["internal"])
    print("External:", dependencies["external"])