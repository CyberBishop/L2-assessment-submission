```bash
# Connect to the database
sqlite3 traffic.db
```

```sql
-- List all tables in the database
.tables
-- Output: request_logs

-- Show the schema of the request_logs table
.schema request_logs
-- Output: id, timestamp, ip_address, status_code, response_time_ms, bytes_sent
```

```bash
# Find the hour of the day with the highest average response time.

sqlite> SELECT strftime('%H', timestamp) AS hour, AVG(response_time_ms) AS avg_response_time
   ...> FROM request_logs
   ...> GROUP BY hour
   ...> ORDER BY avg_response_time DESC
   ...> LIMIT 1;

22|905.177514792899 # The 22nd hour (10 PM) has the highest average response time of 905.18 ms
sqlite>
```

```bash
# Identify any IPs that sent more than 100 requests with a 429 status code (rate-limited).

sqlite> SELECT ip_address, COUNT(*) AS request_count
   ...> FROM request_logs
   ...> WHERE status_code = 429
   ...> GROUP BY ip_address
   ...> HAVING request_count > 100;

# List of IPs with more than 100 requests with status code 429 (rate-limited due to potential brute force attacks)
119.103.226.136|358
122.157.29.219|363
148.57.203.182|344
17.237.57.99|338
81.233.238.12|333

sqlite>
```

```bash
# Calculate the total bytes sent for requests where response time > 500ms.

sqlite> SELECT SUM(bytes_sent) AS total_bytes_sent
   ...> FROM request_logs
   ...> WHERE response_time_ms > 500;

# The total bytes sent for requests with response time greater than 500ms
10719865

sqlite>
```
