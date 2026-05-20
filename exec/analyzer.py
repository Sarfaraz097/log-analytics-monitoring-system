from collections import Counter
from datetime import datetime

# Categorize message into event type
def categorize(message):
    if 'Login failed' in message:        return 'Login Failure'
    if 'Login success' in message:       return 'Login Success'
    if 'Payment failed' in message:      return 'Payment Failure'
    if 'Stock mismatch' in message:      return 'Stock Mismatch'
    if 'Queue backlog' in message:       return 'Queue Backlog'
    if 'Request timeout' in message:     return 'Request Timeout'
    if 'Slow query' in message:          return 'Slow Query'
    if 'High CPU' in message:            return 'High CPU'
    if 'High memory' in message:         return 'High Memory'
    if 'Disk space low' in message:      return 'Disk Space Low'
    if 'Suspicious activity' in message: return 'Suspicious Activity'
    if 'Unauthorized access' in message: return 'Unauthorized Access'
    if 'Deadlock' in message:            return 'Deadlock'
    if 'Service restarted' in message:   return 'Service Restart'
    if 'Email sending failed' in message: return 'Email Failure'
    if 'Config missing' in message:      return 'Config Missing'
    if 'Third-party API' in message:     return 'Third-party API Failure'
    return 'Other'

# Main function - analyze all parsed logs
def analyze(parsed_logs):

    # Basic counters
    total         = len(parsed_logs)
    level_counts  = Counter()   # count per level (ERROR, WARN etc)
    comp_total    = Counter()   # count per component (total)
    comp_errors   = Counter()   # count per component (errors only)
    event_types   = Counter()   # count per event category
    suspicious_users  = set()   # unique suspicious user IDs
    unauthorized_ips  = set()   # unique unauthorized IPs

    # Get first and last timestamp for duration
    first_ts = parsed_logs[0]['timestamp']
    last_ts  = parsed_logs[-1]['timestamp']

    # Loop through every log entry
    for log in parsed_logs:
        level     = log['level']
        component = log['component']
        message   = log['message']
        kv        = log['kv']

        # Count levels
        level_counts[level] += 1

        # Count component total and errors
        comp_total[component] += 1
        if level == 'ERROR':
            comp_errors[component] += 1

        # Categorize event
        event_types[categorize(message)] += 1

        # Collect suspicious users
        if 'Suspicious activity' in message and 'userId' in kv:
            suspicious_users.add(kv['userId'])

        # Collect unauthorized IPs
        if 'Unauthorized access' in message and 'IP' in kv:
            unauthorized_ips.add(kv['IP'])

    # Calculate duration in minutes
    duration_minutes = (last_ts - first_ts).total_seconds() / 60

    # Calculate error density (errors per minute)
    error_count   = level_counts['ERROR']
    error_density = error_count / duration_minutes if duration_minutes > 0 else 0

    # Calculate uptime score
    error_pct    = (error_count / total) * 100
    uptime_score = 100 - error_pct

    # Top 5 failing components
    top5_components = comp_errors.most_common(5)

    # Return all results as a dictionary
    return {
        'total'            : total,
        'level_counts'     : dict(level_counts),
        'error_count'      : error_count,
        'error_density'    : round(error_density, 2),
        'uptime_score'     : round(uptime_score, 2),
        'error_pct'        : round(error_pct, 2),
        'top5_components'  : top5_components,
        'event_types'      : event_types.most_common(10),
        'suspicious_users' : len(suspicious_users),
        'unauthorized_ips' : len(unauthorized_ips),
        'duration_minutes' : round(duration_minutes, 1),
        'first_ts'         : first_ts,
        'last_ts'          : last_ts,
    }