# Decay-Driven Engagement Strength for Cohesive Subgraph Discovery: The s-Hypercore Framework
This repository provides a complete implementation of a novel cohesive subgraph discovery model named s-hypercore for hypergraphs.

## Code Structure
```
.
├── codes/
│   ├── computation.py   # s-hypercore peeling for a given s (Engagement Strength)
│   ├── decomposition.py # Full s-hypercore decomposition with hypercoreness scores
│   ├── func.py          # Hypergraph data structure, DCS/ES helpers, and stats
│   └── main.py          # CLI entry point
├── datasets/
│   ├── congress/network.hyp
│   ├── house_bills/network.hyp
│   ├── meetup/network.hyp
│   └── toy/network.hyp
├── results/
└── README.md
```

## Input format
Each line in `network.hyp` represents a hyperedge as space/comma/tab separated node IDs. Example:
```
1 2 3 6 7 8
2 3 4 5 7 8 9 10
```

## Setup
- Python 3.8+
- Install dependencies:
  ```
  pip install psutil
  ```

## How to Run
The paths in `main.py` are relative to the `codes/` directory. Run commands from `codes/` or adjust paths accordingly.

### s-hypercore computation (fixed s)
```
cd codes
python main.py --network meetup --algorithm computation --s 1 --output_path ../results/output.csv
```
- Writes a row to `results/output.csv` with dataset size, ES statistics, runtime, and memory.

### s-hypercore decomposition
```
cd codes
python main.py --network meetup --algorithm decomposition
```
- Logs runtime/memory to `results/output.csv`.
- Saves coreness assignments to `results/<dataset>_decomposition` (two columns: node ID, coreness).

### Arguments
| Parameter        | Description                                                        |
|------------------|--------------------------------------------------------------------|
| `--network`      | Dataset folder under `datasets/` (e.g., `meetup`, `congress`)      |
| `--algorithm`    | `computation` (default) or `decomposition`                         |
| `--s`            | Engagement Strength threshold for peeling (used by `computation`)  |
| `--output_path`  | CSV file to append run statistics (default: `../results/output.csv`)|

### Available datasets
- `congress`
- `house_bills`
- `meetup`
- `toy`
