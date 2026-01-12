def selection_sort(values, descending=False):
    """
    Sorts a list of values using the Selection Sort algorithm.

    Selection Sort works by repeatedly selecting the smallest
    (or largest, for descending order) element from the unsorted
    portion of the list and moving it to its correct position.

    Parameters:
    - values (iterable): A list or iterable of comparable values.
    - descending (bool): If False (default), sort in ascending order.
                          If True, sort in descending order.

    Returns:
    - list: A new list containing the sorted values.
    """

    # Make a copy so we don’t change the original list
    arr = list(values)
    length = len(arr)

    # Move through the list one position at a time
    for i in range(length):

        best_index = i  # Assume the current position is the best

        # Look for a better value in the rest of the list
        for j in range(i + 1, length):

            # Ascending order
            if descending == False:
                if arr[j] < arr[best_index]:
                    best_index = j

            # Descending order
            else:
                if arr[j] > arr[best_index]:
                    best_index = j

        # Swap the found best value with the current position
        temp = arr[i]
        arr[i] = arr[best_index]
        arr[best_index] = temp

    return arr