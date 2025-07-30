from src.algosinpy.algorithm.data_structures.queue import *
from src.algosinpy.logger.py_logger import PyLogger

logger = PyLogger.get_configured_logger()


class Graph:
    def __init__(self, is_bidirectional=False):
        """
        :param is_bidirectional: to check that graphs is uni directional or bidirectional
        """
        # edges is an adjacency list of the given graphs
        self.edges = {}
        self.bidirectional = is_bidirectional

    def add_edge(self, from_node, to_node):
        if from_node in self.edges.keys():
            self.edges[from_node].append(to_node)
        else:
            self.edges[from_node] = [to_node]

        # update edges to bidirectional
        if self.bidirectional:
            if to_node in self.edges.keys():
                self.edges[to_node].append(from_node)
            else:
                self.edges[to_node] = [from_node]

    def bfs(self, node):
        """
        :param node: from where to start visiting vertex through edges
        :return: a list of visited vertex
        """
        queue = Queue()
        visited = list()

        queue.push(node)
        visited.append(node)

        while not queue.empty():
            node = queue.front()
            queue.pop()

            for adjacent_node in self.edges[node]:
                if adjacent_node not in visited:
                    visited.append(adjacent_node)
                    queue.push(adjacent_node)

        return visited

    def print_graph(self):
        for node in self.edges.keys():
            logger.info(
                f"{node} : {' -> '.join(str(vertex) for vertex in self.edges[node])}"
            )


if __name__ == "__main__":
    g = Graph(is_bidirectional=True)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(2, 3)
    logger.info(f"visited node: {g.bfs(node=3)}")
