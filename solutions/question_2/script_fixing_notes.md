I just tried to run the python script to get the errors at run time.

1. `'>=' not supported between instances of 'str' and 'int'` the status variable is a string, so I need to convert it to an int.

`return status >= 400 and status <= 599`

From the return statement in the parse_log_line function.
I converted the status to an int before returning it in the dictionary, by wrapping it with `int(status)`

```python
return {
    'timestamp': timestamp,
    'status': int(status),
    'ip': ip
}
```

2. I sampled the log file and found out that the log file entries were not sorted by timestamp, which affected the 5-minute window analysis, I parsed all log lines, then sorted them by timestamp before processing:

```python
parsed_lines = []
for line in lines:
    log_data = parse_log_line(line.strip())
    if log_data is not None:
        parsed_lines.append(log_data)

parsed_lines.sort(key=lambda x: x['timestamp'])
return parsed_lines
```

3. Asides that, I also noticed the script only checked for windows where the time difference was greater than 5 minutes, missing exact 5-minute windows.I changed the condition to include windows with a time difference equal to 5 minutes:

```python
if time_diff >= window_size: # previous check was time_diff > window_size
```

4. I also noticed that the percentage output was not very clear as 10% was been represented as 0.10% so I changed the output to be more readable by multiplying the percentage by 100.

```python
print(f"Alert! Error rate {error_rate * 100:.2f}% exceeds threshold at {current_window_start}")
```

Final console output after fixing the issues:

```bash
➜  L2-assessment git:(main) ✗ python3 solutions/question_2/python_monitor.py
Alert! Error rate 71.43% exceeds threshold at 2025-05-17 00:00:14+08:00
Alert! Error rate 63.64% exceeds threshold at 2025-05-17 00:05:17+08:00
...
Alert! Error rate 43.75% exceeds threshold at 2025-05-17 23:52:26+08:00
Alert! Error rate 37.50% exceeds threshold at 2025-05-17 23:57:28+08:00
```
