import random
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
    pivot = a[high]  # last element pivot
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


def run_experiment(sizes, tasks=100):
    """
    For each n:
      - start from a base array of size n
      - for each task: reshuffle the array, search for a constant element
    """
    lin_times = []
    sortbin_times = []

    for n in sizes:
        base = list(range(n))
        target = n // 2  # constant element that is guaranteed to exist

        t_lin = 0.0
        t_sortbin = 0.0

        for _ in range(tasks):
            random.shuffle(base)  # reshuffle every time (per lab requirement)
            t_lin += time_one(lambda a, x: linear_search(a, x), base, target)
            t_sortbin += time_one(lambda a, x: sort_then_binary_search(a, x), base, target)

        lin_times.append(t_lin / tasks)
        sortbin_times.append(t_sortbin / tasks)

    return lin_times, sortbin_times


def plot_results(sizes, lin_times, sortbin_times, title):
    plt.plot(sizes, lin_times, "o-", label="Linear search")
    plt.plot(sizes, sortbin_times, "o-", label="Quicksort + binary search")
    plt.xlabel("Input size (n)")
    plt.ylabel("Avg time per task (seconds)")
    plt.title(title)
    plt.legend()
    plt.xscale("log")  # helps readability across huge n range
    plt.show()


if __name__ == "__main__":
    sizes = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
    lin_times, sortbin_times = run_experiment(sizes, tasks=100)
    plot_results(sizes, lin_times, sortbin_times, "Exercise 6 (Average-ish case)")

    """
    Discussion (put your answer here as comments):
    - For small n, linear search is often faster because sorting costs a lot.
    - As n grows, quicksort+binary may still lose if you sort every single time.
    - In THIS setup, because the array is reshuffled each task, you re-pay the sort cost each task.
      That usually makes linear search win for most sizes, unless you reuse the sorted array.
    """