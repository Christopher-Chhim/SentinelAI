"""
Unit tests for adjacencyList.py

Tests the calculate_adjacency_list function which converts a directed graph
to an undirected graph representation.
"""

import pytest
from collections import defaultdict
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adjacencyList import calculate_adjacency_list, doors


class TestCalculateAdjacencyList:
    """Test suite for the calculate_adjacency_list function"""

    def test_calculate_adjacency_list_basic(self):
        """Test basic adjacency list calculation with simple input"""
        simple_doors = {
            0: [1],
            1: [2],
            2: []
        }
        result = calculate_adjacency_list(simple_doors)
        
        # Check bidirectional connections
        assert 1 in result[0], "Node 0 should connect to node 1"
        assert 0 in result[1], "Node 1 should connect back to node 0"
        assert 2 in result[1], "Node 1 should connect to node 2"
        assert 1 in result[2], "Node 2 should connect back to node 1"

    def test_calculate_adjacency_list_with_default_doors(self):
        """Test adjacency list calculation with the default doors configuration"""
        adjacency_list = calculate_adjacency_list(doors)
        
        # Node 8 should be connected to nodes 0, 1, 2, 3, 4, 6
        assert 0 in adjacency_list[8], "Node 8 should be connected to node 0"
        assert 1 in adjacency_list[8], "Node 8 should be connected to node 1"
        assert 2 in adjacency_list[8], "Node 8 should be connected to node 2"
        assert 3 in adjacency_list[8], "Node 8 should be connected to node 3"
        assert 4 in adjacency_list[8], "Node 8 should be connected to node 4"
        assert 6 in adjacency_list[8], "Node 8 should be connected to node 6"

    def test_calculate_adjacency_list_bidirectional(self):
        """Test that connections are bidirectional"""
        adjacency_list = calculate_adjacency_list(doors)
        
        for node, connections in doors.items():
            for connected_node in connections:
                assert node in adjacency_list[connected_node], \
                    f"Node {connected_node} should connect back to node {node}"

    def test_calculate_adjacency_list_empty_input(self):
        """Test with empty doors dictionary"""
        result = calculate_adjacency_list({})
        assert len(result) == 0, "Empty input should return empty adjacency list"

    def test_calculate_adjacency_list_single_node(self):
        """Test with a single node with no connections"""
        single_node = {0: []}
        result = calculate_adjacency_list(single_node)
        assert 0 not in result or len(result[0]) == 0, \
            "Single node with no connections should have empty list"

    def test_calculate_adjacency_list_multiple_connections(self):
        """Test node with multiple outgoing connections"""
        multi_doors = {
            0: [1, 2, 3],
            1: [],
            2: [],
            3: []
        }
        result = calculate_adjacency_list(multi_doors)
        
        # Check all connections from node 0
        assert 1 in result[0], "Node 0 should connect to node 1"
        assert 2 in result[0], "Node 0 should connect to node 2"
        assert 3 in result[0], "Node 0 should connect to node 3"
        
        # Check reverse connections
        assert 0 in result[1], "Node 1 should connect back to node 0"
        assert 0 in result[2], "Node 2 should connect back to node 0"
        assert 0 in result[3], "Node 3 should connect back to node 0"

    def test_calculate_adjacency_list_complex_graph(self):
        """Test with a more complex graph structure"""
        complex_doors = {
            0: [1, 2],
            1: [2, 3],
            2: [3],
            3: [4],
            4: []
        }
        result = calculate_adjacency_list(complex_doors)
        
        # Node 2 should have connections from 0, 1, and to 3
        assert 0 in result[2], "Node 2 should connect to node 0"
        assert 1 in result[2], "Node 2 should connect to node 1"
        assert 3 in result[2], "Node 2 should connect to node 3"

    def test_calculate_adjacency_list_circular_connections(self):
        """Test with circular connections"""
        circular = {
            0: [1],
            1: [2],
            2: [0]
        }
        result = calculate_adjacency_list(circular)
        
        # All nodes should be connected in both directions
        assert 1 in result[0] and 2 in result[0]
        assert 0 in result[1] and 2 in result[1]
        assert 0 in result[2] and 1 in result[2]

    def test_calculate_adjacency_list_return_type(self):
        """Test that the function returns a defaultdict"""
        result = calculate_adjacency_list(doors)
        assert isinstance(result, defaultdict), \
            "Result should be a defaultdict"

    def test_calculate_adjacency_list_no_duplicate_connections(self):
        """Test that there are no duplicate connections in the adjacency list"""
        adjacency_list = calculate_adjacency_list(doors)
        
        for node, connections in adjacency_list.items():
            unique_connections = set(connections)
            assert len(connections) == len(unique_connections), \
                f"Node {node} has duplicate connections"

    def test_calculate_adjacency_list_self_loops(self):
        """Test handling of self-loops (if any)"""
        self_loop_doors = {
            0: [0, 1],
            1: []
        }
        result = calculate_adjacency_list(self_loop_doors)
        
        # Node 0 should have itself in adjacency list
        assert 0 in result[0], "Node 0 should have self-loop"

    def test_node_9_connections(self):
        """Test that node 9 (outside) has correct connections"""
        adjacency_list = calculate_adjacency_list(doors)
        
        # Node 9 should be connected to nodes 8 and 7 (from the doors dict)
        expected_connections = {8}
        for node, connections in doors.items():
            if 9 in connections:
                expected_connections.add(node)
        
        for expected in expected_connections:
            assert expected in adjacency_list[9], \
                f"Node 9 should be connected to node {expected}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])