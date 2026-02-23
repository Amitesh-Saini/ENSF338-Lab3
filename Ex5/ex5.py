import random
import time
import numpy as np
import matplotlib.pyplot as plt

def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def binary_search(a, key, low, high):
    while low < high:
        mid = (low + high) // 2
        if a[mid] < key:
            low = mid + 1
        else:
            high = mid
    return low


def binary_insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        pos = binary_search(a, key, 0, i)
        a[pos+1:i+1] = a[pos:i]
        a[pos] = key
    return a

def measure(sort_func, arr):
    start = time.perf_counter()
    sort_func(arr)
    end = time.perf_counter()
    return end - start

sizes = [10, 20, 50, 100, 200, 500, 1000]
runs = 20

ins_times = []
bin_ins_times = []

for n in sizes:
    t1 = 0
    t2 = 0
    for _ in range(runs):
        arr = random.sample(range(n*10), n)
        t1 += measure(insertion_sort, arr)
        t2 += measure(binary_insertion_sort, arr)

    ins_times.append(t1 / runs)
    bin_ins_times.append(t2 / runs)

plt.plot(sizes, ins_times, 'o-', label="Insertion Sort")
plt.plot(sizes, bin_ins_times, 'o-', label="Binary Insertion Sort")

# Interpolating curves
p1 = np.polyfit(sizes, ins_times, 2)
p2 = np.polyfit(sizes, bin_ins_times, 2)

plt.plot(sizes, np.polyval(p1, sizes), '--')
plt.plot(sizes, np.polyval(p2, sizes), '--')

plt.xlabel("Input size (n)")
plt.ylabel("Time (seconds)")
plt.legend()
plt.title("Insertion Sort vs Binary Insertion Sort")
plt.show()

"""
Discussion:
Binary insertion sort is consistently faster than traditional insertion sort
for larger inputs. This is because binary insertion sort reduces the number
of comparisons from O(n^2) to O(n log n).

However, both algorithms still require O(n^2) shifts in the worst and average
case, which is why the overall improvement is limited. The benefit comes
purely from fewer comparisons, not fewer moves.

This explains why Python’s Timsort uses binary insertion sort only on
small sub-arrays.
"""

