from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtOpenGL import *
import time;

rotation = 0

class MainWindow(QtGui.QWidget):
    def onClick(self):
        global rotation
        rotation = 0;

    def __init__(self):
        super(MainWindow, self).__init__()

        self.widget = glWidget(self)

        self.button = QtGui.QPushButton('Test', self)
        self.button.pressed.connect(self.onClick)

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.widget)
        mainLayout.addWidget(self.button)

        self.setLayout(mainLayout)

        
class glWidget(QGLWidget):

    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(640, 480)

    def paintGL(self):

    
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()


        glTranslatef(-2.5, 0.5, -6.0)
        glRotatef( rotation, 0, 1, 0 )
        glColor3f( 1.0, 1.5, 0.0 );
        glPolygonMode(GL_FRONT, GL_FILL);

        glBegin(GL_TRIANGLES)
        glVertex3f(2.0,-1.2,0.0)
        glVertex3f(2.6,0.0,0.0)
        glVertex3f(2.9,-1.2,0.0)
        glEnd()


        glFlush()



    def initializeGL(self):



        glClearDepth(1.0)              
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()                    
        gluPerspective(45.0,1.33,0.1, 100.0) 
        glMatrixMode(GL_MODELVIEW)


def spin():
    global rotation, window
    window.widget.updateGL()
    if(rotation%30 == 0):
        print time.time()
    rotation += 1;

class Renderer():
    def render():
        

if __name__ == '__main__':
    app = QtGui.QApplication(['Yo'])
    global window

    renderer = Renderer()
    
    window = MainWindow()
    window.show()

    timer = QtCore.QTimer()
    timer.timeout.connect(spin)
    timer.start(1000/30)
    
    app.exec_()
    
