import json

with open("artemis_raw.json") as f:
    d = json.load(f)

b = d["benchmarks"][0]["stats"]
lat = b["data"]
p99 = sorted(lat)[int(0.99 * len(lat))]

with open("artemis_results.csv", "w") as f:
    f.write("runtime,throughput,memory_peak,latency_p99,cpu_usage\n")
    f.write(f"{b['mean']},{b['ops']},0,{p99},0\n")
