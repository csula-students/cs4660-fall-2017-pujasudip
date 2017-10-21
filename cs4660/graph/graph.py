"""
graph module defines the knowledge representations files
A Graph has following methods:
* adjacent(node_1, node_2)
    - returns true if node_1 and node_2 are directly connected or false otherwise
* neighbors(node)
    - returns all nodes that is adjacency from node
* add_node(node)
    - adds a new node to its internal data structure.
    - returns true if the node is added and false if the node already exists
* remove_node
    - remove a node from its internal data structure
    - returns true if the node is removed and false if the node does not exist
* add_edge
    - adds a new edge to its internal data structure
    - returns true if the edge is added and false if the edge already existed
* remove_edge
    - remove an edge from its internal data structure
    - returns true if the edge is removed and false if the edge does not exist
* distance
    - fetch an edge from its internal data structure
    - returns an edge assuming the passed in nodes and an edge between them exist
"""

from io import open
from operator import itemgetter

def construct_graph_from_file(graph, file_path):
    """
    TODO: read content from file_path, then add nodes and edges to graph object
    note that grpah object will be either of AdjacencyList, AdjacencyMatrix or ObjectOriented
    In example, you will need to do something similar to following:
    1. add number of nodes to graph first (first line)
    2. for each following line (from second line to last line), add them as edge to graph
    3. return the graph
    """
    f = open(file_path, encoding='utf-8')
    content = f.readlines()
    size = (extract_nums_from_line(content[0], ' '))[0];

    """ add nodes to the graph """
    i = 0
    for i in range(size):
        graph.add_node(Node(i))

    """ remove first element which contains only the size """
    content.pop(0)

    """ add the edges """
    for line in content:
        edg = parse_line_to_edge(line)
        graph.add_edge(edg)

    f.close()

    return graph

def parse_line_to_edge(line):
    nums = extract_nums_from_line(line, ":")
    return Edge(Node(nums[0]), Node(nums[1]), nums[2])

def extract_nums_from_line(line, char):
    entries = line.split(char)
    li = []
    for entry in entries:
        try:
            x = int(entry)
            li.append(x)
        except ValueError:
            """do something"""
    return li

class Node(object):
    """Node represents basic unit of graph"""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Node({})'.format(self.data)
    def __repr__(self):
        return 'Node({})'.format(self.data)

    def __eq__(self, other_node):
        return self.data == other_node.data
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)

class Edge(object):
    """Edge represents basic unit of graph connecting between two edges"""
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
    def __str__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)
    def __repr__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __eq__(self, other_node):
        return self.from_node == other_node.from_node and self.to_node == other_node.to_node and self.weight == other_node.weight
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_node, self.to_node, self.weight))


class AdjacencyList(object):
    """
    AdjacencyList is one of the graph representation which uses adjacency list to
    store nodes and edges
    """
    def __init__(self):
        # adjacencyList should be a dictonary of node to edges
        self.adjacency_list = {}

    def adjacent(self, node_1, node_2):
        if node_1 not in self.adjacency_list or node_2 not in self.adjacency_list:
            return False
        for e in self.adjacency_list[node_1]:
            if node_2 == e.to_node:
                return True
        return False


    def neighbors(self, node):
        nb = []
        if node in self.adjacency_list:
            for e in self.adjacency_list[node]:
                nb.append(e.to_node)
        return nb

    def add_node(self, node):
        if node in self.adjacency_list:
            return False
        self.adjacency_list[node] = []
        return True

    def remove_node(self, node):
        if node not in self.adjacency_list:
            return False

        del self.adjacency_list[node]

        for n in self.adjacency_list:
            for e in self.adjacency_list[n]:
                if node == e.to_node:
                    self.adjacency_list[n].remove(e)
        return True

    def add_edge(self, edge):
        if edge.from_node not in self.adjacency_list or edge in self.adjacency_list[edge.from_node]:
            return False
        self.adjacency_list[edge.from_node].append(edge)
        return True

    def remove_edge(self, edge):
        if edge.from_node not in self.adjacency_list or edge not in self.adjacency_list[edge.from_node]:
            return False
        self.adjacency_list[edge.from_node].remove(edge)
        return True

    def distance(self, node_1, node_2):
        for edge in self.adjacency_list[node_1]:
            if node_2 == edge.to_node:
                return edge
        return None

class AdjacencyMatrix(object):
    def __init__(self):
        # adjacency_matrix should be a two dimensions array of numbers that
        # represents how one node connects to another
        self.adjacency_matrix = []
        # in additional to the matrix, you will also need to store a list of Nodes
        # as separate list of nodes
        self.nodes = []

    def adjacent(self, node_1, node_2):
        if node_1 not in self.nodes or node_2 not in self.nodes:
            return False
        index1 = self.__get_node_index(node_1)
        index2 = self.__get_node_index(node_2)
        if self.adjacency_matrix[index1][index2] is not None:
            return True
        return False

    def neighbors(self, node):
        nb = []
        if node in self.nodes:
            index = self.__get_node_index(node)
            for i in range(len(self.nodes)):
                if self.adjacency_matrix[index][i] is not None:
                    nb.append(self.nodes[i])
        return nb

    def add_node(self, node):
        if node in self.nodes:
            return False

        node_list = []
        for i in range(len(self.nodes)):
            node_list.append(None)

        self.adjacency_matrix.append(node_list)

        """ add an extra element to every list """
        for i in range(len(self.adjacency_matrix)):
            self.adjacency_matrix[i].append(None)

        self.nodes.append(node)

        return True

    def remove_node(self, node):
        if node not in self.nodes:
            return False

        index = self.__get_node_index(node)

        """ remove this index from all arrays """
        for i in range(len(self.adjacency_matrix)):
            self.adjacency_matrix[i].pop(index)
        """ remove the whole row """
        self.adjacency_matrix.pop(index)
        self.nodes.remove(node)
        return True

    def add_edge(self, edge):
        if edge.from_node not in self.nodes or edge.to_node not in self.nodes:
            return False
        index1 = self.__get_node_index(edge.from_node)
        index2 = self.__get_node_index(edge.to_node)
        if self.adjacency_matrix[index1][index2] is not None:
            return False
        self.adjacency_matrix[index1][index2] = edge.weight
        return True

    def remove_edge(self, edge):
        if edge.from_node not in self.nodes or edge.to_node not in self.nodes:
            return False
        index1 = self.__get_node_index(edge.from_node)
        index2 = self.__get_node_index(edge.to_node)
        if self.adjacency_matrix[index1][index2] is None:
            return False
        self.adjacency_matrix[index1][index2] = None
        return True

    def distance(self, node_1, node_2):
        index1 = self.__get_node_index(node_1)
        index2 = self.__get_node_index(node_2)
        return Edge(node_1, node_2, self.adjacency_matrix[index1][index2])

    def __get_node_index(self, node):
        """helper method to find node index"""
        index = -1
        i = 0
        while i < len(self.nodes):
            if node == self.nodes[i]:
                index = i
                i = len(self.nodes)
            i += 1
        return index

class ObjectOriented(object):
    """ObjectOriented defines the edges and nodes as both list"""
    def __init__(self):
        # implement your own list of edges and nodes
        self.edges = []
        self.nodes = []

    def adjacent(self, node_1, node_2):
        if node_1 in self.neighbors(node_2) or node_2 in self.neighbors(node_1):
            return True
        return False

    def neighbors(self, node):
        nb = []
        if node in self.nodes:
            for edge in self.edges:
                if edge.from_node == node:
                    nb.append(edge.to_node)
        return nb

    def add_node(self, node):
        if node in self.nodes:
            return False
        self.nodes.append(node)
        return True

    def remove_node(self, node):
        if node not in self.nodes:
            return False

        for edge in self.edges:
            if edge.from_node == node or edge.to_node == node:
                self.edges.remove(edge)

        self.nodes.remove(node)
        return True

    def add_edge(self, edge):
        """ check for invalid nodes or if the edge is already in the list of edges """
        if edge.from_node not in self.nodes or edge.to_node not in self.nodes or edge in self.edges:
            return False
        self.edges.append(edge)
        return True

    def remove_edge(self, edge):
        if edge not in self.edges:
            return False
        self.edges.remove(edge)
        return True

    def distance(self, node_1, node_2):
        for edge in self.edges:
            if edge.from_node == node_1 and edge.to_node == node_2:
                return edge
        return None