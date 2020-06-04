import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(0,255,0)):
        self.pos = start
        self.dirnx = 1 #to move initialy 
        self.dirny = 0
        self.color = color     
    def move(self, dirnx, dirny):
        """to move snake"""
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)#changing positions

    def draw(self, surface, eyes=False):
        dis = (self.w // self.rows) #distance between rows to draw objects onto screen
        i = self.pos[0] #row
        j = self.pos[1] #column

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2)) #drawing cube on the screen
        
        if eyes: #to draw eyes in the head of the snake
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        



class snake(object):
    body = [] #snake body that will store small cube objects 
    turns = {} #dictionary to store head value at every turn
    def __init__(self, color, pos):
        """snake initialization"""
        self.color = color
        self.head = cube(pos) #stores head of snake IMPORTANT
        self.body.append(self.head) #adds head to snake body
        self.dirnx = 0 # X direction
        self.dirny = 1 # Y direction

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed() #pygame action for key being pressed

            '''In pygame top left corner is 0,0 
                so for left we do -1
                    for right 1
                    for up -1
                    for down 1'''


            for key in keys:
                if keys[pygame.K_LEFT]: #left turn
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] #dictionary stores list of x,y

                elif keys[pygame.K_RIGHT]: #right turn
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]: #move up
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]: #move down
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] 

        for i, c in enumerate(self.body): #check positions in body
            p = c.pos[:]
            if p in self.turns: #check if position is in turns dictionary , only then turn
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p) #if last cube at turn remove from list
            else:
                #if snake reaches edge of screen
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])#positions set
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny) #to move to set positions
        

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1


    def addCube(self):
        """find out where cube is being addedd"""
        tail = self.body[-1] #tail where new cube gets added
        dx, dy = tail.dirnx, tail.dirny

        """find out direction in which snake is moving 
            and add cube according to direction of movement"""


        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        #updated coordinates
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        

    def draw(self, surface): #draws snake into 
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    """to draw whole  grid strucuture"""
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        #line color-white                         #start  end
       # pygame.draw.line(surface, (255,255,255), (x,0),  (x,w)) #vertical
        #pygame.draw.line(surface, (255,255,255), (0,y),  (w,y)) #horizontal
        

def redrawWindow(surface):
    """Used to update window after every mover"""
    global rows, width, s, snack
    surface.fill((0,0,0)) # fill whole window with black colour
    s.draw(surface) #put snake in window
    snack.draw(surface) #put snack in window
    drawGrid(width,rows, surface) #draw grid structure
    pygame.display.update() #displays updated window


def randomSnack(rows, item):
    """generate food for the snake at random positions"""
    positions = item.body

    while True:
        #randomly generate coordinates
        x = random.randrange(rows)
        y = random.randrange(rows)

        #to make sure snack doesnt go on top of the snake
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)


def message_box(subject, content):
    """displays score in the end"""
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    #setting size of display window
    width = 500 
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((0,255,0), (1,1))
    snack = cube(randomSnack(rows, s), color=(255,0,0)) #snack is a cube object 
    flag = True

    clock = pygame.time.Clock()
    
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos: #if head hits snack increase length of snake
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(255,0,0))

        #if the snake hits itself then end game
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('Score is ',len(s.body) )
                message_box('You Lost!', 'Play again...')
                s.reset((10,10))
                break

            
        redrawWindow(win)

main()