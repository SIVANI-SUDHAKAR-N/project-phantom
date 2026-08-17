from dependency_graph import build_dependency_graph

result = build_dependency_graph(".")

for file, imports in result.items():
    print("\nFile:", file)
    print("Imports:", imports)