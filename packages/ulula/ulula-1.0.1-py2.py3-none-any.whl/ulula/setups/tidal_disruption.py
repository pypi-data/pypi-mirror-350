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

class SetupTidalDisruption(setup_base.Setup):
    """
    Gravitational tidal disruption

    The gravitational potential in the domain represents a point mass at the center. A gas blob
    moves past the point mass and is tidally disrupted. This setup demonstrates
    
    * Fixed-potential gravity
    * Behavior at strong potential gradients.

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
        self.vx = 0.0
        self.vy = 0.3
        self.r_th = 0.07

        return 

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'tidal_disruption'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialConditions(self, sim, nx):
        
        sim.setGravityMode(gravity_mode = 'fixed_pot')
        sim.setDomain(nx, nx, xmin = 0.0, xmax = 1.0, ymin = 0.0, bc_type = 'outflow')
        
        DN = sim.q_prim['DN']
        VX = sim.q_prim['VX']
        VY = sim.q_prim['VY']
        PR = sim.q_prim['PR']
        GP = sim.q_prim['GP']
        
        # Uniform density/pressure domain
        sim.V[DN] = self.rho0
        sim.V[VX] = self.vx
        sim.V[VY] = self.vy
        sim.V[PR] = self.P0

        # Blob of gas
        x, y = sim.xyGrid()
        r = np.sqrt((x - 0.35)**2 + (y - 0.35)**2)
        sim.V[DN] += self.rho1 * np.exp(-0.5 * r**2 / self.r_th**2)

        # Potential
        r = np.sqrt((x - 0.5)**2 + (y - 0.5)**2)
        sim.V[GP] = -0.1 / (0.01 + r)
        
        return
        
    # ---------------------------------------------------------------------------------------------

    def plotLimits(self, q_plot, plot_geometry):
        
        vmin = []
        vmax = []

        for q in q_plot:
            if q == 'DN':
                vmin.append(0.0)
                vmax.append(self.rho1 * 0.8)
            elif q in ['VX', 'VY']:
                vmin.append(-0.8)
                vmax.append(0.8)
            elif q == 'PR':
                vmin.append(self.P0 * 0.8)
                vmax.append(self.P0 * 1.4)
            elif q == 'ET':
                vmin.append(1.3)
                vmax.append(2.0)
            else:
                vmin.append(None)
                vmax.append(None)
        
        return vmin, vmax, None

###################################################################################################
