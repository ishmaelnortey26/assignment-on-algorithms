def merge_sort(values, descending=False):
    """
    Merge Sort (Divide & Conquer)

    - values: list of numbers
    - descending: if True, sort high -> low
    Returns a NEW sorted list (does not mutate original).
    """
    if values is None:
        raise ValueError("values cannot be None")

        # Base case: if the list has 0 or 1 element, it is already sorted
    if len(values) <= 1:
        return list(values)  # return a copy

        # Split the list into two halves
    middle = len(values) // 2
    left_half = values[:middle]
    right_half = values[middle:]

    # Recursively sort both halves
    sorted_left = merge_sort(left_half, descending)
    sorted_right = merge_sort(right_half, descending)

    # Merge the two sorted halves
    return merge(sorted_left, sorted_right, descending)


def merge(left, right, descending):
    merged = []  # this will hold the final sorted list

    left_index = 0
    right_index = 0

    # Compare elements from both lists
    while left_index < len(left) and right_index < len(right):

        # Ascending order
        if descending == False:
            if left[left_index] <= right[right_index]:
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1

        # Descending order
        else:
            if left[left_index] >= right[right_index]:
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1

    # Add remaining elements from left list (if any)
    while left_index < len(left):
        merged.append(left[left_index])
        left_index += 1

    # Add remaining elements from right list (if any)
    while right_index < len(right):
        merged.append(right[right_index])
        right_index += 1

    return merged
