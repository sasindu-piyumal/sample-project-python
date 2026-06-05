import json
import sys

try:
    # Attempt to read and parse the JSON file
    with open("artemis_raw.json") as f:
        d = json.load(f)
except FileNotFoundError as e:
    print(f"Error: Input file 'artemis_raw.json' not found: {e}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Failed to parse JSON from 'artemis_raw.json': {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error: Unexpected error while reading 'artemis_raw.json': {e}", file=sys.stderr)
    sys.exit(1)

try:
    # Extract benchmark statistics
    b = d["benchmarks"][0]["stats"]
    lat = b["data"]
    p99 = sorted(lat)[int(0.99 * len(lat))]
except (KeyError, IndexError, TypeError) as e:
    print(f"Error: Invalid structure in JSON data: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error: Unexpected error while processing data: {e}", file=sys.stderr)
    sys.exit(1)

try:
    # Write results to CSV
    with open("artemis_results.csv", "w") as f:
        f.write("runtime,throughput,memory_peak,latency_p99,cpu_usage\n")
        f.write(f"{b['mean']},{b['ops']},0,{p99},0\n")
except IOError as e:
    print(f"Error: Failed to write output file 'artemis_results.csv': {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error: Unexpected error while writing output: {e}", file=sys.stderr)
    sys.exit(1)
