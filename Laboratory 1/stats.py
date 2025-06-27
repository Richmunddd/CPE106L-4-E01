def mean(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def median(numbers):
    if not numbers:
        return 0
    sorted_nums = sorted(numbers)
    midpoint = len(sorted_nums) // 2
    if len(sorted_nums) % 2 == 1:
        return sorted_nums[midpoint]
    else:
        return (sorted_nums[midpoint] + sorted_nums[midpoint - 1]) / 2

def mode(numbers):
    if not numbers:
        return 0
    freq = {}
    for num in numbers:
        freq[num] = freq.get(num, 0) + 1
    max_count = max(freq.values())
    modes = [key for key, count in freq.items() if count == max_count]
    return modes[0] if modes else 0  # Return the first mode

def main():
    try:
        user_input = input("Enter numbers separated by spaces: ")
        numbers = [float(x) for x in user_input.split()]

        print("Mean: ", mean(numbers))
        print("Median: ", median(numbers))
        print("Mode: ", mode(numbers))

    except ValueError:
        print("Invalid input. Please enter numeric values only.")

if __name__ == "__main__":
    main()
