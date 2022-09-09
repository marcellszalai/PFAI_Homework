'''
Define nodes of search tree and vanilla bfs search algorithm

Author: Tony Lindgren
'''

import queue

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
    def __init__(self, problem):
        self.start = Node(problem)        
        
    def bfs(self):
        frontier = queue.Queue()
        frontier.put(self.start)
        visited_states = [self.start]
        stop = False
        while not stop:
            if frontier.empty():
                return None
            curr_node = frontier.get()
            if curr_node.goal_state():
                stop = True    
                return curr_node        
                        
            successor = curr_node.successor() 
            while not successor.empty():
                frontier.put(successor.get())
                    