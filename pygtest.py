from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
import qpw.qpygletwidget
import sys
import pyglet
from pyglet import gl
from numpy import linspace
from math import *
from graphics import *
import time

R2D = 360/(2*pi)

class BBVisual():
    def __init__(self):
        self.r_roller = .05;
        self.l_board = .5;
        self.h_body = .6;
    def draw(self, state = [0,0,0]):
        gl.glPushMatrix();

        gl.glLineWidth(1)
        gl.glColor3f(.5,.5,.5)
        draw_rect((-.5,0), (.5,-.01))
        draw_rect((-.01,0),(.01,1))
        
        gl.glTranslatef(state[0], self.r_roller, 0)
        gl.glColor3f(0,0,0)
        gl.glLineWidth(3)
        
        gl.glPushMatrix()
        gl.glRotatef(-R2D*state[0]/self.r_roller,0,0,1)
        draw_mass_center(self.r_roller, (0,0))
        gl.glPopMatrix()

        gl.glRotatef(-R2D*state[1], 0, 0, 1)
        gl.glTranslatef(0,self.r_roller,0)
        gl.glColor3f(.7,.2,.2)
        gl.glPushMatrix()
        gl.glRotatef(R2D*state[1],0,0,1)
        draw_line((0,0),(0,1))
        gl.glPopMatrix()
        gl.glColor3f(0,0,0)
        gl.glTranslatef(state[0],0,0)
        draw_rect( (-self.l_board/2,0), (self.l_board/2,.02))
        gl.glColor3f(.5,.5,.5)
        draw_rect((-.01,0), (.01,self.h_body))

        gl.glTranslatef(0, self.h_body, 0)
        gl.glRotatef(-R2D*state[2], 0, 0, 1)
        gl.glColor3f(0,0,0);
        draw_mass_center(.1, (0,0))
        
        gl.glPopMatrix();
    
class MyPygletWidget(qpw.qpygletwidget.QPygletWidget):
    def on_init(self):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image("logo.png"))
        self.label = pyglet.text.Label(
            text="This is a pyglet label rendered in a Qt widget :)")
        self.setMinimumSize(QtCore.QSize(400, 300))
        self.bbvis = BBVisual()
        self.mode = 0

    def on_draw(self):
        self.sprite.draw()
        self.label.draw()
        t=sin(time.time())
        
        if(self.mode == 0):
            self.bbvis.draw((t*.2, -t*.2/.6, t*.2/.6))
        else:
            self.bbvis.draw((t*.2, 2*-t*.2/.6, 4*t*.2/.6))

    def on_resize(self, w, h):
        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        vw = max(1,w/float(h))*.5
        vh = max(1,h/float(w))*.5

        gl.gluOrtho2D(-vw, vw, -vh+.9*vh, vh+.9*vh)
        gl.glMatrixMode(gl.GL_MODELVIEW)

class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.glWidget = MyPygletWidget()
        self.button = QPushButton('Mode')

        self.button.clicked.connect(self.change_mode)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.glWidget)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def change_mode(self):
        self.glWidget.mode = 1 - self.glWidget.mode    
        

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.move(0,0)
    
    window.setCentralWidget(Widget())
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
    
