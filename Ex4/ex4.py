# Worst case time complexity happens when largest or smalled element is always
# chosen as pivot in that case Results in the sub array result in a size 0 and 
# size n-1 so the worst case becomes O(n^2)

# say we have the follwing array 

array_example = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

# then using the quicksort algoithm assuming we always chose the pivot to be the
# element we get the worst time complexity 

import time
import statistics
import sys
import numpy as np
import matplotlib.pyplot as plt
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


def time_quicksort_on_sorted(n, repeats=7):
    base = list(range(1, n + 1))  # ascending worst-case input
    times = []
    for _ in range(repeats):
        arr = base[:]  
        t0 = time.perf_counter()
        quicksort(arr)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return statistics.median(times)

start_n = 16
max_n = 2000     
step = 1         

sizes = list(range(start_n, max_n + 1, step))

sys.setrecursionlimit(max_n + 1000)

times = []
for n in sizes:
    t = time_quicksort_on_sorted(n, repeats=5) 
    times.append(t)
    if n % 100 == 0:
        print(f"n={n}  time={t:.6f}s")

sizes_np = np.array(sizes, dtype=float)
times_np = np.array(times, dtype=float)

def fit_constant(f, y):
    return float(np.dot(f, y) / np.dot(f, f))

nlogn = sizes_np * np.log2(sizes_np)

c_n2 = fit_constant(sizes_np**2, times_np)
c_nlogn = fit_constant(nlogn, times_np)

fit_n2 = c_n2 * (sizes_np**2)
fit_nlogn = c_nlogn * nlogn

print("Fit constants:")
print("  time ≈ c*n^2      c =", c_n2)
print("  time ≈ c*n*log2 n c =", c_nlogn)


plt.figure()
plt.plot(sizes_np, times_np, marker="o", markersize=2, label="Measured worst-case time (sorted input)")
plt.plot(sizes_np, fit_n2, label="Best fit: c·n²")
plt.plot(sizes_np, fit_nlogn, label="Best fit: c·n·log₂(n)")
plt.xlabel("Input size (n)")
plt.ylabel("Time (seconds)")
plt.title("Quicksort worst-case timing (last-element pivot, sorted input)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# Results match complexity analysis- can see if program ids run a parabolic graph is produced