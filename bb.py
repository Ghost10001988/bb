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
from bbrbdl import BBModel, BBParams
import rbdl
import queue
from queue import Empty
import system_model

R2D = 360/(2*pi)

class BBVisual():
    def __init__(self, bb_params):
        self.r_roller = bb_params.r_roller;
        self.l_board = .5;
        self.h_body = bb_params.h_body - bb_params.r_roller;
        self.h_body2 = .25;
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

        pt0 = rbdl.CalcBodyToBaseCoordinates(mdl, q, bbmdl.board, self.zero, update_kinematics = False)
        pt1 = rbdl.CalcBodyToBaseCoordinates(mdl, q, bbmdl.body, self.zero, update_kinematics = False)
        draw_line(pt0[0:2], pt1[0:2])        

        gl.glColor3f(0,1,0)
        pt0 = rbdl.CalcBodyToBaseCoordinates(mdl, q, bbmdl.body, self.zero, update_kinematics = False)
        pt1 = rbdl.CalcBodyToBaseCoordinates(mdl, q, bbmdl.body, np.asarray([0,.1,0]), update_kinematics = False)
        draw_line(pt0[0:2], pt1[0:2])        

        try:
            gl.glColor3f(0,0,1)
            pt0 = rbdl.CalcBodyToBaseCoordinates(mdl, q, bbmdl.body2, self.zero, update_kinematics = False)
            pt1 = rbdl.CalcBodyToBaseCoordinates(mdl, q, bbmdl.body2, np.asarray([0,-self.h_body + self.r_roller + .05,0]), update_kinematics = False)
            draw_line(pt0[0:2], pt1[0:2])

        except AttributeError:
            pass
        
    def draw(self, state = [0,0,0]):
        gl.glEnable (gl.GL_LINE_SMOOTH);                                                     
        gl.glHint (gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)     
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

        gl.glPushMatrix()
        gl.glTranslatef(0, self.h_body, 0)
        gl.glRotatef(R2D*state[2], 0, 0, 1)
        gl.glColor3f(0,0,0);
        draw_mass_center(.1, (0,0))
        gl.glPopMatrix()

        if len(state) >= 8:
            gl.glPushMatrix()            
            gl.glTranslatef(0, self.h_body, 0)
            gl.glRotatef(R2D*state[3], 0, 0, 1)
            gl.glTranslatef(0, -self.h_body+self.r_roller+.05, 0)
            gl.glColor3f(0,0,0);
            draw_mass_center(.03, (0,0))
            gl.glPopMatrix()
        
        gl.glPopMatrix();
    
class MyPygletWidget(qpw.qpygletwidget.QPygletWidget):
    def on_init(self):
        bb_params = BBParams()
        self.setMinimumSize(QtCore.QSize(800, 600))
        self.bbvis = BBVisual(bb_params)
        self.mode = 'simulate'
        self.bbmdl = BBModel(bb_params)
        self.reset()

    def on_draw(self):
        global window
        if not self.queue is None:
            try:
                self.repl_state = self.queue.get_nowait()
                self.combobox.setCurrentIndex(self.combobox.findText('repl link'))
                window.raise_()
                window.activateWindow()
                self.queue.task_done()
            except Empty:
                pass
            
        self.frame += 1
        
        if(self.mode == 'kinematic'):
            t=sin(self.frame/60.0)

            q0 = t*.2;
            h = self.bbvis.h_body;
            r = self.bbvis.r_roller;
        
            s = (q0/r, -q0/h-q0/r, q0/h, 0)
#            s = (0,q0*30,0)
#            s = (q0/r, 2*-q0/(h+2*r)-q0/r, 4*q0/h)

        elif(self.mode == 'simulate'):
            self.sim.integrate(self.q,self.qdot,np.zeros(self.qdot.size), 1/30.0)
            s = self.q
        elif(self.mode == 'repl link'):
            i = self.frame%self.repl_state.shape[1]
            s = np.copy(self.repl_state[:, i])
            
        self.bbvis.draw(s)
        self.bbvis.draw_model(self.bbmdl, np.asarray(s[:self.bbmdl.model.q_size]))            

    def on_resize(self, w, h):
        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        vw = max(1,w/float(h))*.5
        vh = max(1,h/float(w))*.5

        gl.gluOrtho2D(-vw, vw, -vh+.9*vh, vh+.9*vh)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def reset(self):
        self.q = np.zeros(self.bbmdl.model.q_size)
        self.q[0] = -.01
        self.q[1] = .01
        self.qdot = np.zeros(self.q.size)

        self.sim = system_model.Simulation(self.bbmdl.model, np.concatenate([self.q, self.qdot]))
        self.frame = 0


class Widget(QWidget):
    def __init__(self, queue):
        QWidget.__init__(self)
        self.glWidget = MyPygletWidget()
        self.glWidget.queue = queue
        mode_button = QPushButton('Mode')
        mode_button.clicked.connect(self.change_mode)

        mode_cbox = QComboBox()
        mode_cbox.addItem('simulate')
        mode_cbox.addItem('kinematic')
        mode_cbox.addItem('repl link')
        mode_cbox.currentIndexChanged[str].connect(self.change_mode)

        self.glWidget.combobox = mode_cbox
        
        movie_button = QPushButton('Make Movie')
        movie_button.clicked.connect(self.make_movie)

        reset_button = QPushButton('Reset')
        reset_button.clicked.connect(self.glWidget.reset)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.glWidget)

        button_box = QHBoxLayout()
        button_box.addWidget(mode_cbox)
        button_box.addWidget(reset_button)
        button_box.addWidget(movie_button)

        self.layout.addLayout(button_box)
        self.setLayout(self.layout)

    def change_mode(self, new_mode):
        self.glWidget.mode = new_mode

        if(new_mode == 'simulate'):
            self.glWidget.reset()

    def make_movie(self):
        print("movie")
        if self.glWidget.mode == "repl link":
            total_frames = self.glWidget.repl_state.shape[1]
            self.glWidget.frame = 0
        else:
            total_frames = 300
        movie_writer.save_movie(self.glWidget.width(), self.glWidget.height(), self.glWidget.paintGL, total_frames )

def start(queue = None):
    global window
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.move(0,0)
    window.setWindowTitle("Bongo Board")
    
    window.setCentralWidget(Widget(queue))
    window.show()
    app.exec_()

def main():
    start()

if __name__ == "__main__":
    main()
    
