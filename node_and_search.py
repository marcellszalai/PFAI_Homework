'''
Define nodes of search tree and vanilla bfs search algorithm

Author: Tony Lindgren
'''

import queue, time
from threading import Timer

class Node:
    '''
    This class defines nodes in search trees. It keep track of: 
    state, cost, parent, action, and depth 
    '''
    def __init__(self, state, cost=0, parent=None, action=None):
        self.parent = parent
        self.state = state
        self.action = action
        self.cost = cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1 
        self.statistics = {}

    def goal_state(self):
        return self.state.check_goal()
    
    def successor(self):
        successors = queue.Queue()
        for action in self.state.action:                     
            child = self.state.move(action)      
            if child != None:                                
                childNode = Node(child, self.cost + 1, self, action)              
                successors.put(childNode)
        return successors  

    def pretty_print_solution(self,verbose):

        if self.parent is not None: self.parent.pretty_print_solution(verbose)

        if self.action is not None: 
            print(self.action)

        elif self.statistics:
            print('----------------------------')
            for key in self.statistics:
                print(key, self.statistics[key])
            print('----------------------------')
        
        if verbose:
                print('----------------------------')
                print(' #miss on left bank: ', self.state.state[0][0])
                print(' #cann on left bank: ', self.state.state[0][1])
                print('            boat is: ', self.state.state[1])
                print('#miss on right bank: ', self.state.state[2][0])
                print('#cann on right bank: ', self.state.state[2][1])
                print('----------------------------')

        
             
class SearchAlgorithm:
    '''
    Class for search algorithms, call it with a defined problem 
    '''
    start_time = 0
    depth = 0
    number_of_nodes_explored = 0

    def __init__(self, problem):
        self.start = Node(problem)      
        
    def bfs(self, verbose = False, statistics = False):
        frontier = queue.Queue()
        frontier.put(self.start)
        visited_states = [self.start.state.state]
        stop = False
        self.start_time = time.process_time()


        while not stop:
            if frontier.empty():
                return None
            curr_node = frontier.get()
            if curr_node.goal_state():
                stop = True    
                if statistics:
                    self.statistics(self.start, curr_node)
                return curr_node        
                        
            successor = curr_node.successor()
            while not successor.empty():
                next_state = successor.get()
                self.number_of_nodes_explored += 1
                if next_state.state.state not in visited_states:
                    frontier.put(next_state)
                    visited_states.append(next_state.state.state)

    def dfs(self, verbose = False, statistics = False):
        frontier = queue.LifoQueue()
        frontier.put(self.start)
        visited_states = [self.start.state.state]
        stop = False
        self.start_time = time.process_time()


        while not stop:
            if frontier.empty():
                return None
            curr_node = frontier.get()
            if curr_node.goal_state():
                stop = True    
                if statistics:
                    self.statistics(self.start, curr_node)
                return curr_node        
                        
            successor = curr_node.successor()
            while not successor.empty():
                next_state = successor.get()
                self.number_of_nodes_explored += 1
                if next_state.state.state not in visited_states:
                    frontier.put(next_state)
                    visited_states.append(next_state.state.state)
    
    def statistics(self,root,goal):

        information = {
                "Elapsed time (s): " : 0,
                "Solution found at depth: " : 0,
                "Number of nodes explored: " : 0,
                "Cost of solution: " : 0,
                "Estimated effective branching factor: " : 0
            }

        information["Elapsed time (s): "] = round(time.process_time() - self.start_time,6)

        curr_node = goal
        self.depth += 1
        while curr_node.parent is not None:
            self.depth += 1
            curr_node = curr_node.parent

        information["Solution found at depth: "] = self.depth
        information["Number of nodes explored: "] = self.number_of_nodes_explored
        information["Cost of solution: "]  = self.depth
        information["Estimated effective branching factor: "] = self.number_of_nodes_explored * (1/self.depth)



        root.statistics = information


        return False
                    