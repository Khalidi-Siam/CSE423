from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import math

def set_enemy_color():
    return (random.uniform(0.6, 0.9), random.uniform(0.6, 0.9), random.uniform(0.6, 0.9))

def set_enemy_pos():
    enemy_x = random.randint(enemy_radius, width - enemy_radius)
    enemy_y = height - (button_section_height + enemy_radius)
    return enemy_x, enemy_y


GLUT_BITMAP_HELVETICA_18 = ctypes.c_void_p(int(5))
width = 500
height = 700
button_section_height = 80

catcher_radius = 20
catcher_x = (width // 2) - (catcher_radius // 2) #catcher radius 20
catcher_y = catcher_radius

enemy_radius = 20
enemy_position = []
# enemy_x, enemy_y = set_enemy_pos()
enemy_speed = []
enemy_color = []

spawn_interval = 0
last_spawn_time = 0


score = 0
pause = False
game_over = False

life = 3
life_x = width - 65
life_y = height - button_section_height + 18

shooter_active = False
shooter_x = 0
shooter_y = 0
shooter_speed = 3
shooter_radius = 5



def draw_points(x, y, size = 2):
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


def draw_circle(x_center, y_center, r):
    x = 0
    y = r
    d = 1 - r
    circlePoints(x_center, y_center, x, y)

    while(x < y):
        if(d < 0): #choose E
            d += 2 * x + 3
            x += 1

        else: #choose SE
            d += 2 * x - 2 * y + 5
            x += 1
            y -= 1

        circlePoints(x_center, y_center, x, y) 



def circlePoints(x_center, y_center, x, y):
    draw_points(x + x_center, y + y_center)
    draw_points(y + x_center, x + y_center)
    draw_points(y + x_center, -x + y_center)
    draw_points(x + x_center, -y + y_center)
    draw_points(-x + x_center, -y + y_center)
    draw_points(-y + x_center, -x + y_center)
    draw_points(-y + x_center, x + y_center)
    draw_points(-x + x_center, y + y_center)



def draw_catcher(x, y):
    global game_over
    if(game_over == False):
        glColor3f(1.0, 1.0, 1.0)
    else:
        glColor3f(1.0, 0.0, 0.0)

    draw_circle(x, y, 20)


def draw_enemy(x, y):
    global game_over
    if(game_over):
        glColor3f(0, 0, 0)
    # else:
    #     glColor3f(*enemy_color)

    draw_circle(x, y, enemy_radius)

def draw_shooter(x, y):
    global shooter_active, game_over
    if(game_over or shooter_active == False):
        glColor3f(0, 0, 0)
    else:
        glColor3f(1, 0, 0)

    draw_circle(x, y, shooter_radius)


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
    draw_button_section_background()
    draw_pause()
    draw_cancel()
    draw_restart()


def draw_button_section_background():
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(0, height - button_section_height)  # Bottom left
    glVertex2f(width, height - button_section_height)  # Bottom right
    glVertex2f(width, height)  # Top right
    glVertex2f(0, height)  # Top left
    glEnd()


def draw_life():
    global life, life_x, life_y
    glColor3f(0.0, 1.0, 0)    
    for i in range(life):
        draw_points(life_x + i * 19, life_y, 15)


def draw_score():
    global score, game_over
    if(game_over == False):
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(15, height - button_section_height + 10)
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


def calc_distance(catcher_x, catcher_y, enemy_x, enemy_y):
    return math.sqrt((catcher_x - enemy_x) ** 2 + (catcher_y - enemy_y) ** 2)


def update_ground():
    global enemy_position, enemy_speed, enemy_color, catcher_x, catcher_y, last_spawn_time
    global score, pause, game_over, life
    global shooter_active, shooter_x, shooter_y, shooter_speed

    if(game_over == False and pause == False):
        current_time = glutGet(GLUT_ELAPSED_TIME)
        if(current_time - last_spawn_time > spawn_interval):
            enemy_position.append(set_enemy_pos())
            enemy_speed.append(0.3)
            enemy_color.append(set_enemy_color())
            last_spawn_time = current_time

        if(shooter_active):
            shooter_y += shooter_speed 
            if(shooter_y > height - button_section_height):
                shooter_active = False
                shooter_x, shooter_y = 0, 0

        for i in range(len(enemy_position) - 1, -1, -1):
            enemy_x, enemy_y = enemy_position[i]
            enemy_y -= enemy_speed[i]
            enemy_position[i] = (enemy_x, enemy_y)

            if(shooter_active):
                distance = calc_distance(shooter_x, shooter_y, enemy_x, enemy_y)
                if(distance <= shooter_radius + enemy_radius):
                    score += 1

                    # if(enemy_speed[i] >= 1.0):
                    #     enemy_speed[i] = 1.0
                    # else:
                    #     enemy_speed[i] += 0.1
                    enemy_position.remove(enemy_position[i])
                    enemy_speed.remove(enemy_speed[i])
                    enemy_color.remove(enemy_color[i])


                    shooter_active = False
                    # enemy_x, enemy_y = set_enemy_pos()
                    # enemy_color = set_enemy_color()
                    continue

            distance = calc_distance(catcher_x, catcher_y, enemy_x, enemy_y)
            if(distance <= catcher_radius + enemy_radius):
                game_over = True
                life = 0
                # enemy_x, enemy_y = set_enemy_pos()
                print(f'Game Over! Score: {score}')
                reset()
                
            elif(enemy_y < 0):
                life -= 1
                if(life <= 0):
                    game_over = True
                    # enemy_x, enemy_y = set_enemy_pos()
                    print(f'Game Over! Score: {score}')
                    reset()

                else:
                    enemy_position.remove(enemy_position[i])
                    enemy_speed.remove(enemy_speed[i])
                    enemy_color.remove(enemy_color[i])
            
def reset():
    global enemy_position, enemy_color, enemy_speed, last_spawn_time, spawn_interval
    global score, game_over, pause, life, shooter_active, shooter_speed, shooter_x, shooter_y
    global catcher_x, catcher_y, catcher_radius, width

    enemy_position = []
    enemy_speed = []
    enemy_color = []
    if(game_over == False):
        last_spawn_time = glutGet(GLUT_ELAPSED_TIME)
        score = 0
        life = 3
        game_over = False
        pause = False
        shooter_active = False
        shooter_x = 0
        shooter_y = 0 

        catcher_x = (width // 2) - (catcher_radius // 2) #catcher radius 20
        catcher_y = catcher_radius  
        spawn_interval = 0


def mouseListener(button, state, x, y):
    # global catcher_x, catcher_y, enemy_x, enemy_y, enemy_color, enemy_speed
    global score, game_over, pause, life

    if(button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
        y = height - y
        if(y >= height - 40 and y <= height - 15):
            if(x >= 20 and x <= 50):
                print("Starting over")
                reset()

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
            if(catcher_x < catcher_radius):
                catcher_x = catcher_radius
        elif(key == GLUT_KEY_RIGHT):
            catcher_x += 20
            if(catcher_x > width - catcher_radius):
                catcher_x = width - catcher_radius


def keyboardListener(key, x, y):
    global catcher_x, catcher_y, pause, game_over, shooter_x, shooter_y, shooter_active

    if(game_over == False and pause == False):
        if(key == b'a'):
            catcher_x -= 20
            if(catcher_x < catcher_radius):
                catcher_x = catcher_radius
        elif(key == b"d"):
            catcher_x += 20
            if(catcher_x > width - catcher_radius):
                catcher_x = width - catcher_radius

        elif(key == b" " and shooter_active == False):
            shooter_x = catcher_x
            shooter_y = catcher_y + catcher_radius
            shooter_active = True



def iterate():
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global spawn_interval, shooter_x, shooter_y, catcher_x, catcher_y
    global enemy_position, enemy_color, enemy_speed
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_button()
    draw_score()
    draw_life()
    # draw_circle(width // 2, height // 2, 20)
    draw_catcher(catcher_x, catcher_y)
    # draw_enemy(enemy_x, enemy_y)
    draw_shooter(shooter_x, shooter_y)
    for i in range(len(enemy_position)):
        enemy_x, enemy_y = enemy_position[i]
        glColor3f(*enemy_color[i])
        draw_enemy(enemy_x, enemy_y)
        spawn_interval = 1500

    draw_game_over()
    update_ground()
    glutSwapBuffers()
    glutPostRedisplay()


glutInit()
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Shoot The Circle")
glClearColor(0.0, 0.0, 0.0, 1.0)
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutMouseFunc(mouseListener)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)
glEnable(GL_POINT_SMOOTH) #make the point rounded
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
glutMainLoop()