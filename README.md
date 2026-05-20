# Universal Log Intelligence Engine

## What is this?
A Format-Agnostic Log Analytics Engine that parses any timestamped log file
and generates a System Health Intelligence Report via the command line.

## Folder Structure
log-engine/
├── exec/
│   ├── main.py           # Entry point - run this file
│   ├── parser.py         # Reads and parses log file
│   ├── analyzer.py       # Calculates KPIs and detects anomalies
│   └── reporter.py       # Prints report to CLI and saves markdown
├── config/
│   ├── log_mapping.json  # Log format configuration
│   └── requirements.txt  # Python dependencies
├── hackathon_logs.txt    # Sample log file
└── README.md
## Requirements
- Python 3.8+
- rich library

## Installation

### Step 1 - Create virtual environment
```bash
python -m venv venv
```

### Step 2 - Activate virtual environment
Windows:
```bash
venv\Scripts\activate
```

### Step 3 - Install dependencies
```bash
pip install rich
```

## How to Run
```bash
python exec/main.py --log hackathon_logs.txt --config config/log_mapping.json --output both
```

## Output Options
| Option | Description |
|--------|-------------|
| cli | Show report in terminal only |
| markdown | Save report.md file only |
| both | CLI + markdown both |

## Sample Output
Total Events     → 200,000
Error Rate       → 25.13%
Uptime Score     → 74.87%
Error Density    → 5.03 errors/min
Suspicious Users → 899
Unauthorized IPs → 6,631
## How Config Works
Edit `config/log_mapping.json` to support any log format.

Example log line:
2026-04-01 00:00:00 ERROR [DBService] Payment failed orderId=O462
Config maps each part:
- timestamp → `2026-04-01 00:00:00`
- level     → `ERROR`
- component → `DBService`
- message   → `Payment failed orderId=O462`

## Key Features
- Dynamic log parsing via JSON config — no hardcoded logic
- KPI extraction — error density, uptime score, error rate
- Top 5 failing components detection
- Failure nature breakdown — 15+ event categories
- Anomaly insights — cascading failures, security threats
- Markdown report export