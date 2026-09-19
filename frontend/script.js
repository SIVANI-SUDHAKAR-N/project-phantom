// ============================================================
// PROJECT-PHANTOM 👽
// Dashboard Intelligence Controller
// ============================================================

let phantomData = null;
let dependencyCy = null;


// ============================================================
// API
// ============================================================

async function fetchAPI(endpoint, options = {}) {

    try {

        const response =
            await fetch(
                endpoint,
                options
            );

        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}`
            );
        }

        return await response.json();

    } catch (error) {

        console.error(
            `API Error [${endpoint}]:`,
            error
        );

        throw error;
    }
}


// ============================================================
// 👽 PROJECT SELECTOR
// ============================================================

async function loadCurrentProject() {

    const projectName =
        document.getElementById(
            "currentProjectName"
        );

    const projectPath =
        document.getElementById(
            "projectPath"
        );

    const selectorStatus =
        document.getElementById(
            "projectSelectorStatus"
        );

    const message =
        document.getElementById(
            "projectSelectorMessage"
        );


    try {

        const data =
            await fetchAPI(
                "/current-project"
            );


        if (
            data &&
            data.status === "success"
        ) {

            if (projectName) {

                projectName.textContent =
                    data.project ||
                    "PROJECT-PHANTOM";
            }


            if (
                projectPath &&
                data.path
            ) {

                projectPath.value =
                    data.path;
            }


            if (selectorStatus) {

                selectorStatus.textContent =
                    "READY";
            }


            if (message) {

                message.textContent =
                    `Current project: ${
                        data.project ||
                        "PROJECT-PHANTOM"
                    }`;
            }

        }

    } catch (error) {

        console.warn(
            "⚠️ Could not load current project:",
            error
        );


        if (selectorStatus) {

            selectorStatus.textContent =
                "UNAVAILABLE";
        }
    }
}


// ============================================================
// SELECT PROJECT
// ============================================================

async function selectProject() {

    const pathInput =
        document.getElementById(
            "projectPath"
        );

    const button =
        document.getElementById(
            "selectProjectButton"
        );

    const selectorStatus =
        document.getElementById(
            "projectSelectorStatus"
        );

    const message =
        document.getElementById(
            "projectSelectorMessage"
        );

    const path =
        pathInput
            ? pathInput.value.trim()
            : "";


    // --------------------------------------------------------
    // VALIDATE PATH
    // --------------------------------------------------------

    if (!path) {

        if (message) {

            message.textContent =
                "⚠️ Please enter a project folder path.";
        }

        if (selectorStatus) {

            selectorStatus.textContent =
                "PATH REQUIRED";
        }

        if (pathInput) {
            pathInput.focus();
        }

        return;
    }


    try {

        // ----------------------------------------------------
        // UI — SELECTING
        // ----------------------------------------------------

        if (button) {

            button.disabled = true;

            button.textContent =
                "SELECTING...";
        }


        if (selectorStatus) {

            selectorStatus.textContent =
                "SELECTING";
        }


        if (message) {

            message.textContent =
                "👽 PHANTOM is switching projects...";
        }


        // ----------------------------------------------------
        // SEND PROJECT PATH TO BACKEND
        // ----------------------------------------------------

        const result =
            await fetchAPI(
                "/select-project",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        path: path
                    })
                }
            );


        // ----------------------------------------------------
        // HANDLE BACKEND ERROR
        // ----------------------------------------------------

        if (
            !result ||
            result.status !== "success"
        ) {

            throw new Error(
                result?.error ||
                "Project selection failed."
            );
        }


        // ----------------------------------------------------
        // UPDATE PROJECT DISPLAY
        // ----------------------------------------------------

        const projectName =
            document.getElementById(
                "currentProjectName"
            );


        if (projectName) {

            projectName.textContent =
                result.project ||
                "Unknown Project";
        }


        if (selectorStatus) {

            selectorStatus.textContent =
                "SELECTED";
        }


        if (message) {

            message.textContent =
                `👽 Project selected: ${
                    result.project ||
                    "Unknown Project"
                }`;
        }


        console.log(
            "👽 Project selected:",
            result
        );


        // ----------------------------------------------------
        // RUN COMPLETE PHANTOM SCAN
        // ----------------------------------------------------

        await runPhantomScan();


        if (selectorStatus) {

            selectorStatus.textContent =
                "ANALYZED";
        }


        if (message) {

            message.textContent =
                `✅ ${
                    result.project ||
                    "Project"
                } analyzed successfully.`;
        }

    } catch (error) {

        console.error(
            "❌ Project selection failed:",
            error
        );


        if (selectorStatus) {

            selectorStatus.textContent =
                "ERROR";
        }


        if (message) {

            message.textContent =
                "❌ " +
                error.message;
        }

    } finally {

        if (button) {

            button.disabled = false;

            button.textContent =
                "👽 SELECT PROJECT";
        }
    }
}


// ============================================================
// MAIN PHANTOM SCAN
// ============================================================

async function runPhantomScan() {

    const scanButton =
        document.getElementById(
            "scanButton"
        );

    try {

        if (scanButton) {

            scanButton.disabled =
                true;

            scanButton.textContent =
                "SCANNING...";
        }


        updateScanStatus(
            "PHANTOM is analyzing the project..."
        );


        // ----------------------------------------------------
        // STEP 1 — GET INTELLIGENCE
        // ----------------------------------------------------

        console.log(
            "👽 Requesting /intelligence..."
        );


        let intelligence;


        try {

            intelligence =
                await fetchAPI(
                    "/intelligence"
                );


            console.log(
                "👽 Intelligence received:",
                intelligence
            );

        } catch (error) {

            console.error(
                "❌ /intelligence FAILED:",
                error
            );


            updateScanStatus(
                "❌ Backend intelligence request failed: " +
                error.message
            );

            return;
        }


        // ----------------------------------------------------
        // STEP 2 — STORE DATA
        // ----------------------------------------------------

        phantomData =
            intelligence;


        // ----------------------------------------------------
        // UPDATE CURRENT PROJECT DISPLAY
        // ----------------------------------------------------

        if (
            intelligence.project
        ) {

            const projectName =
                document.getElementById(
                    "currentProjectName"
                );


            if (projectName) {

                projectName.textContent =
                    intelligence.project;
            }
        }


        // ----------------------------------------------------
        // STEP 3 — UPDATE DASHBOARD
        // ----------------------------------------------------

        try {

            console.log(
                "👽 Updating dashboard..."
            );


            updateDashboard(
                intelligence
            );


            console.log(
                "✅ Dashboard updated successfully."
            );

        } catch (error) {

            console.error(
                "❌ Dashboard update FAILED:",
                error
            );


            updateScanStatus(
                "❌ Dashboard error: " +
                error.message
            );

            return;
        }


        // ----------------------------------------------------
        // STEP 4 — RECOMMENDATIONS
        // ----------------------------------------------------

        try {

            console.log(
                "👽 Loading recommendations..."
            );


            const recommendations =
                await fetchAPI(
                    "/recommendations"
                );


            renderRecommendations(
                recommendations
            );


            console.log(
                "✅ Recommendations loaded."
            );

        } catch (error) {

            console.warn(
                "⚠️ Recommendation engine unavailable:",
                error
            );
        }


        // ----------------------------------------------------
        // STEP 5 — DEPENDENCY GRAPH
        // ----------------------------------------------------

        try {

            console.log(
                "👽 Loading dependency graph..."
            );


            await loadDependencyGraph(
                intelligence.dependencies
            );


            console.log(
                "✅ Dependency graph loaded."
            );

        } catch (error) {

            console.warn(
                "⚠️ Dependency graph unavailable:",
                error
            );
        }


        // ----------------------------------------------------
        // COMPLETE
        // ----------------------------------------------------

        updateScanStatus(
            "✅ PHANTOM analysis complete."
        );


        console.log(
            "👽 PHANTOM SCAN COMPLETE."
        );

    } catch (error) {

        console.error(
            "❌ PHANTOM scan failed:",
            error
        );


        updateScanStatus(
            "❌ PHANTOM scan failed: " +
            error.message
        );

    } finally {

        if (scanButton) {

            scanButton.disabled =
                false;

            scanButton.textContent =
                "SCAN PROJECT";
        }
    }
}


// ============================================================
// DASHBOARD UPDATE
// ============================================================

function updateDashboard(data) {

    if (!data) {
        return;
    }


    console.log(
        "👽 PHANTOM Intelligence:",
        data
    );


    const metrics =
        data.metrics || {};

    const architecture =
        data.architecture_score || {};

    const cycles =
        data.cycles || {};

    const complexity =
        data.complexity || [];

    const codeSmells =
        data.code_smells || {};

    const risks =
        data.risks || {};

    const hotspots =
        data.hotspots || {};

    const moduleData =
        data.modules || {};


    // ========================================================
    // OVERVIEW METRICS
    // ========================================================

    setText(
        "totalFiles",
        metrics.total_files ?? 0
    );

    setText(
        "linesOfCode",
        metrics.lines_of_code ?? 0
    );

    setText(
        "functions",
        metrics.functions ?? 0
    );

    setText(
        "classes",
        metrics.classes ?? 0
    );

    setText(
        "externalDependencies",
        metrics.external_dependencies ?? 0
    );

    setText(
        "codeSmells",
        codeSmells.total_smells ?? 0
    );


    // ========================================================
    // ARCHITECTURE HEALTH
    // ========================================================

    setText(
        "architectureScore",
        architecture.score !== undefined
            ? architecture.score
            : "--"
    );

    setText(
        "architectureGrade",
        architecture.grade ||
        "UNKNOWN"
    );

    setText(
        "cycleCount",
        cycles.count !== undefined
            ? cycles.count
            : 0
    );

    setText(
        "moduleCount",
        moduleData.module_count !== undefined
            ? moduleData.module_count
            : 0
    );

    setText(
        "mainContributor",
        architecture.main_contributor
            ? formatLabel(
                architecture.main_contributor
            )
            : "None"
    );


    // ========================================================
    // COMPLEXITY
    // ========================================================

    updateComplexitySection(
        complexity,
        metrics
    );


    // ========================================================
    // RISK
    // ========================================================

    renderRiskIntelligence(
        risks
    );


    // ========================================================
    // HOTSPOTS
    // ========================================================

    renderHotspotIntelligence(
        hotspots
    );


    // ========================================================
    // CODE SMELLS
    // ========================================================

    renderCodeSmellIntelligence(
        codeSmells
    );


    // ========================================================
    // ARCHITECTURE MAP
    // ========================================================

    renderArchitectureMap(
        moduleData
    );


    // ========================================================
    // SEARCH
    // ========================================================

    initializeSearch();


    // ========================================================
    // HEALTH HISTORY
    // ========================================================

    loadHealthHistory();
}


// ============================================================
// COMPLEXITY
// ============================================================

function updateComplexitySection(
    complexity,
    metrics
) {

    metrics =
        metrics || {};

    complexity =
        Array.isArray(complexity)
            ? complexity
            : [];


    let average =
        Number(
            metrics.average_complexity
        );


    if (!Number.isFinite(average)) {
        average = 0;
    }


    const functions = [];


    complexity.forEach(
        fileData => {

            if (
                !fileData ||
                typeof fileData !==
                "object"
            ) {
                return;
            }


            const file =
                fileData.file ||
                "Unknown file";


            const fileFunctions =
                Array.isArray(
                    fileData.functions
                )
                    ? fileData.functions
                    : [];


            fileFunctions.forEach(
                func => {

                    if (
                        !func ||
                        typeof func !==
                        "object"
                    ) {
                        return;
                    }


                    const value =
                        Number(
                            func.complexity
                        );


                    if (
                        Number.isFinite(
                            value
                        )
                    ) {

                        functions.push({

                            name:
                                func.name ||
                                "Unknown function",

                            complexity:
                                value,

                            file:
                                file
                        });
                    }
                }
            );
        }
    );


    let maximum =
        Number(
            metrics.maximum_complexity
        );


    if (
        !Number.isFinite(maximum) ||
        maximum <= 0
    ) {

        maximum =
            functions.length
                ? Math.max(
                    ...functions.map(
                        item =>
                            item.complexity
                    )
                )
                : 0;
    }


    let mostComplex =
        metrics.most_complex_function;


    if (
        mostComplex &&
        typeof mostComplex ===
        "object"
    ) {

        const functionName =
            mostComplex.name ||
            mostComplex.function ||
            mostComplex.function_name ||
            "Unknown function";


        const functionComplexity =
            Number(
                mostComplex.complexity
            );


        if (
            Number.isFinite(
                functionComplexity
            )
        ) {

            mostComplex =
                `${functionName} (${functionComplexity})`;

        } else {

            mostComplex =
                String(
                    functionName
                );
        }
    }


    if (
        !mostComplex ||
        mostComplex === "None detected"
    ) {

        if (functions.length) {

            const highest =
                functions.reduce(
                    (
                        best,
                        current
                    ) =>
                        current.complexity >
                        best.complexity
                            ? current
                            : best
                );


            mostComplex =
                `${highest.name} (${highest.complexity})`;

        } else {

            mostComplex =
                "None detected";
        }
    }


    if (
        average === 0 &&
        functions.length
    ) {

        average =
            functions.reduce(
                (
                    sum,
                    item
                ) =>
                    sum +
                    item.complexity,
                0
            ) /
            functions.length;
    }


    setText(
        "averageComplexity",
        Number(
            average
        ).toFixed(2)
    );


    setText(
        "maxComplexity",
        maximum
    );


    setText(
        "mostComplexFunction",
        mostComplex
    );
}


// ============================================================
// 👃 CODE SMELL INTELLIGENCE
// ============================================================

function renderCodeSmellIntelligence(
    smellData
) {

    const container =
        document.getElementById(
            "codeSmellIntelligence"
        );


    const status =
        document.getElementById(
            "smellStatus"
        );


    if (!container) {
        return;
    }


    if (
        !smellData ||
        smellData.error
    ) {

        if (status) {

            status.textContent =
                "Code smell analysis unavailable.";
        }


        container.innerHTML =
            "";

        return;
    }


    const total =
        smellData.total_smells ??
        0;


    const severity =
        smellData.severity_counts ||
        {};


    const files =
        smellData.files ||
        {};


    if (status) {

        status.textContent =
            `${total} code smell(s) detected`;
    }


    const fileEntries =
        Object.entries(files)
            .filter(
                ([, data]) =>
                    data &&
                    Number(
                        data.smell_count ||
                        0
                    ) > 0
            )
            .sort(
                ([, a], [, b]) =>
                    (
                        b.smell_count ||
                        0
                    ) -
                    (
                        a.smell_count ||
                        0
                    )
            );


    container.innerHTML = `

        <div class="smell-summary">

            <div>
                <span>Total</span>
                <strong>
                    ${total}
                </strong>
            </div>

            <div>
                <span>High</span>
                <strong>
                    ${severity.high || 0}
                </strong>
            </div>

            <div>
                <span>Medium</span>
                <strong>
                    ${severity.medium || 0}
                </strong>
            </div>

            <div>
                <span>Low</span>
                <strong>
                    ${severity.low || 0}
                </strong>
            </div>

        </div>


        <div class="smell-files">

            ${
                fileEntries.length
                    ? fileEntries
                        .slice(0, 10)
                        .map(
                            ([file, data]) =>
                                createSmellCard(
                                    file,
                                    data
                                )
                        )
                        .join("")
                    : `
                        <div class="empty-state">
                            No code smells detected.
                        </div>
                    `
            }

        </div>
    `;
}


// ============================================================
// SMELL CARD
// ============================================================

function createSmellCard(
    file,
    data
) {

    const smells =
        Array.isArray(
            data.smells
        )
            ? data.smells
            : [];


    return `

        <div class="smell-card">

            <div class="smell-card-header">

                <strong>
                    ${escapeHTML(file)}
                </strong>

                <span>
                    ${data.smell_count || 0}
                </span>

            </div>


            <div class="smell-list">

                ${
                    smells
                        .map(
                            smell => {

                                const type =
                                    formatSmellType(
                                        smell.type
                                    );


                                const severity =
                                    smell.severity ||
                                    "warning";


                                return `

                                    <div class="smell-item">

                                        <span class="smell-type">
                                            ${escapeHTML(type)}
                                        </span>

                                        <span class="smell-severity">
                                            ${escapeHTML(
                                                severity.toUpperCase()
                                            )}
                                        </span>

                                        <p>
                                            ${escapeHTML(
                                                smell.message ||
                                                smell.reason ||
                                                "Code smell detected."
                                            )}
                                        </p>

                                    </div>
                                `;
                            }
                        )
                        .join("")
                }

            </div>

        </div>
    `;
}


// ============================================================
// SMELL TYPE FORMATTER
// ============================================================

function formatSmellType(
    type
) {

    if (!type) {
        return "Code smell";
    }


    return String(type)
        .replace(
            /_/g,
            " "
        )
        .replace(
            /\b\w/g,
            letter =>
                letter.toUpperCase()
        );
}


// ============================================================
// 🏗️ ARCHITECTURE MAP
// ============================================================

function renderArchitectureMap(
    moduleData
) {

    const container =
        document.getElementById(
            "architectureMap"
        );


    const status =
        document.getElementById(
            "architectureMapStatus"
        );


    if (!container) {
        return;
    }


    if (
        !moduleData ||
        !moduleData.modules
    ) {

        if (status) {

            status.textContent =
                "Architecture data unavailable.";
        }


        container.innerHTML =
            "";

        return;
    }


    const modules =
        moduleData.modules;


    const moduleNames =
        Object.keys(modules);


    if (
        moduleNames.length === 0
    ) {

        if (status) {

            status.textContent =
                "No modules detected.";
        }


        container.innerHTML =
            "";

        return;
    }


    if (status) {

        status.textContent =
            `${moduleNames.length} modules detected • ` +
            `Most connected: ${
                moduleData.most_connected_module ||
                "None"
            }`;
    }


    container.innerHTML =
        "";


    const mapWrapper =
        document.createElement(
            "div"
        );


    mapWrapper.className =
        "architecture-map-grid";


    moduleNames.forEach(
        moduleName => {

            const data =
                modules[moduleName] ||
                {};


            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "architecture-module";


            const dependsOn =
                Array.isArray(
                    data.depends_on
                )
                    ? data.depends_on
                    : [];


            const dependedBy =
                Array.isArray(
                    data.depended_by
                )
                    ? data.depended_by
                    : [];


            card.innerHTML = `

                <div class="architecture-module-header">

                    <span class="architecture-module-icon">
                        🧩
                    </span>

                    <strong>
                        ${escapeHTML(
                            moduleName
                        )}
                    </strong>

                </div>


                <div class="architecture-stats">

                    <div>
                        <span>Fan In</span>
                        <strong>
                            ${data.fan_in || 0}
                        </strong>
                    </div>

                    <div>
                        <span>Fan Out</span>
                        <strong>
                            ${data.fan_out || 0}
                        </strong>
                    </div>

                    <div>
                        <span>Coupling</span>
                        <strong>
                            ${data.coupling_score || 0}
                        </strong>
                    </div>

                    <div>
                        <span>Edges</span>
                        <strong>
                            ${data.edge_count || 0}
                        </strong>
                    </div>

                </div>


                <div class="architecture-connections">

                    <div class="connection-group">

                        <span class="connection-title">
                            Depends On
                        </span>

                        ${
                            dependsOn.length
                                ? dependsOn
                                    .map(
                                        item =>
                                            `
                                                <span class="module-tag">
                                                    ${escapeHTML(
                                                        item
                                                    )}
                                                </span>
                                            `
                                    )
                                    .join("")
                                : `
                                    <span class="empty-connection">
                                        None
                                    </span>
                                `
                        }

                    </div>


                    <div class="connection-group">

                        <span class="connection-title">
                            Depended By
                        </span>

                        ${
                            dependedBy.length
                                ? dependedBy
                                    .map(
                                        item =>
                                            `
                                                <span class="module-tag">
                                                    ${escapeHTML(
                                                        item
                                                    )}
                                                </span>
                                            `
                                    )
                                    .join("")
                                : `
                                    <span class="empty-connection">
                                        None
                                    </span>
                                `
                        }

                    </div>

                </div>
            `;


            if (
                moduleName ===
                moduleData.most_connected_module
            ) {

                card.classList.add(
                    "most-connected"
                );
            }


            mapWrapper.appendChild(
                card
            );
        }
    );


    container.appendChild(
        mapWrapper
    );
}


// ============================================================
// 🔗 DEPENDENCY GRAPH
// ============================================================

async function loadDependencyGraph(
    dependencies
) {

    const graphContainer =
        document.getElementById(
            "dependencyGraph"
        );


    const status =
        document.getElementById(
            "graphStatus"
        );


    if (!graphContainer) {
        return;
    }


    if (
        typeof cytoscape ===
        "undefined"
    ) {

        if (status) {

            status.textContent =
                "Cytoscape library unavailable.";
        }

        return;
    }


    if (!dependencies) {

        if (status) {

            status.textContent =
                "No dependency data.";
        }

        return;
    }


    const elements =
        buildDependencyElements(
            dependencies
        );


    if (dependencyCy) {

        dependencyCy.destroy();

        dependencyCy =
            null;
    }


    dependencyCy =
        cytoscape({

            container:
                graphContainer,

            elements:
                elements,

            layout: {

                name:
                    "cose",

                animate:
                    true,

                fit:
                    true,

                padding:
                    30
            },

            style: [

                {
                    selector:
                        "node",

                    style: {

                        label:
                            "data(label)",

                        "text-valign":
                            "center",

                        "text-halign":
                            "center",

                        "font-size":
                            "10px",

                        width:
                            35,

                        height:
                            35
                    }
                },

                {
                    selector:
                        "edge",

                    style: {

                        width:
                            1.5,

                        "curve-style":
                            "bezier",

                        "target-arrow-shape":
                            "triangle"
                    }
                },

                {
                    selector:
                        ":selected",

                    style: {

                        "border-width":
                            3
                    }
                }
            ]
        });


    if (status) {

        status.textContent =
            `${elements.nodes.length} files • ` +
            `${elements.edges.length} dependencies`;
    }


    dependencyCy.on(
        "tap",
        "node",
        event => {

            const node =
                event.target;


            const file =
                node.data(
                    "id"
                );


            inspectSearchFile(
                file
            );
        }
    );
}


// ============================================================
// DEPENDENCY ELEMENTS
// ============================================================

function buildDependencyElements(
    dependencies
) {

    const nodes = [];
    const edges = [];

    const nodeSet =
        new Set();


    Object.entries(
        dependencies || {}
    ).forEach(
        ([file, data]) => {

            if (
                !nodeSet.has(file)
            ) {

                nodes.push({

                    data: {

                        id:
                            file,

                        label:
                            getShortFileName(
                                file
                            )
                    }
                });


                nodeSet.add(
                    file
                );
            }


            const internal =
                Array.isArray(
                    data.internal
                )
                    ? data.internal
                    : [];


            internal.forEach(
                target => {

                    if (
                        !nodeSet.has(
                            target
                        )
                    ) {

                        nodes.push({

                            data: {

                                id:
                                    target,

                                label:
                                    getShortFileName(
                                        target
                                    )
                            }
                        });


                        nodeSet.add(
                            target
                        );
                    }


                    const edgeId =
                        `${file}->${target}`;


                    if (
                        !edges.some(
                            edge =>
                                edge.data.id ===
                                edgeId
                        )
                    ) {

                        edges.push({

                            data: {

                                id:
                                    edgeId,

                                source:
                                    file,

                                target:
                                    target
                            }
                        });
                    }
                }
            );
        }
    );


    return {
        nodes,
        edges
    };
}


// ============================================================
// 💡 RECOMMENDATIONS
// ============================================================

function renderRecommendations(
    data
) {

    const container =
        document.getElementById(
            "recommendations"
        );


    if (!container) {
        return;
    }


    const recommendations =
        data?.recommendations ||
        [];


    if (
        !recommendations.length
    ) {

        container.innerHTML = `

            <div class="empty-state">
                No recommendations generated.
            </div>

        `;

        return;
    }


    container.innerHTML =
        recommendations
            .map(
                item => {

                    const priority =
                        item.priority ||
                        "low";


                    return `

                        <div class="recommendation-card">

                            <div class="recommendation-header">

                                <strong>
                                    ${escapeHTML(
                                        item.title ||
                                        "Recommendation"
                                    )}
                                </strong>

                                <span>
                                    ${escapeHTML(
                                        priority.toUpperCase()
                                    )}
                                </span>

                            </div>

                            <p>
                                ${escapeHTML(
                                    item.description ||
                                    item.message ||
                                    ""
                                )}
                            </p>

                        </div>
                    `;
                }
            )
            .join("");
}


// ============================================================
// 📈 HEALTH HISTORY
// ============================================================

async function loadHealthHistory() {

    const container =
        document.getElementById(
            "healthHistory"
        );


    const status =
        document.getElementById(
            "historyStatus"
        );


    if (!container) {
        return;
    }


    try {

        if (status) {

            status.textContent =
                "Loading health history...";
        }


        const data =
            await fetchAPI(
                "/health-history"
            );


        const history =
            data.history ||
            data.snapshots ||
            [];


        if (
            !history.length
        ) {

            container.innerHTML = `

                <div class="empty-state">

                    <div class="empty-icon">
                        📈
                    </div>

                    <h3>
                        No snapshots yet
                    </h3>

                    <p>
                        Run PHANTOM scans to begin
                        tracking project health over time.
                    </p>

                </div>
            `;


            if (status) {

                status.textContent =
                    "Waiting for snapshots";
            }


            return;
        }


        container.innerHTML =
            history
                .slice()
                .reverse()
                .map(
                    (
                        snapshot,
                        index
                    ) => {

                        const metrics =
                            snapshot.metrics ||
                            {};


                        const architecture =
                            snapshot.architecture ||
                            {};


                        const score =
                            architecture.score ??
                            snapshot.architecture_score ??
                            0;


                        const loc =
                            metrics.loc ??
                            metrics.total_loc ??
                            snapshot.loc ??
                            0;


                        let smells =
                            metrics.code_smells ??
                            snapshot.code_smells ??
                            snapshot.total_smells ??
                            0;


                        // ------------------------------------
                        // FIX: OBJECT → NUMBER
                        // ------------------------------------

                        if (
                            smells &&
                            typeof smells ===
                            "object"
                        ) {

                            smells =
                                smells.total_smells ??
                                smells.count ??
                                0;
                        }


                        const complexity =
                            metrics.average_complexity ??
                            snapshot.average_complexity ??
                            0;


                        const cycles =
                            architecture.circular_dependency_count ??
                            snapshot.cycles ??
                            snapshot.circular_dependencies ??
                            0;


                        const timestamp =
                            snapshot.timestamp ||
                            snapshot.created_at ||
                            snapshot.date ||
                            "Unknown time";


                        return `

                            <div class="history-card">

                                <div class="history-header">

                                    <div>

                                        <span class="history-index">
                                            SNAPSHOT
                                            ${history.length - index}
                                        </span>

                                        <h3>
                                            ${escapeHTML(
                                                formatHistoryDate(
                                                    timestamp
                                                )
                                            )}
                                        </h3>

                                    </div>


                                    <div class="history-score">

                                        <span>
                                            ${score}
                                        </span>

                                        <small>
                                            /100
                                        </small>

                                    </div>

                                </div>


                                <div class="history-metrics">

                                    <div class="history-metric">

                                        <span>📄</span>

                                        <strong>
                                            ${loc}
                                        </strong>

                                        <small>
                                            LOC
                                        </small>

                                    </div>


                                    <div class="history-metric">

                                        <span>🧠</span>

                                        <strong>
                                            ${Number(
                                                complexity
                                            ).toFixed(2)}
                                        </strong>

                                        <small>
                                            AVG COMPLEXITY
                                        </small>

                                    </div>


                                    <div class="history-metric">

                                        <span>👃</span>

                                        <strong>
                                            ${smells}
                                        </strong>

                                        <small>
                                            CODE SMELLS
                                        </small>

                                    </div>


                                    <div class="history-metric">

                                        <span>🔗</span>

                                        <strong>
                                            ${cycles}
                                        </strong>

                                        <small>
                                            CYCLES
                                        </small>

                                    </div>

                                </div>

                            </div>
                        `;
                    }
                )
                .join("");


        if (status) {

            status.textContent =
                `${history.length} snapshot` +
                `${
                    history.length === 1
                        ? ""
                        : "s"
                } recorded`;
        }

    } catch (error) {

        console.error(
            "Health history error:",
            error
        );


        container.innerHTML = `

            <div class="error-state">

                <div class="empty-icon">
                    ⚠️
                </div>

                <h3>
                    Health history unavailable
                </h3>

                <p>
                    ${escapeHTML(
                        error.message
                    )}
                </p>

            </div>
        `;


        if (status) {

            status.textContent =
                "History unavailable";
        }
    }
}


// ============================================================
// HISTORY DATE
// ============================================================

function formatHistoryDate(
    value
) {

    if (!value) {
        return "Unknown";
    }


    const date =
        new Date(value);


    if (
        Number.isNaN(
            date.getTime()
        )
    ) {

        return String(value);
    }


    return date.toLocaleString();
}


// ============================================================
// 🔎 SEARCH & FILTER
// ============================================================

function initializeSearch() {

    const searchInput =
        document.getElementById(
            "searchInput"
        );


    const riskFilter =
        document.getElementById(
            "riskFilter"
        );


    const complexityFilter =
        document.getElementById(
            "complexityFilter"
        );


    const highlyCoupledFilter =
        document.getElementById(
            "highlyCoupledFilter"
        );


    if (!searchInput) {
        return;
    }


    if (
        searchInput.dataset.initialized ===
        "true"
    ) {

        return;
    }


    searchInput.dataset.initialized =
        "true";


    const performSearch =
        debounce(
            async () => {

                try {

                    const params =
                        new URLSearchParams();


                    params.set(
                        "query",
                        searchInput.value
                    );


                    if (riskFilter) {

                        params.set(
                            "risk",
                            riskFilter.value
                        );
                    }


                    if (complexityFilter) {

                        params.set(
                            "complexity",
                            complexityFilter.value
                        );
                    }


                    if (
                        highlyCoupledFilter
                    ) {

                        params.set(
                            "highly_coupled",
                            highlyCoupledFilter.checked
                        );
                    }


                    const data =
                        await fetchAPI(
                            `/search?${params.toString()}`
                        );


                    renderSearchResults(
                        data
                    );

                } catch (error) {

                    console.warn(
                        "Search unavailable:",
                        error
                    );
                }
            },
            300
        );


    searchInput.addEventListener(
        "input",
        performSearch
    );


    if (riskFilter) {

        riskFilter.addEventListener(
            "change",
            performSearch
        );
    }


    if (complexityFilter) {

        complexityFilter.addEventListener(
            "change",
            performSearch
        );
    }


    if (
        highlyCoupledFilter
    ) {

        highlyCoupledFilter.addEventListener(
            "change",
            performSearch
        );
    }


    performSearch();
}


// ============================================================
// SEARCH RESULTS
// ============================================================

function renderSearchResults(
    data
) {

    const container =
        document.getElementById(
            "searchResults"
        );


    if (!container) {
        return;
    }


    const results =
        Array.isArray(
            data?.results
        )
            ? data.results
            : [];


    if (!results.length) {

        container.innerHTML = `

            <div class="empty-state">
                👽 No files match
                the selected filters.
            </div>

        `;

        return;
    }


    container.innerHTML = `

        <div class="search-summary">

            <strong>
                ${results.length}
            </strong>

            matching file(s)

        </div>


        <div class="search-result-list">

            ${
                results
                    .map(
                        result =>
                            createSearchResultCard(
                                result
                            )
                    )
                    .join("")
            }

        </div>
    `;
}


// ============================================================
// SEARCH RESULT CARD
// ============================================================

function createSearchResultCard(
    result
) {

    const risk =
        String(
            result.risk ||
            "low"
        ).toLowerCase();


    const complexityLevel =
        String(
            result.complexity_level ||
            "low"
        ).toLowerCase();


    const coupled =
        result.highly_coupled ===
        true;


    return `

        <div class="search-result-card">

            <div class="search-result-header">

                <div class="search-file">

                    <span class="file-icon">
                        📄
                    </span>

                    <strong>
                        ${escapeHTML(
                            result.file ||
                            "Unknown file"
                        )}
                    </strong>

                </div>


                <span
                    class="search-risk ${escapeHTML(
                        risk
                    )}"
                >
                    ${escapeHTML(
                        risk.toUpperCase()
                    )}
                </span>

            </div>


            <div class="search-result-metrics">

                <div class="search-metric">

                    <span>
                        LOC
                    </span>

                    <strong>
                        ${result.lines ?? 0}
                    </strong>

                </div>


                <div class="search-metric">

                    <span>
                        Dependencies
                    </span>

                    <strong>
                        ${result.dependencies ?? 0}
                    </strong>

                </div>


                <div class="search-metric">

                    <span>
                        Complexity
                    </span>

                    <strong>
                        ${result.complexity ?? 0}
                    </strong>

                </div>


                <div class="search-metric">

                    <span>
                        Level
                    </span>

                    <strong
                        class="${escapeHTML(
                            complexityLevel
                        )}"
                    >
                        ${escapeHTML(
                            complexityLevel.toUpperCase()
                        )}
                    </strong>

                </div>

            </div>


            <div class="search-result-footer">

                <span
                    class="complexity-badge ${escapeHTML(
                        complexityLevel
                    )}"
                >
                    Complexity:
                    ${escapeHTML(
                        complexityLevel.toUpperCase()
                    )}
                </span>


                ${
                    coupled
                        ? `
                            <span class="coupled-badge">
                                🔗 HIGHLY COUPLED
                            </span>
                        `
                        : ""
                }


                <button
                    class="inspect-search-file"
                    onclick="inspectSearchFile('${escapeJS(
                        result.file ||
                        ""
                    )}')"
                >
                    Inspect →
                </button>

            </div>

        </div>
    `;
}


// ============================================================
// FILE INSPECTOR
// ============================================================

async function renderFileInspector(
    file
) {

    const inspector =
        document.getElementById(
            "inspectorContent"
        );


    if (!inspector) {
        return;
    }


    inspector.innerHTML = `

        <div class="empty-state">

            <div class="empty-icon">
                👽
            </div>

            <h3>
                Analyzing file...
            </h3>

            <p>
                PHANTOM is building the
                file intelligence profile.
            </p>

        </div>
    `;


    try {

        const result =
            await fetchAPI(
                `/file-inspector?file=${encodeURIComponent(
                    file
                )}`
            );


        if (result.error) {

            throw new Error(
                result.error
            );
        }


        const metrics =
            result.metrics || {};

        const dependencies =
            result.dependencies || {};

        const hotspot =
            result.hotspot || {};

        const risk =
            result.risk || {};

        const smells =
            result.code_smells || {};


        const internal =
            Array.isArray(
                dependencies.internal
            )
                ? dependencies.internal
                : [];


        const external =
            Array.isArray(
                dependencies.external
            )
                ? dependencies.external
                : [];


        const smellList =
            Array.isArray(
                smells.smells
            )
                ? smells.smells
                : [];


        inspector.innerHTML = `

            <div class="file-intelligence">

                <div class="inspector-header">

                    <span class="file-icon">
                        📄
                    </span>

                    <div>

                        <h3>
                            ${escapeHTML(
                                result.file ||
                                file
                            )}
                        </h3>

                        <p>
                            Module:
                            ${escapeHTML(
                                result.module ||
                                "Unknown"
                            )}
                        </p>

                    </div>

                </div>


                <div class="inspector-section">

                    <h4>
                        📊 File Metrics
                    </h4>

                    <div class="inspector-metric-grid">

                        <div class="inspector-metric">
                            <span>Lines</span>
                            <strong>
                                ${metrics.lines ?? 0}
                            </strong>
                        </div>

                        <div class="inspector-metric">
                            <span>Functions</span>
                            <strong>
                                ${metrics.functions ?? 0}
                            </strong>
                        </div>

                        <div class="inspector-metric">
                            <span>Classes</span>
                            <strong>
                                ${metrics.classes ?? 0}
                            </strong>
                        </div>

                        <div class="inspector-metric">
                            <span>Complexity</span>
                            <strong>
                                ${metrics.complexity ?? 0}
                            </strong>
                        </div>

                    </div>

                </div>


                <div class="inspector-section">

                    <h4>
                        🛡️ Risk Intelligence
                    </h4>

                    <div class="inspector-intelligence-card">

                        <div>

                            <span>
                                Risk Score
                            </span>

                            <strong>
                                ${risk.score ?? 0}
                            </strong>

                        </div>

                        <span class="inspector-badge">
                            ${escapeHTML(
                                String(
                                    risk.level ||
                                    "low"
                                ).toUpperCase()
                            )}
                        </span>

                    </div>

                    ${
                        Array.isArray(
                            risk.reasons
                        ) &&
                        risk.reasons.length
                            ? `
                                <ul class="inspector-list">

                                    ${risk.reasons
                                        .map(
                                            reason =>
                                                `<li>
                                                    ${escapeHTML(
                                                        reason
                                                    )}
                                                </li>`
                                        )
                                        .join("")}

                                </ul>
                            `
                            : ""
                    }

                </div>


                <div class="inspector-section">

                    <h4>
                        🔥 Hotspot Intelligence
                    </h4>

                    <div class="inspector-intelligence-card">

                        <div>

                            <span>
                                Hotspot Score
                            </span>

                            <strong>
                                ${hotspot.score ?? 0}
                            </strong>

                        </div>

                        <span class="inspector-badge">
                            ${escapeHTML(
                                String(
                                    hotspot.level ||
                                    "low"
                                ).toUpperCase()
                            )}
                        </span>

                    </div>

                </div>


                <div class="inspector-section">

                    <h4>
                        🔗 Dependencies
                    </h4>

                    <div class="dependency-summary">

                        <span>
                            Internal:
                            <strong>
                                ${
                                    dependencies.internal_count ??
                                    internal.length
                                }
                            </strong>
                        </span>

                        <span>
                            External:
                            <strong>
                                ${
                                    dependencies.external_count ??
                                    external.length
                                }
                            </strong>
                        </span>

                    </div>


                    <h5>
                        Internal Dependencies
                    </h5>

                    <ul class="inspector-list">

                        ${
                            internal.length
                                ? internal
                                    .map(
                                        item =>
                                            `<li>
                                                ${escapeHTML(
                                                    item
                                                )}
                                            </li>`
                                    )
                                    .join("")
                                : "<li>None</li>"
                        }

                    </ul>


                    <h5>
                        External Dependencies
                    </h5>

                    <ul class="inspector-list">

                        ${
                            external.length
                                ? external
                                    .map(
                                        item =>
                                            `<li>
                                                ${escapeHTML(
                                                    item
                                                )}
                                            </li>`
                                    )
                                    .join("")
                                : "<li>None</li>"
                        }

                    </ul>

                </div>


                <div class="inspector-section">

                    <h4>
                        👃 Code Smells
                    </h4>

                    <div class="smell-count-large">

                        ${
                            smells.smell_count ??
                            smellList.length
                        }

                        <span>
                            detected
                        </span>

                    </div>


                    ${
                        smellList.length
                            ? `
                                <div class="inspector-smells">

                                    ${smellList
                                        .map(
                                            smell =>
                                                `
                                                    <div class="inspector-smell">

                                                        <strong>
                                                            ${escapeHTML(
                                                                formatSmellType(
                                                                    smell.type
                                                                )
                                                            )}
                                                        </strong>

                                                        <span>
                                                            ${escapeHTML(
                                                                String(
                                                                    smell.severity ||
                                                                    "warning"
                                                                ).toUpperCase()
                                                            )}
                                                        </span>

                                                        <p>
                                                            ${escapeHTML(
                                                                smell.message ||
                                                                smell.reason ||
                                                                "Code smell detected."
                                                            )}
                                                        </p>

                                                    </div>
                                                `
                                        )
                                        .join("")}

                                </div>
                            `
                            : `
                                <div class="empty-state">
                                    No code smells detected.
                                </div>
                            `
                    }

                </div>

            </div>
        `;

    } catch (error) {

        console.error(
            "File inspector error:",
            error
        );


        inspector.innerHTML = `

            <div class="error-state">

                <div class="empty-icon">
                    ⚠️
                </div>

                <h3>
                    File intelligence unavailable
                </h3>

                <p>
                    ${escapeHTML(
                        error.message
                    )}
                </p>

            </div>
        `;
    }
}


// ============================================================
// RISK INTELLIGENCE
// ============================================================

function renderRiskIntelligence(
    riskData
) {

    const container =
        document.getElementById(
            "riskIntelligence"
        );


    const status =
        document.getElementById(
            "riskStatus"
        );


    if (!container) {
        return;
    }


    if (
        !riskData ||
        riskData.error
    ) {

        container.innerHTML =
            "";


        if (status) {

            status.textContent =
                "Risk analysis unavailable.";
        }


        return;
    }


    const risks =
        Array.isArray(
            riskData.risks
        )
            ? riskData.risks
            : [];


    if (status) {

        status.textContent =
            `${
                riskData.risk_count ??
                risks.length
            } files analyzed`;
    }


    if (!risks.length) {

        container.innerHTML = `

            <div class="empty-state">
                No risk data available.
            </div>

        `;

        return;
    }


    container.innerHTML =
        risks
            .slice(
                0,
                10
            )
            .map(
                risk => `

                    <div class="risk-card">

                        <div class="risk-card-header">

                            <strong>
                                ${escapeHTML(
                                    risk.file ||
                                    "Unknown file"
                                )}
                            </strong>

                            <span>
                                ${escapeHTML(
                                    String(
                                        risk.level ||
                                        "low"
                                    ).toUpperCase()
                                )}
                            </span>

                        </div>


                        <div class="risk-score">

                            <span>
                                Risk Score
                            </span>

                            <strong>
                                ${risk.score ?? 0}
                            </strong>

                        </div>


                        <div class="risk-details">

                            <span>
                                Complexity:
                                ${risk.complexity ?? 0}
                            </span>

                            <span>
                                Hotspot:
                                ${risk.hotspot_score ?? 0}
                            </span>

                            <span>
                                Smells:
                                ${risk.code_smells ?? 0}
                            </span>

                        </div>

                    </div>
                `
            )
            .join("");
}


// ============================================================
// HOTSPOT INTELLIGENCE
// ============================================================

function renderHotspotIntelligence(
    hotspotData
) {

    const container =
        document.getElementById(
            "hotspotIntelligence"
        );


    const status =
        document.getElementById(
            "hotspotStatus"
        );


    if (!container) {
        return;
    }


    if (
        !hotspotData ||
        hotspotData.error
    ) {

        container.innerHTML =
            "";


        if (status) {

            status.textContent =
                "Hotspot analysis unavailable.";
        }


        return;
    }


    const hotspots =
        Array.isArray(
            hotspotData.hotspots
        )
            ? hotspotData.hotspots
            : [];


    if (status) {

        status.textContent =
            `${
                hotspotData.hotspot_count ??
                hotspots.length
            } files analyzed`;
    }


    if (!hotspots.length) {

        container.innerHTML = `

            <div class="empty-state">
                No hotspots detected.
            </div>

        `;

        return;
    }


    container.innerHTML =
        hotspots
            .slice(
                0,
                10
            )
            .map(
                hotspot =>
                    createHotspotCard(
                        hotspot
                    )
            )
            .join("");
}


// ============================================================
// HOTSPOT CARD
// ============================================================

function createHotspotCard(
    hotspot
) {

    const level =
        String(
            hotspot.level ||
            "low"
        ).toLowerCase();


    return `

        <div class="hotspot-card ${escapeHTML(level)}">

            <div class="hotspot-card-header">

                <strong>
                    ${escapeHTML(
                        hotspot.file ||
                        "Unknown file"
                    )}
                </strong>

                <span class="hotspot-level">
                    ${escapeHTML(
                        level.toUpperCase()
                    )}
                </span>

            </div>


            <div class="hotspot-score">

                <span>
                    Hotspot Score
                </span>

                <strong>
                    ${hotspot.score ?? 0}
                </strong>

            </div>


            <div class="hotspot-details">

                <span>
                    Complexity:
                    ${hotspot.complexity ?? 0}
                </span>

                <span>
                    Internal deps:
                    ${hotspot.internal_dependencies ?? 0}
                </span>

                <span>
                    External deps:
                    ${hotspot.external_dependencies ?? 0}
                </span>

            </div>

        </div>
    `;
}


// ============================================================
// SEARCH FILE INSPECTOR
// ============================================================

function inspectSearchFile(
    file
) {

    if (
        phantomData &&
        phantomData.dependencies &&
        phantomData.dependencies[file]
    ) {

        renderFileInspector(
            file
        );


        const inspector =
            document.getElementById(
                "fileInspector"
            );


        if (inspector) {

            inspector.scrollIntoView({

                behavior:
                    "smooth",

                block:
                    "center"
            });
        }

    } else {

        renderFileInspector(
            file
        );
    }
}


// ============================================================
// UTILITIES
// ============================================================

function setText(
    id,
    value
) {

    const element =
        document.getElementById(
            id
        );


    if (element) {

        element.textContent =
            value !== undefined &&
            value !== null
                ? value
                : "--";
    }
}


function formatLabel(
    value
) {

    return String(value)
        .replace(
            /_/g,
            " "
        )
        .replace(
            /\b\w/g,
            letter =>
                letter.toUpperCase()
        );
}


function getShortFileName(
    file
) {

    if (!file) {
        return "Unknown";
    }


    const parts =
        String(file).split("/");


    return parts[
        parts.length - 1
    ];
}


function escapeHTML(
    value
) {

    return String(value)
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );
}


function escapeJS(
    value
) {

    return String(value)
        .replace(
            /\\/g,
            "\\\\"
        )
        .replace(
            /'/g,
            "\\'"
        )
        .replace(
            /"/g,
            '\\"'
        )
        .replace(
            /\n/g,
            "\\n"
        )
        .replace(
            /\r/g,
            "\\r"
        );
}


function debounce(
    callback,
    delay
) {

    let timeout;


    return function (...args) {

        clearTimeout(
            timeout
        );


        timeout =
            setTimeout(
                () =>
                    callback.apply(
                        this,
                        args
                    ),
                delay
            );
    };
}


function updateScanStatus(
    message
) {

    const status =
        document.getElementById(
            "scanStatus"
        );


    if (status) {

        status.textContent =
            message;
    }
}


// ============================================================
// INITIALIZATION
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        console.log(
            "👽 PROJECT-PHANTOM dashboard initialized."
        );


        // ----------------------------------------------------
        // SCAN BUTTON
        // ----------------------------------------------------

        const scanButton =
            document.getElementById(
                "scanButton"
            );


        if (scanButton) {

            scanButton.addEventListener(
                "click",
                runPhantomScan
            );
        }


        // ----------------------------------------------------
        // PROJECT SELECTOR BUTTON
        // ----------------------------------------------------

        const selectProjectButton =
            document.getElementById(
                "selectProjectButton"
            );


        if (
            selectProjectButton
        ) {

            selectProjectButton.addEventListener(
                "click",
                selectProject
            );
        }


        // ----------------------------------------------------
        // ENTER KEY IN PROJECT PATH
        // ----------------------------------------------------

        const projectPath =
            document.getElementById(
                "projectPath"
            );


        if (projectPath) {

            projectPath.addEventListener(
                "keydown",
                event => {

                    if (
                        event.key ===
                        "Enter"
                    ) {

                        event.preventDefault();

                        selectProject();
                    }
                }
            );
        }


        // ----------------------------------------------------
        // LOAD CURRENT PROJECT
        // ----------------------------------------------------

        loadCurrentProject();


        // ----------------------------------------------------
        // INITIAL PHANTOM SCAN
        // ----------------------------------------------------

        runPhantomScan();
    }
);