const kind = document.body.dataset.kind;
const runButton = document.getElementById("run-btn");
const selector = document.getElementById("run-select");
const errorBox = document.getElementById("error");
let results = [];
let charts = {};

function setText(id, value) {
    const element = document.getElementById(id);
    if (element) element.textContent = value;
}

function drawGrid(id, data) {
    const box = document.getElementById(id);
    box.textContent = "";
    box.style.gridTemplateColumns = "repeat(" + data[0].length + ", 1fr)";
    box.style.aspectRatio = data[0].length + " / " + data.length;
    for (let i = 0; i < data.length; i++) {
        for (let j = 0; j < data[i].length; j++) {
            const cell = document.createElement("div");
            cell.textContent = data[i][j];
            if (data[i][j]) cell.className = data[i][j];
            box.appendChild(cell);
        }
    }
}

// Grafik: https://www.chartjs.org/docs/latest/charts/line.html
// Ganti grafik pada canvas: https://www.chartjs.org/docs/latest/developers/api.html#destroy
function drawChart(id, datasets, start) {
    if (charts[id]) charts[id].destroy();
    const labels = [];
    for (let i = 0; i < datasets[0].data.length; i++) labels.push(i + start);
    charts[id] = new Chart(document.getElementById(id), {
        type: "line",
        data: { labels: labels, datasets: datasets },
        options: { responsive: true, maintainAspectRatio: false, animation: false,
                   elements: { point: { radius: 0 }, line: { borderWidth: 1 } } }
    });
}

function showResult(index) {
    const result = results[index];
    const extra = result.extra;
    drawGrid("initial-state-container", result.initial_state_grid);
    drawGrid("final-state-container", result.final_state_grid);
    if (kind === "ga") {
        drawChart("fitness-chart", [
            { label: "Terbaik", data: extra.max_history, borderColor: "#222" },
            { label: "Rata-rata", data: extra.mean_history, borderColor: "#888" }
        ], 0);
    } else {
        drawChart("fitness-chart", [
            { label: "Nilai", data: result.fitness_history, borderColor: "#222" }
        ], 0);
    }
    if (kind === "sa") {
        const reference = [];
        for (let i = 0; i < extra.acceptance_history.length; i++) reference.push(extra.acceptance_threshold);
        drawChart("acceptance-chart", [
            { label: "Peluang", data: extra.acceptance_history, borderColor: "#222", showLine: false, pointRadius: 2 },
            { label: "Referensi 0,5", data: reference, borderColor: "#888", borderDash: [4, 4] }
        ], 1);
    }
    setText("stat-initial", result.initial_fitness);
    setText("stat-final", result.final_fitness);
    setText("stat-fee", result.shipping_fee);
    setText("stat-eta", result.eta_penalty);
    setText("stat-iterations", result.iterasi);
    setText("stat-duration", result.durasi);
    setText("stat-population", extra.population_size);
    setText("stat-capacity", extra.total_weight + " / " + extra.max_capacity);
    setText("stat-stuck", extra.stuck_count);
    document.getElementById("result-area").hidden = false;
}

if (selector) {
    selector.onchange = function () {
        showResult(Number(selector.value));
    };
}
// fetch dan JSON: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
runButton.onclick = async function () {
    runButton.disabled = true;
    runButton.textContent = "Menjalankan…";
    if (selector) selector.disabled = true;
    errorBox.hidden = true;
    try {
        const response = await fetch(document.body.dataset.endpoint, { method: "POST" });
        if (!response.ok) throw new Error("HTTP " + response.status + ". Periksa terminal Flask.");
        const payload = await response.json();
        results = payload.data;
        if (selector) {
            selector.textContent = "";
            for (let i = 0; i < results.length; i++) {
                const option = document.createElement("option");
                const extra = results[i].extra;
                option.value = i;
                option.textContent = "Populasi " + extra.population_size + " / Generasi " + extra.generations + " / " + extra.selector_label;
                selector.appendChild(option);
            }
            selector.hidden = false;
        }
        showResult(0);
    } catch (error) {
        errorBox.textContent = error.message;
        errorBox.hidden = false;
    } finally {
        runButton.disabled = false;
        runButton.textContent = "Jalankan";
        if (selector) selector.disabled = false;
    }
};
