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
```

---

## 🔄 Analysis Pipeline

PHANTOM processes a project through a multi-stage intelligence pipeline:

```text
Project
   ↓
Scanner
   ↓
AST / File Analysis
   ↓
Project Metrics
   ↓
Dependency Intelligence
   ↓
Complexity Analysis
   ↓
Architecture Analysis
   ↓
Code Smell Detection
   ↓
Hotspot Detection
   ↓
Risk Analysis
   ↓
Recommendation Engine
   ↓
Health History
   ↓
Reports + Dashboard
```

---

## 🖥️ Dashboard

The PHANTOM dashboard provides a centralized interface for exploring project intelligence.

It includes:

- Project overview
- Architecture health
- Complexity intelligence
- Risk intelligence
- Hotspot intelligence
- Code smell intelligence
- Architecture map
- Dependency visualization
- Search and filtering
- Recommendations
- Health history
- Report generation
- File-level inspection

---

## 🛠️ Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn

### Static Analysis

- Python `ast`
- File-system analysis
- Dependency graph analysis
- Complexity analysis

### Frontend

- HTML
- CSS
- JavaScript
- Cytoscape.js

### Development

- Git
- GitHub
- VS Code

---

## 📂 Project Structure

```text
PROJECT-PHANTOM/
│
├── backend/
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── parser/
│   ├── analyzer.py
│   ├── architecture_analyzer.py
│   ├── architecture_score.py
│   ├── code_smell_analyzer.py
│   ├── complexity_analyzer.py
│   ├── cycle_detector.py
│   ├── dependency_analyzer.py
│   ├── dependency_graph.py
│   ├── health_history.py
│   ├── hotspot_analyzer.py
│   ├── module_analyzer.py
│   ├── phantom_intelligence.py
│   ├── project_metrics.py
│   ├── recommendation_engine.py
│   ├── report_engine.py
│   ├── risk_analyzer.py
│   └── search_engine.py
│
├── docs/
│
├── phantom_external_test/
│
├── phantom_nested_test/
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/SIVANI-SUDHAKAR-N/project-phantom.git
```

Move into the project:

```bash
cd project-phantom
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## ▶️ Running PHANTOM

Start the FastAPI server:

```powershell
python -m uvicorn backend.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/dashboard/
```

---

## 📁 Analyzing a Project

PHANTOM supports selecting a local project folder from the dashboard.

Enter the absolute path of the project you want to analyze.

Example:

```text
C:\Users\IND1\Desktop\MyProject
```

PHANTOM then analyzes the selected project and updates the dashboard with its available intelligence.

> Current static-analysis capabilities are primarily implemented around Python source-code analysis.

---

## 🧪 Testing

PHANTOM includes test and synthetic project structures used to verify analysis behavior, including dependency-resolution and nested-module scenarios.

Test files are located within the project parser/test structure and dedicated PHANTOM test projects.

---

## 📊 Example Intelligence

A PHANTOM analysis can produce information such as:

```text
Project Metrics
├── Files
├── Lines of Code
├── Functions
├── Classes
└── External Dependencies

Architecture
├── Modules
├── Coupling
├── Architecture Score
└── Circular Dependencies

Code Intelligence
├── Complexity
├── Code Smells
├── Hotspots
├── Risk
└── Recommendations
```

---

## 🛣️ Future Improvements

Potential future development areas include:

- Broader multi-language analysis
- Deeper AST intelligence
- More advanced architecture detection
- Improved dependency resolution
- Additional code-quality rules
- Historical trend visualization
- Advanced project comparison
- Expanded automated testing
- More report formats
- Improved developer experience

---

## 🎯 Project Goal

The goal of PROJECT-PHANTOM is to make unfamiliar codebases easier to understand.

Rather than forcing developers to manually discover relationships between files, PHANTOM attempts to transform raw source code into a structured, explainable representation of the software system.

---

## 👩‍💻 Author

**Sivani Sudhakar N**

B.Tech Computer Science Engineering Student

---

## ⭐ Project

If you find the project interesting, feel free to explore the repository and follow its development.

**PROJECT-PHANTOM 👽**

> Scan. Understand. Map. Measure. Detect. Assess. Recommend. Track. Report.