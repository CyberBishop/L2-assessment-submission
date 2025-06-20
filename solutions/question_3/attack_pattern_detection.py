import re
from datetime import datetime, timedelta
from collections import defaultdict, Counter

def parse_log_line(line):
    pattern = r'(\d+\.\d+\.\d+\.\d+) - \w+ \[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\] "([^"]+)" "(\w+) ([^ ]+) [^"]*" (\d+)'
    match = re.match(pattern, line)
    if match:
        ip, timestamp_str, domain, method, url, status = match.groups()
        timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S %z')
        return {
            'ip': ip,
            'timestamp': timestamp,
            'domain': domain,
            'method': method,
            'url': url,
            'status': int(status)
        }
    return None

def summarize_attacks(log_file, freq_threshold=15, window_minutes=5, error_404_threshold=15):
    logs = []
    status_counter = Counter()
    error_503_counter = Counter()
    error_429_counter = Counter()
    unique_codes = set()
    with open(log_file, 'r') as f:
        for line in f:
            data = parse_log_line(line.strip())
            if data:
                logs.append(data)
                status_counter[data['status']] += 1
                unique_codes.add(data['status'])
                if data['status'] == 503:
                    error_503_counter[(data['domain'], data['url'])] += 1
                if data['status'] == 429:
                    error_429_counter[data['ip']] += 1
    logs.sort(key=lambda x: x['timestamp'])

    flagged_429_ips = set(error_429_counter.keys())
    flagged_503_login_ips = set()
    flagged_404_ips = set()
    ip_timestamps = defaultdict(list)
    ip_404_counter = Counter()

    for log in logs:
        ip_timestamps[log['ip']].append(log['timestamp'])
        if log['status'] == 503 and "/login" in log['url']:
            flagged_503_login_ips.add(log['ip'])
        if log['status'] == 404:
            ip_404_counter[log['ip']] += 1

    for ip, count in ip_404_counter.items():
        if count > error_404_threshold:
            flagged_404_ips.add(ip)

    print("Potential Attack Patterns Summary:\n")

    if flagged_429_ips:
        print("Flagged IPs that hit rate limit (429) potential bruteforce attack:")
        for ip in flagged_429_ips:
            print(f"- {ip} ({error_429_counter[ip]} times)")
    else:
        print("No IPs hit the rate limit.")

    if flagged_503_login_ips:
        print("\nFlagged IPs that caused 503 errors on login path (potential SQL injection):")
        for ip in flagged_503_login_ips:
            count = sum(1 for log in logs if log['ip'] == ip and log['status'] == 503 and "/login" in log['url'])
            print(f"- {ip} ({count} times)")
    else:
        print("\nNo IPs caused 503 errors on login path.")

    if flagged_404_ips:
        print("\nFlagged IPs with excessive 404 errors:")
        for ip in flagged_404_ips:
            print(f"- {ip} ({ip_404_counter[ip]} times)")
    else:
        print("\nNo IPs with excessive 404 errors.")

    print("\nAbnormal Request Frequencies (>{} requests in {} minutes):".format(freq_threshold, window_minutes))
    abnormal_ips = set()
    for ip, times in ip_timestamps.items():
        times.sort()
        for i in range(len(times)):
            count = 1
            for j in range(i+1, len(times)):
                if (times[j] - times[i]) <= timedelta(minutes=window_minutes):
                    count += 1
                else:
                    break
            if count > freq_threshold:
                abnormal_ips.add(ip)
                print(f"- IP {ip} sent {count} requests between {times[i]} and {times[j-1]} (>{freq_threshold} in {window_minutes} mins)")
                break
    if not abnormal_ips:
        print("No abnormal request frequencies detected.")

    print("\nUnique status codes in the logs:")
    for code in sorted(unique_codes):
        print(f"- {code} ({status_counter[code]} times)")

    print("\n503 Error Counts by Domain and Path:")
    if error_503_counter:
        for (domain, url), count in error_503_counter.items():
            print(f"- {count} times: {domain} {url}")
    else:
        print("No 503 errors detected.")

if __name__ == "__main__":
    summarize_attacks('nginx_access.log')