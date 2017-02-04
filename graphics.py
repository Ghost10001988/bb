from pyglet import gl, graphics
from numpy import linspace
from math import *

def draw_mass_center(r, pt):
    x,y = pt
    gl.glPushAttrib(gl.GL_CURRENT_BIT)
    gl.glColor3f(1,1,1)
    draw_circle(r, pt, filled=True)
    gl.glColor3f(0,0,0)
    draw_circle(r, pt, filled=False)
    draw_arc((r, r), pt, (0,pi/2))
    draw_arc((r, r), pt, (pi,3*pi/2))
    gl.glPopAttrib()

def draw_line(p1, p2):
    (x0,y0) = p1
    (x1,y1) = p2
    graphics.draw(2, gl.GL_LINES, ('v2f', (x0,y0,x1,y1)))

def draw_circle(r, pt, n = 15, filled = True):
    (x, y) = pt
    graphics.draw(n, gl.GL_POLYGON if filled else gl.GL_LINE_STRIP,
                  ('v2f', sum([(cos(n)*r+x,sin(n)*r+y) for n in linspace(0, 2*pi, n)],())))

def draw_arc(size, pt, angles, n=15, filled = True):
    (r1,r2) = size
    (x,y) = pt
    (t1,t2) = angles
    graphics.draw(n+1, gl.GL_POLYGON if filled else gl.GL_LINE_STRIP,
                  ('v2f', sum([(cos(n)*r1+x,sin(n)*r2+y) for n in linspace(t1, t2, n)] + [(x,y)],())))

def draw_rect(pt1, pt2):
    (x0, y0) = pt1
    (x1, y1) = pt2
    graphics.draw(4, gl.GL_POLYGON, ('v2f', (x0,y0,x0,y1,x1,y1,x1,y0) ))

    
