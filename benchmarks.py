#!/usr/bin/env python
"""
Standalone benchmark runner
"""

import cProfile
import profile
import pstats

import numpy as np

print("Running Rust, Python, and Flexpolyline benchmarks. 1000 points, 500 runs.\n")

# calibrate
print("Calibrating system")
pr = profile.Profile()
calibration = np.mean([pr.calibrate(100000) for x in range(5)])
# add the bias
profile.Profile.bias = calibration
print("Calibration complete, running benchmarks\n")
bmarks = [
    ("benches/benchmark_rust.py", "benches/output_stats_rust", "Rust + Cython"),
    ("benches/benchmark_python.py", "benches/output_stats_python", "Pure Python"),
    (
        "benches/benchmark_flexpolyline.py",
        "benches/output_stats_flexpolyline",
        "Python Flexpolyline",
    ),
]

results = []
for benchmark in bmarks:
    with open(benchmark[0], "rb") as f:
        cProfile.run(f.read(), benchmark[1])
        results.append(pstats.Stats(benchmark[1]))

for i, benchmark in enumerate(bmarks):
    print("%s Benchmark\n" % benchmark[2])
    results[i].sort_stats("cumulative").print_stats(3)
