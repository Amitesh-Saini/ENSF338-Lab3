import time
import matplotlib.pyplot as plt



def linear_search(arr, target):
    for v in arr:
        if v == target:
            return True
    return False


def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return True
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False




def partition(a, low, high):
    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[high] = a[high], a[i + 1]
    return i + 1


def quicksort(a, low=0, high=None):
    if high is None:
        high = len(a) - 1
    if low < high:
        p = partition(a, low, high)
        quicksort(a, low, p - 1)
        quicksort(a, p + 1, high)


def sort_then_binary_search(arr, target):
    a = arr.copy()
    quicksort(a)
    return binary_search(a, target)


def time_one(fn, arr, target):
    t0 = time.perf_counter()
    fn(arr, target)
    t1 = time.perf_counter()
    return t1 - t0


def run_worst_case(sizes, tasks=100):
    """
    Worst-case setup:
      - Each task uses a sorted array (already sorted)
      - With last-element pivot quicksort, that yields worst-case behavior
    """
    lin_times = []
    sortbin_times = []

    for n in sizes:
        target = n // 2
        t_lin = 0.0
        t_sortbin = 0.0

        for _ in range(tasks):
            arr = list(range(n))  # sorted every time -> worst-case for this quicksort
            t_lin += time_one(linear_search, arr, target)
            t_sortbin += time_one(sort_then_binary_search, arr, target)

        lin_times.append(t_lin / tasks)
        sortbin_times.append(t_sortbin / tasks)

    return lin_times, sortbin_times


def plot_results(sizes, lin_times, sortbin_times, title):
    plt.plot(sizes, lin_times, "o-", label="Linear search")
    plt.plot(sizes, sortbin_times, "o-", label="Worst-case quicksort + binary search")
    plt.xlabel("Input size (n)")
    plt.ylabel("Avg time per task (seconds)")
    plt.title(title)
    plt.legend()
    plt.xscale("log")
    plt.show()


if __name__ == "__main__":
    sizes = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
    lin_times, sortbin_times = run_worst_case(sizes, tasks=100)
    plot_results(sizes, lin_times, sortbin_times, "Exercise 6 (Worst-case quicksort)")

    """
    Discussion (comments):
    - Linear search cost ~ O(n)
    - Quicksort here becomes O(n^2) due to sorted input + last-element pivot
    - So "sort then binary search" becomes dramatically slower as n grows
    """