
class Connection:
    def __init__(self, src=None, dst=None, cost:int=None):
        self._src=src
        self._dst=dst
        self._cost=cost

    @property
    def cost(self):
        """ Returns the integer cost of this connection """
        return self._cost

    @property
    def dst(self):
        """ Returns a reference to the Node this connection is to."""
        return self._dst

    @property
    def src(self):
        """ Returns a reference to the Node this connection is from."""
        return self._src

    @dst.setter
    def dst(self, dst):
        """ Set the destination Node of this connection """
        self._dst = dst

    @src.setter
    def src(self, src):
        """ Set the source Node of this connection """
        self._src = src

    @cost.setter
    def cost(self, cost):
        """ Set the path cost of this connection """
        self._cost = cost

    def __str__(self):
        basestr = f"{self._src.name} - {self._dst.name}"
        basestr += f" cost={self._cost}" if self._cost != None else ""
        return basestr

class Node:
    """
    A Node represents a named Node in a graph, which may have a cost attribute
    between connections. It holds a list of its "children" Nodes' IDs and
    respective connection costs, and can be marked as the child
    """
    def __init__(self, name):
        self._name=name
        self._connections=[]
        #  Path cost will remain None until
        self._path_cost=None
        self._parent=None
        self._explored=False
        self._observed=False

    @property
    def name(self):
        """ Returns the string ID (name) of this Node """
        return self._name

    @property
    def parent(self):
        """
        Returns the string ID of the parent Node connected to this Node
        """
        return self._parent

    @property
    def explored(self) -> bool:
        """
        Returns a bool indicating whether this node has been explored by a
        search. If this node is explored,  it will have a least-expensive path
        through a configured parent and connected nodes are either in the
        observed list or already explored.
        """
        return self._explored

    @property
    def path_cost(self):
        """
        The total cost of the cheapest known path to this node.
        This value is first established when the node is added to
        the observed list..

        If no costs are configured, this value will be None.
        """
        if not self._path_cost:
            raise ValueError(f"Path cost requested for Node {self._name},"+
                    " but no cost has been set for this Node.")
        return self._path_cost

    def __str__(self):
        """ String representation of this Node """
        my_str = f"\n\nNode={self._name}, path_cost={self._path_cost}"
        my_str += "\nConnections:"
        my_cons = [ f"\n\t{self._name} - {c.dst.name} cost={c.cost}"
                for c in self._connections ]
        for s in my_cons:
            my_str+=s
        return my_str

    def get_connections(self, by_cost:bool=False):
        """ Returns tuple of all configured Connection objects. """
        if by_cost:
            return tuple(sorted(self._connections, key=lambda c: c.cost)
        return tuple(self._connections)

    def explore(self, parent, path_cost:int=None):
        """
        @:param parent      The parent Node object observing this Node
        @:param path_cost   Total path cost of the cheapest currently known
                            path to this Node from the source node. If this
                            is not a cost-driven tree, path_cost will default
                            to None.

        "Visit" this Node and mark it as explored. Exploring this Node will
        add all of its
        """
        print("Exploring {self._name} from parent {parent.name}")
        self._explored = True

        #  Observe all of this Node's connections.
        for c in self._connections:
            print("\tObserving {c.dst.name} with connection cost {c.cost}")
            c.dst.observe(parent=self,
                path_cost=self._path_cost+c.cost
                if self._path_cost != None else None)

        #  Set the new path cost and parent.
        self._path_cost = path_cost
        self._parent = parent

    def connect(self, connection:Connection):
        """
        @:param connection: A Connection object from this Node to a child
                            which may have an associated Cost.
        """
        if connection.src.name != self._name:
            raise ValueError(f"Connection {connection} doesn't have node"+
                    " {self._name} as a source!")
        else:
            self._connections.append(connection)

    def observe(self, parent, path_cost:int=None):
        """
        @:param parent      The parent Node object observing this Node
        @:param path_cost   Total path cost of the cheapest currently known
                            path to this Node from the source node. If this
                            is not a cost-driven tree, path_cost will default
                            to None.

        When a Node is observed, its path to an explored node has been
        discovered by the provided parent, but the node hasn't neccesarily
        been explored yet.

        After a Node has been observed, it should always have a parent as long
        as the graph is running, even though its parent may change. The Node
        should also remain observed for its entire lifetime.

        If this Node has been observed before and the new path cost is less
        than the previous path cost, switch the parent/path to the new ones.
        """
        if not self._parent:
            self._path_cost = path_cost
            self._parent = parent
        else:
            #  Only switch paths if the new path is better
            if self._path_cost > path_cost:
                self._path_cost = path_cost
                self._parent = parent
        self._observed = True

class Graph:
    """
    Acts as an interface class for a cost-directed graph, offering methods
    for getting nodes' connections (including costs), setting the
    """
    def __init__(self, connections:tuple):
        """
        @:param connections:    tuple with nested 3-tuples or 2-tuples defined
                                to represent the source, destination, and cost
                                of a route in the form (src, dest, cost), or
                                (src, dest) if it's not a cost-directed graph.


        Set up the graph for analysis or use with search algorithms by
        initializing all Nodes and Connections.
        """
        self._nodes = {}
        self._connections = self._make_graph(connections)

    def _make_graph(self, connections:list):
        if len(connections[0]) == 2:
            sources, destinations = tuple(zip(*connections))[:2]
            cost = (None for i in range(len(sources)))
            connections = tuple(zip(sources, destinations, cost))

        for src, dst, cost in connections:
            #  Make nodes in this connection if they don't exist
            #  and point the connection to the two nodes.
            new_connection = Connection()
            new_connection.cost = cost
            if src in self._nodes.keys():
                new_connection.src = self._nodes[src]
            else:
                self._nodes.update({src:Node(src)})
                new_connection.src = self._nodes[src]
            if dst in self._nodes.keys():
                new_connection.dst = self._nodes[dst]
            else:
                self._nodes.update({dst:Node(dst)})
                new_connection.dst = self._nodes[dst]

            #  Give the new source Node the new connection with a reference to
            #  its child node and the cost.
            self._nodes[src].connect(new_connection)
        print(*self._nodes.values())

    def visit(self, connection:Connection):
        src_id = connection.src.name
        node_id = connection.dst.name
        if node_id not in self._nodes.keys():
            raise ValueError(f"Attempting to visit unknown node {node_id}")
        node = self._nodes[node_id]
        if node.explored:
            raise ValueError(
                    f"Attempting to visit already-explored node {node_id}")
        if not node.observed:
            raise ValueError(f"Attempting to visit unobserved node {node_id}")
        connection.dst.explore(connection.src, connection.cost)

class SearchGraph(Graph):
    """
    Represents a graph capable of running multiple search algorithms on
    user-defined cost tree.

    Currently Supported:
     - Breadth-First Search (BFS)         : run_bfs(start, goal)
     - Depth-First Search (DFS)           : run_dfs(start, goal)
     - Uniform Cost Dijkstra's algorithm  : run_ucs(start, goal)
    """
    def __init__(self, nodes:list):
        super().__init__(nodes)

    @property
    def frontier(self):
        return [ n for n in self._nodes.values()
                if n.observed and not n.explored]

    @property
    def explored(self):
        return [ n for n in self._nodes.values()
                if n.explored ]

    def djikstra_step(self):
        for n in self.explored:
            pass


if __name__=="__main__":
    connections = (
            ("S", "a", 2),
            ("S", "c", 4),
            ("a", "b", 2),
            ("a", "G", 7),
            ("c", "b", 3),
            ("c", "G", 6),
            ("b", "G", 1),
            )
    G = Graph(connections)
