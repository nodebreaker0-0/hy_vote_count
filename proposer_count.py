import json
from collections import defaultdict

date_input = input("Enter the date (e.g. 20241204)")
# Prompt user for the last part of the path (hour)
hour_input = input("Enter the hour (e.g., 12): ")

# Construct the file path dynamically
log_file_path_latest = f'/data/hl/data/node_logs/consensus/hourly/{date_input}/{hour_input}'


# Reading the new log file
try:
    with open(log_file_path_latest, 'r', encoding='utf-8') as file:
        log_data_latest = file.readlines()
except FileNotFoundError:
    print(f"File not found: {log_file_path_latest}")
    exit(1)

# Count occurrences of each proposer
proposer_counts_latest = defaultdict(int)

for line in log_data_latest:
    try:
        log_entry = json.loads(line)
        msg = log_entry[1][1]["msg"]

        # Check if the message contains a Block with proposer
        if "Block" in msg and "proposer" in msg["Block"]:
            proposer = msg["Block"]["proposer"]
            proposer_counts_latest[proposer] += 1
    except (json.JSONDecodeError, KeyError):
        # Skip invalid entries or those without relevant keys
        continue

# Sorting the proposers by their count
sorted_proposer_counts_latest = sorted(proposer_counts_latest.items(), key=lambda x: x[1], reverse=True)

# Printing the result in the format "proposer:count"
if sorted_proposer_counts_latest:
    for proposer, count in sorted_proposer_counts_latest:
        print(f"{proposer}: {count}")
else:
    print("No proposers found in the provided log file.")