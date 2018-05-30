#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Standalone benchmark runner
"""

import cProfile
import pstats
import profile
import numpy as np

print("Running Rust, Python, and C++ benchmarks. 1000 points, 500 runs.\n")

# calibrate
print("Calibrating system")
pr = profile.Profile()
calibration = np.mean([pr.calibrate(100000) for x in range(5)])
# add the bias
profile.Profile.bias = calibration
print("Calibration complete, running benchmarks\n")
bmarks = [
    ('benches/benchmark_rust.py', 'benches/output_stats_rust', 'Rust + Cython'),
    ('benches/benchmark_python.py', 'benches/output_stats_python', 'Pure Python'),
    ('benches/benchmark_cgg.py', 'benches/output_stats_cgg', 'C++')
]

results = []
for benchmark in bmarks:
    cProfile.run(open(benchmark[0], 'rb'), benchmark[1])
    results.append(pstats.Stats(benchmark[1]))

for i, benchmark in enumerate(bmarks):
    print("%s Benchmark\n" % benchmark[2])
    results[i].sort_stats('cumulative').print_stats(3)
