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

class SetupCloudCrushing(setup_base.Setup):
    """
    Cloud-crushing setup

    In this classic setup, a dense cloud is embedded in a hot, fast-moving, less dense wind at equal
    pressure. The sharp cloud edge creates some initial shocks, but those quicky leave the domain 
    given the outflow boundary conditions. The cloud is rapidly destroyed, but the rate of 
    destruction and the details of the evolution depend quite strongly on resolution. 
    It is tempting to simply set outflow boundary conditions, but the fluid can back-react on the
    left edge as the flow is reflected off the dense blob. Thus, we manually enforce the wind state
    in the left boundary. This setup demonstrates
    
    * Rectangular domain shapes
    * Mixture of standard and user-defined boundary conditions
    * Strong resolution dependence.

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
        
        self.aspect_ratio = 2.0
        self.rho0 = 1.0
        self.rho1 = 100.0
        self.P0 = 1.0
        self.vx = 0.1
        self.r_c = 0.02

        return 

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'cloud_crushing'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialConditions(self, sim, nx):
        
        ny = int(nx // self.aspect_ratio)
        ymax = float(ny) / float(nx)
        sim.setDomain(nx, ny, xmin = 0.0, xmax = 1.0, ymin = 0.0, bc_type = 'outflow')
        
        self.DN = sim.q_prim['DN']
        self.VX = sim.q_prim['VX']
        self.VY = sim.q_prim['VY']
        self.PR = sim.q_prim['PR']

        sim.V[self.DN] = self.rho0
        sim.V[self.VX] = self.vx
        sim.V[self.VY] = 0.0
        sim.V[self.PR] = self.P0

        # Set tophat into the center of the domain
        x, y = sim.xyGrid()
        
        r = np.sqrt((x - 0.1)**2 + (y - 0.5 * ymax)**2)
        mask = (r <= self.r_c)
        sim.V[self.DN][mask] = self.rho1
        sim.V[self.VX][mask] = 0.0
        
        return

    # ---------------------------------------------------------------------------------------------

    def setBoundaryConditions(self, sim):
        
        sim.V[self.DN][:sim.nghost, :] = self.rho0
        sim.V[self.VX][:sim.nghost, :] = self.vx
        sim.V[self.VY][:sim.nghost, :] = 0.0
        sim.V[self.PR][:sim.nghost, :] = self.P0
        
        return

    # ---------------------------------------------------------------------------------------------

    def plotLimits(self, q_plot, plot_geometry):

        vmin = []
        vmax = []
        log = []

        for q in q_plot:
            if q == 'DN':
                vmin.append(self.rho0)
                vmax.append(self.rho1 * 0.8)
                log.append(True)
            elif q in ['VX', 'VY']:
                vmin.append(-self.vx * 1.1)
                vmax.append(self.vx * 1.1)
                log.append(False)
            elif q == 'PR':
                vmin.append(self.P0 * 0.5)
                vmax.append(self.P0 * 1.3)
                log.append(True)
            else:
                vmin.append(None)
                vmax.append(None)
                log.append(False)
        
        return vmin, vmax, log

###################################################################################################
