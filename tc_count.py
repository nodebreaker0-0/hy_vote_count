import json
from collections import defaultdict

# Prompt user for the last part of the path (hour)
hour_input = input("Enter the hour (e.g., 12): ")

# Construct the file path dynamically
log_file_path_latest = f'/data/hl/data/node_logs/consensus/hourly/20241202/{hour_input}'

# Reading the new log file
try:
    with open(log_file_path_latest, 'r', encoding='utf-8') as file:
        log_data_latest = file.readlines()
except FileNotFoundError:
    print(f"File not found: {log_file_path_latest}")
    exit(1)

# Count occurrences of each proposer
tc_counts_latest = defaultdict(int)

for line in log_data_latest:
    try:
        log_entry = json.loads(line)
        msg = log_entry[1][1]["msg"]

        # Check if the message contains a Block with proposer
        if "Block" in msg and "tc" in msg["Block"]:
            tc = msg["Block"]["tc"]
            print(tc)
            #tc_counts_latest[tc] += 1
    except (json.JSONDecodeError, KeyError):
        # Skip invalid entries or those without relevant keys
        continue

# Sorting the proposers by their count
sorted_tc_counts_latest = sorted(tc_counts_latest.items(), key=lambda x: x[1], reverse=True)

# Printing the result in the format "proposer:count"
if sorted_proposer_counts_latest:
    for tc, count in sorted_tc_counts_latest:
        print(f"{tc}: {count}")
else:
    print("No proposers found in the provided log file.")