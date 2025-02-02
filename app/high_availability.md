# High Availability Implementation Details

The high availability implementation includes the following key components:

1. **Service Discovery**
   - Uses Consul for service registration and discovery
   - Dynamic node updates based on service health
   - Automatic service registration with health checks

2. **Failover Mechanism**
   - Health monitoring of all service nodes
   - Automatic failover to healthy nodes when failures occur
   - Circuit breaker pattern to prevent cascading failures
   - Exponential backoff for recovery attempts

3. **Load Balancing**
   - Round-robin distribution with node weights
   - Health-aware routing (only routes to healthy nodes)
   - Dynamic node pool updates

4. **Recovery Procedures**
   - Automated recovery attempts for failed nodes
   - Circuit breaker state management (Closed -> Open -> Half-Open)
   - Service re-registration after recovery

## Usage

1. Start the Consul service:
```bash
docker-compose -f docker-compose.ha.yml up -d consul
```

2. Initialize the LoadBalancer with Consul configuration:
```python
lb = LoadBalancer(
    nodes=[...],
    consul_host="localhost",
    consul_port=8500,
    service_name="email-validator"
)
```

3. Start the load balancer:
```python
await lb.start()
```

The system will automatically handle:
- Service registration
- Health monitoring
- Failover routing
- Recovery attempts
- Dynamic node updates