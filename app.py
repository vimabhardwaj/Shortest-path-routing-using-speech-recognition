from decimal import Decimal
import pandas as pd

# ---------------------------------------------------------------------------------------


import speech_recognition as sr

# r = sr.Recognizer()
# with sr.Microphone() as source:
#     print("Speak your source location and destination location")
#     audio = r.listen(source)
#     try:
#         text = r.recognize_google(audio)
#         print(" {}".format(text))
#     except:
#         print("Sorry could not recognize what you said")

# ---------------------------------------------------------------------------------------

class Node:
    def __init__(self, label):
        self.label = label

class Edge:
    def __init__(self, to_node, length):
        self.to_node = to_node
        self.length = length


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = dict()

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, from_node, to_node, length):
        edge = Edge(to_node, length)
        if from_node.label in self.edges:
            from_node_edges = self.edges[from_node.label]
        else:
            self.edges[from_node.label] = dict()
            from_node_edges = self.edges[from_node.label]
        from_node_edges[to_node.label] = edge


def min_dist(q, dist):
    """
    Returns the node with the smallest distance in q.
    Implemented to keep the main algorithm clean.
    """
    min_node = None
    for node in q:
        if min_node == None:
            min_node = node
        elif dist[node] < dist[min_node]:
            min_node = node

    return min_node

INFINITY = Decimal('Infinity')

def dijkstra(graph, source):
    q = set()
    dist = {}
    prev = {}

    for v in graph.nodes:       # initialization
        dist[v] = INFINITY      # unknown distance from source to v
        prev[v] = INFINITY      # previous node in optimal path from source
        q.add(v)                # all nodes initially in q (unvisited nodes)

    # distance from source to source
    dist[source] = 0

    while q:
        # node with the least distance selected first
        u = min_dist(q, dist)

        q.remove(u)

        if u.label in graph.edges:
            for _, v in graph.edges[u.label].items():
                alt = dist[u] + v.length
                if alt < dist[v.to_node]:
                    # a shorter path to v has been found
                    dist[v.to_node] = alt
                    prev[v.to_node] = u

    return dist, prev


def to_array(prev, from_node):
    """Creates an ordered list of labels as a route."""
    previous_node = prev[from_node]
    route = [from_node.label]
    while previous_node != INFINITY:
        route.append(previous_node.label)
        temp = previous_node
        previous_node = prev[temp]

    route.reverse()
    return route

graph = Graph()
dict_of_nodes={}
type_of_input=int(input("Do you want to add places manually or through file? \n Press 1 for manual entry \n Press 2 for adding a csv file \n pn:The csv file must contain three columns having 'source','dest' and 'dist' as column names \n "))
if type_of_input == 2:
    path=input("Enter path of file: ")
    df=pd.read_csv(path)
    print(df)
    list_of_places=list(df['source'])+list(df['dest'])
    for place in set(list_of_places):
        node_temp=Node(place)
        dict_of_nodes[place]=node_temp
        graph.add_node(node_temp)

    for i,row in df.iterrows():
        graph.add_edge(dict_of_nodes[row['source']],dict_of_nodes[row['dest']],int(row['dist']))
        graph.add_edge(dict_of_nodes[row['dest']],dict_of_nodes[row['source']],int(row['dist']))
elif type_of_input == 1:
    while True:
        print("enter the places. Type exit when done")
        node_name=input()
        if node_name == "exit":
            break
        node_temp=Node(node_name)
        dict_of_nodes[node_name]=node_temp
        graph.add_node(node_temp)

    while True:
        print("enter the places and distance between them. Type exit when done")
        node1=input()
        if node1 == "exit":
             break
        node2=input()
        dist=int(input())
        graph.add_edge(dict_of_nodes[node1], dict_of_nodes[node2],dist)
        graph.add_edge(dict_of_nodes[node2], dict_of_nodes[node1],dist)

while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak your source location")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            source = text
            print(" {}".format(text))
        except:
            print("Sorry could not recognize what you said")
    r = sr.Recognizer()
    with sr.Microphone() as dest:
        print("Speak your destination location")
        audio = r.listen(dest)
        try:
            text = r.recognize_google(audio)
            dest = text
            print(" {}".format(text))
        except:
            print("Sorry could not recognize what you said")
    print("The source and the destination are : " + source + " " + dest)
    dist, prev = dijkstra(graph, dict_of_nodes[source])

    print("The quickest path from {} to {} is [{}] with a distance of {}".format(
        source,
        dest,
        " -> ".join(to_array(prev, dict_of_nodes[dest])),
        str(dist[dict_of_nodes[dest]])
        )
    )
    exit_s=input("DO YOU WANT TO RUN AGAIN. PRESS Y OR N: ")
    if exit_s.lower()=='n':
        break
