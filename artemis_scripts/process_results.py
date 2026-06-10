import json
import logging
import sys

# Configure logging to help identify issues with malformed JSON
logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

try:
    with open("artemis_raw.json") as f:
        d = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    logger.error(f"Failed to load artemis_raw.json: {e}")
    sys.exit(1)

# Validate 'benchmarks' key exists and is a non-empty list
if 'benchmarks' not in d:
    logger.error("Missing required key 'benchmarks' in JSON structure")
    sys.exit(1)

if not isinstance(d['benchmarks'], list):
    logger.error(f"Expected 'benchmarks' to be a list, got {type(d['benchmarks']).__name__}")
    sys.exit(1)

if len(d['benchmarks']) == 0:
    logger.error("No benchmarks data found in JSON (empty 'benchmarks' list)")
    sys.exit(1)

# Validate the first benchmark entry has 'stats' key
benchmark_entry = d['benchmarks'][0]
if not isinstance(benchmark_entry, dict):
    logger.error(f"Expected first benchmark to be a dict, got {type(benchmark_entry).__name__}")
    sys.exit(1)

if 'stats' not in benchmark_entry:
    logger.error("Missing required key 'stats' in first benchmark entry")
    sys.exit(1)

b = benchmark_entry['stats']

# Validate 'stats' is a dictionary and contains 'data' key
if not isinstance(b, dict):
    logger.error(f"Expected 'stats' to be a dict, got {type(b).__name__}")
    sys.exit(1)

if 'data' not in b:
    logger.error("Missing required key 'data' in benchmark stats")
    sys.exit(1)

lat = b['data']

# Validate 'data' is a non-empty list or array-like
if not isinstance(lat, (list, tuple)):
    logger.error(f"Expected 'data' to be a list or tuple, got {type(lat).__name__}")
    sys.exit(1)

if len(lat) == 0:
    logger.error("No data points found in benchmark (empty 'data' list)")
    sys.exit(1)

# Calculate p99 latency
try:
    p99 = sorted(lat)[int(0.99 * len(lat))]
except (TypeError, ValueError) as e:
    logger.error(f"Failed to calculate p99 from latency data: {e}")
    sys.exit(1)

# Validate required fields for output
if 'mean' not in b:
    logger.error("Missing required key 'mean' in benchmark stats")
    sys.exit(1)

if 'ops' not in b:
    logger.error("Missing required key 'ops' in benchmark stats")
    sys.exit(1)

# Write results to CSV file
try:
    with open("artemis_results.csv", "w") as f:
        f.write("runtime,throughput,memory_peak,latency_p99,cpu_usage\n")
        f.write(f"{b['mean']},{b['ops']},0,{p99},0\n")
except IOError as e:
    logger.error(f"Failed to write artemis_results.csv: {e}")
    sys.exit(1)
