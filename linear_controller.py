import numpy as np
from collections import deque

class LinearController():
    def __init__(self, K, q0 = None, u0 = None):
        self.K = K
        if q0 is None:
            q0 = np.zeros(self.K.shape[1])
        if u0 is None:
            u0 = np.zeros(self.K.shape[0])
            
        self.q0 = q0
        self.u0 = u0

    def computeU(self, q, tau):
        u = -self.K.dot(q - self.q0) + self.u0
        np.copyto(tau, u)


class ControlDelay():
    def __init__(self, wrapped, input_delay):
        self.wrapped = wrapped
        self.buffer = None
        self.input_delay = input_delay

    def computeU(self, q, tau):
        if self.buffer is None:
            self.buffer = deque()
            for i in range(self.input_delay):
                self.buffer.append(np.copy(q))

        self.buffer.append(np.copy(q))
        self.wrapped.computeU(self.buffer.popleft(), tau)
    
class AddControl():
    def __init__(self, wA, wB):
        self.wA = wA
        self.wB = wB
        self.tau = None

    def computeU(self, q, tau):
        if self.tau is None:
            self.tau = np.copy(tau)

        self.wA.computeU(q, self.tau)
        self.wB.computeU(q, tau)

        tau += self.tau

class Disturbance():
    def __init__(self, start, stop, force):
        self.start = start
        self.stop = stop
        self.force = force
        self.t = 0

    def computeU(self, q, tau):
        if(self.t > self.start and self.t < self.stop):
            np.copyto(tau, self.force)
        else:
            tau.fill(0)
        self.t += 1
