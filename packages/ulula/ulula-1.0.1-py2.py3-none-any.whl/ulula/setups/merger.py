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

class SetupMerger(setup_base.Setup):
    """
    Merger of two gas blobs
    
    This setup demonstrates Poisson gravity in a periodic domain. Two gas blobs with Gaussian
    density profiles are set along the diagonal of the domain and fall towards each other. The
    interplay of gravity and pressure creates complex (but symmetric) patterns, and the blobs 
    eventually merging into a single blob. This test demonstrates:
    
    * Poisson gravity in 2D
    * Preservation of symmetry

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

        self.rho0 = 0.05
        self.rho1 = 2.0
        self.P0 = 1.0
        self.ux = 0.0
        self.uy = 0.0
        self.r_th = 0.05
        self.d_origin = 0.15

        return 

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'merger'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialConditions(self, sim, nx):
        
        sim.setGravityMode(gravity_mode = 'poisson', G = 1.0)
        sim.setDomain(nx, nx, xmin = 0.0, xmax = 1.0, ymin = 0.0, bc_type = 'periodic')

        DN = sim.q_prim['DN']
        VX = sim.q_prim['VX']
        VY = sim.q_prim['VY']
        PR = sim.q_prim['PR']

        sim.V[DN] = self.rho0
        sim.V[VX] = self.ux
        sim.V[VY] = self.uy
        sim.V[PR] = self.P0

        x, y = sim.xyGrid()

        blob_xy = 0.5 - self.d_origin
        r = np.sqrt((x - blob_xy)**2 + (y - blob_xy)**2)
        sim.V[DN] += self.rho1 * np.exp(-0.5 * r**2 / self.r_th**2)

        blob_xy = 0.5 + self.d_origin
        r = np.sqrt((x - blob_xy)**2 + (y - blob_xy)**2)
        sim.V[DN] += self.rho1 * np.exp(-0.5 * r**2 / self.r_th**2)
        
        return

    # ---------------------------------------------------------------------------------------------

    def plotLimits(self, q_plot, plot_geometry):
        
        vmin = []
        vmax = []

        for q in q_plot:
            if q == 'DN':
                vmin.append(0.0)
                vmax.append(self.rho1 * 1.05)
            elif q in ['VX', 'VY']:
                vmin.append(-1.05)
                vmax.append(1.05)
            elif q == 'PR':
                vmin.append(0.95)
                vmax.append(1.12)
            elif q == 'GP':
                vmin.append(1.27)
                vmax.append(1.45)
            elif q in ['GX', 'GY']:
                vmin.append(-0.7)
                vmax.append(0.7)
            else:
                vmin.append(None)
                vmax.append(None)
        
        return vmin, vmax, None
    
###################################################################################################
