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

class SetupAdvection1D(setup_base.Setup):
    """
    1D advection test
    
    This setup represents the perhaps simplest meaningful test of a hydro solver. An initial 
    distribution in density is advected at a constant velocity across the domain. The shape should
    be preserved. This setup demonstrates
    
    * Stability and instability of schemes
    * Importance of choices such as slope limiters and Riemann solvers.
    
    Parameters
    ----------
    shape: str
        Initial density shape that is being advected. Can be ``'sine'`` or ``'tophat'``.
    unit_l: float
        Code unit for length in units of centimeters.
    unit_t: float
        Code unit for time in units of seconds.
    unit_m: float
        Code unit for mass in units of gram.
    """
    
    def __init__(self, shape = 'sine', unit_l = 1.0, unit_t = 1.0, unit_m = 1.0):
        
        setup_base.Setup.__init__(self, unit_l = unit_l, unit_t = unit_t, unit_m = unit_m)
    
        self.shape = shape
        self.sine_k = 2.0
        self.vx = 1.0
        self.P = 1.0
    
        return 

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'advection1d'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialConditions(self, sim, nx):
        
        sim.setEquationOfState(eos_mode = 'ideal', gamma = 5.0 / 3.0)
        sim.setDomain(nx, 1, xmin = 0.0, xmax = 1.0, bc_type = 'periodic')

        x, _ = sim.xyGrid()
        sim.V[sim.q_prim['DN']] = self.density(sim, x)
        sim.V[sim.q_prim['VX']] = self.vx
        sim.V[sim.q_prim['PR']] = self.P
        
        return

    # ---------------------------------------------------------------------------------------------

    def density(self, sim, x):
        
        xt = x - sim.t * self.vx
        
        if self.shape == 'sine':
            rho = 0.6 + 0.4 * np.sin(xt * self.sine_k * 2.0 * np.pi)
        
        elif self.shape == 'tophat':
            rho = np.ones_like(x) * 0.1
            th_left = (1.0 / 3.0 + sim.t * self.vx) % sim.xmax
            th_right = (2.0 / 3.0 + sim.t * self.vx) % sim.xmax
            if th_left < th_right:
                rho[np.logical_and(x >= th_left, x <= th_right)] = 1.0
            else:
                rho[np.logical_or(x >= th_left, x <= th_right)] = 1.0
            
        else:
            raise Exception('Unknown shape, %s.' % (self.shape))
        
        return rho

    # ---------------------------------------------------------------------------------------------

    def trueSolution(self, sim, x, q_plot, plot_geometry):
        
        sol_list = []
        for i in range(len(q_plot)):
            q = q_plot[i]
            sol = np.zeros((len(x)), float)
            if q == 'DN':
                sol[:] = self.density(sim, x)
            elif q == 'VX':
                sol[:] = self.vx
            elif q == 'PR': 
                sol[:] = self.P
            else:
                sol = None
            sol_list.append(sol)
            
        return sol_list

    # ---------------------------------------------------------------------------------------------

    def plotLimits(self, q_plot, plot_geometry):
        
        vmin = []
        vmax = []

        for q in q_plot:
            if q == 'DN':
                vmin.append(0.0)
                vmax.append(1.3)
            elif q in ['VX']:
                vmin.append(self.vx - 0.1)
                vmax.append(self.vx + 0.1)
            elif q == 'PR':
                vmin.append(self.P - 0.1)
                vmax.append(self.P + 0.1)
            else:
                vmin.append(None)
                vmax.append(None)
        
        return vmin, vmax, None
  
###################################################################################################
