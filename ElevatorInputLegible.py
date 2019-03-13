#Function giving the user the ability to give input
def xmove():
    tok = 1
    global finish, start
    
    while tok == 1:
        try:
            elevChoice = int(input('Which elevator?: '))
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
        self.allConn = ['ab', 'bc','ad','de','ef','ag', 'gh', 'hi', 'gj', 'jk', 'kl', 'be', 'cf', 'dj', 'ek', 'fl', 'il', 'hk', 'bh', 'ci',
                        'ba','cb','da','ed','fe','ga', 'hg', 'ih', 'jg', 'kj', 'lk', 'eb', 'fc', 'jd', 'ke', 'lf', 'li', 'kh', 'hb', 'ic']
        self.allMove = []

#The actual elevator itself      
class Elevator():
    #movement function, returns path
    def move(self, start, end):
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
        for x in Serv.allMove:
            if ans[0][len(ans[0]) - 1][1] == x[0][len(x[0]) - 1][1] and len(ans[0]) == len(x[0]):
                ans = (((str(ans[0][0][0]) * 2,) + ans[0][0:len(ans[0]) - 1] + (ans[0][len(ans[0]) - 1],)), ans[1] + 1)
        
        #remove our path from our allConn
        if start == end:
            ans = ((start * 2,), 0)
        
        Serv.allMove.append(ans)
        print(ans)
        
#Constants 
allPoints = []
allPrint = []
character = ord('a') - 1  
CHAR_LIMIT = 11   
   
#Instanstialization              
Serv = Server()
Elev = Elevator()
Elev2 = Elevator()
Elev3 = Elevator()

#Array containing the elevators
allElev = [Elev, Elev2, Elev3]

#Ask the user for input ad infinitum
while True:
    xmove()