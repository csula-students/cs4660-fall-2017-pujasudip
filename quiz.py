"""
quiz2!
Use path finding algorithm to find your way through dark dungeon!
Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9
TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)

def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.
    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = json.load(urlopen(req, jsondataasbytes))
    return response


def neighbors(self, node):
    nb = []
    if node in self.nodes:
        for edge in self.edges:
            if edge.from_node == node:
                nb.append(edge.to_node)
    return nb

def distance(self, node_1, node_2):
    for edge in self.edges:
        if edge.from_node == node_1 and edge.to_node == node_2:
            return edge
    return None

def bfs(initial_node, dest_node):
    path = []
    que = []
    que.append(initial_node)

    while len(que) != 0:
        u = que.pop(0)

        if u not in path:
            path.append(u)

            if u['id'] == dest_node['id']:
                return path

            for i in range(len(u['neighbors'])):
                que.append(u['neighbors'][i])




    # cost = {}
    # parentNode = {}
    # edge = {}
    #
    # que = []
    # que.append((0, initial_node))
    #
    # cost[initial_node['id']] = 0
    #
    # while len(que) > 0:
    #     u = que.pop()[1]
    #
    #     for node in neighbors(u):
    #         if node not in cost:
    #             edge[node] = distance(u, node)
    #             cost[node] = cost[u] + edge[node].weight
    #             parentNode[node] = u
    #
    #             if node['id'] != dest_node['id']:
    #                 que.append((cost[node], node))
    #
    #     que = sorted(que, key=lambda x: x[0])
    #     que.reverse()
    #
    # path = []
    # end_node = dest_node

    # while end_node in parentNode:
    #     path.append(edge[end_node])
    #     end_node = parentNode[end_node]
    #
    # path.reverse()
    #
    # return path

def dijkstra(initial_node, dest_node):
    cost = {}
    parentNode = {}
    edge = {}

    cost[initial_node] = 0

    que = []
    que.append((0, initial_node))

    while len(que) > 0:
        u = que.pop()[1]

        for v in neighbors(u):
            edge = distance(u, v)
            alt = cost[u] + edge.weight

            if v not in cost or alt < cost[v]:
                if v in cost:
                    que.remove((cost[v], v))
                que.append((alt, v))

                cost[v] = alt
                parentNode[v] = u
                edge[v] = edge

        que = sorted(que, key=lambda x: x[0])
        que.reverse()

    path = []
    current_node = dest_node

    while current_node in parentNode:
        path.append(edge[current_node])
        current_node = parentNode[current_node]

    path.reverse()

    return path



if __name__ == "__main__":
    # Your code starts here
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    dest_room = get_state('f1f131f647621a4be7c71292e79613f9')
    # print(empty_room)
    # print(dest_room)
    # print(transition_state(empty_room['id'], empty_room['neighbors'][0]['id']))
    print(bfs(empty_room, dest_room))
    print(dijkstra(empty_room, dest_room))
