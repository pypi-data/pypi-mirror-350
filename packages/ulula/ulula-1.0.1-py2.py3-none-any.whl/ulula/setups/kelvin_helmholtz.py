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

class SetupKelvinHelmholtz(setup_base.Setup):
    """
    Kelvin-Helmholtz instability
    
    The KH instability forms at the interface between two fluids that are moving past each other. 
    The user can choose between a setup where the interface is infinitely sharp and the smooth
    ICs of Robertson et al. `2010 <https://ui.adsabs.harvard.edu/abs/2010MNRAS.401.2463R/abstract>`_. 
    In the sharp case, the instability is seeded by grid noise, but
    we still add a small velocity perturbation to obtain more well-defined behavior. The smooth
    version is recommended as it leads to a more physical test case. This setup demonstrates
    
    * Instability at two-fluid interface
    * Periodic boundary conditions
    * Sharp vs. smooth gradients in initial conditions.

    Parameters
    ----------
    sharp_ics: bool
        Use sharp boundary between fluids instead of smoothed ICs.
    n_waves: int
        Number of wave periods in the domain. The number of periods that can be resolved depends on
        the resolution.
    unit_l: float
        Code unit for length in units of centimeters.
    unit_t: float
        Code unit for time in units of seconds.
    unit_m: float
        Code unit for mass in units of gram.
    """
    
    def __init__(self, sharp_ics = False, n_waves = 1, unit_l = 1.0, unit_t = 1.0, unit_m = 1.0):

        setup_base.Setup.__init__(self, unit_l = unit_l, unit_t = unit_t, unit_m = unit_m)
        
        self.rho1     =  2.0
        self.rho2     =  1.0
        self.v1       =  0.5
        self.v2       = -0.5
        self.P0       =  2.5
        self.lamb     =  1.0 / n_waves

        if sharp_ics:
            self.delta_y = 0.0
            self.delta_vy =  0.001
        else:
            self.delta_y  =  0.05
            self.delta_vy =  0.1

        return

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'kh'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialConditions(self, sim, nx):
        
        sim.setDomain(nx, nx, xmin = 0.0, xmax = 1.0, ymin = 0.0, bc_type = 'periodic')

        DN = sim.q_prim['DN']
        VX = sim.q_prim['VX']
        VY = sim.q_prim['VY']
        PR = sim.q_prim['PR']

        x, y = sim.xyGrid()
        
        if self.delta_y > 0.0:
            
            # Softened initial conditions from Robertson et al (2010), Abel (2010)
            y1 = (y - 0.25) / self.delta_y
            y2 = (0.75 - y) / self.delta_y
            R = (1.0 + np.exp(0.5 / self.delta_y))**2 / ((1.0 + np.exp(2 * y1)) * (1.0 + np.exp(2 * y2)))
            vy = self.delta_y * np.sin(2.0 * np.pi * x / self.lamb)
        
        else:
            
            # Instability seeded by grid-noise, e.g. Springel (2010)
            R = np.zeros_like(x)
            R[np.abs(y - 0.5) < 0.25] = 1.0
            vy = self.delta_vy * np.sin(2.0 * np.pi * x / self.lamb) * (np.exp(-0.5 * (y - 0.25)**2) + np.exp(-0.5 * (0.75 - y)**2))

        sim.V[DN] = self.rho2 + R * (self.rho1 - self.rho2)
        sim.V[VX] = self.v2 + R * (self.v1 - self.v2)
        sim.V[VY] = vy
        sim.V[PR] = self.P0
        
        return
    
    # ---------------------------------------------------------------------------------------------

    def plotLimits(self, q_plot, plot_geometry):
        
        vmin = []
        vmax = []

        for q in q_plot:
            if q == 'DN':
                vmin.append(self.rho2 * 0.85)
                vmax.append(self.rho1 * 1.05)
            elif q in ['VX', 'VY']:
                vmin.append(self.v2 * 1.2)
                vmax.append(self.v1 * 1.2)
            elif q == 'PR':
                vmin.append(self.P0 * 0.9)
                vmax.append(self.P0 * 1.15)
            else:
                vmin.append(None)
                vmax.append(None)
        
        return vmin, vmax, None

###################################################################################################
