import rbdl
import numpy as np

from math import *

class BBModel():

    def __init__(self):
        roller_rad = .05
        density = 100
        self.model = rbdl.Model()
        model = self.model

        #define the roller
        roller_mass = pi*roller_rad**2 * .81 * density
        roller_moi = roller_mass * roller_rad**2
        
        axis = np.asarray([[0.,0.,-1.,roller_rad,0,0]])
        joint = rbdl.Joint.fromJointAxes(axis)

        ytrans =rbdl.SpatialTransform()
        ytrans.r = np.array([0,roller_rad,0])
        
        body = rbdl.Body.fromMassComInertia(roller_mass, np.array([0.,0.,0.]), np.diag([roller_moi, roller_moi, 1]))
        self.roller = model.AppendBody(rbdl.SpatialTransform(), joint, body)

        #define the board (and junk fixed to it)
        board_mass = 1
        
        joint = rbdl.Joint.fromJointType("JointTypeRevoluteZ")
        body = rbdl.Body.fromMassComInertia(board_mass, np.array([0, .2, 0]), np.eye(3))
        self.board = model.AppendBody(ytrans, joint, body)

        q = np.zeros (model.q_size)
        qdot = np.zeros (model.qdot_size)
        self.qddot = np.zeros (model.qdot_size)
        tau = np.zeros (model.qdot_size)
        

    def integrate(self, q, qdot, tau, dt):
        tau[1] = -dt * qdot[1]
        rbdl.ForwardDynamics(self.model, q, qdot, tau, self.qddot)
        q += qdot * dt
        qdot += self.qddot * dt
        
