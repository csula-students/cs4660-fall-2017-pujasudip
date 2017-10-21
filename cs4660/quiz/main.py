"""
quiz2!
Use path finding algorithm to find your way through dark dungeon!
Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9
TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json
import codecs

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
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urlopen(req, jsondataasbytes)
    reader = codecs.getreader('utf-8')
    return json.load(reader(response))


def bfs(init_node, dest_node):
    """
    Breadth First Search
    queries the game to do search from the init_id to dest_id
    returns a list of actions going from the init_id to dest_id
    """
    cost = {}
    cost[init_node['id']] = 0

    parent = {}
    edges = {}

    que = []
    que.append((0, init_node['id']))

    while len(que) != 0:
        dq_id = que.pop()[1]
        neighbors = get_state(dq_id)['neighbors']

        for i in range(len(neighbors)):
            single_nb = neighbors[i]
            if single_nb['id'] not in cost:
                edge = transition_state(dq_id, single_nb['id'])
                edges[single_nb['id']] = edge
                cost[single_nb['id']] = cost[dq_id] + 1
                parent[single_nb['id']] = dq_id

                if single_nb['id'] != dest_node['id']:
                    que.append((cost[single_nb['id']], single_nb['id']))

        que = sorted(que, key=lambda x: x[0])
        que.reverse()

    path = []
    node_id = dest_node['id']

    while node_id in parent:
        path.append(edges[node_id])
        node_id = parent[node_id]

    path.reverse()
    return path


def dijkstra(init_node, dest_node):
    """
    Dijkstra Search
    queries the game to do search from the init_node to dest_node
    returns a list of actions going from the init_node to dest_node
    """
    cost = {}
    cost[init_node['id']] = 0

    parent = {}
    edges = {}

    que = []
    que.append((0, init_node['id']))
    visited = []

    while len(que) != 0:
        dq_id = que.pop()[1]
        visited.append(dq_id)
        neighbors = get_state(dq_id)['neighbors']

        for i in range(len(neighbors)):
            single_nb_id = neighbors[i]['id']
            edge = transition_state(dq_id, single_nb_id)
            alt = cost[dq_id] + edge['event']['effect']

            if single_nb_id not in visited and (single_nb_id not in cost or alt > cost[single_nb_id]):
                if single_nb_id in cost:
                    que.remove((cost[single_nb_id], single_nb_id))
                que.append((alt, single_nb_id))

                cost[single_nb_id] = alt
                parent[single_nb_id] = dq_id
                edges[single_nb_id] = edge

        que = sorted(que, key=lambda x: x[0])

    path = []
    node_id = dest_node['id']

    while node_id in parent:
        path.append(edges[node_id])
        node_id = parent[node_id]

    path.reverse()
    return path

def printAllActions(actionList, initNode_id):
    previous_id = initNode_id
    sum = 0
    for action in range(len(actionList)):
        previous_node = get_state(previous_id)
        next_id = actionList[action]['id']
        sum += actionList[action]['event']['effect']

        print("%s(%s):%s(%s):%i"%(
            previous_node['location']['name'],
            previous_id, actionList[action]['action'],
            actionList[action]['id'], actionList[action]['event']['effect']))

        previous_id = next_id
    print("\nTotal hp: ", sum)


if __name__ == "__main__":
    # Your code starts here
    s_id = '7f3dc077574c013d98b2de8f735058b4'
    e_id = 'f1f131f647621a4be7c71292e79613f9'
    start_empty_room = get_state(s_id)
    dest_dark_room = get_state(e_id)
    # print(start_empty_room)
    # print(transition_state(start_empty_room['id'], start_empty_room['neighbors'][1]['id']))

    print("BFS Path:\n")
    route_bfs = bfs(start_empty_room, dest_dark_room)
    printAllActions(route_bfs, s_id)
    print("\n")
    print("Dijkstra Path:\n")
    route_dfs = dijkstra(start_empty_room, dest_dark_room)
    printAllActions(route_dfs, s_id)