# PROJECT-PHANTOM 👽

### Static Code Intelligence & Software Architecture Analysis Platform

> PROJECT-PHANTOM transforms a software project from raw source files into an explainable model of its architecture, dependencies, complexity, code smells, hotspots, and risks.

---

## 🧠 What is PROJECT-PHANTOM?

**PROJECT-PHANTOM** is a static code-intelligence platform designed to help developers understand unfamiliar software projects.

Instead of manually exploring hundreds of source files, PHANTOM analyzes a project and builds an intelligence layer around its structure and code.

It follows the pipeline:

**Scan → Understand → Map → Measure → Detect → Assess → Recommend → Track → Report**

---

## ✨ Features

### 📁 Project Analysis
- Project file and folder scanning
- Lines of code analysis
- Function and class detection
- External dependency analysis
- Project-level metrics

### 🏗️ Architecture Intelligence
- Architecture health analysis
- Module detection
- Module relationship analysis
- Fan-in / fan-out analysis
- Coupling analysis
- Architecture scoring
- Architecture grading

### 🔗 Dependency Intelligence
- Internal dependency detection
- External dependency detection
- Dependency graph generation
- Dependency visualization
- Circular dependency detection
- Relative import resolution

### 🧠 Complexity Intelligence
- Function-level complexity analysis
- Average complexity
- Maximum complexity
- Most complex functions
- Complexity-based project insights

### 👃 Code Smell Detection
PHANTOM identifies several structural code-quality indicators, including:

- Large files
- Excessive dependencies
- High branching
- Complex functions
- Duplicate imports
- Parse warnings

### 🔥 Hotspot Intelligence
PHANTOM combines complexity and dependency information to identify files that deserve closer inspection.

Hotspots are classified into:

- High
- Medium
- Low

### ⚠️ Risk Intelligence
PHANTOM combines multiple signals to calculate file-level risk information, including:

- Complexity
- Internal dependencies
- External dependencies
- Hotspot score
- Code smells

### 💡 Recommendation Engine
PHANTOM generates recommendations from detected project conditions such as:

- Complexity
- Architecture health
- Circular dependencies
- Code smells

Recommendations are organized by priority.

### 📈 Health History
PHANTOM can create project health snapshots and track metrics such as:

- Lines of code
- Functions
- Average complexity
- Maximum complexity
- Architecture score
- Code smells
- Circular dependencies

### 🔎 Search & File Intelligence
Search and filtering capabilities allow files to be explored using:

- File path
- Risk level
- Complexity
- Highly-coupled status

PHANTOM also provides file-level inspection containing:

- File metrics
- Dependencies
- Hotspot information
- Risk information
- Code smells

### 📊 Dependency Visualization
The dashboard provides a visual representation of project dependencies and module relationships.

### 📄 Report Generation
PHANTOM can generate project reports in:

- TXT
- JSON
- CSV

---

## 🏗️ Architecture

```text
                         PROJECT-PHANTOM
                                │
                                ▼
                       ┌─────────────────┐
                       │ Project Scanner │
                       └────────┬────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ AST + File Analysis  │
                    └───────────┬───────────┘
                                │
             ┌──────────────────┼──────────────────┐
             ▼                  ▼                  ▼
       Project Metrics      Complexity        Dependencies
             │                  │                  │
             └──────────────────┼──────────────────┘
                                ▼
                    ┌───────────────────────┐
                    │ Intelligence Layer   │
                    └───────────┬───────────┘
                                │
          ┌─────────────┬───────┼────────┬─────────────┐
          ▼             ▼       ▼        ▼             ▼
     Architecture    Smells  Hotspots   Risk     Recommendations
          │             │       │        │             │
          └─────────────┴───────┼────────┴─────────────┘
                                ▼
                       Health History
                                │
                                ▼
                         Report Engine
                                │
                                ▼
                       Web Dashboard
