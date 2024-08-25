from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
# import time
import math



width, height = 800, 600


points = []
point_speeds = []
point_colors = []
point_directions = []


speed = 0.05
blink = False
frozen = False


def detect_collisions(): #detect collision between two points and reverse their direction
    global points, point_directions   
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            x1, y1 = points[i]
            x2, y2 = points[j]
            dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            
            if(dist < 3):
                c_x, c_y = point_directions[i]
                point_directions[i] = (-c_x, -c_y)
                
                c_x, c_y = point_directions[j]
                point_directions[j] = (-c_x, -c_y)


def draw_points():
    glPointSize(4)
    global blink

    if(blink):
        glColor3f(0.0, 0.0, 0.0)
        for i in range(len(points)):
            x, y = points[i]
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()
    else:
        for i in range(len(points)):
            x, y = points[i]
            color = point_colors[i]
            glColor3f(color[0], color[1], color[2])
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()
    

def update_points():
    global points
    for i in range(len(points)):
        if(not frozen):
            x, y = points[i]
            c_x, c_y = point_directions[i]
            points[i] = (x + (c_x * speed), y + (c_y * speed))
            if(x + (c_x * speed) < 0 or x + (c_x * speed) > 800):
                point_directions[i] = (-c_x, c_y)
            if(y + (c_y * speed) < 0 or y + (c_y * speed) > 600):
                point_directions[i] = (c_x, -c_y)

    detect_collisions()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_points()
    update_points()
    glutSwapBuffers()
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global blink
    if(button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not frozen):
        if (0 < x < 800 and 0 < (height - y) < 600):
            points.append((x, height - y))
            point_speeds.append(speed)
            point_colors.append((random.random(), random.random(), random.random()))
            point_directions.append((random.choice([-1, 1]), random.choice([-1, 1])))
    elif(button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not frozen):
        blink = True
        glutTimerFunc(100, stop_blink, 0)

def stop_blink(val):
    global blink
    blink = False

def keyboardListener(key, x, y):
    global speed, frozen
    if(key == GLUT_KEY_UP):
        if(speed >= 1): #avoid infinite speed
            speed = 1
        else:
            speed += 0.01
    elif(key == GLUT_KEY_DOWN):
        if(speed <= 0.01): #avoid freeze
            speed = 0.01
        else:
            speed -= 0.01

    elif(key == b" "):
        frozen = not frozen


glutInit()
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Amazing Box")
glClearColor(0.0, 0.0, 0.0, 1.0)
glOrtho(0.0, 800, 0.0, 600, 0.0, 1.0)
glutDisplayFunc(display)

glEnable(GL_POINT_SMOOTH) #make the point rounded
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)

glutMouseFunc(mouseListener)
glutSpecialFunc(keyboardListener)
glutKeyboardFunc(keyboardListener)
glutMainLoop()

