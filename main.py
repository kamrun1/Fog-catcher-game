from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

player_x = 250
fall_x = random.randint(50, 450)
fall_y = 500
score = 0
speed = 5
game_over = False

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def init():
    glClearColor(0, 0, 0, 1)

    # Blending
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Shading
    glShadeModel(GL_SMOOTH)

    # Depth
    glEnable(GL_DEPTH_TEST)

    # Fog
    glEnable(GL_FOG)
    fogColor = [0.0, 0.0, 0.0, 1.0]
    glFogfv(GL_FOG_COLOR, fogColor)
    glFogf(GL_FOG_DENSITY, 0.08)
    glFogi(GL_FOG_MODE, GL_EXP)

def draw_player():
    glBegin(GL_TRIANGLES)
    glColor4f(0, 1, 0, 0.9)
    glVertex3f(player_x-20, 50, -1)
    glVertex3f(player_x+20, 50, -1)
    glVertex3f(player_x, 100, -1)
    glEnd()

def draw_falling():
    glBegin(GL_QUADS)
    glColor4f(1, 0, 0, 0.8)
    glVertex3f(fall_x-10, fall_y-10, -5)
    glVertex3f(fall_x+10, fall_y-10, -5)
    glVertex3f(fall_x+10, fall_y+10, -5)
    glVertex3f(fall_x-10, fall_y+10, -5)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if not game_over:
        draw_player()
        draw_falling()
        draw_text(10, 470, f"Score: {score}")
    else:
        draw_text(200, 250, "GAME OVER")
        draw_text(180, 220, "Press R to Restart")

    glutSwapBuffers()

def update(v):
    global fall_y, fall_x, score, speed, game_over

    if not game_over:
        fall_y -= speed

        # catch
        if 40 < fall_y < 100 and abs(fall_x - player_x) < 30:
            score += 1
            speed += 0.5
            fall_y = 500
            fall_x = random.randint(50, 450)

        # miss
        if fall_y < 0:
            game_over = True

    glutPostRedisplay()
    glutTimerFunc(30, update, 0)

def keyboard(key, x, y):
    global player_x, game_over, score, fall_y, speed

    if key == b'a':
        player_x -= 20
    elif key == b'd':
        player_x += 20

    if key == b'r' and game_over:
        game_over = False
        score = 0
        speed = 5
        fall_y = 500

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 0, 500, -10, 10)
    glMatrixMode(GL_MODELVIEW)

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(500, 500)
glutCreateWindow(b"Fog Catcher Game")

init()
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutTimerFunc(0, update, 0)

glutMainLoop()