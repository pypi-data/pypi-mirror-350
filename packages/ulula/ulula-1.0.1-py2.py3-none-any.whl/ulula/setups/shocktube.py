###################################################################################################
#
# This file is part of the ULULA code.
#
# (c) Benedikt Diemer, University of Maryland
#
###################################################################################################

import numpy as np
import scipy.optimize

import ulula.core.setup_base as setup_base

###################################################################################################

class SetupShocktube(setup_base.Setup):
    """
    Shocktube problem
    
    The shocktube setup represents a Riemann problem, i.e., a sharp discontinuity in a 1D domain.
    The default parameters represent the Sod 
    (`1978 <https://ui.adsabs.harvard.edu/abs/1978JCoPh..27....1S/abstract>`_) setup, which is a 
    classic test for Riemann solvers. The sharp break in fluid properties causes a shock and a 
    contact discontinuity traveling to the right and a rarefaction wave traveling to the left. 
    This setup demonstrates:
    
    * Ability of hydro solver to handle strong shocks
    * Impact of slope limiting on the solution
    * Softening of sharp discontinuities at lower resolution.
    
    The Sod problem can be solved analytically. The solution used here is based on lecture notes by 
    `Frank van den Bosch <https://campuspress.yale.edu/vdbosch/>`__
    (`pdf <http://www.astro.yale.edu/vdbosch/Astrophysical_Flows.pdf>`__)
    and `Susanne Hoefner <https://www.uu.se/en/contact-and-organisation/staff?query=N99-874>`__
    (`pdf <https://www.astro.uu.se/~hoefner/astro/teach/ch10.pdf>`__). However, this solution may not 
    work for all sets of input parameters.
    
    Parameters
    ----------
    gamma: float
        The adiabatic index of the ideal gas.
    x0: float
        The position of the discontinuity.
    rhoL: float
        The density of the left state.
    rhoR: float
        The density of the right state.
    PL: float
        The pressure of the left state.
    PR: float
        The pressure of the right state.
    vL: float
        The velocity of the left state.
    vR: float
        The velocity of the right state.
    unit_l: float
        Code unit for length in units of centimeters.
    unit_t: float
        Code unit for time in units of seconds.
    unit_m: float
        Code unit for mass in units of gram.
    """
    
    def __init__(self, gamma = 1.4, x0 = 0.5, rhoL = 1.0, rhoR = 1.0 / 8.0,  
                 PL = 1.0, PR = 1.0 / 10.0, vL = 0.0, vR = 0.0,
                 unit_l = 1.0, unit_t = 1.0, unit_m = 1.0):
        
        setup_base.Setup.__init__(self, unit_l = unit_l, unit_t = unit_t, unit_m = unit_m)
    
        self.gamma = gamma
        self.x0 = x0
        self.rhoL = rhoL
        self.rhoR = rhoR
        self.PL = PL
        self.PR = PR
        self.vL = vL
        self.vR = vR

        return 

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'shocktube'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialConditions(self, sim, nx):
        
        sim.setEquationOfState(eos_mode = 'ideal', gamma = self.gamma)
        sim.setDomain(nx, 1, xmin = 0.0, xmax = 1.0, bc_type = 'outflow')

        DN = sim.q_prim['DN']
        VX = sim.q_prim['VX']
        PR = sim.q_prim['PR']

        maskL = (sim.x <= self.x0)
        maskR = np.logical_not(maskL)
        sim.V[DN, maskL, :] = self.rhoL
        sim.V[DN, maskR, :] = self.rhoR
        sim.V[VX, maskL, :] = self.vL
        sim.V[VX, maskR, :] = self.vR
        sim.V[PR, maskL, :] = self.PL
        sim.V[PR, maskR, :] = self.PR
        
        return

    # ---------------------------------------------------------------------------------------------

    def trueSolution(self, sim, x, q_plot, plot_geometry):
    
        # Grid variables
        t = sim.t
        nx = len(x)
    
        # Shorthand for Sod input variables
        P_L = self.PL
        P_R = self.PR
        rho_L = self.rhoL
        rho_R = self.rhoR
        v_L = self.vL
        v_R = self.vR
        x_0 = self.x0
        
        # gamma and sound speed
        g = self.gamma
        gm1 = g - 1.0
        gp1 = g + 1.0
        cs_L = np.sqrt(g * P_L / rho_L)
        cs_R = np.sqrt(g * P_R / rho_R)
    
        # Implicit equation to solve for shock speed in Sod problem
        def eq(M):
            t1 = P_R / P_L * (2.0 * g / gp1 * M**2 - gm1 / gp1)
            rhs = cs_L * gp1 / gm1 * (1.0 - t1**(gm1 / 2.0 / g))
            return M - 1.0 / M - rhs
        
        # Compute speed of shock in frame of tube. This calculation can crash for certain input
        # values, in which case we return no solution.
        try:
            M = scipy.optimize.brentq(eq, 1.0001, 20.0, xtol = 1E-6)
        except Exception:
            return None
        
        # The numerical solution comes out wrong by this factor for some yet unknown reason.
        M *= 0.986
        M_2 = M**2
        v_s = M * cs_R
        
        # Post-shock state after shock has passed through area R. van den Bosch has
        # v_1 = 2.0 / gp1 * (M - 1.0 / M) 
        # for the velocity, but this seems to give the wrong result. The current way of computing v_1
        # was derived by going into the shock frame where vRp = vR - vs, v1p = v_1 - vs, and using the
        # RH-condition that v1p / vRp = (gm1 * M2 + 2)/(gp1 * M2)
        P_1 = P_R * (2.0 * g / gp1 * M_2 - gm1 / gp1)
        rho_1 = rho_R / (2.0 / gp1 / M_2 + gm1 / gp1)
        v_1 = v_s * (1.0 - (2.0 / gp1 / M_2 + gm1 / gp1))
        
        # State to the left of contact discontinuity with state 1
        P_2 = P_1
        v_2 = v_1
        rho_2 = rho_L * (P_2 / P_L)**(1.0 / g)
        cs_2 = np.sqrt(g * P_2 / rho_2)
        
        # Boundaries of states. The rarefacton wave progresses at speed csL to the left and thus
        # reaches x1 by time t. The shock to the right goes as us * t to x4, whereas the contact
        # discontinuity moves at the speed of state 2. 
        x_1 = x_0 - cs_L * t
        x_2 = x_0 + (v_2 - cs_2) * t
        x_3 = x_0 + v_2 * t
        x_4 = x_0 + v_s * t
        
        # Areas of array where solutions are valid
        maskL = (x <= x_1)
        maskE = (x > x_1) & (x <= x_2)
        mask2 = (x > x_2) & (x <= x_3)
        mask1 = (x > x_3) & (x <= x_4)
        maskR = (x > x_4)
    
        # Compute rarefaction state, which depends on position unlike the other states
        x_E = x[maskE]
        v_E = 2.0 / gp1 * (cs_L + (x_E - x_0) / t)
        cs_E = cs_L - 0.5 * gm1 * v_E
        P_E = P_L * (cs_E / cs_L)**(2.0 * g / gm1)
        rho_E = g * P_E / cs_E**2
        
        # Set solution
        nq = len(q_plot)
        sol_list = []
        for i in range(nq):
            sol = np.zeros((nx), float)
            if q_plot[i] == 'DN':
                sol[maskL] = rho_L
                sol[maskE] = rho_E
                sol[mask2] = rho_2
                sol[mask1] = rho_1
                sol[maskR] = rho_R
            elif q_plot[i] == 'VX':
                sol[maskL] = v_L
                sol[maskE] = v_E
                sol[mask2] = v_2
                sol[mask1] = v_1
                sol[maskR] = v_R
            elif q_plot[i] == 'PR':
                sol[maskL] = P_L
                sol[maskE] = P_E
                sol[mask2] = P_2
                sol[mask1] = P_1
                sol[maskR] = P_R
            elif q_plot[i] == 'EI':
                sol[maskL] = P_L / gm1 / rho_L
                sol[maskE] = P_E / gm1 / rho_E
                sol[mask2] = P_2 / gm1 / rho_2
                sol[mask1] = P_1 / gm1 / rho_1
                sol[maskR] = P_R / gm1 / rho_R
            else:
                sol = None
            sol_list.append(sol)
        
        return sol_list

###################################################################################################
