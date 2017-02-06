import bb
from threading import Thread
import queue
import system_model
import numpy as np
import bbrbdl
import control
import linear_controller
import math

class BBInteractive():
    def __init__(self):
        self.queue = queue.Queue()
        t = Thread(None, lambda:bb.start(self.queue))
        t.start()

    def show_state(self, q):
            self.queue.put(q)

def begin():
    return BBInteractive()

def show_mode(x, amp = 1, n = 60):
    X = np.zeros([x.size, n])
    for i in range(n):        
        X[:,i] = math.sin(i/float(n)*2.*np.pi) * x
    return X

