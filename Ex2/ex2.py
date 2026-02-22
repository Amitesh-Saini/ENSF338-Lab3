import random
import matplotlib.pyplot as plt 
import numpy as np 
import timeit
import statistics   
import sys
import time

sys.setrecursionlimit(1_000_000)

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                temp = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = temp
    return arr


def partition(arr, low, high):

    pivot = arr[high]
    i = low-1

    for j in range(low, high):
        if arr[j] < pivot:
            i+=1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]

    return i+1

def quicksort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    if low<high:
        p = partition(arr, low, high)
        quicksort(arr, low, p-1)
        quicksort(arr, p+1, high)

    return arr


def make_sorted(n):
    return list(range(n))

def make_reverse(n):
    return list(range(n, 0, -1))

def make_random(n, rng):
    arr = list(range(n))
    rng.shuffle(arr)
    return arr

def time_one(sort_fn, base_arr, repeats=7):
    times = []
    for _ in range(repeats):
        arr = base_arr[:]  # IMPORTANT: copy each time
        t0 = time.perf_counter()
        sort_fn(arr)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return statistics.median(times)

def find_crossover(sizes, bubble_times, quick_times):
    # first n where quick < bubble
    for n, b, q in zip(sizes, bubble_times, quick_times):
        if q < b:
            return n
    return None


def run_experiment(sizes, repeats=7, seed=123):
    rng = random.Random(seed)

    scenarios = {
        "sorted": make_sorted,
        "reverse": make_reverse,
        "random": lambda n: make_random(n, rng)
    }

    results = {
        "bubble": {k: [] for k in scenarios},
        "quick":  {k: [] for k in scenarios},
    }

    for n in sizes:
        for scen_name, gen in scenarios.items():
            base = gen(n)

            tb = time_one(bubble_sort, base, repeats=repeats)
            tq = time_one(quicksort, base, repeats=repeats)

            results["bubble"][scen_name].append(tb)
            results["quick"][scen_name].append(tq)

            print(f"n={n:5d}  {scen_name:7s}  bubble={tb:.6f}s  quick={tq:.6f}s")

    return results

def plot_results(sizes, results, logy=False):
    for scen in ["sorted", "reverse", "random"]:
        plt.figure()
        plt.plot(sizes, results["bubble"][scen], marker="o", label="Bubble sort")
        plt.plot(sizes, results["quick"][scen], marker="o", label="Quicksort")
        plt.xlabel("Input size (n)")
        plt.ylabel("Time (seconds)")
        plt.title(f"Performance on {scen} inputs")
        if logy:
            plt.yscale("log")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

sizes = [10, 20, 30, 45, 70, 100, 150, 220, 330, 500,
         750, 1000, 1300, 1700, 2200, 2800, 3500, 4300, 5200, 6200]

results = run_experiment(sizes, repeats=7, seed=123)

# Crossover thresholds (small vs not small)
for scen in ["sorted", "reverse", "random"]:
    n0 = find_crossover(sizes, results["bubble"][scen], results["quick"][scen])
    print(f"Crossover (quicksort faster) for {scen}: {n0}")

plot_results(sizes, results, logy=True)


# - Bubble sort (no early exit):
#     Best case (sorted) is still Θ(n^2) comparisons (but fewer swaps).
#      Worst case (reverse) is Θ(n^2) comparisons + many swaps.
#      Average case (random) is Θ(n^2).
# - Quicksort here is Lomuto partition with LAST element pivot:
#      Worst case: sorted and reverse -> Θ(n^2) due to unbalanced partitions.
#      Average case: random -> Θ(n log n).
#      Best case: perfectly balanced splits (theoretical), not guaranteed by last-pivot.
#
# measured results showed 
# - Random: quicksort becomes faster very early (n≈10 in run).
# - Reverse: quicksort becomes faster around n≈20 in run.
# - Sorted: quicksort never became faster in your tested range because
#          last-pivot quicksort hits worst-case and has recursion overhead.
#



