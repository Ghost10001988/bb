import numpy as np
import rbdl
# Xdot = A*X + B*U + C
class LinearSystem():
    def __init__(self, nq, nu):
        self.A = np.zeros([2*nq, 2*nq])
        self.B = np.zeros([2*nq, nu])
        self.C = np.zeros(2*nq)

class LinearSystemApproximator():
    def __init__(self):
        pass

    def calculate(self,model, q, qdot, u):
        qddot0 = np.empty_like(q)
        qddot1 = np.empty_like(q)
        dq = 1e-4
        du = 1e-4

        ss = LinearSystem(len(q), len(u))
        
        rbdl.ForwardDynamics(model, q, qdot, u, qddot0)
        
        ss.A[:len(q),len(q):] = np.eye(len(q))
        
        for i in range(len(q)):
            q1 = np.copy(q)
            q1[i] += dq
            rbdl.ForwardDynamics(model, q1, qdot, u, qddot1)
            ss.A[len(q):,i] = (qddot1 - qddot0)/dq

            qdot1 = np.copy(qdot)
            qdot1[i] += dq
            rbdl.ForwardDynamics(model, q, qdot1, u, qddot1)
            ss.A[len(q):,i+len(q)] = (qddot1 - qddot0)/dq

        for i in range(len(u)):
            u1 = np.copy(u)
            u1[i] += du
            rbdl.ForwardDynamics(model, q, qdot, u1, qddot1)
            ss.B[len(q):,i] = (qddot1 - qddot0)/du

        ss.C = qddot0
        
        return ss

def stateLimits(minNorm = 1e-2, maxNorm = 1e2):
    def predicate(x):
        norm = np.linalg.norm(x)
        return minNorm < norm and maxNorm > norm
    return predicate    
    
class Simulation():
    def __init__(self, model, x0, control = None):
        assert(x0.size == model.q_size + model.qdot_size)
        self.model = model
        self.x0 = np.copy(x0)
        self.x = np.copy(x0)
        self.control = control
        self.dt = 1/30.0
        self.xdot = np.zeros (model.qdot_size)
        self.tau = np.zeros(model.qdot_size)

        self.qddot = np.empty(model.qdot_size)
        
        self.reset()

    def sim(self,t):
        dt = 1/30.
        steps = int(t/dt)
        X = np.empty([len(self.x0), steps])
        for i in range(steps):
            X[:,i] = self.x

            sub_steps = 10
            for i in range(sub_steps):
                if not self.control is None:
                    self.control.computeU(self.x, self.tau)
                self.integrate(self.x[:self.model.q_size], self.x[self.model.q_size:], self.tau, dt/sub_steps)

        self.X = np.concatenate([self.X, X],1)
        return self.X
    
    def simUntil(self, predicate = stateLimits(), tMax = 10 ):
        t = 0
        while t < tMax and predicate(self.x):
            self.sim(0.5)
            t += 0.5
        return self.X
    
    def integrate(self, q, qdot, tau, dt):        
        rbdl.ForwardDynamics(self.model, q, qdot, tau, self.qddot)
        q += qdot * dt
        qdot += self.qddot * dt

    def reset(self):
        self.X = np.zeros([self.x0.size,0])
        self.x = np.copy(self.x0)
