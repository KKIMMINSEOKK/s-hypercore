import argparse
import psutil
import os
import time
import csv
import func
import computation
import decomposition

# ===== Argument parsing =====
parser = argparse.ArgumentParser(description="Peeling Algorithm for s-Hypercore")
parser.add_argument("--network", help="Path to the network file", default='meetup')
parser.add_argument("--algorithm", type=str, help="Algorithm to run", default='computation')
parser.add_argument("--s", type=float, help="Value of s",default=1)
parser.add_argument("--output_path", type=str, default=f'../results/output.csv')
args = parser.parse_args()

# ===== Load hypergraph from file =====
network = f'../datasets/{args.network}/network.hyp'
G = func.Hypergraph()
G.load_from_file(network)

# ===== Measure memory usage before execution =====
process = psutil.Process(os.getpid())
memory_before = process.memory_info().rss / (1024 * 1024)

# ===== Statistics =====
results = {}
results['dataset'] = args.network
results['|V|'] = len(G.nodes)
results['|E|'] = len(G.hyperedges)
results['s'] = args.s

# ===== Run the s-hypercore peeling algorithm =====
start_time = time.time()
if args.algorithm == 'computation':
    t1 = time.time()
    G1, results1 = computation.run(G, args.s)
    t2 = time.time()
    results1['run time'] = t2 - t1

# ===== Run the s-hypercore decomposition algorithm =====
elif args.algorithm == 'decomposition':
    t1 = time.time()
    CN, results1 = decomposition.run(G)
    t2 = time.time()
    results1['run time'] = t2 - t1
results = {**results, **results1}

# ===== Measure memory usage after execution =====
memory_after = process.memory_info().rss / (1024 * 1024)
memory_usage = memory_after - memory_before
results['memory'] = memory_usage

# ===== Save results to CSV =====
values = list(results.values())
file_exists = os.path.exists(args.output_path)
with open(args.output_path, "a", newline="") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(results.keys())
    writer.writerow(values)

# ===== Save decomposition results =====
if args.algorithm == 'decomposition':
    file_exists = os.path.exists(f"../results/{args.network}_decomposition")
    with open(f"../results/{args.network}_decomposition", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            for k, v in CN.items():
                writer.writerow([k, v])