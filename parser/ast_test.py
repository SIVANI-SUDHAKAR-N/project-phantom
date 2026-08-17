import ast

code = """
import os
import math

class User:
    def login(self):
        print("Login")

def calculate():
    return 10

def greet():
    print("Hello")
"""

tree = ast.parse(code)

functions = 0
classes = 0
imports = 0

for node in ast.walk(tree):

    if isinstance(node, ast.FunctionDef):
        functions += 1

    elif isinstance(node, ast.ClassDef):
        classes += 1

    elif isinstance(node, (ast.Import, ast.ImportFrom)):
        imports += 1

print("Functions:", functions)
print("Classes:", classes)
print("Imports:", imports)