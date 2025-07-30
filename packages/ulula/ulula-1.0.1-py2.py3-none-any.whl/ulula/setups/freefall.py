###################################################################################################
#
# This file is part of the ULULA code.
#
# (c) Benedikt Diemer, University of Maryland
#
###################################################################################################

import numpy as np

import ulula.core.setup_base as setup_base

###################################################################################################

class SetupFreefall(setup_base.Setup):
    """
    Gravitational free-fall

    This setup is mostly a test of the gravity solver. The outflow BCs mean that the entire domain
    is free-falling under a constant gravitational acceleration. We compare the position of a 
    Gaussian gas blob in pressure equilibrium to the known solution. This setup demonstrates
    
    * Fixed-acceleration gravity combined with outflow boundary conditions
    * Accuracy of the gravity source term.
    
    Parameters
    ----------
    unit_l: float
        Code unit for length in units of centimeters.
    unit_t: float
        Code unit for time in units of seconds.
    unit_m: float
        Code unit for mass in units of gram.
    """
    
    def __init__(self, unit_l = 1.0, unit_t = 1.0, unit_m = 1.0):

        setup_base.Setup.__init__(self, unit_l = unit_l, unit_t = unit_t, unit_m = unit_m)
        
        self.rho0 = 0.1
        self.rho1 = 1.0
        self.P0 = 1.0
        self.g = 1.0

        self.blob_r = 0.05
        self.blob_x = 0.8

        return 

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'freefall'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialConditions(self, sim, nx):
        
        sim.setGravityMode(gravity_mode = 'fixed_acc', g = self.g)
        sim.setDomain(nx, 1, xmin = 0.0, xmax = 1.0, bc_type = 'outflow')
        
        DN = sim.q_prim['DN']
        VX = sim.q_prim['VX']
        VY = sim.q_prim['VY']
        PR = sim.q_prim['PR']

        sim.V[VX] = 0.0
        sim.V[VY] = 0.0
        sim.V[PR] = self.P0

        x, _ = sim.xyGrid()
        r = np.sqrt((x - self.blob_x)**2)
        sigma = self.blob_r * sim.xmax
        sim.V[DN] = self.rho0 + self.rho1 * np.exp(-0.5 * r**2 / sigma**2)
        
        return
        
    # ---------------------------------------------------------------------------------------------

    def plotLimits(self, q_plot, plot_geometry):
        
        vmin = []
        vmax = []

        for q in q_plot:
            if q == 'DN':
                vmin.append(0.0)
                vmax.append(self.rho1 * 1.2)
            elif q in ['VX']:
                vmin.append(-2.0)
                vmax.append(0.1)
            elif q == 'PR':
                vmin.append(self.P0 * 0.8)
                vmax.append(self.P0 * 1.2)
            elif q == 'ET':
                vmin.append(1.3)
                vmax.append(2.0)
            else:
                vmin.append(None)
                vmax.append(None)
        
        return vmin, vmax, None
  
    # ---------------------------------------------------------------------------------------------

    def trueSolution(self, sim, x, q_plot, plot_geometry):
        
        t = sim.t
        x_blob = self.blob_x - 0.5 * self.g * t**2
        sigma = self.blob_r * sim.xmax
        
        sol_list = []
        for i in range(len(q_plot)):
            q = q_plot[i]
            sol = np.zeros((len(x)), float)
            if q == 'DN':
                sol = self.rho0 + self.rho1 * np.exp(-0.5 * (x - x_blob)**2 / sigma**2)
            elif q == 'PR':
                sol[:] = self.P0
            elif q == 'VX':
                sol[:] = -self.g * t
            else:
                sol = None
            sol_list.append(sol)
        
        return sol_list

###################################################################################################
