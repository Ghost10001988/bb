import bb
from threading import Thread
import queue
import system_model
import numpy as np
import bbrbdl
import control
import linear_controller

class BBInteractive():
    def __init__(self):
        self.queue = queue.Queue()
        t = Thread(None, lambda:bb.start(self.queue))
        t.start()

    def show_state(self, q):
            self.queue.put(q)

def begin():
    return BBInteractive()

BB = begin()
M = bbrbdl.BBModel()
s = system_model.Simulation(M.model,np.zeros(4))
X = s.sim(5)

lsa = system_model.LinearSystemApproximator()
ss = lsa.calculate(M.model, s.x0[:2], s.x0[2:], np.zeros(2))

css = control.ss(ss.A, ss.B, np.eye(4), np.zeros([4,2]))

[K,S,E] = control.lqr(css, np.diag([10, 10, 1, 1]), np.eye(2))
print(K)
P = linear_controller.LinearController( K, np.zeros(4), np.zeros(2))
s.control = P
s.x0[0] = -.5
s.reset()
X = s.sim(2)

BB.show_state(X)
