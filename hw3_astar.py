from queue import PriorityQueue as priorityq
import time

from copy import deepcopy
start_time = time.time()
end_time=0


class Node(object):
    
    def __init__(self, puzzle, move,parent=None,depth=0):
        self.puzzle = puzzle
        self.move = move
        self.parent = parent
        self.depth=depth
        self.count_transport=0
    def __lt__(self,other): 
        return 0

    def solvable(self):
        inversions = 0
        for i in range(9):
            for j in range(i+1,9):
                if self.puzzle[i//3][i%3]==0 or self.puzzle[j//3][j%3]==0:
                    continue
                if self.puzzle[i//3][i%3]>self.puzzle[j//3][j%3]:
                    inversions+=1
        if inversions%2==0:
            return True
        else:
            return False
    
    def find_zero(self):
        for i in range(3):
            for j in range(3):
                if self.puzzle[i][j] == 0:
                    return i,j
    
    def manhattan_distance(self):
        total = 0
        for i in range(3):
            for j in range(3):
                row = int(self.puzzle[i][j]/3)
                column = int(self.puzzle[i][j]%3)
                total += abs(i-row)+abs(j-column)
        return total
 
    def reversing_path(self):
        path = []
        path.append((self.move,self.puzzle))
        state = self.parent
        while state.parent is not None:
            path.append((state.move,state.puzzle))
            state = state.parent
        path.append((state.move,state.puzzle))
        path.reverse()
        return path    
 
    
    def moving_action(self):
        zero_place = self.find_zero() 
        board = self.puzzle 
        allnodes = [] 
        if not zero_place[0]-1<0: 
            move_up = deepcopy(board) 
            move_up[zero_place[0]][zero_place[1]] = move_up[zero_place[0]-1][zero_place[1]] 
            move_up[zero_place[0]-1][zero_place[1]] = 0 
            move_up_node = Node(move_up,'down',self,self.depth+1)
            allnodes.append(move_up_node) 
        if zero_place[0]+1<3: 
            move_down = deepcopy(board)
            move_down[zero_place[0]][zero_place[1]] = move_down[zero_place[0]+1][zero_place[1]] 
            move_down[zero_place[0]+1][zero_place[1]] = 0 
            move_down_node = Node(move_down, 'up',self,self.depth+1)
            allnodes.append(move_down_node)
        if not zero_place[1]-1<0: 
            move_left = deepcopy(board)
            move_left[zero_place[0]][zero_place[1]] = move_left[zero_place[0]][zero_place[1]-1] 
            move_left[zero_place[0]][zero_place[1]-1] = 0 
            move_left_node = Node(move_left,'right',self,self.depth+1)
            allnodes.append(move_left_node)
        if zero_place[1]+1<3: 
            move_right = deepcopy(board)
            move_right[zero_place[0]][zero_place[1]] = move_right[zero_place[0]][zero_place[1]+1] 
            move_right[zero_place[0]][zero_place[1]+1] = 0 
            move_right_node = Node(move_right,'left',self,self.depth+1)
            allnodes.append(move_right_node)
        
        return allnodes
    


      
initial_state = Node([[3,1,2],[0,5,8],[4,6,7]],'start')
initial_table = [[3,1,2],[0,5,8],[4,6,7]]
goal= [[0,1,2],[3,4,5],[6,7,8]]
print(initial_state)
print(' initial state of 8_puzzle :')
def A_star(initial_node):
    frontier = priorityq() 
    explored_set = []
    number_visited = 0
    function_g=0
    global x
    x=0
    frontier.put((initial_state.manhattan_distance(),initial_state)) 
    function_g+=1
    while not frontier.empty():  
       huristic, node = frontier.get() 
       huristic = node.manhattan_distance()
       if node.puzzle in explored_set:   
           continue
       if huristic==0: 
           print('The numbered of explored set:',number_visited)
           path_puzzle(node.reversing_path())
           
           return None
       
       explored_set.append(node.puzzle)
       
       number_visited+=1
       x+=1

       for child in node.moving_action(): 
           frontier.put((child.manhattan_distance()+child.depth,child))
             

def solvable():  
  priority = 0
  for i in range(9):
    for j in range(i + 1, 9):
      if initial_table[i // 3][i % 3] == 0 or initial_table[j // 3][j % 3] == 0:
        continue
      if  initial_table[i // 3][i % 3] > initial_table[j // 3][j % 3]:
        priority += 1
  if priority % 2 == 0:
    return True
  else:
    return False

        
def path_puzzle(path):
    movement=0
    for solution in path:
        movement+=1
        print(solution[0])
        draw_puzzle(solution[1])
        
    print('\n')    
    print('END OF A* ALGORITHM') 
    print('Number of displacements:',movement)
    print('explored_set :',x)

 
def draw_puzzle(board):
    print('\n')
    for i in board:
        print((i[0],i[1],i[2]))    

if solvable():
#    print('4 DEPTH',initial_state.depth)
    A_star(initial_state)
    end_time=time.time()
    print("--- %s seconds is this runtime ---" % (end_time - start_time))    
    

else :
    print(" ERRORE: ( not solvable)" )