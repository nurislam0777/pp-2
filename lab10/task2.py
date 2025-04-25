import pygame
import psycopg2
from pygame.locals import *
import random
pygame.init()
screen = pygame.display.set_mode((1920,1080))
screen.fill((0,0,0))
len = 3
LEVEL = 0
WeightToColour = {1:(255,0,0),2:(0,255,0),3:(0,0,255)}
SCORE = 0
try:
    connection = psycopg2.connect(
    dbname="ex1",
    user="nurislambekbolat",
    password="",  # если не нужен пароль
    host="localhost",
    port="5432"
)

    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_score (
        name VARCHAR(100) UNIQUE,
        level INT,
        score INT
    );
    """
    cursor.execute(create_table_query)
except (Exception, psycopg2.Error) as error:
    print(f"Error connecting to the database: {error}")
def CreateFood(Needed):
    global FOOD
    for i in range(Needed):
        x,y = random.randint(200,1600),random.randint(200,880)
        while (True):
            NEAR = False
            for j in OBSTACLES:
                if abs(j[0]-x)<=15 and abs(j[1]-y)<=15:
                    NEAR = True
                    break
            for j in FOOD:
                if abs(j.pos[0]-x)<=15 and abs(j.pos[1]-y)<=15:
                    NEAR = True
                    break
            if abs(P.pos[0]-x)<=40 and abs(P.pos[1]-y)<=40:
                NEAR = True
            if (NEAR):
                x,y = random.randint(200,1600),random.randint(200,880)
            else: 
                break
        FOOD.add(Food(x,y,random.randint(1,3),random.randint(1000//timer*10,1000//timer*15)))
def Win(level = -1,score = -1):
    global LEVEL
    global SCORE
    LEVEL+=1
    if level != -1:
        LEVEL = level
        SCORE = score
    global timer
    timer=int(200/(1.1**(LEVEL-1)))
    pygame.time.set_timer(MOVE, timer)
    global OBSTACLES
    global P
    global len
    global FOOD
    P = Player()
    len = 3
    CreateFood(5)
    OBSTACLES.clear()
    for i in range(10*LEVEL):
        x,y = random.randint(200,1600),random.randint(200,880)
        while (True):
            NEAR = False
            for j in OBSTACLES:
                if abs(j[0]-x)<=15 and abs(j[1]-y)<=15:
                    NEAR = True
                    break
            for j in FOOD:
                if abs(j.pos[0]-x)<=15 and abs(j.pos[1]-y)<=15:
                    NEAR = True
                    break
            if abs(P.pos[0]-x)<=40 and abs(P.pos[1]-y)<=40:
                NEAR = True
            if NEAR:
                x,y = random.randint(200,1600),random.randint(200,880)
            else:
                break
        OBSTACLES.append((x,y))
def Draw():
    for i in FOOD:
        pygame.draw.rect(screen,WeightToColour[i.weight],(i.pos[0],i.pos[1],15,15))
    for i in OBSTACLES:
        pygame.draw.rect(screen,(202,204,206),(i[0],i[1],15,15))
class Food(pygame.sprite.Sprite):
    def __init__(self,x,y,w,time):
        super().__init__()
        self.weight = w
        self.pos = (x,y)
        self.timer = time
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.moved = False
        self.direction = (15,0)
        self.pos = (960,540)
        self.positions = [(960,540)]
    def move(self):
        global playing,SCORE
        self.moved = True
        self.pos = (self.pos[0]+self.direction[0],self.pos[1]+self.direction[1])
        if self.pos[0] > 1700 or self.pos[0] < 190 or self.pos[1] < 110 or self.pos[1] > 950:
            playing = False
        if self.pos in self.positions:
            playing = False
        for i in FOOD:
            i.timer-=1
            if abs(i.pos[0]-self.pos[0]) <= 15 and abs(i.pos[1]-self.pos[1]) <= 15:
                FOOD.remove(i)
                global len
                len += i.weight
                SCORE += i.weight
                if not FOOD:
                    Win()
            elif i.timer <= 0:
                FOOD.remove(i)
                CreateFood(1)
        for i in OBSTACLES:
            if abs(i[0]-self.pos[0]) <= 15 and abs(i[1]-self.pos[1]) <= 15:
                playing = False
        self.positions.append(self.pos)
        self.positions = self.positions[-len::]
        screen.fill((0,0,0))
        Draw()
        for i in self.positions:
            pygame.draw.rect(screen,(255,0,0),(i[0],i[1],14.5,14.5))
        score = pygame.font.SysFont("Verdana", 40).render(str(SCORE), True, (255,255,255))
        screen.blit(score,(200,100))
        level = pygame.font.SysFont("Verdana", 40).render(str(LEVEL), True, (255,255,255))
        screen.blit(level,(1700,100))
playing = True
P = Player()
timer = 200
MOVE = pygame.USEREVENT
FOOD = pygame.sprite.Group()
OBSTACLES = []
TIMER = pygame.time.Clock()
paused = 0
font = pygame.font.Font(None, 32)
def GET_INFO(user):
    cursor.execute("SELECT * FROM user_score WHERE name = '{}'".format(user))
    res = cursor.fetchone()
    if not res:
        return (1,0)
    cursor.execute("SELECT level FROM user_score WHERE name = '{}'".format(user))
    level = cursor.fetchone()[0]
    cursor.execute("SELECT score FROM user_score WHERE name = '{}'".format(user))
    score = cursor.fetchone()[0]
    return (level,score)
def SAVE(user,level,score):
    cursor.execute("DELETE FROM user_score WHERE name = '{}';".format(user))
    cursor.execute("INSERT INTO user_score VALUES ('{}' , {} , {});".format(user,level,score))
    connection.commit()
def get_input():
    input_text = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
        screen.fill((255, 255, 255))
        text_surface = font.render(input_text, True, (0, 0, 0))
        screen.blit(text_surface, (900, 500))
        pygame.display.flip()
user = get_input()
info = GET_INFO(user)
Win(info[0],info[1])
while (playing):
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == pygame.K_s:
                SAVE(user,LEVEL,SCORE)
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == K_ESCAPE:
                playing = False
            if event.key == K_RIGHT:
                if P.moved and P.direction != (-15,0):
                    P.direction = (15,0)
                    P.moved = False
            if event.key == K_LEFT:
                if P.moved and P.direction != (15,0):
                    P.direction = (-15,0)
                    P.moved = False
            if event.key == K_UP:
                if P.moved and P.direction != (0,15):
                    P.direction = (0,-15)
                    P.moved = False
            if event.key == K_DOWN:
                if P.moved and P.direction != (0,-15):
                    P.direction = (0,15)
                    P.moved = False
        if event.type == MOVE and not paused:
            P.move()
    pygame.display.flip()
