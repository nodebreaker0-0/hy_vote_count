import json
import numpy as np

# Attempting to load JSON lines as separate JSON objects
data_entries = []

with open("/data/hl/data/node_logs/status/hourly/20241203/3", 'r', encoding='utf-8') as file:
    for line in file:
        try:
            data_entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue

# Extracting data for the specific validator
validator_address = "0xef22f260eec3b7d1edebe53359f5ca584c18d5ac"
since_last_success_values = []
last_ack_duration_values = []

for entry in data_entries:
    if isinstance(entry, list) and len(entry) == 2 and isinstance(entry[1], dict):
        heartbeat_statuses = entry[1].get("heartbeat_statuses", [])
        for validator, status in heartbeat_statuses:
            if validator == validator_address:
                since_last_success_values.append(status.get("since_last_success"))
                last_ack_duration = status.get("last_ack_duration")
                if last_ack_duration is not None:
                    last_ack_duration_values.append(last_ack_duration)

# Calculate statistics for since_last_success
since_last_success_avg = np.mean(since_last_success_values) if since_last_success_values else None
since_last_success_min = np.min(since_last_success_values) if since_last_success_values else None
since_last_success_max = np.max(since_last_success_values) if since_last_success_values else None

# Calculate statistics for last_ack_duration
last_ack_duration_avg = np.mean(last_ack_duration_values) if last_ack_duration_values else None
last_ack_duration_min = np.min(last_ack_duration_values) if last_ack_duration_values else None
last_ack_duration_max = np.max(last_ack_duration_values) if last_ack_duration_values else None

print(since_last_success_avg, since_last_success_min, since_last_success_max,
 last_ack_duration_avg, last_ack_duration_min, last_ack_duration_max)