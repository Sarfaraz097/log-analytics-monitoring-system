import re
import json
from datetime import datetime

# Read the log_mapping.json config file
def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

# Read log file and convert each line into clean data
def parse_log_file(log_path, config):

    # Each log line looks like this:
    # 2026-04-01 00:00:00 ERROR [DBService] Payment failed
    pattern = re.compile(
        r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+'  # timestamp
        r'(\w+)\s+'                                      # level (ERROR/WARN etc)
        r'\[([^\]]+)\]\s+'                               # component [DBService]
        r'(.+)$'                                         # message (rest of line)
    )

    parsed_logs = []  # empty list, will store all parsed lines

    with open(log_path, 'r') as f:
        for line in f:
            line = line.strip()  # remove spaces and newlines

            if not line:
                continue  # skip empty lines

            # Try to match the line with our pattern
            match = pattern.match(line)
            if not match:
                continue  # skip lines that don't match

            # Extract 4 parts from the matched line
            timestamp_str, level, component, message = match.groups()

            # Convert timestamp string to datetime object
            try:
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                continue  # skip if timestamp format is wrong

            # Extract key=value pairs from message
            # Example: "Payment failed orderId=O462 reason=INSUFFICIENT_FUNDS"
            # Result:  {"orderId": "O462", "reason": "INSUFFICIENT_FUNDS"}
            kv_data = {}
            if config.get('kv_extraction', False):
                kv_pairs = re.findall(r'(\w+)=(\S+)', message)
                for key, value in kv_pairs:
                    kv_data[key] = value

            # Store clean data as a dictionary
            parsed_logs.append({
                'timestamp': timestamp,   # datetime object
                'level': level,           # "ERROR"
                'component': component,   # "DBService"
                'message': message,       # "Payment failed..."
                'kv': kv_data            # {"orderId": "O462"}
            })

    # Return list of all parsed log entries
    return parsed_logs