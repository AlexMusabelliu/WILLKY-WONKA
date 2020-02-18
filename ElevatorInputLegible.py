#Function giving the user the ability to give input
'''
Current progress:

>creating the act() function to simulate path movement and detect collision

'''
import math
from random import randint
def randmove():
    '''
    takes nothing, returns nothing
    calls Elev.move() for every elevator using start and finish parameters given through input in the function
    '''
    tok = 1
    global finish, start
    
    while tok == 1:
        try:
            elevChoice = randint(1, 3)
            if elevChoice not in range(1, 4):
                raise Exception
            tok = 0
        except:
            print("Try Again")
            
    tok = 1
      
    while tok == 1:
        start = chr(randint(97, 108))
        if start in "".join(Serv.allConn):
            tok = 0
        else:
          print('Try Again')
        
    tok = 1
    
    while tok == 1:
        finish = chr(randint(97, 108))
        if finish in "".join(Serv.allConn):
            tok = 0
        else:
            print('Try Again')
    # print(elevChoice - 1)
    allElev[elevChoice - 1].move(start, finish)
    
def xmove():
    '''
    takes nothing, returns nothing
    calls Elev.move() for every elevator using start and finish parameters given through input in the function
    '''
    tok = 1
    global finish, start
    
    while tok == 1:
        try:
            elevChoice = int(input('Which elevator?: '))
            if elevChoice not in range(1, 4):
                raise Exception
            tok = 0
        except:
            print("Try Again")
            
    tok = 1
      
    while tok == 1:
        start = input('Starting Point: ')
        if start in "".join(Serv.allConn):
            tok = 0
        else:
          print('Try Again')
        
    tok = 1
    
    while tok == 1:
        finish = input('Ending Point: ')
        if finish in "".join(Serv.allConn):
            tok = 0
        else:
            print('Try Again')
            
    allElev[elevChoice - 1].move(start, finish)

#Main server, currently only holds all possible connections (allConn) and all queued routes (allMove)
class Server():
    def __init__(self):
        DELAY_LENGTH = self.computeDelay()

        self.allMove = []
        self.allConn = ['ab', 'bc','ad','de','ef','ag', 'gh', 'hi', 'gj', 'jk', 'kl', 'be', 'cf', 'dj', 'ek', 'fl', 'il', 'hk', 'bh', 'ci']          
        # self.allDist = [(i % 10) + 1 for i in range(len(self.allConn))] * 2
        self.allDist = [1] * len(self.allConn) * 2
        # allDist = []
        self.allConn = self.allConn + [x[1] + x[0] for x in self.allConn]
        self.limbs = dict(zip(self.allConn, self.allDist))
        self.limbs.update({END_KEY:DELAY_LENGTH})
        print(self.limbs)

    def computeDelay(self):
        SECONDS_OF_DELAY = 7
        return SECONDS_OF_DELAY * MAX_V
        

def split(m):
    '''
    takes allMove, 
    returns an allMove split based on elev
    i.e. {1:(paths), 2:(paths), 3:(paths)}
    '''
    u = set([x[1] for x in m])
    mod = {}
    for x in m:
        mod.update({x[1]:mod.get(x[1], ()) + x[0]})
    return mod

def getMax(s):
    '''
    takes splitMove,
    returns maximum length of splitMove elev.
    i.e. a number
    '''
    mod = {}
    for x in s:
        mod.update({x:sum([Serv.limbs.get(y) for y in s.get(x)])})
    print(mod)
    return mod.get(max(mod, key = lambda x:mod.get(x)))
        
def act(allMove):
    '''
    takes all queued paths in the form of allMoves, which is formatted:
    (paths, elev number)
    returns a modified allMove with adjusted pathing for delays, if necessary
    '''
    DIST_FUNC = (lambda t: 0.5 * t**2)
    V_FUNC = (lambda t: 2 * DIST_FUNC(t) / t)
    T_FUNC = (lambda x: math.sqrt(2 * x))
    ACC = 1 #m / s

    splitMove = split(allMove) #dict
    maxLen = getMax(splitMove) #number
    totalTime = int(T_FUNC(maxLen)) # in s
    
    print(allMove)

    dMem = {} # {elev:(path, index, curTime, totTime)}
    dHist = {} #{elev:(path,)}

    usedPaths = {}

    for key in splitMove:
        path = splitMove.get(key)[0]
        dist = Serv.limbs.get(path)
        usedPaths.update({path:key})

        dMem.update({key:(path, 0, 0, dist)})

    for s in range(totalTime):
        for key in dMem:
            path, place, ti, df = dMem.get(key)
            di = DIST_FUNC(ti)

            if place == len(splitMove.get(key)) - 1:
                df = 0
                path = path[1] * 2

            elif di >= df:
                dHist.update({key:(usedPaths.pop(usedPaths.index(path))) + dHist.get(key, ())})
                place += 1
                path = splitMove.get(key)[place]
                df = Serv.limbs.get(path)
                ti = 0
                usedPaths.update({path:key})

            else:
                ti = s * 0.001
                
            #adds delay
            if path in usedPaths and usedPaths.get(path) != key:
                path = path[0] * 2
                ti = 0
                df = DIST_FUNC(1)
                print("ADDED DELAY")
                dHist.update({key:(path) + dHist.get(key, ())})

            dMem.update({key:(path, place, ti, df)})
    #TODO: test the program

    #return the updated path
    print(dHist)
    return dHist if dHist else allMove[-1]

#The actual elevator itself      
class Elevator():
    def __init__(self, num):
        self.num = num

    #movement function, returns path
    def move(self, start, end):
        '''
        take start, end points
        returns nothing
        appends paths to Serv.allMove (which contains all the queued connections)
        '''
        global ans
            
        pos = start
        potConn = [x for x in Serv.allConn if x[0] == pos]
        usedConn = [pos] + [x[1] for x in potConn]
        pos = []
        
        #gives the pos list all possible first connections as tuples
        for conn in potConn:
            #pos = ((AB), 0), where AB is a tuple
            pos.append(((conn,), 1))
        
        #while we haven't reached the end point...   
        while end not in usedConn:
            nupos = []
            
            #look at all the possible first moves...
            for (x, totMoves) in pos:
                #look at all the moves already used...
                for xconn in Serv.allConn:
                    curUsedPath = []
                    
                    #if our current connection that we are building is connceted, isn't used by another path, and isn't used by our own path,
                    #then add it to our list of paths
                    if xconn[0] == x[len(x) - 1][1] and xconn[1] not in usedConn and xconn not in curUsedPath:
                        #nupos = ((AB, BC), 1)
                        nupos.append(((pos[pos.index((x, totMoves))][0] + (xconn,)), totMoves + 1))
                        
                        usedConn.append(xconn[0])
                        
                        usedConn.append(xconn[1])
                        
            pos = nupos
            
        #sort our paths by weight    
        pos = sorted(pos, key=lambda x: x[1])
        
        #however, we still check to make sure all of the paths
        #actually reach the end point with this for loop
        for x in pos: 
            if x[0][len(x[0]) - 1][1] == end:
                pos.pop(pos.index(x))
                pos.insert(0, x)
        
        ans = pos[0]
        
        #delay if last move == another last move
        # for x in Serv.allMove:
        #     if ans[0][len(ans[0]) - 1][1] == x[0][len(x[0]) - 1][1] and len(ans[0]) == len(x[0]):
        #         ans = (((str(ans[0][0][0]) * 2,) + ans[0][0:len(ans[0]) - 1] + (ans[0][len(ans[0]) - 1],)), ans[1] + 1)
        

        tempMove = [x for x in Serv.allMove]
        tempMove.append((ans[0] + (END_KEY,), self.num))
        ans = act(tempMove)

        #if our path is nonexistant (i.e. a-a, which is a stall), then ans = (stall, len)
        if start == end:
            ans = ((start * 2,), 0)
        # print(ans)
        Serv.allMove.append((ans[0] + (END_KEY,), self.num))
        # print(ans[0])
        # print(ans)
        
#Constants 
allPoints = []
allPrint = []
character = ord('a') - 1  
CHAR_LIMIT = 11   
END_KEY = "end"
MAX_V = (550 * 1000) / 3600 #evaluates to 152.777...8 m/s
   
#Instanstialization              
Serv = Server()
Elev = Elevator(1)
Elev2 = Elevator(2)
Elev3 = Elevator(3)

# DELAY_LENGTH = Serv.delayLength

#Array containing the elevators
allElev = [Elev, Elev2, Elev3]

#Ask the user for input ad infinitum
# while True:
#     xmove()
#     print(Serv.allMove)
for x in range(4):
    xmove()