import numpy as np

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
