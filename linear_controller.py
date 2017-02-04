import numpy as np

class LinearController():
    def __init__(self, K, q0, u0):
        self.K = K
        self.q0 = q0
        self.u0 = u0

    def computeU(self, q, tau):
        u = -self.K.dot(q - self.q0) + self.u0
        np.copyto(tau, u)
