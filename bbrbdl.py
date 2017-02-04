import rbdl
import numpy as np
import system_model

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
        ytrans.r = np.array([0,0,0])
        
        body = rbdl.Body.fromMassComInertia(roller_mass, np.array([0.,0.,0.]), np.diag([1, 1, roller_moi]))
        self.roller = model.AppendBody(rbdl.SpatialTransform(), joint, body)

        #define the board (and junk fixed to it)
        board_mass = 1

        print(roller_mass, board_mass)

        axis = np.asarray([[0.,0.,1.,roller_rad,0,0]])
        joint = rbdl.Joint.fromJointAxes(axis)
        joint.mReversedPolarity = True
        body = rbdl.Body.fromMassComInertia(board_mass, np.array([0, 0.5, 0]), np.eye(3)*.1)
        self.board = model.AppendBody(ytrans, joint, body)

#        self.roller = self.board
        
