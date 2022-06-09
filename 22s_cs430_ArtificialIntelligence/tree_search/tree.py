#!/usr/bin/python

from collections import namedtuple as NT
from dataclasses import dataclass

C = NT("C", ["src", "dst", "cost"])

connections = [
        C("s", "a", 2),
        C("s", "c", 4),
        C("a", "b", 2),
        C("a", "g", 7),
        C("c", "b", 3),
        C("c", "g", 6),
        C("b", "g", 1)
        ]

"""
connections = {
        "s":{"a":2, "c":4},
        "a":{"b":2, "g":7},
        "c":{"b":3, "g":6},
        "b":{"g":1},
        "g":{}
        }
"""
@dataclass
class Connection:
    src: str
    dst: str
    cost:0
    total:0


class Nodes:
    def __init__(self, connections:list, mode:str):
        """  """
        self._funcs = {
            "bfs":self._breadth_step,
            "dfs":self._greedy_step,
            "djk":self._dijkstra_step
            }
        print("Starting node")
        if mode not in self._funcs.keys():
            raise ValueError("Only breadth first search (mode='bfs') and depth-first search (mode='dfs') are currently supported.")
        self._mode = mode
        self._current = ""
        self._connections = connections
        self._path = []
        self._frontier = []
        self._explored = []

    def _step(self, connection):
        """
        Take this connection and make its destination node the current node.
        Updates the path with the path taken to this
        """

        if new_node not in self._frontier:
            raise ValueError("Attempting to step to node not in the frontier!")
        #  Move to the new node
        self._current = new_node
        #  Set the new node to explored
        self._explored.append(new_node)
        #  Set the new frontier
        self._frontier += [n for n in self._nodes[new_node].keys()
                if n not in self._explored+self._frontier]
        if _debug: print(f"    Unexplored new frontier: {new_frontier}")
        if _debug: print(f"    Frontier now: {self._frontier}")


    def _dijkstra_step(self, current_node:str, _debug:bool=False):
        cur_min

        cur_min = 9999999
        min_choice = ""
        for n in self._frontier:
            if self._nodes[current_node][n] < cur_min:
                cur_min = self._nodes[current_node][n]
                min_choice = n
        return (
        if _debug:
            print(f"    Min choice is node {min_choice} with cost={cur_min}")

        new_explored = min_choice

        new_frontier = [ n for n in self._noews[new_explored].keys()
                if n not in self._explored ]
        self._frontier +=new_frontier
        self._explored.append(new_explored)
        if _debug: print(f"    Explored now: {self._explored}")
        return new_explored

    def _breadth_step(self, current_node:str, _debug:bool=False):
        new_explored = self._frontier.pop(0)
        if _debug: print(f"    Exploring {new_explored}")
        new_frontier = [ n for n in self._nodes[new_explored].keys()
                if n not in self._explored ]
        self._frontier += new_frontier
        if _debug: print(f"    Unexplored new frontier: {new_frontier}")
        if _debug: print(f"    Frontier now: {self._frontier}")
        self._explored.append(new_explored)
        if _debug: print(f"    Explored now: {self._explored}")
        return new_explored

    def _greedy_step(self, current_node:str, _debug:bool=False):
        new_explored = self._frontier.pop(len(self._frontier)-1)
        if _debug: print(f"    Exploring {new_explored}")
        new_frontier = [
                n for n in self._nodes[new_explored].keys()
                if n not in self._explored ]
        self._frontier += new_frontier
        if _debug: print(f"    New frontier: {new_frontier}")
        if _debug: print(f"    Frontier now: {self._frontier}")
        self._explored.append(new_explored)
        if _debug: print(f"    Explored now: {self._explored}")
        return new_explored

    def start(self, start_node:str, goal_node:str, _debug:bool=False):
        if _debug: print(f"Starting with node {start_node}")
        self._frontier.append(start_node)
        current_node = start_node
        steps = -1  # -1 since the first node load isn't a step.
        log = []
        while current_node != goal_node:
            steps+= 1
            new_node = self._funcs[self._mode](current_node, _debug=_debug)
            if _debug: print(f"{current_node} -> {new_node}    step: {steps}")
            log.append(new_node)
            current_node = new_node
        print(f"Step log: {log}")
        return steps

if __name__=="__main__":

    start = "s"
    goal = "g"

    #n = Nodes(nodes, "dfs")
    n = Nodes(connections, "djk")
    n.start(start, goal, _debug=True)
