###################################################################################################
#
# This file is part of the ULULA code.
#
# (c) Benedikt Diemer, University of Maryland
#
###################################################################################################

import numpy as np 

import ulula.core.setup_base as setup_base
import ulula.physics.constants as constants

###################################################################################################

class SetupAtmosphere(setup_base.Setup):
    """
    Earth's hydrostratic atmosphere

    This setup represents the Earth's atmosphere in 1D. This hydro problem can be solved 
    analytically for a fixed temperature, but in reality the temperature does evolve somewhat
    with altitude. This setup thus offers two modes. For an isothermal EOS, the air settles into
    an exponential density and pressure profile. We perturb the initial density away from the 
    known solution by assuming a "wrong" scale height. After some time, the atmosphere settles to
    the correct solution. 
    
    If the ideal gas EOS is chosen, a piecewise-linear approximation to the known temperature 
    profile is enforced at each timestep. In this setup, the initial profile is set to the 
    isothermal solution, and that solution is also plotted as the "true solution" for comparison.
    This setup demonstrates
    
    * Fixed-acceleration gravity with wall boundary conditions
    * Isothermal and ideal equations of state
    * Code units suitable to Earth conditions, including Earth gravity
    * User-defined function to update the fluid state at runtime.
    
    By default, the code units are set to kilometers, hours, and tons. Depending on the initial 
    conditions, the setup can be numerically unstable due to strong motions that develop into 
    shocks. For example, if too much mass is initially placed in the upper atmosphere, that 
    mass falls to the surface. Similarly, extending the upper limit to much higher altitude than 
    the default of 30 km can lead to difficulties due to the very low pressure and density. 

    Parameters
    ----------
    eos_mode: str
        Equation of state to use. Can be ``'isothermal'``, in which case the temperature is set by 
        the ``T`` parameter, or ``'ideal'``, in which case an approximation to Earth's true 
        atmosphere used.
    T: float
        Air temperature in Kelvin for isothermal equation of state; ignored for ideal gas EOS.
    xmax: float
        The height of the domain in code units (kilometers by default). This number cannot get
        arbitrarily large because the density and pressure get very low, which can lead to 
        numerical instabilities.
    unit_l: float
        Code unit for length in units of centimeters.
    unit_t: float
        Code unit for time in units of seconds.
    unit_m: float
        Code unit for mass in units of gram.
    """
    
    def __init__(self, eos_mode = 'isothermal', T = 270.0, xmax = 30.0,
                 unit_l = 1E5, unit_t = 3600.0, unit_m = 1E12):

        setup_base.Setup.__init__(self, unit_l = unit_l, unit_t = unit_t, unit_m = unit_m)

        # Constants. The T_z table gives the approximate temperature of Earth's atmosphere as a 
        # function of height (in K, km).
        self.gamma = 7.0 / 5.0
        self.mu = constants.mu_air
        self.T_z = np.array([[287.0, 0.0], [217.0, 11.0], [217.0, 20.0], [228.0, 32.0],
                             [270.0, 49.0], [270.0, 53.0], [256.0, 60.0], [190.0, 80.0], 
                             [190.0, 90.0], [202.0, 100.0]])

        # Parameters; even if using the ideal gas EOS, we derive the isothermal solution in code
        # units to set it as the ICs.
        self.eos_mode = eos_mode
        self.xmax = xmax
        self.T = T
        self.g_cu = constants.g_earth_cgs / unit_l * unit_t**2
        self.rho0_cu = constants.rho_air_cgs / unit_m * unit_l**3
        self.eint_cu = self.internalEnergyFromTemperature(self.T, self.mu, self.gamma)

        print('Atmosphere setup: in code units, rho_air = %.2e, g = %.2e, eint = %.2e.' \
              % (self.rho0_cu, self.g_cu, self.eint_cu))
                
        return 

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'atmosphere'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialConditions(self, sim, nx):

        if self.eos_mode == 'isothermal':
            sim.setEquationOfState(eos_mode = 'isothermal', eint_fixed = self.eint_cu, gamma = self.gamma, mu = self.mu)
        elif self.eos_mode == 'ideal':
            sim.setEquationOfState(eos_mode = 'ideal', gamma = self.gamma, mu = self.mu)
        else:
            raise Exception('Unsupported EOS mode for atmosphere setup, %s.' % (self.eos_mode))
        
        sim.setGravityMode(gravity_mode = 'fixed_acc', g = self.g_cu)
        sim.setDomain(nx, 1, xmin = 0.0, xmax = self.xmax, bc_type = 'wall')

        # Compute the hydrostatic, isothermal solution
        DN = sim.q_prim['DN']
        x, _ = sim.xyGrid()
        rho_isothermal, h0 = self.hydrostaticDensity(x, sim)
        
        # If isothermal, we offset the ICs from the true solution and normalize to the same total
        # mass. If ideal, we use the isothermal solution as the ICs and we pre-compute a grid of
        # T(x).
        if self.eos_mode == 'isothermal':
            sim.V[DN] = self.rho0_cu * np.exp(-x / h0 * 0.6) 
            m_tot_ics = np.sum(sim.V[DN])
            m_tot_sol = np.sum(rho_isothermal)
            sim.V[DN] *= m_tot_sol / m_tot_ics
        elif self.eos_mode == 'ideal':
            sim.V[DN] = rho_isothermal
            x, _ = sim.xyGrid()
            x_km = x * self.unit_l / 1E5
            self.T_x = np.interp(x_km, self.T_z[:, 1], self.T_z[:, 0])
            self.updateFunction(sim)
        else:
            raise Exception('Unsupported EOS mode for atmosphere setup, %s.' % (self.eos_mode))
        
        return
  
    # ---------------------------------------------------------------------------------------------

    # Since eint = kT / ((gamma - 1) mu mp), we have that h0 = kT g / mu mp = eint * (gamma - 1) / g
    
    def hydrostaticDensity(self, x, sim):
        
        h0 = self.eint_cu * (self.gamma - 1.0) / sim.gravity_g
        rho = self.rho0_cu * np.exp(-x / h0)
        
        return rho, h0
    
    # ---------------------------------------------------------------------------------------------

    # This function is executed at every timestep. If we are using the ideal EOS, we enforce the
    # temperature profile. 

    def updateFunction(self, sim):

        if self.eos_mode == 'isothermal':
            return

        # Compute pressure in cgs and then convert to code units
        rho_cgs = sim.V[sim.q_prim['DN']] * self.unit_m / self.unit_l**3
        P_cgs = rho_cgs * constants.kB_cgs * self.T_x / (self.mu * constants.mp_cgs)
        P_cu = P_cgs / self.unit_m * self.unit_l * self.unit_t**2

        # Set pressure to simulation grid and ensure primitive-conserved conversion
        sim.V[sim.q_prim['PR']] = P_cu
        sim.primitiveToConserved(sim.V, sim.U)
        
        return
    
    # ---------------------------------------------------------------------------------------------

    def plotLimits(self, q_plot, plot_geometry):
        
        vmin = []
        vmax = []

        for q in q_plot:
            if q == 'DN':
                vmin.append(0.0)
                vmax.append(self.rho0_cu * 1.2)
            elif q in ['VX', 'VY']:
                vmin.append(-3E2)
                vmax.append(3E2)
            elif q in ['PR', 'ET']:
                vmin.append(0.0)
                vmax.append(self.rho0_cu * self.eint_cu * (self.gamma - 1.0) * 1.2)
            elif q == 'EI':
                vmin.append(0.0)
                vmax.append(self.eint_cu * (self.gamma - 1.0) * 1.2)
            else:
                vmin.append(None)
                vmax.append(None)
        
        return vmin, vmax, None

    # ---------------------------------------------------------------------------------------------

    def trueSolution(self, sim, x, q_plot, plot_geometry):
        
        rho_true, _ = self.hydrostaticDensity(x, sim)
        
        sol_list = []
        for i in range(len(q_plot)):
            q = q_plot[i]
            sol = np.zeros((len(x)), float)
            if q == 'DN':
                sol[:] = rho_true
            elif q == 'VX':
                sol[:] = 0.0
            elif q == 'PR': 
                sol[:] = rho_true * self.eint_cu * (self.gamma - 1.0)
            elif q == 'TK': 
                sol[:] = self.T
            else:
                sol = None
            sol_list.append(sol)
        
        return sol_list

###################################################################################################
