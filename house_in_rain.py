from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random



rain_direction = 0.0
background_color = [1.0, 1.0, 1.0]
other_color = [0, 0, 0]
raindrops = []
max_press = 25 # left 0-25 and right 25-50

def draw_points(x, y, s = 5):
    glPointSize(s) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()

def draw_lines(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def draw_triangle(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()

def draw_rect(x1, y1, x2, y2, x3, y3, x4, y4):
    glBegin(GL_QUADS)
    glVertex2f(x1, y1) # bottom left
    glVertex2f(x2, y2) # bottom right
    glVertex2f(x3, y3) # top right
    glVertex2f(x4, y4) # top left
    glEnd()


def draw_rain():
    global raindrops
    glColor3f(0.6, 0.6, 1.0)
    for drop in raindrops:
        draw_points(drop[0], drop[1], 3)

def update_raindrops():
    global raindrops
    temp = []
    for drop in raindrops:
        new_x = drop[0] + rain_direction
        new_y = drop[1] - 1.0

        if(new_y > 40.0):
            if(new_y < 300):
                if(new_x < 200.0 or new_x > 615):
                    if(new_y > 0):
                        temp_tuple = (new_x, new_y)
                        temp.append(temp_tuple)
            else:
                if(new_x < 180.0 or new_x > 635):
                    if(new_y > 0):
                        temp_tuple = (new_x, new_y)
                        if(temp_tuple not in raindrops):
                            temp.append(temp_tuple)
                else:
                    border_y = new_y
                    if(new_x < 407.5):
                        border_y = 0.44 * new_x + 220.8
                    elif(new_x > 407.5):
                        border_y = -0.44 * new_x + 579.4
                    if(new_y > border_y):
                        if(new_y > 0):
                            temp_tuple = (new_x, new_y)
                            temp.append(temp_tuple)

             
    if(len(temp) < 1000):
        temp_tuple = (random.randint(-600, 1200), 600)
        temp.append(temp_tuple)

    raindrops = temp


def draw_house():
    global other_color
    glColor3f(*other_color)
    draw_rect(200.0, 40.0, 215.0, 40.0, 215.0, 300.0, 200.0, 300.0) #left side
    draw_rect(200.0, 40.0, 600.0, 40.0, 600.0, 55.0, 200.0, 55.0) # bottom side
    draw_rect(600.0, 40.0, 615.0, 40.0, 615.0, 300.0, 600.0, 300.0) # right side
    draw_triangle(180, 300, 635, 300, 407.5, 400) #outer triange
    glColor3f(0.54, 0.53, 0.57)
    draw_triangle(245, 315, 560, 315, 407, 380) #inner Triangle

    glColor3f(0.7, 0.7, 0.4)
    draw_rect(300.0, 55.0, 360.0, 55.5, 360.0, 170.0, 300.0, 170.0) #door

    glColor3f(0, 0, 0)
    draw_points(345.0, 110.0) #door lock

    glColor3f(0.7, 0.7, 0.4)
    draw_rect(500.0, 180.0, 550.0, 180.0, 550.0, 230.0, 500.0, 230.0) #window

    glColor3f(0, 0.6, 0)
    draw_rect(0.0, 0.0, 800.0, 0, 800.0, 40.0, 0.0, 40.0)#grass


def change_color(change):
    global background_color
    global other_color

    for i in range(3):
        new_background_color = background_color[i] + change
        new_other_color = other_color[i] - change

        if(new_background_color < 0.0):
            new_background_color = 0.0
        elif(new_background_color > 1.0):
            new_background_color = 1.0

        if(new_other_color < 0.0):
            new_other_color = 0.0
        elif(new_other_color > 1.0):
            new_other_color = 1.0  

        background_color[i] = new_background_color
        other_color[i] = new_other_color


def specialKeyListener(key, x, y):
    global max_press
    global rain_direction
    if(key==GLUT_KEY_LEFT):
        if(max_press > 0):
            rain_direction -= 0.03
            max_press -= 1
        else:
            max_press = 0
            
    if(key==GLUT_KEY_RIGHT):
        if(max_press < 50):
            rain_direction += 0.03
            max_press += 1
        else:
            max_press = 50

    if(key==GLUT_KEY_UP): #day to night
        change_color(-0.01)
    
    if(key == GLUT_KEY_DOWN): #night to day
        change_color(0.01)   



def iterate():
    glViewport(0, 0, 800, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 600, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glClearColor(*background_color, 1.0)
    draw_house()
    draw_rain()
    update_raindrops()
    glutSwapBuffers()
    glutPostRedisplay()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 600) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"House with Rain") #window name
glClearColor(*background_color, 1.0)

glEnable(GL_POINT_SMOOTH) #make the point rounded
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)

glutDisplayFunc(showScreen)
glutSpecialFunc(specialKeyListener)
glutMainLoop()