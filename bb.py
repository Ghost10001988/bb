from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
import qpw.qpygletwidget
import sys
import pyglet
import movie_writer
from pyglet import gl
from numpy import linspace
import numpy as np
from math import *
from graphics import *
import time
from bbrbdl import BBModel
import rbdl

R2D = 360/(2*pi)

class BBVisual():
    def __init__(self):
        self.r_roller = .05;
        self.l_board = .5;
        self.h_body = .6;
        self.zero = np.array([0.,0,0])
        self.unit_y = np.array([0.,.2,0])

    def draw_model(self, bbmdl, q):
        mdl = bbmdl.model

        gl.glColor3f(0,1,1)
        pt0 = rbdl.CalcBodyToBaseCoordinates(mdl, q, bbmdl.roller, self.zero)
        draw_line(pt0[0:2], (0,0))
        
        gl.glColor3f(0,1,0)
        pt0 = rbdl.CalcBodyToBaseCoordinates(mdl, q, bbmdl.roller, self.zero, update_kinematics = False)
        pt1 = rbdl.CalcBodyToBaseCoordinates(mdl, q, bbmdl.roller, self.unit_y, update_kinematics = False)
        draw_line(pt0[0:2], pt1[0:2])


        gl.glColor3f(0,0,1)
        pt0 = rbdl.CalcBodyToBaseCoordinates(mdl, q, bbmdl.roller, self.zero, update_kinematics = False)
        pt1 = rbdl.CalcBodyToBaseCoordinates(mdl, q, bbmdl.board, self.zero, update_kinematics = False)
        draw_line(pt0[0:2], pt1[0:2])

        gl.glColor3f(1,.5,0)
        pt0 = rbdl.CalcBodyToBaseCoordinates(mdl, q, bbmdl.board, np.array([-self.l_board/2,self.r_roller,0]), update_kinematics = False)
        pt1 = rbdl.CalcBodyToBaseCoordinates(mdl, q, bbmdl.board, np.array([self.l_board/2,self.r_roller,0]), update_kinematics = False)
        draw_line(pt0[0:2], pt1[0:2])
        
        gl.glColor3f(1,0,0)
        pt0 = rbdl.CalcBodyToBaseCoordinates(mdl, q, bbmdl.board, self.zero, update_kinematics = False)
        pt1 = rbdl.CalcBodyToBaseCoordinates(mdl, q, bbmdl.board, self.unit_y, update_kinematics = False)
        draw_line(pt0[0:2], pt1[0:2])
        
    def draw(self, state = [0,0,0]):
        gl.glLoadIdentity()
        gl.glLineWidth(1)
        gl.glColor3f(.7,.7,.7)
        draw_rect((-.5,0), (.5,-.01))
        draw_rect((-.01,0),(.01,1))

        gl.glTranslatef(0,self.r_roller,0);

        gl.glPushMatrix();
        
        gl.glTranslatef(state[0]*self.r_roller, 0, 0)
        gl.glColor3f(0,0,0)
        gl.glLineWidth(3)
        
#        gl.glPushMatrix()
        gl.glRotatef(-R2D*state[0],0,0,1)
        draw_mass_center(self.r_roller, (0,0))
#        gl.glPopMatrix()

        gl.glRotatef(-R2D*state[1], 0, 0, 1)

        gl.glTranslatef(0,self.r_roller,0)
        
        gl.glPushMatrix()
        gl.glRotatef(R2D*(state[1]+state[0]),0,0,1)
        gl.glPushAttrib(gl.GL_ENABLE_BIT);
        gl.glColor3f(.7,.2,.2)
        gl.glLineStipple(1, 0xF00F)  # [1]
        gl.glEnable(gl.GL_LINE_STIPPLE)
        draw_line((0,0),(0,1))
        gl.glPopAttrib()
        gl.glPopMatrix()
        
        gl.glTranslatef(-state[1] * self.r_roller,0,0)
        
        gl.glColor3f(0,0,0)        
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
        self.setMinimumSize(QtCore.QSize(800, 600))
        self.bbvis = BBVisual()
        self.mode = 0
        self.frame = 0
        self.bbmdl = BBModel()

    def on_draw(self):
        self.frame += 1

        t=sin(self.frame/60.0)

        q0 = t*.2;
        h = self.bbvis.h_body;
        r = self.bbvis.r_roller;
        
        if(self.mode == 0):
            s = (q0/r, -q0/h-q0/r, q0/h)
#            s = (q0*30,0,0)
            self.bbvis.draw(s)
            self.bbvis.draw_model(self.bbmdl, np.array(s))
        elif(self.mode == 1):
            s = (q0/r, 2*-q0/(h+2*r)-q0/r, 4*q0/h)
            self.bbvis.draw(s)
            self.bbvis.draw_model(self.bbmdl, np.array(s))
        elif(self.mode == 2):
            self.bbmdl.integrate(self.q,self.qdot,np.zeros(2), 1/100.0)
            self.bbvis.draw([self.q[0], self.q[1], 0])
            self.bbvis.draw_model(self.bbmdl, self.q)

    def on_resize(self, w, h):
        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        vw = max(1,w/float(h))*.5
        vh = max(1,h/float(w))*.5

        gl.gluOrtho2D(-vw, vw, -vh+.9*vh, vh+.9*vh)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def reset_sim(self):
        self.q = np.array([1,-1.])
        self.qdot = np.array([0.,0])


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.glWidget = MyPygletWidget()
        self.button = QPushButton('Mode')
        self.button.clicked.connect(self.change_mode)

        movie_button = QPushButton('Make Movie')
        movie_button.clicked.connect(self.make_movie)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.glWidget)

        button_box = QHBoxLayout()
        button_box.addWidget(self.button)
        button_box.addWidget(movie_button)

        self.layout.addLayout(button_box)
        self.setLayout(self.layout)

    def change_mode(self):
        self.glWidget.mode = (self.glWidget.mode + 1)%3

        if(self.glWidget.mode == 2):
            self.glWidget.reset_sim()

    def make_movie(self):
        print("movie")
        movie_writer.save_movie(self.glWidget.width(), self.glWidget.height(), self.glWidget.paintGL)
        

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.move(0,0)
    
    window.setCentralWidget(Widget())
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
    
