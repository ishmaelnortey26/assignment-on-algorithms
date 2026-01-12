def compute_statistics(numbers):
    """
    Computes statistics for a list of numbers:
    - Smallest (min)
    - Largest (max)
    - Mode
    - Median
    - 1st Quartile (Q1)
    - 3rd Quartile (Q3)
    """

    # Check that input is valid
    if numbers is None or len(numbers) == 0:
        raise ValueError("Input array must not be empty")

    # Step 1: Sort the numbers
    nums = sorted(numbers)
    length = len(nums)

    # Step 2: Smallest and largest values
    smallest = nums[0]
    largest = nums[length - 1]

    # Step 3: Function to calculate median
    def find_median(values):
        size = len(values)
        middle = size // 2

        if size % 2 == 1:
            return values[middle]
        else:
            return (values[middle - 1] + values[middle]) / 2

    median_value = find_median(nums)

    # Step 4: Split list for quartiles
    if length % 2 == 1:
        lower_half = nums[:length // 2]
        upper_half = nums[length // 2 + 1:]
    else:
        lower_half = nums[:length // 2]
        upper_half = nums[length // 2:]

    q1 = find_median(lower_half)
    q3 = find_median(upper_half)

    # Step 5: Find the mode
    frequency = {}

    for number in nums:
        if number in frequency:
            frequency[number] += 1
        else:
            frequency[number] = 1

    highest_frequency = 0
    for count in frequency.values():
        if count > highest_frequency:
            highest_frequency = count

    if highest_frequency == 1:
        mode = None
    else:
        mode = []
        for number in frequency:
            if frequency[number] == highest_frequency:
                mode.append(number)

    # Step 6: Return results
    return {
        "smallest": smallest,
        "largest": largest,
        "mode": mode,
        "median": median_value,
        "q1": q1,
        "q3": q3
    }
