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

class SetupGreshoVortex(setup_base.Setup):
    """
    Gresho Vortex
    
    This setup tests the symmetry and angular momentum conservation of the hydro solver. A ring at
    the center of the domain has positive azimuthal velocity, which creates a centrifugal force 
    that is balanced by pressure gradients. Ideally, the setup should be stable as the gas rotates 
    around the center. Any smoothing of the ring is an indication that angular momentum is not 
    perfectly preserved. The problem was presented in Gresho & Sani 
    `1987 <https://ui.adsabs.harvard.edu/abs/1987IJNMF...7.1111G/abstract>`_ (see also Liska & 
    Wendroff `2003 <https://ui.adsabs.harvard.edu/abs/2003SJSC...25..995L/abstract>`_). This setup 
    demonstrates
    
    * Computing and plotting of azimuthal velocities
    * Angular momentum conservation.
    
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
        
        return

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'gresho'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialConditions(self, sim, nx):
        
        sim.setDomain(nx, nx, xmin = -1.0, xmax = 1.0, ymin = -1.0, bc_type = 'periodic')

        DN = sim.q_prim['DN']
        VX = sim.q_prim['VX']
        VY = sim.q_prim['VY']
        PR = sim.q_prim['PR']

        # Generate the ICs as a function of r
        x, y = sim.xyGrid()
        r = np.sqrt(x**2 + y**2)
        phi = np.arctan2(y, x)
        u_phi, P = self.vortexICs(r)
        
        # Set in domain
        sim.V[DN] = 1.0
        sim.V[VX] = -np.sin(phi) * u_phi
        sim.V[VY] = np.cos(phi) * u_phi
        sim.V[PR] = P
        
        return

    # ---------------------------------------------------------------------------------------------

    def vortexICs(self, r):
        
        u_phi = np.zeros_like(r)
        P = np.zeros_like(r)
        
        # Inner ring, r < 0.2
        mask = (r <= 0.2)
        u_phi[mask] = 5.0 * r[mask]
        P[mask] = 5.0 + 25.0 / 2.0 * r[mask]**2
        
        # Middle ring, 0.2 < r < 0.4
        mask = (r > 0.2) & (r <= 0.4)
        u_phi[mask] = 2.0 - 5.0 * r[mask]
        P[mask] = 9.0 - 4.0 * np.log(0.2) + 25.0 / 2.0 * r[mask]**2 - 20.0 * r[mask] + 4.0 * np.log(r[mask])

        # Outer ring, r > 0.4
        mask = (r > 0.4)
        u_phi[mask] = 0.0
        P[mask] = 3.0 + 4.0 * np.log(2.0)

        return u_phi, P

    # ---------------------------------------------------------------------------------------------

    def plotLimits(self, q_plot, plot_geometry):
        
        vmin = []
        vmax = []

        for q in q_plot:
            if q == 'DN':
                vmin.append(0.9965)
                vmax.append(1.0035)
            elif q in ['VX', 'VY']:
                vmin.append(-1.05)
                vmax.append(1.05)
            elif q == 'VA':
                if plot_geometry == '2d':
                    vmin.append(-1.05)
                    vmax.append(1.05)
                else:
                    vmin.append(-0.1)
                    vmax.append(1.05)
            elif q == 'VR':
                vmin.append(-3.5E-2)
                vmax.append(3.5E-2)
            elif q == 'PR':
                vmin.append(5.0)
                vmax.append(5.9)
            else:
                vmin.append(None)
                vmax.append(None)
        
        return vmin, vmax, None
    
    # ---------------------------------------------------------------------------------------------
    
    def trueSolution(self, sim, x, q_plot, plot_geometry):

        if plot_geometry != 'radius':
            return None

        nq = len(q_plot)
        u_phi, P = self.vortexICs(x)

        sol_list = []
        for i in range(nq):
            sol = np.zeros((len(x)), float)
            if q_plot[i] == 'DN':
                sol[:] = 1.0
            elif q_plot[i] == 'VR':
                sol[:] = 0.0
            elif q_plot[i] == 'PR':
                sol = P
            elif q_plot[i] == 'VA':
                sol = u_phi
            else:
                sol = None
            sol_list.append(sol)
        
        return sol_list
    
###################################################################################################
