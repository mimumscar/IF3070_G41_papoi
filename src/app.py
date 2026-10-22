# Route dan template: https://flask.palletsprojects.com/en/stable/quickstart/
# API JSON: https://flask.palletsprojects.com/en/stable/patterns/javascript/
import json
from pathlib import Path
from flask import Flask, jsonify, render_template
from data import SHIP, VEHICLES
from ga import GA_CONFIGS, GeneticAlgorithm
from hc import HillClimbing
from sa import SimulatedAnnealing

app = Flask(__name__)
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def buat_grid(state):
    grid = []
    for x in range(state.ship.width):
        grid.append([""] * state.ship.length)
    for kendaraan in state.vehicles:
        if kendaraan.x is None or kendaraan.y is None:
            continue
        lebar, panjang = kendaraan.getCurrentDimensions()
        for x in range(kendaraan.x, kendaraan.x + lebar):
            for y in range(kendaraan.y, kendaraan.y + panjang):
                grid[x][y] = kendaraan.id
    return grid


def buat_hasil(algoritma, akhir, riwayat, nomor=1, tambahan=None):
    berat = 0
    for kendaraan in akhir.vehicles:
        if kendaraan.x is not None:
            berat += kendaraan.weight
    extra = {"total_weight": berat, "max_capacity": akhir.ship.maxCapacity}
    if tambahan is not None:
        extra.update(tambahan)
    return {
        "status": "success", "run_id": nomor,
        "initial_fitness": algoritma.initialState.getFitness(),
        "final_fitness": akhir.getFitness(),
        "shipping_fee": akhir.getShippingFee(),
        "eta_penalty": akhir.getEtaPenalty(),
        "iterasi": len(riwayat) - 1,
        "durasi": round(algoritma.duration, 4),
        "initial_state_grid": buat_grid(algoritma.initialState),
        "final_state_grid": buat_grid(akhir),
        "fitness_history": riwayat, "extra": extra,
    }

def output(algoritma, data):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filea = OUTPUT_DIR / (algoritma + ".json")
    with filea.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("index.html", title="Hill Climbing", kind="hc", endpoint="/run_hill_climbing")


@app.route("/sa")
def simulated_annealing_page():
    return render_template("index.html", title="Simulated Annealing", kind="sa", endpoint="/run_simulated_annealing")


@app.route("/ga")
def genetic_algorithm_page():
    return render_template("index.html", title="Genetic Algorithm", kind="ga", endpoint="/run_genetic_algorithm")


@app.route("/run_hill_climbing", methods=["POST"])
def run_hill_climbing():
    algoritma = HillClimbing(SHIP, VEHICLES)
    akhir = algoritma.runSteepestAscent()
    hasil = buat_hasil(algoritma, akhir, algoritma.history)
    output("hc", [hasil])
    return jsonify({"status": "success", "algorithm": "hc", "data": [hasil]})


@app.route("/run_simulated_annealing", methods=["POST"])
def run_simulated_annealing():
    algoritma = SimulatedAnnealing(SHIP, VEHICLES)
    akhir = algoritma.run()
    tambahan = {
        "temperature": algoritma.temperature, "cooling": algoritma.cooling,
        "acceptance_history": algoritma.acceptance_history,
        "acceptance_threshold": 0.5, "stuck_count": algoritma.stuck_count,
    }
    hasil = buat_hasil(algoritma, akhir, algoritma.history, tambahan=tambahan)
    output("sa", [hasil])
    return jsonify({"status": "success", "algorithm": "sa", "data": [hasil]})


@app.route("/run_genetic_algorithm", methods=["POST"])
def run_genetic_algorithm():
    hasil = []
    for i in range(len(GA_CONFIGS)):
        konfigurasi = GA_CONFIGS[i]
        for j in range(3):
            algoritma = GeneticAlgorithm(SHIP, VEHICLES,
                populationSize=konfigurasi["populationSize"],
                generations=konfigurasi["generations"])
            akhir = algoritma.runGeneticAlgorithm()
            tambahan = {
                "config_id": i, "population_size": konfigurasi["populationSize"],
                "generations": konfigurasi["generations"],
                "max_history": algoritma.maxHistory, "mean_history": algoritma.meanHistory,
                "selector_label": "K" + str(i + 1) + "/R" + str(j + 1),
            }
            hasil.append(buat_hasil(algoritma, akhir, algoritma.maxHistory, len(hasil) + 1, tambahan))
    output("ga", hasil)
    return jsonify({"status": "success", "algorithm": "ga", "data": hasil})


if __name__ == "__main__":
    app.run(debug=True)
