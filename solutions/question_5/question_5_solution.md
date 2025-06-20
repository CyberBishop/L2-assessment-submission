5. (Bonus) CDN Performance Optimization
   Based on your findings in Tasks 1-3, suggest one mitigation step to improve CDN performance for this
   customer. Keep it concise (2-3 sentences).

   Automatically blacklist IPs that exceed a threshold of 100 requests with a 429 status code can significantly reduce the load on the CDN and improve performance. This proactive measure helps prevent potential brute force attacks and ensures that legitimate users experience faster response times by reducing unnecessary traffic from problematic IPs.

   I also noticed that the hour of the day with the highest average response time is 10 PM. This suggests that traffic patterns may be causing congestion during peak hours, so implementing load balancing strategies like spinning up another instance of the server during these times could further enhance CDN performance.

   Additionally, optimizing the caching strategy to ensure that frequently accessed resources are served from the cache rather than hitting the origin server can lead to improved response times and reduced latency for end users.
