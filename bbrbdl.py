import rbdl
import numpy as np
import system_model

from math import *

class BBParams():
    def __init__(self):
        self.r_roller = 0.05
        self.h_body = 0.4
        self.use_second_mass = False

class BBModel():

    def __init__(self, bb_params):
        roller_rad = bb_params.r_roller
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

        print("Masses: ", roller_mass, board_mass)

        axis = np.asarray([[0.,0.,1.,roller_rad,0,0]])
        joint = rbdl.Joint.fromJointAxes(axis)
        joint.mReversedPolarity = True
        body = rbdl.Body.fromMassComInertia(board_mass, np.array([0, 0.5, 0]), np.eye(3)*.1)
        self.board = model.AppendBody(ytrans, joint, body)

        body_height = bb_params.h_body
        body_mass = 3
        body_moi = body_mass * 0.5 * 0.3**2

        if(bb_params.use_second_mass):
            axis = np.asarray([[0,0,1.0,0,0,0]])
            joint = rbdl.Joint.fromJointAxes(axis)
            body = rbdl.Body.fromMassComInertia(body_mass, np.array([0, .0, 0]), np.eye(3) * body_moi)
            ytrans.r = np.array([0,body_height,0])
            self.body = model.AppendBody(ytrans, joint, body)

            ## Second Spinner

            axis = np.asarray([[0,0,1.0,0,0,0]])
            joint = rbdl.Joint.fromJointAxes(axis)
            body = rbdl.Body.fromMassComInertia(body_mass, np.array([0, -body_height+.05, 0]), np.eye(3) * body_moi/4.0)
            ytrans.r = np.array([0,body_height,0])
            self.body2 = model.AddBody(self.board, ytrans, joint, body)
        else:
            axis = np.asarray([[0,0,1.0,0,0,0]])
            joint = rbdl.Joint.fromJointAxes(axis)
            body = rbdl.Body.fromMassComInertia(body_mass, np.array([0, 0., 0]), np.eye(3) * body_moi)
            ytrans.r = np.array([0,body_height,0])
            self.body = model.AppendBody(ytrans, joint, body)                    

#        self.roller = self.board
        
