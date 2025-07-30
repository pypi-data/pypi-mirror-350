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

class SetupKeplerianDisk(setup_base.Setup):
    """
    Keplerian rotating disk
    
    In this classic test, a dense gas disk is rotating with a velocity that balances a point-mass 
    potential via the centrifugal force. This is a notoriously difficult test for Eulerian (grid) 
    codes. To avoid the singularity at the center, the potential is softened. The boundary conditions 
    are set to the same rotation speed and fluid state as the initial conditions. This setup 
    demonstrates:
    
    * Rotating boundary conditions
    * Fixed potential with softening
    * Conservation of angular momentum.
    
    Parameters
    ----------
    soft_edges: bool
        If True, soften the edges of the disk in density with a Gaussian profile of width 
        ``edge_delta_r``. 
    edge_delta_r: float
        See ``soft_edges``.
    unit_l: float
        Code unit for length in units of centimeters.
    unit_t: float
        Code unit for time in units of seconds.
    unit_m: float
        Code unit for mass in units of gram.
    """
    
    def __init__(self, soft_edges = False, edge_delta_r = 0.02,
                 unit_l = 1.0, unit_t = 1.0, unit_m = 1.0):

        setup_base.Setup.__init__(self, unit_l = unit_l, unit_t = unit_t, unit_m = unit_m)
        
        self.rho0 = 0.01
        self.rho_disk = 1.0
        self.P0 = 1.0
        self.r0 = 0.25
        self.r1 = 0.75
        self.soft_edges = soft_edges
        self.delta_r = edge_delta_r
        self.eps = 0.1
        
        return

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'disk'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialConditions(self, sim, nx):
        
        sim.setGravityMode(gravity_mode = 'fixed_pot')
        sim.setDomain(nx, nx, xmin = -1.0, xmax = 1.0, ymin = -1.0, bc_type = 'periodic')

        self.DN = sim.q_prim['DN']
        self.VX = sim.q_prim['VX']
        self.VY = sim.q_prim['VY']
        self.PR = sim.q_prim['PR']
        self.GP = sim.q_prim['GP']

        x, y = sim.xyGrid()
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        
        self.V_ini = np.array(sim.V)
        rho, u_c, phi = self.diskICsSimple(r)
        
        # Set ICs permanently
        self.V_ini[self.DN] = rho
        self.V_ini[self.VX] = -np.sin(theta) * u_c
        self.V_ini[self.VY] = np.cos(theta) * u_c
        self.V_ini[self.PR] = self.P0
        self.V_ini[self.GP] = phi
        
        # Copy to sim
        sim.V[...] = self.V_ini[...]
        
        return

    # ---------------------------------------------------------------------------------------------

    # Generate the ICs as a function of r. For a point-mass potential with no softening, we have
    #
    # F_c = m u^2 / r = F_g = d phi / dr * m --> u = root(r dphi/dr)
    #
    # If we did not soften the potential, we would have 
    #
    # phi        = -r^-1
    # d phi / dr = 1/r^2
    # u          = root(1/r)
    # 
    # This is the classic Keplerian potential. However, the divergence at the center makes the
    # solution highly unstable (and unphysical). So we soften the potential,
    #
    # phi        = -(r^2 + eps^2)^-1/2
    # d phi / dr = - (-1/2) (r^2 + eps^2)^-3/2 * 2r = r (r^2 + eps^2)^-3/2
    # u          = root(r^2 (r^2 + eps^2)^-3/2) = r (r^2 + eps^2)^-3/4

    def diskICsSimple(self, r):
        
        if self.soft_edges:
            rho = np.ones_like(r) * self.rho0
            mask = (r < self.r0)
            rho[mask] = self.rho0 + (self.rho_disk - self.rho0) * np.exp(-0.5 * (self.r0 - r[mask])**2 / self.delta_r**2)
            mask = (r >= self.r0) & (r <= self.r1)
            rho[mask] = self.rho_disk
            mask = (r > self.r1)
            rho[mask] = self.rho0 + (self.rho_disk - self.rho0) * np.exp(-0.5 * (r[mask] - self.r1)**2 / self.delta_r**2)
        else:
            rho = np.ones_like(r) * self.rho0
            mask = (r >= self.r0) & (r <= self.r1)
            rho[mask] = self.rho_disk

        phi = -(r**2 + self.eps**2)**-0.5
        u_c = r * (r**2 + self.eps**2)**-0.75
        
        return rho, u_c, phi

    # ---------------------------------------------------------------------------------------------

    def diskICsGroth(self, r):
        
        g = 1.0 / r**2
        rho = np.ones_like(r) * 0.01

        # Density
        mask = (r < 0.5)
        rho[mask] += (r[mask] / 0.5)**3.0
        mask = (r >= 0.5) & (r <= 2.0)
        rho[mask] += 1.0
        mask = (r > 2.0)
        rho[mask] += (1.0 + (r[mask] - 2.0) / 0.1)**-3.0
        
        # Acceleration
        mask = (r <= 0.35)
        g[mask] *= (r[mask] / 0.35)**2 - (0.35 - r[mask]) / 0.35
        mask = (r >= 2.1)
        g[mask] *= 1.0 + (r[mask] - 2.1) / 0.1
        
        return rho, g

    # ---------------------------------------------------------------------------------------------
    
    def setBoundaryConditions(self, sim):
        
        ng = sim.nghost
        
        sim.V[:, 0:ng, :] = self.V_ini[:, 0:ng, :]
        sim.V[:, -ng:, :] = self.V_ini[:, -ng:, :]
        sim.V[:, :, 0:ng] = self.V_ini[:, :, 0:ng]
        sim.V[:, :, -ng:] = self.V_ini[:, :, -ng:]
        
        sim.primitiveToConserved(sim.V, sim.U)
        
        return
    
    # ---------------------------------------------------------------------------------------------
    
    def trueSolution(self, sim, x, q_plot, plot_geometry):

        if plot_geometry != 'radius':
            return None

        nq = len(q_plot)
        rho, u_c, phi = self.diskICsSimple(x)

        sol_list = []
        for i in range(nq):
            sol = np.zeros((len(x)), float)
            if q_plot[i] == 'DN':
                sol = rho
            elif q_plot[i] == 'VR':
                sol[:] = 0.0
            elif q_plot[i] == 'PR':
                sol[:] = self.P0
            elif q_plot[i] == 'VA':
                sol = u_c
            elif q_plot[i] == 'GP':
                sol = phi
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
                vmax.append(1.25)
            elif q == 'VA':
                vmin.append(0.0)
                vmax.append(2.1)
            elif q == 'VR':
                vmin.append(-0.15)
                vmax.append(0.15)
            elif q == 'PR':
                vmin.append(0.8)
                vmax.append(1.29)
            else:
                vmin.append(None)
                vmax.append(None)
        
        return vmin, vmax, None
    
###################################################################################################
