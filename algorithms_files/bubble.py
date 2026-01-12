def bubble_sort(values, descending=False):
    """
    Sorts a list of values using the Bubble Sort algorithm.

    Bubble Sort works by repeatedly stepping through the list,
    comparing adjacent elements, and swapping them if they are
    in the wrong order. This process is repeated until the list
    is fully sorted.

    Parameters:
    - values (iterable): A list or iterable of comparable values.
    - descending (bool): If False (default), sort in ascending order.
                          If True, sort in descending order.

    Returns:
    - list: A new list containing the sorted values.
    """
    # Create a copy of the input so the original list is not modified
    arr = list(values)
    length = len(arr)

    for i in range(length):
        swapped = False
        # Inner loop compares adjacent elements
        # The last i elements are already in correct position
        # Compare each pair of adjacent elements
        for j in range(length - 1):

            # Ascending order
            if descending == False:
                if arr[j] > arr[j + 1]:
                    temp = arr[j]
                    arr[j] = arr[j + 1]
                    arr[j + 1] = temp
                    swapped = True

            # Descending order
            else:
                if arr[j] < arr[j + 1]:
                    temp = arr[j]
                    arr[j] = arr[j + 1]
                    arr[j + 1] = temp
                    swapped = True

        # If no swaps happened, the list is already sorted
        if swapped == False:
            break

    return arr