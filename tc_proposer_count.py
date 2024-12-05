import json
from collections import defaultdict

# Create a file path with user input
date_input = input("Enter the date (e.g., 20241204): ")
hour_input = input("Enter the hour (e.g., 12): ")
log_file_path_latest = f'/data/hl/data/node_logs/consensus/hourly/{date_input}/{hour_input}'

# Read the log file
try:
    with open(log_file_path_latest, 'r', encoding='utf-8') as file:
        log_data_latest = file.readlines()
except FileNotFoundError:
    print(f"File not found: {log_file_path_latest}")
    exit(1)

# initialize TC block count per proposer
proposer_tc_counts = defaultdict(int)

# Process log files
for line in log_data_latest:
    try:
        # JSON Parsing
        log_entry = json.loads(line)
        msg = log_entry[1][1]["msg"]

        # Check “Block” and “proposer”
        if "Block" in msg and "proposer" in msg["Block"]:
            proposer = msg["Block"]["proposer"]

            # increment the count of the corresponding proposer if “tc” exists
            if "tc" in msg["Block"] and msg["Block"]["tc"] is not None:
                proposer_tc_counts[proposer] += 1
    except (json.JSONDecodeError, KeyError):
        # Ignore JSON errors or missing keys
        continue

# Sort and print the results
if proposer_tc_counts:
    sorted_tc_counts = sorted(proposer_tc_counts.items(), key=lambda x: x[1], reverse=True)
    print("Proposer : TC Block Count")
    for proposer, count in sorted_tc_counts:
        print(f"{proposer} : {count}")
else:
    print("No proposers with TC blocks found in the provided log file.")