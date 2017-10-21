"""
Searches module defines all different search algorithms
"""
import math
try:
    import Queue as que
except ImportError:
    import queue as que

def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    cost = {}
    cost[initial_node] = 0

    parent = {}
    edges = {}

    que = []
    que.append((0, initial_node))

    while len(que) != 0:
        dq = que.pop()[1]

        for node in graph.neighbors(dq):
            if node not in cost:
                edges[node] = graph.distance(dq, node)
                cost[node] = cost[dq] + edges[node].weight
                parent[node] = dq

                if node != dest_node:
                    que.append((cost[node], node))

        que = sorted(que, key=lambda x: x[0])
        que.reverse()

    result = []
    end_node = dest_node

    while end_node in parent:
        result.append(edges[end_node])
        end_node = parent[end_node]

    result.reverse()

    return result


def dfs(graph, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """

    for node in graph.neighbors(initial_node):
        if node == dest_node:
            return [graph.distance(initial_node, dest_node)]
        else:
            paths = dfs(graph, node, dest_node)
            if paths != []:
                result = [graph.distance(initial_node, node)]
                result.extend(paths)
                return result
    return []


def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    dist = {}
    dist[initial_node] = 0

    prev = {}
    edges = {}



    que = []
    que.append((0, initial_node))

    while len(que) != 0:
        dq = que.pop()[1]

        for node in graph.neighbors(dq):
            edge = graph.distance(dq, node)
            alt = dist[dq] + edge.weight

            if node not in dist or alt < dist[node]:
                if node in dist:
                    que.remove((dist[node], node))
                que.append((alt, node))

                dist[node] = alt
                prev[node] = dq
                edges[node] = edge

        que = sorted(que, key=lambda x: x[0])
        que.reverse()

    result = []
    current_node = dest_node

    while current_node in prev:
        result.append(edges[current_node])
        current_node = prev[current_node]

    result.reverse()

    return result


def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """

    frontier = que.PriorityQueue()
    exploredSet = []
    unexploredSet = [(0, initial_node)]
    parents = {}

    gScore = {}
    gScore[initial_node] = 0

    fScore = {}
    fScore[initial_node] = heuristic(initial_node, dest_node)

    edges = {}

    while len(unexploredSet) != 0:
        dq = unexploredSet.pop()[1]

        if dq == dest_node:
            current_node = dq
            constructPath = []
            while current_node in parents:
                constructPath.append(edges[current_node])
                current_node = parents[current_node]
            constructPath.reverse()
            return constructPath

        exploredSet.append(dq)

        for node in graph.neighbors(dq):
            if node not in exploredSet:
                edge = graph.distance(dq, node)
                tempGScore = gScore[dq] + edge.weight
                if node not in gScore:
                    unexploredSet.append((float('inf'), node))
                    gScore[node] = float('inf')
                    fScore[node] = float('inf')
                if tempGScore < gScore[node]:
                    unexploredSet.remove((fScore[node], node))

                    parents[node] = dq
                    edges[node] = edge

                    gScore[node] = tempGScore
                    tempfScore = tempGScore + heuristic(node, dest_node)
                    fScore[node] = tempfScore

                    unexploredSet.append((fScore[node], node))

        unexploredSet = sorted(unexploredSet, key=lambda x: x[0])
        unexploredSet.reverse()
    return []

def heuristic(node, goal):
    return 3.5 * math.sqrt((node.data.x - goal.data.x)**2 + (node.data.y - goal.data.y)**2)