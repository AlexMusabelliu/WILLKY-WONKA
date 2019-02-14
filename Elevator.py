from turtle import Turtle, Screen
from random import randint
#Finds shortest available path for one elevator: |*|
#Finds shortest available path for multiple elevators: |*|
#Adds delay to command to prevent bumping with more than minEdge(n) elevators: |*|
#Able to queue command: | |
#---STAGE 2---
#Works with different weights: | |
#


t = Turtle('circle')
t2 = Turtle('circle')
t3 = Turtle('circle')

t.ht()
t2.ht()
t3.ht()

s = Screen()
s.tracer(False)

allPoints = []
character = ord('a') - 1

def quit():
    s.bye()

def startup():
    global Serv, character
    tpoints = [(-100,100), (100,100), (100,-100), (-100, -100), (-100,100)]
    tt = [t,t2,t3]
    
    for x in tt:
        x.penup()
        x.goto(-100,100)
        x.pendown()
    
    for y in range(5):
        for x in range(3):
            s1 = tt[x]
        
            s1.goto(tpoints[y][0] * (x + 1), tpoints[y][1] * (x + 1))
                
            allPoints.append((s1.stamp(), (s1.xcor(), s1.ycor())))
            
            
            character += 1
            
            
            
            s1.color('red')
            
            
            #s1.write(chr(character), False, align='center', font=('comic sans', 12, 'bold'))
            s1.color('black')
            
        tt[0].goto(tpoints[y][0] * (3), tpoints[y][1] * (3))
            
        tt[0].goto(tpoints[y][0] * (1), tpoints[y][1] * (1))
    
    s.update()
        
    t.penup()
    
    xmove()

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
        #start = chr(randint(97, 108))
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
    
class Server():
    def __init__(self):
        self.allConn = ['ab', 'bc','ad','de','ef','ag', 'gh', 'hi', 'gj', 'jk', 'kl', 'be', 'cf', 'dj', 'ek', 'fl', 'il', 'hk', 'bh', 'ci',
                        'ba','cb','da','ed','fe','ga', 'hg', 'ih', 'jg', 'kj', 'lk', 'eb', 'fc', 'jd', 'ke', 'lf', 'li', 'kh', 'hb', 'ic']
        self.allMove = []
        
class Elevator():
    def move(self, start, end):
        global ans
            
        pos = start
        
        potConn = [x for x in Serv.allConn if x[0] == pos]
        
        usedConn = [pos] + [x[1] for x in potConn]
        
        pos = []
        
        for conn in potConn:
            #pos = ((AB), 0), where AB is a tuple
            pos.append(((conn,), 1))
            
        while end not in usedConn:
            nupos = []
            
            
            for (x, totMoves) in pos:
                for xconn in Serv.allConn:
                    #print(Serv.allMove)
                    curUsedPath = []
                    for zed in Serv.allMove:
                        try:
                            curUsedPath.append(zed[0][len(x[0]) - 1])
                        except:
                            pass
                    #print(Serv.allMove)
                    #print(curUsedPath)    
                    if xconn[0] == x[len(x) - 1][1] and xconn[1] not in usedConn and xconn not in curUsedPath:
                        #nupos = ((AB, BC), 1)
                        nupos.append(((pos[pos.index((x, totMoves))][0] + (xconn,)), totMoves + 1))
                        
                        usedConn.append(xconn[0])
                        
                        usedConn.append(xconn[1])
                        
            pos = nupos
            
        pos = sorted(pos, key=lambda x: x[1])
        
        for x in pos: 
            if x[0][len(x[0]) - 1][1] == end:
                pos.pop(pos.index(x))
                pos.insert(0, x)
        
        ans = pos[0]
       # print(ans[0][0:len(ans[0]) - 1], (str(ans[0][len(ans[0]) - 2][1]) * 2,), ans[0][len(ans[0]) - 1])
        #delay if last move == another last move
        for x in Serv.allMove:
            if ans[0][len(ans[0]) - 1][1] == x[0][len(x[0]) - 1][1] and len(ans[0]) == len(x[0]):
                ans = (((str(ans[0][0][0]) * 2,) + ans[0][0:len(ans[0]) - 1] + (ans[0][len(ans[0]) - 1],)), ans[1])
        
        #remove our path from our allConn
        if start == end:
            ans = ((start * 2,), 0)
        
        Serv.allMove.append(ans)

        #print(ans)  
        return(ans)
        
Serv = Server()
Elev = Elevator()
Elev2 = Elevator()
Elev3 = Elevator()

allElev = [Elev, Elev2, Elev3]
      
s.listen()
s.onkey(quit,'Escape')
#startup()

allPrint = []
first = [chr(randint(0, 12) + ord('a')), chr(randint(0, 12) + ord('a')), chr(randint(0, 12) + ord('a'))]
#print(chr(11 + ord('a')))
#print(first)
for x in range(5):
    for y in range(3):
        
        last = chr(randint(0, 12) + ord('a'))
        
        #print(first[y], last)
        allPrint.append((y + 1, allElev[y].move(first[y], last)))
        
        first[y] = last
#print(allPrint)    
for x in allPrint:
    print(x)
  