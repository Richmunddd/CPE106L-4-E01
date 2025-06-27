def mean(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def median(numbers):
    if not numbers:
        return 0
    sorted_nums = sorted(numbers)
    midpoint = len(sorted_nums) // 2
    if len(sorted_nums)%2 ==1:
        return sorted_nums[midpoint]
    else:
        return (sorted_nums[midpoint] + sorted_nums[midpoint -1]) /2
    
def mode(numbers):
    if not numbers:
        return 0
    freq = {}
    for num in numbers:
        freq[num] = freq.get(num,0) + 1
        max_count = max(freq.values())
        for key in freq:
            if freq[key] == max_count:
                return key

def main():
    filename = input("Input the file name: ")
    try:
        with open(filename, 'r') as f:
            numbers = []
            for line in f:
                for word in line.split():
                    try:
                        numbers.append(float(word))
                    except ValueError:
                        continue

        print("Mean: ",mean(numbers))
        print("Median: ",median(numbers))
        print("Mode: ",mode(numbers))

    except FileNotFoundError:
        print("File not found.")

if __name__ == "__main__":
    main()