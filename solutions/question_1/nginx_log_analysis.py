import re
from collections import Counter

"""
1. Nginx Log Analysis

Analyze the provided nginx_access.log file (Go through some initial logs to understand the pattern).

Write a Python script to:
- Identify the top 5 IP addresses by request count.
- Calculate the percentage of requests with status codes in the 400-599 range.
- Find the average response size in bytes for GET requests.

Output: The script should generate a readable output (console or text file).
"""

log_file = "nginx_access.log"
log_pattern = re.compile(
    r'(?P<ip>\S+) - \S+ \[.*?\] "(?P<host>[^"]+)" "(?P<method>\S+) (?P<url>\S+) [^"]*" (?P<status>\d{3}) (?P<size>\d+)'
)

def parse_log(log_file):
    ip_counter = Counter()
    total_requests = 0
    error_requests = 0
    get_response_sizes = []

    with open(log_file, "r") as f:
        for line in f:
            match = log_pattern.match(line)
            if match:
                total_requests += 1
                ip = match.group("ip")
                method = match.group("method")
                status = int(match.group("status"))
                size = match.group("size")
                ip_counter[ip] += 1

                if 400 <= status <= 599:
                    error_requests += 1
                if method == "GET" and size != "-":
                    get_response_sizes.append(int(size))
    return ip_counter, total_requests, error_requests, get_response_sizes

def top_5_ips(ip_counter):
    print("\nTop 5 IP addresses by request count:")
    for ip, count in ip_counter.most_common(5):
        print(f"{ip}: {count} requests")

def error_percentage(total_requests, error_requests):
    if total_requests:
        error_percent = (error_requests / total_requests) * 100
    else:
        error_percent = 0
    print(f"\nTotal requests: {total_requests}")
    print(f"Total requests with status 400-599: {error_requests}")
    print(f"Percentage of requests with status 400-599: {error_percent:.2f}%")

def average_get_response_size(get_response_sizes):
    if get_response_sizes:
        avg_size = sum(get_response_sizes) / len(get_response_sizes)
    else:
        avg_size = 0

    print("\nTotal GET requests with response size:", len(get_response_sizes))
    print(f"Average response size for GET requests: {avg_size:.2f} bytes")

def main():
    ip_counter, total_requests, error_requests, get_response_sizes = parse_log(log_file)
    top_5_ips(ip_counter)
    error_percentage(total_requests, error_requests)
    average_get_response_size(get_response_sizes)

if __name__ == "__main__":
    main()