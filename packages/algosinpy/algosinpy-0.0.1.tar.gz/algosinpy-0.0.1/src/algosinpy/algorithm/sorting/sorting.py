from src.algosinpy.logger.py_logger import PyLogger

logger = PyLogger.get_configured_logger()


"""
Bubble Sort
"""

def check_list_of_number(list_of_number):
    if not isinstance(list_of_number, list):
        raise TypeError("Input must be a list of numbers.")
    if not all(isinstance(x, (int, float)) for x in list_of_number):
        raise ValueError("All elements in the list must be numbers.")
    

def bubble_sort(list_of_number):
    """Sorts a list of numbers using the bubble sort algorithm.
    Args:
        list_of_number (list): A list of numbers to be sorted.
    Returns:
        list: The sorted list of numbers.
    """
    check_list_of_number(list_of_number)
    list_len = len(list_of_number)

    for i in range(list_len - 1):
        for j in range(list_len - 1 - i):
            if list_of_number[j] > list_of_number[j + 1]:
                list_of_number[j], list_of_number[j + 1] = (
                    list_of_number[j + 1],
                    list_of_number[j],
                )

    return list_of_number


"""
Selection Sort
"""


def selection_sort(list_of_number):
    """Sorts a list of numbers using the selection sort algorithm.
    Args:
        list_of_number (list): A list of numbers to be sorted.
    Returns:
        list: The sorted list of numbers.
    """
    check_list_of_number(list_of_number)

    for i in range(len(list_of_number)):
        min_index = i

        for j in range(i, len(list_of_number)):
            if list_of_number[min_index] > list_of_number[j]:
                min_index = j

        list_of_number[i], list_of_number[min_index] = (
            list_of_number[min_index],
            list_of_number[i],
        )

    return list_of_number


"""
Insertion Sort
"""


def insertion_sort(list_of_number):
    """Sorts a list of numbers using the insertion sort algorithm.
    Args:
        list_of_number (list): A list of numbers to be sorted.
    Returns:
        list: The sorted list of numbers.
    """
    check_list_of_number(list_of_number)

    for i in range(1, len(list_of_number)):

        key = list_of_number[i]
        j = i - 1

        while j >= 0 and key < list_of_number[j]:
            list_of_number[j + 1] = list_of_number[j]
            j -= 1

        list_of_number[j + 1] = key
    logger.info(list_of_number)
    return list_of_number


"""
Quick Sort
"""


def partition(array, low, high):
    i = low - 1
    pivot = array[high]

    for j in range(low, high):
        if array[j] <= pivot:
            array[i + 1], array[j] = array[j], array[i + 1]
            i += 1
    array[i + 1], array[high] = array[high], array[i + 1]

    return i + 1


def quick_sort(array, low, high):
    """Sorts a list of numbers using the quick sort algorithm.
    Args:
        array (list): A list of numbers to be sorted.
        low (int): The starting index of the list.
        high (int): The ending index of the list.
    Returns:
        list: The sorted list of numbers.
    """
    check_list_of_number(array)
    # base case low < high
    if low < high:

        p = partition(array, low, high)

        quick_sort(array, low, p - 1)
        quick_sort(array, p + 1, high)
    return array


"""
Merge Sort
"""


def merge(array, l, m, r):
    len_1 = m - l + 1
    len_2 = r - m

    # create two arrary for two parts
    left = []
    right = []
    # copy array between two parts
    for i in range(0, len_1):
        left.append(array[l + i])

    for j in range(0, len_2):
        right.append(array[m + 1 + j])

    i = 0
    j = 0
    k = l
    # comparing two parts
    while i < len_1 or j < len_2:

        if i == len_1:  # inserting remaining part
            array[k] = right[j]
            j += 1

        elif j == len_2:  # inserting remaining part
            array[k] = left[i]
            i += 1

        elif left[i] <= right[j]:
            array[k] = left[i]
            i += 1

        elif left[i] >= right[j]:
            array[k] = right[j]
            j += 1
        k += 1
    return array


def merge_sort(array, l, r):
    """Sorts a list of numbers using the merge sort algorithm.
    Args:
        array (list): A list of numbers to be sorted.
        l (int): The starting index of the list.
        r (int): The ending index of the list.
    Returns:
        list: The sorted list of numbers.
    """
    check_list_of_number(array)
    if l < r:

        # Same as (l+r)//2, but avoids overflow for
        # large l and h
        m = (l + (r - 1)) // 2

        # Sort first and second halves
        merge_sort(array, l, m)
        merge_sort(array, m + 1, r)
        merge(array, l, m, r)
    return array


"""
Counting sort: 

For simplicity, consider the data in the range 0 to 9. 
Input data: 1, 4, 1, 2, 7, 5, 2
  1) Take a count array to store the count of each unique object.
  Index:     0  1  2  3  4  5  6  7  8  9
  Count:     0  2  2  0   1  1  0  1  0  0

  2) Modify the count array such that each element at each index 
  stores the sum of previous counts. 
  Index:     0  1  2  3  4  5  6  7  8  9
  Count:     0  2  4  4  5  6  6  7  7  7

The modified count array indicates the position of each object in 
the output sequence.
 
  3) Output each object from the input sequence followed by 
  decreasing its count by 1.
  Process the input data: 1, 4, 1, 2, 7, 5, 2. Position of 1 is 2.
  Put data 1 at index 2 in output. Decrease count by 1 to place 
  next data 1 at an index 1 smaller than this index.
"""

# The algosinpy function that sort the given string arr[] in
# alphabetical order
def countSort(arr):
    """Sorts a list of characters using the counting sort algorithm.
    Args:
        arr (list): A list of characters to be sorted.
    Returns:
        list: The sorted list of characters.
    """
    # print(arr)
    # The output character array that will have sorted arr
    output = [0 for i in range(256)]

    # Create a count array to store count of inidividul
    # characters and initialize count array as 0
    count = [0 for i in range(256)]
    # For storing the resulting answer since the
    # string is immutable
    ans = ["" for _ in arr]
    # Store count of each character
    for i in arr:
        count[ord(i)] += 1

    # Change count[i] so that count[i] now contains actual
    # position of this character in output array
    for i in range(256):
        count[i] += count[i - 1]

    # Build the output character array
    for i in range(len(arr)):
        output[count[ord(arr[i])] - 1] = arr[i]
        count[ord(arr[i])] -= 1

    # Copy the output array to arr, so that arr now
    # contains sorted characters
    for i in range(len(arr)):
        ans[i] = output[i]
    return ans


"""
Radix Sort = counting Sort + radix

The idea of Radix Sort is to do digit by digit sort starting from least significant digit to most significant digit.
Radix sort uses counting sort as a subroutine to sort.
"""


# Python program for implementation of Radix Sort

# A function to do counting sort of arr[] according to
# the digit represented by exp.
def countingSort(arr, exp1):

    n = len(arr)

    # The output array elements that will have sorted arr
    output = [0] * (n)

    # initialize count array as 0
    count = [0] * (10)

    # Store count of occurrences in count[]
    for i in range(0, n):
        index = int(arr[i] / exp1)
        count[(index) % 10] += 1

    # Change count[i] so that count[i] now contains actual
    #  position of this digit in output array
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build the output array
    i = n - 1
    while i >= 0:
        index = int(arr[i] / exp1)

        output[count[(index) % 10] - 1] = arr[i]
        count[(index) % 10] -= 1
        i -= 1
    # Copying the output array to arr[],
    # so that arr now contains sorted numbers
    i = 0
    for i in range(0, len(arr)):
        arr[i] = output[i]
    # return arr


# Method to do Radix Sort
def radixSort(arr):
    """Sorts a list of numbers using the radix sort algorithm.
    Args:
        arr (list): A list of numbers to be sorted.
    Returns:
        list: The sorted list of numbers.
    """
    check_list_of_number(arr)

    # Find the maximum number to know number of digits
    max1 = max(arr)

    # Do counting sort for every digit. Note that instead
    # of passing digit number, exp is passed. exp is 10^i
    # where i is current digit number
    exp = 1
    while (max1 // exp) > 0:
        countingSort(arr, exp)
        exp *= 10
    return arr


"""
Bucket Sort = insertion + bucket

bucketSort(arr[], n)
1) Create n empty buckets (Or lists).
2) Do following for every array element arr[i].
.......a) Insert arr[i] into bucket[n*array[i]]
3) Sort individual buckets using insertion sort.
4) Concatenate all sorted buckets.
"""


def insertionSort(b):
    for i in range(1, len(b)):
        up = b[i]
        j = i - 1
        while j >= 0 and b[j] > up:
            b[j + 1] = b[j]
            j -= 1
        b[j + 1] = up
    return b


def bucketSort(x):
    """Sorts a list of numbers using the bucket sort algorithm.
    Args:
        x (list): A list of numbers to be sorted.
    Returns:
        list: The sorted list of numbers.
    """
    check_list_of_number(x)
    arr = []
    slot_num = 10  # 10 means 10 slots, each
    # slot's size is 0.1
    for i in range(slot_num):
        arr.append([])

    # Put array elements in different buckets
    for j in x:
        index_b = int(slot_num * j)
        arr[index_b].append(j)
    # Sort individual buckets
    for i in range(slot_num):
        arr[i] = insertion_sort(arr[i])
        #arr[i] = insertionSort(arr[i])

    # concatenate the result
    k = 0
    for i in range(slot_num):
        for j in range(len(arr[i])):
            x[k] = arr[i][j]
            k += 1
    return x
