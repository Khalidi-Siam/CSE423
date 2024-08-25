from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

GLUT_BITMAP_HELVETICA_18 = ctypes.c_void_p(int(5))

width = 500
height = 600

diamond_x = random.randint(20, width - 20)
diamond_y = height - 40
diamond_speed = 0.3
diamond_color = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))

catcher_x = (width - 100) / 2
catcher_y = 0

score = 0
pause = False
game_over = False

life = 3
life_x = 70
life_y = height - 27.5



def draw_points(x, y, size = 1):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()

def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if(abs(dx) > abs(dy)):
        if(dx > 0 and dy >= 0):
            return 0
        elif(dx < 0 and dy >= 0):
            return 3
        elif(dx < 0 and dy <= 0):
            return 4
        else:
            return 7
    else:
        if(dx >= 0 and dy > 0):
            return 1
        elif(dx <= 0 and dy > 0):
            return 2
        elif(dx <= 0 and dy < 0):
            return 5
        else:
            return 6
        

def original_to_zone0(x, y, zone):
    if(zone == 0):
        return x, y
    elif(zone == 1):
        return y, x
    elif(zone == 2):
        return y, -x
    elif(zone == 3):
        return -x, y
    elif(zone == 4):
        return -x, -y
    elif(zone == 5):
        return -y, -x
    elif(zone == 6):
        return -y, x
    elif(zone == 7):
        return x, -y
    

def zone0_to_original(x, y, zone):
    if(zone == 0):
        return x, y
    elif(zone == 1):
        return y, x
    elif(zone == 2):
        return -y, x
    elif(zone == 3):
        return -x, y
    elif(zone == 4):
        return -x, -y
    elif(zone == 5):
        return -y, -x
    elif(zone == 6):
        return y, -x
    elif(zone == 7):
        return x, -y
    


def draw_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    x1, y1 = original_to_zone0(x1, y1, zone)
    x2, y2 = original_to_zone0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    y = y1

    for x in range(int(x1), int(x2) + 1):
        draw_x, draw_y = zone0_to_original(x, y, zone)
        draw_points(draw_x, draw_y)
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE


def draw_catcher(x, y):
    global game_over
    if(game_over == False):
        glColor3f(1.0, 1.0, 1.0)
    else:
        glColor3f(1.0, 0.0, 0.0)

    draw_line(x, y + 20, x + 100, y + 20) # upper -
    draw_line(x + 10, y, x + 90, y) # lower -
    draw_line(x, y + 20, x + 10, y) # \ left side
    draw_line(x + 90, y, x + 100, y + 20) # / right side


def draw_diamond(x, y):
    global game_over, diamond_color
    if(game_over):
        glColor3f(0, 0, 0)
    else:
        glColor3f(*diamond_color)

    draw_line(x, y, x + 10, y + 15) #upper /
    draw_line(x, y, x + 10, y - 15) #lower \
    draw_line(x + 10, y + 15, x + 20, y) # upper \
    draw_line(x + 10, y - 15, x + 20, y) # lower /


def draw_pause():
    glColor3f(1, 0.73, 0.2)

    if(pause == False):
        draw_line(width / 2 - 5, height - 15, width / 2 - 5, height - 40) #parallel line
        draw_line(width / 2 + 5, height - 15, width / 2 + 5, height - 40)

    else:
        draw_line(width / 2 - 5, height - 15, width / 2 - 5, height - 40) # vertical line
        draw_line(width / 2 - 5, height - 15, width / 2 + 15, height - 27.5) # upper \
        draw_line(width / 2 - 5, height - 40, width / 2 + 15, height - 27.5) #lower /
        

def draw_cancel():
    glColor3f(1, 0, 0)
    draw_line(width - 30, height - 15, width - 60, height - 40) # /
    draw_line(width - 60, height - 15, width - 30, height - 40) # \


def draw_restart():
    glColor3f(0, 0.7, 0.7)
    draw_line(20, height - 27.5, 50, height - 27.5) # horizontal line
    draw_line(20, height - 27.5, 30, height - 15) #up side
    draw_line(20, height - 27.5, 30, height - 40) #down side


def draw_button():
    draw_pause()
    draw_cancel()
    draw_restart()


def draw_life():
    global life, life_x, life_y
    glColor3f(0.0, 1.0, 0)    
    for i in range(life):
        draw_points(life_x + i * 10, life_y, 10)


def draw_score():
    global score, game_over
    if(game_over == False):
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(width - 200, height - 35)
        score_str = "Score: " + str(score)
        for char in score_str:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def draw_game_over():
    global score, game_over
    if(game_over):
        glColor3f(1.0, 0.0, 0.0)
        glRasterPos2f(width / 2 - 60, height/ 2 + 40)
        string = "GAME OVER!"
        for char in string:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(width / 2 - 30, height/ 2 + 10)
        score_str = "Score: " + str(score)
        for char in score_str:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))



def mouseListener(button, state, x, y):
    global catcher_x, catcher_y, diamond_x, diamond_y, diamond_color, diamond_speed
    global score, game_over, pause, life

    if(button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
        y = height - y
        if(y >= height - 40 and y <= height - 15):
            if(x >= 20 and x <= 40):
                print("Starting over")
                diamond_x = random.randint(20, width - 20)
                diamond_y = height - 40
                diamond_speed = 0.3
                diamond_color = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))
                catcher_x = (width - 100) / 2
                catcher_y = 0

                pause = False
                game_over = False
                score = 0
                life = 3

            elif(x >= width / 2 - 5 and x <= width / 2 + 15):
                if(pause == False):
                    pause = True
                else:
                    pause = False

            elif(x >= width - 60 and x <= width - 30):
                print("Good bye Your score :", score)
                glutLeaveMainLoop()


def specialKeyListener(key, x, y):
    global catcher_x, pause, game_over

    if(game_over == False and pause == False):
        if(key == GLUT_KEY_LEFT):
            catcher_x -= 20
            if(catcher_x < 5):
                catcher_x = 5
        elif(key == GLUT_KEY_RIGHT):
            catcher_x += 20
            if(catcher_x > width - 105):
                catcher_x = width - 105



def update_ground():
    global diamond_x, diamond_y, diamond_speed, diamond_color, catcher_x, catcher_y
    global score, pause, game_over, life

    if(game_over == False and pause == False):
        diamond_y -= diamond_speed
        if((diamond_x >= catcher_x - 10 and diamond_x <= catcher_x + 110) and (diamond_y >= catcher_y and diamond_y <= catcher_y + 30)):
            score += 1
            print(f'Score: {score}')
            diamond_x = random.randint(20, width - 20)
            diamond_y = height - 40
            if(diamond_speed >= 2.0):
                diamond_speed = 2.0
            else:
                diamond_speed += 0.1
            diamond_color = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))

        if(diamond_y < 0):
            life -= 1
            if(life <= 0):
                game_over = True
                print(f'Game Over! Score: {score}')

            else:
                diamond_x = random.randint(20, width - 20)
                diamond_y = height - 40
                diamond_speed = 0.3
                diamond_color = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))
           


def iterate():
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_button()
    draw_score()
    draw_life()
    draw_catcher(catcher_x, catcher_y)
    draw_diamond(diamond_x, diamond_y)
    draw_game_over()
    update_ground()
    glutSwapBuffers()
    glutPostRedisplay()


glutInit()
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Catch the Diamonds")
glClearColor(0.0, 0.0, 0.0, 1.0)
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutMouseFunc(mouseListener)
glutSpecialFunc(specialKeyListener)
glEnable(GL_POINT_SMOOTH) #make the point rounded
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
glutMainLoop()