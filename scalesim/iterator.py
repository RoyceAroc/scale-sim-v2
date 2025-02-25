import csv

arr = []

with open('output.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    idx = -1
    for row in csv_reader:
        idx = idx + 1
        config = eval(row[0])
        output = eval(row[1])

        area = (525 * config[0] * config[1]) + (1015.7 * (config[2]*1024 + config[2]*1024*2 + config[3]*1024 + config[3]*1024*2))
        
        total_cycles = 0

        for stage in output:
            total_cycles += int(stage[0])

      
        score = (17500 / total_cycles) + (15000 / area)

        arr.append((idx, score, config))


# Sort the array by score in descending order
arr_sorted = sorted(arr, key=lambda x: x[1], reverse=True)
arr_sorted = arr_sorted[:10]
# Print the sorted array
for item in arr_sorted:
    print(f"Index: {item[0]}, Score: {item[1]}, Config {item[2]}")
