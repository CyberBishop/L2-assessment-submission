Below is the console output for the provided Python script that detects potential attack patterns in the logs:

**NB: While I do not consider 15 requests in 5 minutes as an attack, I have included it in the output to demonstrate the detection of abnormal request frequencies.**

````python

```bash
➜  L2-assessment git:(main) ✗ python3 solutions/question_3/attack_pattern_detection.py
Potential Attack Patterns Summary:

Flagged IPs that hit rate limit (429) potential bruteforce attack:
- 110.105.174.63 (110 times)
- 49.217.128.165 (114 times)
- 145.98.68.30 (106 times)
- 32.90.145.204 (102 times)
- 49.17.221.77 (108 times)
- 24.74.238.114 (114 times)
- 221.34.171.155 (121 times)
- 188.230.178.192 (108 times)

Flagged IPs that caused 503 errors on login path (potential SQL injection):
- 110.105.174.63 (129 times)
- 49.217.128.165 (118 times)
- 32.90.145.204 (134 times)
- 145.98.68.30 (135 times)
- 49.17.221.77 (121 times)
- 24.74.238.114 (134 times)
- 221.34.171.155 (123 times)
- 188.230.178.192 (117 times)

No IPs with excessive 404 errors.

Abnormal Request Frequencies (>15 requests in 5 minutes):
- IP 145.98.68.30 sent 16 requests between 2025-05-17 08:59:15+08:00 and 2025-05-17 09:04:11+08:00 (>15 in 5 mins)
- IP 110.105.174.63 sent 17 requests between 2025-05-17 08:50:31+08:00 and 2025-05-17 08:55:16+08:00 (>15 in 5 mins)

Unique status codes in the logs:
- 200 (2310 times)
- 304 (1485 times)
- 404 (1511 times)
- 429 (883 times)
- 503 (1011 times)

503 Error Counts by Domain and Path:
- 512 times: api.customer.com /login
- 499 times: domain.customer.com /login
➜  L2-assessment git:(main) ✗
````
