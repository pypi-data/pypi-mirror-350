from src.algosinpy.logger.py_logger import PyLogger

logger = PyLogger.get_configured_logger()


class Graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, from_node, to_node):
        if from_node in self.edges.keys():
            self.edges[from_node].append(to_node)
        else:
            self.edges[from_node] = [to_node]

    def dfs_recursive(self, node, visited, visited_node):
        """
        :param node: a starting point to travel through edges
        :param visited: to mark a node is already visited or not
        :param visited_node: to store a list of visited node
        :return: a list of visited node
        """
        visited[node] = True
        if node in self.edges.keys():
            for adjacent_node in self.edges[node]:
                if not visited[adjacent_node]:
                    visited_node.append(adjacent_node)
                    self.dfs_recursive(adjacent_node, visited, visited_node)
        return visited_node

    def dfs(self, starting_node):
        """
        :param starting_node: starting point to visit
        :return: list of visited node
        """
        visited = [False] * (len(self.edges) + 1)
        return self.dfs_recursive(
            node=starting_node, visited=visited, visited_node=[starting_node]
        )

    def print_graph(self):
        for node in self.edges.keys():
            logger.info(f"{node}: {self.edges[node]}")


if __name__ == "__main__":
    dfs = Graph()
    dfs.add_edge(0, 1)
    dfs.add_edge(0, 2)
    dfs.add_edge(1, 2)
    dfs.add_edge(2, 0)
    dfs.add_edge(2, 3)
    dfs.print_graph()
    logger.info(dfs.dfs(2))
