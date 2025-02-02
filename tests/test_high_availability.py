"""Unit tests for high availability features."""

import pytest
from unittest.mock import MagicMock, patch
import aiohttp
from app.high_availability import LoadBalancer, ServiceNode

@pytest.fixture
def nodes_config():
    return [
        {"url": "http://node1:8000", "weight": 100},
        {"url": "http://node2:8000", "weight": 100},
        {"url": "http://node3:8000", "weight": 100}
    ]

@pytest.fixture
def load_balancer(nodes_config):
    return LoadBalancer(nodes=nodes_config)

@pytest.mark.asyncio
async def test_load_balancer_initialization(load_balancer, nodes_config):
    """Test load balancer initialization."""
    assert len(load_balancer.nodes) == len(nodes_config)
    assert all(isinstance(node, ServiceNode) for node in load_balancer.nodes)
    assert all(node.healthy for node in load_balancer.nodes)

@pytest.mark.asyncio
async def test_node_health_check(load_balancer):
    """Test node health checking."""
    node = load_balancer.nodes[0]
    
    # Mock successful health check
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_get.return_value.__aenter__.return_value = mock_response
        
        await load_balancer._check_node(node)
        assert node.healthy
        assert node.consecutive_failures == 0

    # Mock failed health check
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.side_effect = aiohttp.ClientError()
        
        for _ in range(load_balancer.max_failures):
            await load_balancer._check_node(node)
            
        assert not node.healthy
        assert node.consecutive_failures >= load_balancer.max_failures

@pytest.mark.asyncio
async def test_node_selection(load_balancer):
    """Test node selection algorithm."""
    # All nodes healthy
    node = load_balancer.get_next_node()
    assert node is not None
    assert node.healthy
    
    # Mark all nodes unhealthy
    for node in load_balancer.nodes:
        node.healthy = False
    
    assert load_balancer.get_next_node() is None

@pytest.mark.asyncio
async def test_failover_handling(load_balancer):
    """Test failover handling when node fails."""
    failed_node = load_balancer.nodes[0]
    
    # Simulate node failure
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.side_effect = aiohttp.ClientError()
        
        for _ in range(load_balancer.max_failures):
            await load_balancer._check_node(failed_node)
    
    assert not failed_node.healthy
    
    # Verify we can still get a healthy node
    next_node = load_balancer.get_next_node()
    assert next_node is not None
    assert next_node.healthy
    assert next_node != failed_node

@pytest.mark.asyncio
async def test_node_recovery(load_balancer):
    """Test node recovery after failure."""
    node = load_balancer.nodes[0]
    
    # First make node fail
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.side_effect = aiohttp.ClientError()
        
        for _ in range(load_balancer.max_failures):
            await load_balancer._check_node(node)
    
    assert not node.healthy
    
    # Then simulate recovery
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_get.return_value.__aenter__.return_value = mock_response
        
        await load_balancer._check_node(node)
    
    assert node.healthy
    assert node.consecutive_failures == 0