from random import randint
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline

def getRandom():
    '''
    takes nothing, returns nothing
    calls Elev.move() for every elevator using start and finish parameters given through input in the function
    '''
    
    elev = randint(1, 3)
    start = chr(randint(97, 108))
    finish = chr(randint(97, 108))
    while finish == start:
        finish = chr(randint(97,108))
    
    return elev, start, finish
    
def getInput():
    '''
    takes nothing, returns nothing
    calls Elev.move() for every elevator using start and finish parameters given through input in the function
    '''
    
    while True:
        elev = int(input('Which elevator?: '))
        if elev in range(1, 4):
            break
        print("Try again")
 
    while True:
        start = input('Starting Point: ')
        if start in "".join(vn):
            break
        print('Try Again')
        
    while True:
        finish = input('Ending Point: ')
        if finish in "".join(sv.allConn):
            break
        print('Try Again')
            
    return elev, start, finish
    
#Main server, currently only holds all possible connections (allConn) and all queued routes (allMove)

class Server():
    def __init__(self):
        DELAY_LENGTH = self.computeDelay()
        self.frequencies = {}
        self.allMove = []
        self.allConn = ['ab', 'bc','ad','de','ef','ag', 'gh', 'hi', 'gj', 'jk', 'kl', 'be', 'cf', 'dj', 'ek', 'fl', 'il', 'hk', 'bh', 'ci']          
        self.allDist = [(i % 10) + 1 for i in range(len(self.allConn))] * 2
        # self.allDist = [1] * len(self.allConn) * 2
        # allDist = []
        self.allConn = self.allConn + [x[1] + x[0] for x in self.allConn]
        self.limbs = dict(zip(self.allConn, self.allDist))
        self.limbs.update({END_KEY:DELAY_LENGTH})
        # print(self.limbs)

    def computeDelay(self):
        SECONDS_OF_DELAY = 7
        return SECONDS_OF_DELAY * MAX_V



#movement function, returns path
def shortest_path(num, start, end):
    '''
    take start, end points
    returns nothing
    appends paths to s.allMove (which contains all the queued connections)
    '''

    if start == end:
        ans = ((start * 2,), 0)
        return ans

    pos = start
    potConn = [x for x in sv.allConn if x[0] == pos]
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
            for xconn in sv.allConn:
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

    #if our path is nonexistant (i.e. a-a, which is a stall), then ans = (stall, len)
    return ans

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
    # print("MOD:", mod)
    return mod

def getMax(s):
    '''
    takes splitMove,
    returns maximum length of splitMove elev.
    i.e. a number
    '''
    mod = {}
    for x in s:
        mod.update({x:sum([sv.limbs.get(y) for y in s.get(x)])})
    # print(mod)
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
    totalTime = int(T_FUNC(maxLen)) * 1000# in ms
    
    # print(allMove)

    dMem = {} # {elev:(path, index, curTime, totTime)}
    dHist = {} #{elev:(path,)}

    usedPaths = {}

    for key in splitMove:
        path = splitMove.get(key)[0]
        dist = sv.limbs.get(path)
        usedPaths.update({path:key, path[::-1]:key})

        dMem.update({key:(path, 0, 0, dist)})

    for s in range(totalTime):
        for key in dMem:
            path, place, ti, df = dMem.get(key)
            di = DIST_FUNC(ti)
            # print("DMEM: ", dMem, "\n", "DHIST: ", dHist, "\n", "PATH: ", path, sep="", end="\n-------\n")
            if place == len(splitMove.get(key)) - 1:
                df = 0
                path = path[1] * 2

            elif di >= df:
                # print(usedPaths)
                # dHist.update({key:(path, place) + dHist.get(key, ())})
                try:
                    usedPaths.pop(path)
                    usedPaths.pop(path[::-1])
                except:
                    pass
                place += 1
                path = splitMove.get(key)[place]
                df = sv.limbs.get(path)
                ti = 0
                usedPaths.update({path:key, path[::-1]:key})

            else:
                ti = s
                
            #adds delay
            if path in usedPaths and usedPaths.get(path) != key:
                path = path[0] * 2
                ti = 0
                df = DIST_FUNC(1)
                # print("ADDED DELAY")
                dHist.update({key:(path, place) + dHist.get(key, ())})

            dMem.update({key:(path, place, ti, df)})
    #TODO: test the program

    #return the updated path
    # print(dHist)
    return dHist

def _delay(moves, fmoves):
    # moves = tuple(zip(moves.keys(), moves.values()))
    # print("MOVES: ", moves)
    # print("UNSPLIT FMOVES: ", fmoves)
    fmoves = split(fmoves)
    # print("FMOVES: ", fmoves)
    for elev in moves:
        path = list(fmoves.get(elev))
        delays = moves.get(elev)
        for delay, i in [(delays[x], delays[x + 1]) for x in range(0, len(delays) // 2, 2)]:
            path.insert(int(i), delay)
        fmoves.update({elev:path})
    return fmoves         

def delay(fmoves):
    moves = act(fmoves)
    return _delay(moves, fmoves)

def accumulate(path):
    path = path[0]
    # print("PATH",path)
    legs = {}
    for x in path:
        if x[::-1] in sv.frequencies:
            x = x[::-1]
        legs.update({x:1 + sv.frequencies.get(x, 0)})
    sv.frequencies.update(legs)

def graph(freq):
    x1 = [x for x in freq]
    y1 = [freq.get(x) for x in x1]
    plt.scatter(x1, y1)

    x = np.linspace(0, len(freq) - 1, len(freq))
    spl = make_interp_spline(x, y1, k=3)
    line = spl(np.linspace(0, len(freq) - 1, len(freq) * 2))

    # plt.plot(line, label="")
    plt.plot(x, y1)
    plt.title("Random generated data")

    axes = plt.gca()
    axes.set_xlim([0, len(freq)])
    plt.show()

def main(rep=1):
    allMoves = []
    
    for _ in range(rep):
        elev, start, finish = getRandom()
        # print(elev, start, finish)
        sp = shortest_path(elev, start, finish)
        allMoves.append(sp)
        accumulate(sp)
    
    allMoves = delay(allMoves)
    # print(len(allMoves))
    # print(allMoves)
    print(sv.frequencies)
    graph(sv.frequencies)
    # print(sv.allConn)
    # print(sv.allDist) #print distances n shieeeeeeeeet


#globals
END_KEY = "end"
MAX_V = (550 * 1000) / 3600 #evaluates to 152.777...8 m/s

if __name__ == "__main__":
    sv = Server()
    main(1000)
