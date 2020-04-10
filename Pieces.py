from tabulate import tabulate
from pprint import pprint
import itertools
##import codecs
##import sys 
##UTF8Writer = codecs.getwriter('utf8')
##sys.stdout = UTF8Writer(sys.stdout)
tabulate.PRESERVE_WHITESPACE = True
def m(x1,y1,x2,y2,current):
    if GB[y1][x1].move(y2,x2,GB,current):
        GB[y1][x1], GB[y2][x2] = Null(), GB[y1][x1]
        return True
    else:
        return False
def check(gb,current,side):
    if side == 'white':
        i=king_black
    else:
        i=king_black
    for j in GB:
        for k in j:
            if i.side !=k.side and k.side != 'nothing':
                if k.isPossible(i.y,i.x,GB,current):
                    return f'Check by {k.side} {k.shape} {k.x , k.y}'


def win(gb):
    present = [False,False]
    important=[king_white,king_black]
    for i in important:
        for j in gb:
            if i in j:
                present[important.index(i)]=True
                break

    return not(present[0] and present[1])

def createp(side):
    z=1
    k=0
    if side=='white':
        z=6
        k=7
    x=[Pawn(i,z,side) for i in range(8)]
    globals()[f'king_{side}']=King(3,k,side)
    y=[Rook(0,k,side),Knight(1,k,side),Bishop(2,k,side),globals()[f'king_{side}'],Queen(4,k,side),
       Bishop(5,k,side),Knight(6,k,side),Rook(7,k,side)]
    if side=='black':
        return [y]+[x]
    return [x]+[y]

def CreateGB():
    return createp('black') + [[Null() for _ in range(8)] for _ in range(4)] + createp('white')

def vertical(y1,y2,x,gb):
    z=1
    if y2-y1 < 0:
        y1, y2= y2,y1
        
    #flag=True
    #print(str((x1,y1)) + ' to ' + str((x2,y2)))
    for i in range(y1+z,y2):
        if gb[i][x].side != 'nothing':
            print('Error')
            return False
    return True

def horizontal(x1,x2,y,gb):
    z=1
    if x2-x1 < 0:
        x1, x2= x2,x1
    print(str((x1,y1)) + ' to ' + str((x2,y2)))
    for i in range(x1+z,x2):
        if gb[y][i].side != 'nothing':
            print('Error')
            return False
    return True

def diagonal(x1,y1,x2,y2,gb):
    
    if x2-x1 > 0 and y2-y1>0:
        kx=ky=1     
        
    elif x2-x1 > 0 and y2-y1<0:
        kx=1
        ky=-1
        
    elif x2-x1 < 0 and y2-y1<0:
        kx=-1
        ky=-1
        
    elif x2-x1 < 0 and y2-y1>0:
        kx=-1
        ky=1
    distance = pow((abs(y2 - y1)**2 + abs(x2 - x1)**2 )/2,0.5)
    print(distance.is_integer())
    if distance.is_integer():
        for i in range(1,int(distance)):
            if gb[y1 + ky*i][x1 + kx*i].side !='nothing':
                print('Error')
                return False
        return True
    return False
        
class Null:
    def __init__(self):
        self.side='nothing'

    def __repr__(self):
        return '   '


class BasicPieces:
    def __init__(self,y,x,side):
        self.x=x
        self.y=y
        self.side=side

    def move(self,y,x,GB,current):
        if self.isPossible(y,x,GB,current):
            #GB[self.y][self.x]=Null()
            self.x=x
            self.y=y
            return True
        return False
    def isPossible(self,y,x,GB,current):
        pass

    def __repr__(self):
        return self.shape

class Pawn(BasicPieces):
    def __init__(self,y,x,side):
        super().__init__(x,y,side)
        if side=='white':
            self.shape='♙'
        else:
            self.shape='♟'

        self.moves=1

    def isPossible(self,y,x,GB,current):
        if 0 <= x < 8 and 0 <= y < 8:
            if  abs(y-self.y) == 2 and abs(self.x - x) == 0:
                print('True')
                if self.moves == 1 and vertical(self.y,y,x,GB):
                    self.moves+=1
                    print('True')
                    return True
                return False
            
            elif abs(y-self.y) == 1 and abs(self.x - x) == 0:
                if GB[y][x].side == 'nothing':
                    self.moves+=1
                    return True
                return False
            
            elif abs(y-self.y) ==1 and abs(self.x - x) == 1:
                if GB[y][x].side not in ['nothing',self.side]:
                    self.moves+=1
                    return True
                return False
            return False
        return False

class Knight(BasicPieces):
    def __init__(self,y,x,side):
        super().__init__(x,y,side)
        if side=='white':
            self.shape='♘'
        else:
            self.shape='♞'

    def isPossible(self,y,x,GB,current):
        if 0 <= x < 8 and 0 <= y < 8:
            if abs(self.x-x) in [1,2] and abs(self.y-y) in [1,2]:
                if GB[y][x].side != self.side:
                    return True
                return False
            return False
        return False

class Bishop(BasicPieces):
    def __init__(self,y,x,side):
        super().__init__(x,y,side)
        if side=='white':
            self.shape='♗'
        else:
            self.shape='♝'
            
    def isPossible(self,y,x,GB,current):
        if 0 <= x < 8 and 0 <= y < 8:
            self.distance=pow((abs(self.y - y)**2 + abs(self.x - x)**2 )/2,0.5)
            if pow((abs(self.y - y)**2 + abs(self.x - x)**2 )/2,0.5).is_integer():
                #print(y,x)
                if GB[y][x].side != self.side and diagonal(self.x,self.y,x,y,GB):
                    return True
            return False
        return False

class Rook(BasicPieces):
    def __init__(self,y,x,side):
        super().__init__(x,y,side)
        if side=='white':
            self.shape=u'♖'
        else:
            self.shape=u'♜'
            
    def isPossible(self,y,x,GB,current):
        if 0 <= x < 8 and 0 <= y < 8:
            if  abs(self.y - y) and abs(self.x - x) == 0:
                if GB[y][x].side != self.side and vertical(self.y,y,x,GB):
                    return True
            
            elif abs(self.y - y) == 0 and abs(self.x - x):
                if GB[y][x].side != self.side and horizontal(self.x,x,y,GB):
                    return True
                
            return False
        return False

class Queen(BasicPieces):
    def __init__(self,y,x,side):
        super().__init__(x,y,side)
        if side=='white':
            self.shape='♕'
        else:
            self.shape='♛'
            
    def isPossible(self,y,x,GB,current):
        if 0 <= x < 8 and 0 <= y < 8:
            if  abs(self.y - y) and abs(self.x - x) == 0:
                if GB[y][x].side != self.side and vertical(self.y,y,x,GB):
                    return True
            
            elif abs(self.y - y) == 0 and abs(self.x - x):
                if GB[y][x].side != self.side and horizontal(self.x,x,y,GB):
                    return True
            elif pow((abs(self.y - y)**2 + abs(self.x - x)**2 )/2,0.5).is_integer():
                #print(y,x)
                if GB[y][x].side != self.side and diagonal(self.x,self.y,x,y,GB):
                    return True
            return False
        return False

class King(BasicPieces):
    def __init__(self,y,x,side):
        super().__init__(x,y,side)
        if side=='white':
            self.shape=u'♔'
        else:
            self.shape=u'♚'
            
    def isPossible(self,y,x,GB,current):
        if 0 <= x < 8 and 0 <= y < 8:
            if  abs(self.y - y) == 1 and abs(self.x - x) == 0:
                if GB[y][x].side != self.side:
                    return True
            
            elif abs(self.y - y) == 0 and abs(self.x - x) == 1:
                if GB[y][x].side != self.side:
                    return True
            elif ((abs(self.y - y)**2 + abs(self.x - x)**2 )**0.5)/2 == 0.7071067811865476:
                if GB[y][x].side != self.side:
                    return True
            return False
        return False



def p():
    
    print(tabulate(GB,[str(i) for i in range(8)],'pretty',showindex="always", colalign="left"))

play = True
while play:
    game_won=False
    global GB
    GB=CreateGB()
    player_choice=itertools.cycle(['white','black'])
    global moves
    moves={'white':1,'black':1}
    while not game_won:
        current_player = next(player_choice)
        print(f"Current player {current_player} - moves = {moves[current_player]}")
        played=False
        p()
        while not played:
            x1=int(input('X1 > '))
            y1=int(input('Y1 > '))
            x2=int(input('X2 > '))
            y2=int(input('Y2 > '))
            if GB[y1][x1].side == current_player:
                if m(x1,y1,x2,y2,moves[current_player]):
                    break
                else:
                    p()
            else:
                print('Its not your piece')

        if win(GB):
            game_won=True
            print('won')
        else:
            moves[current_player]+=1
            print(check(GB,moves[current_player],current_player))
            continue
        
