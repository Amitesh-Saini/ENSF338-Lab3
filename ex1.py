import random
import numpy as np

def merge_sort(arr, low, high):
    if low < high:
        mid = (low + high) // 2
        merge_sort(arr, low, mid)
        merge_sort(arr, mid + 1, high)
        merge(arr, low, mid, high)  

def merge(arr, low, mid, high):
    left_size = mid - low + 1
    right_size = high - mid
    
    left_arr = arr[low:mid+1]
    right_arr = arr[mid+1:high+1]
    
    i = j = 0  
    k = low   
    
    while i < left_size and j < right_size:
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    while i < left_size:
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    while j < right_size:
        arr[k] = right_arr[j]
        j += 1
        k += 1

def test_merge_sort():
    arr = [38, 27, 43, 3, 9, 82, 10]
    print(f"Original array: {arr}")
    merge_sort(arr, 0, len(arr) - 1)
    print(f"Sorted array: {arr}")
    
    test_arr = [random.randint(1, 100) for _ in range(10)]
    print(f"\nRandom array: {test_arr}")
    merge_sort(test_arr, 0, len(test_arr) - 1)
    print(f"Sorted array: {test_arr}")

if __name__ == "__main__":
    test_merge_sort()