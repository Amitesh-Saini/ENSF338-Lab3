import json
import time
import random
import matplotlib.pyplot as plt



def binary_search_first_mid(arr, target, first_mid_index):
    """
    Returns True/False. First iteration uses first_mid_index as the midpoint.
    All later iterations use standard midpoint splitting.
    """
    n = len(arr)
    if n == 0:
        return False

    # clamp the first mid into range
    mid = max(0, min(n - 1, first_mid_index))

    lo, hi = 0, n - 1

    # first probe
    if arr[mid] == target:
        return True
    elif arr[mid] < target:
        lo = mid + 1
    else:
        hi = mid - 1

    # standard binary search after the first step
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return True
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return False


def time_search(arr, target, first_mid_index, repeats=30):
    """
    Times the same search multiple times and returns the best (min) time.
    Using min helps reduce noise from OS scheduling.
    """
    best = float("inf")
    for _ in range(repeats):
        t0 = time.perf_counter()
        binary_search_first_mid(arr, target, first_mid_index)
        t1 = time.perf_counter()
        best = min(best, t1 - t0)
    return best


def candidate_midpoints(n, k=25):
    """
    Picks a set of candidate first-midpoints to test.
    Strategy: evenly spaced indices across the array + a few important points.
    """
    if n <= 1:
        return [0]

    cands = set()

    # evenly spaced
    for i in range(k):
        idx = int(i * (n - 1) / (k - 1))
        cands.add(idx)

    # extra important points
    extras = [0, 1, n // 4, n // 2, (3 * n) // 4, n - 2, n - 1]
    for e in extras:
        if 0 <= e < n:
            cands.add(e)

    return sorted(cands)



def best_midpoint_for_task(arr, task_value):
    n = len(arr)
    cands = candidate_midpoints(n, k=25)

    best_idx = cands[0]
    best_time = float("inf")

    for idx in cands:
        t = time_search(arr, task_value, idx, repeats=20)
        if t < best_time:
            best_time = t
            best_idx = idx

    return best_idx, best_time

def main():
    # Load the lab files (put ex7data.json and ex7tasks.json in same folder)
    with open("ex7data.json", "r") as f:
        arr = json.load(f)

    with open("ex7tasks.json", "r") as f:
        tasks = json.load(f)


    arr.sort()

    chosen = []  # list of (task_value, best_midpoint_index)


    tasks = tasks.copy()
    random.shuffle(tasks)

    for x in tasks:
        best_idx, best_t = best_midpoint_for_task(arr, x)
        chosen.append((x, best_idx))


    xs = [p[0] for p in chosen]
    ys = [p[1] for p in chosen]

    plt.scatter(xs, ys, s=12)
    plt.xlabel("Task value (number being searched)")
    plt.ylabel("Chosen first midpoint index")
    plt.title("Exercise 7: Best first-midpoint by task value")
    plt.show()


    """
    Discussion:
    - If the array values are roughly uniformly distributed and tasks vary across the
      array range, you may see a trend: smaller task values prefer earlier midpoints,
      larger task values prefer later midpoints.
    - Why? The first midpoint acts like a 'guess' of where the value lies. If your first
      guess is closer to the true position, you reduce the number of iterations.
    - If you do NOT see a strong trend, it can be because:
        (1) the array is not uniformly distributed,
        (2) timing noise dominates because binary search is extremely fast,
        (3) many tasks are near the middle anyway,
        (4) Python overhead is larger than the algorithmic differences.
    """


if __name__ == "__main__":
    main()