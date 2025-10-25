"""
Unit tests for zone_traversal.py

Tests the BFS (Breadth-First Search) pathfinding algorithm.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zone_traversal import bfs


class TestBFS:
    """Test suite for the BFS pathfinding function"""

    def test_bfs_simple_path(self):
        """Test BFS with a simple linear path"""
        adjacency = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2]
        }
        result = bfs(adjacency, 0, goal=3)
        assert result == [0, 1, 2, 3], "Should find direct path from 0 to 3"

    def test_bfs_direct_connection(self):
        """Test BFS when start is directly connected to goal"""
        adjacency = {
            0: [1],
            1: [0]
        }
        result = bfs(adjacency, 0, goal=1)
        assert result == [0, 1], "Should find direct path"

    def test_bfs_start_is_goal(self):
        """Test BFS when start and goal are the same"""
        adjacency = {
            0: [1],
            1: [0]
        }
        result = bfs(adjacency, 0, goal=0)
        assert result == [0], "Should return just the start node"

    def test_bfs_no_path_exists(self):
        """Test BFS when no path exists between start and goal"""
        adjacency = {
            0: [1],
            1: [0],
            2: [3],
            3: [2]
        }
        result = bfs(adjacency, 0, goal=3)
        assert result is None, "Should return None when no path exists"

    def test_bfs_multiple_paths_shortest(self):
        """Test that BFS finds the shortest path when multiple paths exist"""
        adjacency = {
            0: [1, 2],
            1: [0, 3],
            2: [0, 3],
            3: [1, 2, 4],
            4: [3]
        }
        result = bfs(adjacency, 0, goal=4)
        
        # BFS should find one of the shortest paths
        assert len(result) == 4, "Should find path of length 4"
        assert result[0] == 0 and result[-1] == 4, "Path should start at 0 and end at 4"

    def test_bfs_complex_graph(self):
        """Test BFS with a more complex graph structure"""
        adjacency = {
            0: [1, 2],
            1: [0, 3, 4],
            2: [0, 5],
            3: [1, 6],
            4: [1, 7],
            5: [2, 8],
            6: [3, 9],
            7: [4, 9],
            8: [5, 9],
            9: [6, 7, 8]
        }
        result = bfs(adjacency, 0, goal=9)
        
        assert result is not None, "Path should exist"
        assert result[0] == 0, "Path should start at 0"
        assert result[-1] == 9, "Path should end at 9"
        
        # Verify path validity
        for i in range(len(result) - 1):
            assert result[i + 1] in adjacency[result[i]], \
                f"Invalid path: {result[i]} not connected to {result[i+1]}"

    def test_bfs_cyclic_graph(self):
        """Test BFS with a graph containing cycles"""
        adjacency = {
            0: [1],
            1: [0, 2],
            2: [1, 3, 0],  # Cycle back to 0
            3: [2]
        }
        result = bfs(adjacency, 0, goal=3)
        assert result == [0, 1, 2, 3] or result == [0, 2, 3], \
            "Should find a valid path despite cycles"

    def test_bfs_single_node_graph(self):
        """Test BFS with a graph containing only one node"""
        adjacency = {0: []}
        result = bfs(adjacency, 0, goal=0)
        assert result == [0], "Should return the single node"

    def test_bfs_empty_adjacency_no_goal(self):
        """Test BFS with empty adjacency list for start node"""
        adjacency = {0: [], 1: []}
        result = bfs(adjacency, 0, goal=1)
        assert result is None, "Should return None when no connections exist"

    def test_bfs_default_goal_parameter(self):
        """Test BFS with default goal parameter (goal=9)"""
        adjacency = {
            0: [1],
            1: [0, 2],
            2: [1, 9],
            9: [2]
        }
        result = bfs(adjacency, 0)  # Default goal is 9
        assert result == [0, 1, 2, 9], "Should find path to default goal 9"

    def test_bfs_mall_scenario(self):
        """Test BFS with a realistic mall scenario"""
        # Simulating a simplified mall layout
        mall_adjacency = {
            0: [8],  # Store 0 to corridor 8
            1: [8],  # Store 1 to corridor 8
            2: [8],  # Store 2 to corridor 8
            3: [8],  # Store 3 to corridor 8
            4: [7, 8],  # Store 4 to corridors
            5: [7, 8],  # Store 5 to corridors
            6: [7, 8],  # Store 6 to corridors
            7: [4, 5, 6, 9],  # Corridor 7 connections
            8: [0, 1, 2, 3, 4, 5, 6, 9],  # Corridor 8 connections
            9: [7, 8]  # Outside (goal)
        }
        
        # Test path from store 0 to outside (9)
        result = bfs(mall_adjacency, 0, goal=9)
        assert result is not None, "Path should exist from store to outside"
        assert result[0] == 0 and result[-1] == 9
        
        # Verify it's a valid path
        for i in range(len(result) - 1):
            assert result[i + 1] in mall_adjacency[result[i]]

    def test_bfs_path_order(self):
        """Test that BFS returns path in correct order from start to goal"""
        adjacency = {
            0: [1, 2],
            1: [0, 3],
            2: [0, 3],
            3: [1, 2, 4],
            4: [3]
        }
        result = bfs(adjacency, 0, goal=4)
        
        # Path should be in order from start to goal
        assert result[0] == 0, "First element should be start"
        assert result[-1] == 4, "Last element should be goal"
        
        # Each consecutive pair should be connected
        for i in range(len(result) - 1):
            assert result[i + 1] in adjacency[result[i]]

    def test_bfs_visited_tracking(self):
        """Test that BFS doesn't revisit nodes (implicit test via graph with cycles)"""
        # Create a graph with many cycles
        adjacency = {
            0: [1, 2, 3],
            1: [0, 2, 4],
            2: [0, 1, 3, 4],
            3: [0, 2, 4],
            4: [1, 2, 3]
        }
        result = bfs(adjacency, 0, goal=4)
        
        # Check for duplicate nodes in path
        assert len(result) == len(set(result)), "Path should not contain duplicate nodes"

    def test_bfs_disconnected_components(self):
        """Test BFS with disconnected graph components"""
        adjacency = {
            0: [1],
            1: [0],
            2: [3],
            3: [2],
            4: []
        }
        
        # Try to find path between disconnected components
        result = bfs(adjacency, 0, goal=2)
        assert result is None, "Should return None for disconnected components"
        
        result = bfs(adjacency, 0, goal=4)
        assert result is None, "Should return None when goal is isolated"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])