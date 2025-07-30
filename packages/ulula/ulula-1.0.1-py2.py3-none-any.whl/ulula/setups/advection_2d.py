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

class SetupAdvection2D(setup_base.Setup):
    """
    2D advection test
    
    In this test, an initially overdense tophat or sine pattern is placed at the center of the domain. 
    The entire fluid moves towards the northeast direction. The edges of the disk diffuse into the 
    surrounding fluid at a rate that depends on the hydro solver. For example, when using no spatial 
    reconstruction, the hydro scheme will be extremely diffusive and the tophat will quickly spread 
    into the surrounding fluid. Linear interpolation leads to less diffusion, especially if an 
    aggressive slope limiter is used. However, when combining the resulting sharp gradients with a 
    hydro scheme that is 1st-order in time, the test quickly becomes unstable and fails 
    spectacularly. This setup demonstrates

    * Stability of time integration schemes
    * Diffusivity of reconstruction schemes
    * Importance of slope limiters.

    Parameters
    ----------
    shape: str
        Initial shape of density that is being advected. Can be ``'sine'`` or ``'tophat'``.
    unit_l: float
        Code unit for length in units of centimeters.
    unit_t: float
        Code unit for time in units of seconds.
    unit_m: float
        Code unit for mass in units of gram.
    """
    
    def __init__(self, shape = 'tophat', unit_l = 1.0, unit_t = 1.0, unit_m = 1.0):

        setup_base.Setup.__init__(self, unit_l = unit_l, unit_t = unit_t, unit_m = unit_m)
        
        self.shape = shape
        self.rho0 = 1.0
        self.rho1 = 2.0
        self.P0 = 1.0
        self.vx = 0.5
        self.vy = 0.4
        self.r_th = 0.2
        
        return 

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'advection2d'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialConditions(self, sim, nx):
        
        sim.setDomain(nx, nx, xmin = 0.0, xmax = 1.0, ymin = 0.0, bc_type = 'periodic')

        DN = sim.q_prim['DN']
        VX = sim.q_prim['VX']
        VY = sim.q_prim['VY']
        PR = sim.q_prim['PR']
        
        sim.V[DN] = self.densityField(sim, 0.0)
        sim.V[VX] = self.vx
        sim.V[VY] = self.vy
        sim.V[PR] = self.P0

        return
    
    # ---------------------------------------------------------------------------------------------

    # Set tophat into the center of the domain and move it along

    def densityField(self, sim, t):

        x, y = sim.xyGrid()
        rho = np.ones_like(sim.V[sim.q_prim['DN']]) * self.rho0

        if self.shape == 'tophat':
            th_x = (0.5 + self.vx * t) % 1.0
            th_y = (0.5 + self.vy * t) % 1.0
            r = np.sqrt((x - th_x)**2 + (y - th_y)**2)
            mask = (r <= self.r_th)
            rho[mask] = self.rho1
            
        elif self.shape == 'sine':
            rho += 0.5 + 0.25 * (np.sin(4.0 * np.pi * (x - self.vx * t)) + np.sin(4.0 * np.pi * (y - self.vy * t)))
            
        else:
            raise Exception('Unknown shape for 2D advection test, %s.' % (self.shape))
        
        return rho

    # ---------------------------------------------------------------------------------------------

    def plotLimits(self, q_plot, plot_geometry):

        vmin = []
        vmax = []

        for q in q_plot:
            if q == 'DN':
                vmin.append(self.rho0 * 0.9)
                vmax.append(self.rho1 * 1.05)
            elif q in ['VX', 'VY']:
                vmin.append(0.0)
                vmax.append(1.0)
            elif q == 'PR':
                vmin.append(self.P0 * 0.8)
                vmax.append(self.P0 * 1.2)
            else:
                vmin.append(None)
                vmax.append(None)
        
        return vmin, vmax, None

###################################################################################################
