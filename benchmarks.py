#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Standalone benchmark runner
"""

import cProfile
import pstats
import profile
import numpy as np

print("Running Rust, Python, and C++ benchmarks. 100 points, 50 runs.\n")

# calibrate
pr = profile.Profile()
calibration = np.mean([pr.calibrate(100000) for x in xrange(5)])
# add the bias
profile.Profile.bias = calibration

cProfile.run(open('benches/benchmark_rust.py', 'rb'), 'benches/output_stats_rust')
rust = pstats.Stats('benches/output_stats_rust')

cProfile.run(open('benches/benchmark_python.py', 'rb'), 'benches/output_stats_python')
rust_cython = pstats.Stats('benches/output_stats_python')

cProfile.run(open('benches/benchmark_cgg.py', 'rb'), 'benches/output_stats_cgg')
pyproj_ = pstats.Stats('benches/output_stats_cgg')

print("Rust Benchmark\n")
rust.sort_stats('cumulative').print_stats(5)
print("Python Benchmark\n")
rust_cython.sort_stats('cumulative').print_stats(5)
print("C++ Benchmark\n")
pyproj_.sort_stats('cumulative').print_stats(5)
