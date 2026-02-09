import random
import matplotlib.pyplot as plt
import numpy as np

# 1. Complexity Analysis Formulas:
# For bubble sort on n elements:
# (i) Number of comparisons: Always n*(n-1)/2 (regardless of input order)
# (ii) Average-case number of swaps: n*(n-1)/4 (for randomly ordered input)


#4 The number of comparisons matches the theoretical formula n(n-1)/2 for all input sizes. It shows that the bubble sort always does the same 
# amount of comparisons despite the input order. However the swap counts are close but not identical to the theoretical predictions. 
# The statistical version was the most accurate to an average case because we used a randomly filled array.

def bubble_sort_with_counts(arr):
    """Bubble sort that counts comparisons and swaps"""
    n = len(arr)
    comparisons = 0
    swaps = 0
    
    arr_copy = arr.copy()
    
    for i in range(n):
        for j in range(0, n-i-1):
            comparisons += 1
            if arr_copy[j] > arr_copy[j+1]:
                arr_copy[j], arr_copy[j+1] = arr_copy[j+1], arr_copy[j]
                swaps += 1
    
    return arr_copy, comparisons, swaps

def run_experiments():
    """Run bubble sort on inputs of increasing size"""
    sizes = [10, 20, 30, 40, 50, 75, 100, 150, 200]
    results = []
    
    for n in sizes:
        arr = [random.randint(1, 1000) for _ in range(n)]
        
        sorted_arr, comparisons, swaps = bubble_sort_with_counts(arr)
        
        results.append({
            'n': n,
            'comparisons': comparisons,
            'swaps': swaps
        })
        
        print(f"n={n}: comparisons={comparisons}, swaps={swaps}")
    
    return results

def plot_results(results):
    """Plot comparison and swap counts"""
    n_values = [r['n'] for r in results]
    comparisons = [r['comparisons'] for r in results]
    swaps = [r['swaps'] for r in results]
    
    theoretical_comparisons = [n*(n-1)/2 for n in n_values]
    theoretical_swaps = [n*(n-1)/4 for n in n_values]  
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    ax1.plot(n_values, comparisons, 'bo-', label='Actual comparisons', linewidth=2)
    ax1.plot(n_values, theoretical_comparisons, 'r--', label='Theoretical n(n-1)/2', linewidth=2)
    ax1.set_xlabel('Input size (n)')
    ax1.set_ylabel('Number of comparisons')
    ax1.set_title('Bubble Sort: Comparisons vs Input Size')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(n_values, swaps, 'go-', label='Actual swaps', linewidth=2)
    ax2.plot(n_values, theoretical_swaps, 'r--', label='Theoretical n(n-1)/4', linewidth=2)
    ax2.set_xlabel('Input size (n)')
    ax2.set_ylabel('Number of swaps')
    ax2.set_title('Bubble Sort: Swaps vs Input Size (Average Case)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print("\n=== Complexity Analysis ===")
    print("1. Comparisons formula: n*(n-1)/2")
    print("   - Each pass compares adjacent pairs")
    print("   - First pass: n-1 comparisons")
    print("   - Second pass: n-2 comparisons")
    print("   - Total: (n-1) + (n-2) + ... + 1 = n*(n-1)/2")
    print()
    print("2. Average-case swaps formula: n*(n-1)/4")
    print("   - Probability that two random elements are out of order: 0.5")
    print("   - Each comparison has 50% chance of requiring a swap")
    print("   - Average swaps = 0.5 * comparisons = n*(n-1)/4")

if __name__ == "__main__":
    print("Running bubble sort complexity analysis...\n")
    
    results = run_experiments()
    
    plot_results(results)
    
    print("\n=== Verification ===")
    for r in results:
        n = r['n']
        actual_comparisons = r['comparisons']
        actual_swaps = r['swaps']
        theoretical_comparisons = n*(n-1)/2
        theoretical_swaps = n*(n-1)/4
        
        print(f"n={n}:")
        print(f"  Comparisons: actual={actual_comparisons}, theoretical={theoretical_comparisons:.0f}")
        print(f"  Swaps: actual={actual_swaps}, theoretical={theoretical_swaps:.0f}")
        print(f"  Swaps ratio: {actual_swaps/theoretical_swaps:.2f} (expected ~1.0)")