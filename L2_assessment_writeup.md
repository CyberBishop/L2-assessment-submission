# L2 Assessment Write-Up

## Task 2 – Bug Fixes and Improvements

While running the attack detection script, I encountered several runtime issues and logic inconsistencies that were resolved as follows:

### 1. TypeError with Status Code Comparison

The script raised a `TypeError: '>=' not supported between instances of 'str' and 'int'` when comparing HTTP status codes. This occurred because `status` was being treated as a string. I fixed this by converting it to an integer in the `parse_log_line()` function:

```python
return {
    'timestamp': timestamp,
    'status': int(status),
    'ip': ip
}
```

### 2. Unsorted Log Entries

The logs were not sorted by timestamp, affecting the accuracy of the 5-minute window error rate analysis. I added logic to sort the parsed log lines before processing:

```python
parsed_lines.sort(key=lambda x: x['timestamp'])
```

### 3. Incomplete 5-Minute Window Comparison

The condition used to check time windows excluded cases where the difference was exactly 5 minutes. I modified:

```python
if time_diff > window_size
```

to:

```python
if time_diff >= window_size
```

This ensures all relevant windows are analyzed.

### 4. Improved Error Rate Display

The error rate was displayed as a decimal (e.g., `0.10%` instead of `10%`). I multiplied the result by 100 for better readability:

```python
print(f"Alert! Error rate {error_rate * 100:.2f}% exceeds threshold at {current_window_start}")
```

### Final Console Output Sample

```bash
Alert! Error rate 71.43% exceeds threshold at 2025-05-17 00:00:14+08:00
Alert! Error rate 63.64% exceeds threshold at 2025-05-17 00:05:17+08:00
... # Truncated
Alert! Error rate 37.50% exceeds threshold at 2025-05-17 23:57:28+08:00
```

---

## Task 3 – Explanation of Attack Detection Script

The `summarize_attacks()` function analyzes logs to detect malicious patterns using the following approach:

### 🔍 Log Parsing

Each line is matched with a regex pattern to extract:

- IP address
- Timestamp
- Domain
- HTTP Method
- URL
- Status Code

### Attack Pattern Detection

- **429 Errors (Rate Limiting):** IPs repeatedly triggering 429 responses are flagged for potential brute force or DoS attempts.
- **503 Errors on `/login`:** These may indicate backend abuse or injection attempts.
- **Excessive 404 Errors:** More than 15 `404 Not Found` responses from the same IP indicate potential directory scanning or probing.
- **Request Frequency Analysis:** Detects IPs making over 15 requests within any 5-minute window.

### Summary Output

The script provides:

- List of suspicious IPs grouped by attack type
- Details on request bursts
- Distribution of HTTP status codes
- Breakdown of `503` errors by domain and path

---

## Task 5 – CDN Optimization Recommendation (Bonus)

To enhance CDN performance and reduce vulnerability to attack patterns observed:

- **IP Blacklisting:** Automatically block IPs that send over 100 requests with 429 errors. This helps mitigate brute force attempts and reduces unnecessary load on CDN resources.

- **Traffic-Aware Load Balancing:** The highest average response times were observed at **10 PM**, suggesting peak usage. Deploying additional server instances during this time can distribute load and maintain fast response times.

- **Improved Caching Strategy:** Ensure static or frequently requested assets are served from the CDN cache to reduce hits to the origin server and minimize latency for end users.

---
