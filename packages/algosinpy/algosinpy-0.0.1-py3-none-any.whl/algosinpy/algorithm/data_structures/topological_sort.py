"""
    Topological Sort Algorithm Implementation
    Topological sorting is an algorithm for arranging the nodes of a directed acyclic graph (DAG) in a special linear order where for each directed edge from node A to node B, node A appears before node B in the ordering. The topological sort order is not necessarily unique, there can be multiple valid topological orderings for a given DAG.
    Topological sorting has many applications in scheduling, data science, computer science, and other fields. 
    
    Some key use cases include:
        Scheduling tasks that have dependencies on each other
        Ordering compilation tasks to compile source code files
        Data science workflows to run models with dependencies
        Finding instruction ordering in dependency graphs for processors
        Network routing algorithms
    
    This module provides a function to perform topological sorting on a directed acyclic graph (DAG).
    It uses Kahn's algorithm to return a list of vertices in topologically sorted order.
"""

from src.algosinpy.logger.py_logger import PyLogger

logger = PyLogger.get_configured_logger()

class TopologicalSort:
    @staticmethod
    def topological_sort(graph):
        """
        Perform topological sorting on a directed acyclic graph (DAG).

        :param graph: A dictionary representing the graph where keys are nodes and values are lists of adjacent nodes.
        :return: A list of nodes in topologically sorted order.

        examples:
        >>> graph = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}
        >>> TopologicalSort.topological_sort(graph)
        ['A', 'B', 'C', 'D']
        """
        from collections import defaultdict, deque

        in_degree = defaultdict(int)
        for node in graph:
            for neighbor in graph[node]:
                in_degree[neighbor] += 1

        queue = deque([node for node in graph if in_degree[node] == 0])
        sorted_order = []

        while queue:
            current_node = queue.popleft()
            sorted_order.append(current_node)

            for neighbor in graph[current_node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sorted_order) != len(graph):
            logger.error("Graph has at least one cycle, topological sort not possible.")
            return []

        return sorted_order

if __name__ == "__main__":
    import doctest
    import time

    start_time = time.time()
    doctest.testmod()
    end_time = time.time()
    logger.info(f"Time taken for tests: {end_time - start_time} seconds")
    logger.info("All tests passed successfully.")   
