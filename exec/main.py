import argparse
import os
import sys

# Add exec folder to path
sys.path.append(os.path.dirname(__file__))

from parser import parse_log_file, load_config
from analyzer import analyze
from reporter import print_report, save_markdown

def main():

    # Setup command line arguments
    parser = argparse.ArgumentParser(
        description='Universal Log Intelligence Engine'
    )

    parser.add_argument(
        '--log',
        required=True,
        help='Path to log file (e.g. hackathon_logs.txt)'
    )

    parser.add_argument(
        '--config',
        required=True,
        help='Path to config file (e.g. config/log_mapping.json)'
    )

    parser.add_argument(
        '--output',
        default='markdown',
        choices=['cli', 'markdown', 'both'],
        help='Output format: cli, markdown, or both (default: markdown)'
    )

    args = parser.parse_args()

    # Check if log file exists
    if not os.path.exists(args.log):
        print(f"Error: Log file not found → {args.log}")
        sys.exit(1)

    # Check if config file exists
    if not os.path.exists(args.config):
        print(f"Error: Config file not found → {args.config}")
        sys.exit(1)

    # Step 1 - Load config
    print("Loading config...")
    config = load_config(args.config)

    # Step 2 - Parse log file
    print("Parsing log file... (this may take a few seconds)")
    parsed_logs = parse_log_file(args.log, config)
    print(f"Parsed {len(parsed_logs)} log entries successfully!")

    # Step 3 - Analyze
    print("Analyzing...")
    results = analyze(parsed_logs)

    # Step 4 - Output report
    if args.output == 'cli':
        print_report(results)

    elif args.output == 'markdown':
        print_report(results)
        save_markdown(results, 'report.md')

    elif args.output == 'both':
        print_report(results)
        save_markdown(results, 'report.md')

if __name__ == '__main__':
    main()