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

class SetupSoundwave(setup_base.Setup):
    """
    Propagating sound wave
    
    A sound wave is created at the left edge of the domain and travels to the right. We assume the
    density and adiabatic index of air, and either standard pressure or an isothermal EOS given
    by a particular temperature. This setup demonstrates
    
    * User-defined boundary conditions on one side of the domain
    * Outflow boundary conditions on another side
    * Difference between ideal and isothermal equations of state
    * Code units.
    
    The true solution is based on linear theory, which only holds for small amplitudes. We observe 
    wave steepening for large amplitudes.

    Parameters
    ----------
    L: float
        The box size in cm.
    frequency: float
        The frequency of the soundwave in Hertz.
    amplitude: float
        The relative amplitude by which the density oscillates compared to the background. 
    eos_mode: str
        Can be ``'ideal'`` or ``'isothermal'``.
    eos_T_K: float
        Air temperature in Kelvin (if using isothermal EOS, ignored otherwise).
    unit_l: float
        Code unit for length in units of centimeters.
    unit_t: float
        Code unit for time in units of seconds.
    unit_m: float
        Code unit for mass in units of gram.
    """
    
    def __init__(self, L = 1E5, frequency = 1.0, amplitude = 0.01, eos_mode = 'ideal', eos_T_K = 300.0,
                 unit_l = 1E5, unit_t = 1.0, unit_m = 1E12):

        setup_base.Setup.__init__(self, unit_l = unit_l, unit_t = unit_t, unit_m = unit_m)
        
        self.eos_mode = eos_mode
        self.eos_T_K = eos_T_K
        self.frequency = frequency * self.unit_t
        self.amplitude = amplitude

        # Assume air
        self.xmax = L / self.unit_l
        self.rho0 = constants.rho_air_cgs / unit_m * unit_l**3
        self.P0 = constants.P_standard / unit_m * unit_l * unit_t**2
        self.eos_gamma = 7.0 / 5.0
        self.eos_mu = constants.mu_air
        self.eos_eint_fixed = None

        # Derived variables        
        if self.eos_mode == 'ideal':
            self.cs = np.sqrt(self.eos_gamma * self.P0 / self.rho0)
            print('Soundwave setup: ideal EOS, in code units, rho0 = %.1e, P0 = %.1e, cs = %.1e.' \
                  % (self.rho0, self.P0, self.cs))

        elif self.eos_mode == 'isothermal':
            self.eos_eint_fixed = self.internalEnergyFromTemperature(self.eos_T_K, self.eos_mu, self.eos_gamma)
            self.P0 = self.rho0 * self.eos_eint_fixed * (self.eos_gamma - 1.0)
            self.cs = np.sqrt(self.eos_eint_fixed * (self.eos_gamma - 1.0))
            print('Soundwave setup: isothermal EOS, in code units, rho0 = %.1e, P0 = %.1e, cs = %.1e, eint = %.1e.' \
                  % (self.rho0, self.P0, self.cs, self.eos_eint_fixed))
            
        else:
            raise Exception('Unknown EOS mode, %s.' % (self.eos_mode))

        self.omega = 2.0 * np.pi * self.frequency
        self.k = self.omega / self.cs
        
        return 

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'soundwave'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialConditions(self, sim, nx):
        
        sim.setEquationOfState(eos_mode = self.eos_mode, eint_fixed = self.eos_eint_fixed, 
                               gamma = self.eos_gamma, mu = self.eos_mu)
        sim.setDomain(nx, 1, xmin = 0.0, xmax = self.xmax, bc_type = 'outflow')

        sim.V[sim.q_prim['DN'], ...] = self.rho0
        if sim.track_pressure:
            sim.V[sim.q_prim['PR'], ...] = self.P0
        
        return

    # ---------------------------------------------------------------------------------------------

    def soundWaveSolution(self, x, t):

        d_rho = self.amplitude * np.sin(self.omega * t - self.k * x)
        rho = self.rho0 * (1.0 + d_rho)
        vx = d_rho * self.cs
        
        if self.eos_mode == 'ideal':
            P = self.P0 * (rho / self.rho0)**self.eos_gamma
        elif self.eos_mode == 'isothermal':
            P = rho * self.eos_eint_fixed * (self.eos_gamma - 1.0)
        else:
            raise Exception('Unknown EOS mode, %s.' % (self.eos_mode))
        
        return rho, P, vx

    # ---------------------------------------------------------------------------------------------

    # We set the left ghost cells to the time-evolving density and pressure corresponding to a 
    # sound wave. We need to manually convert the primitive variables back to conserved ones.
    
    def setBoundaryConditions(self, sim):
        
        ng = sim.nghost
        rho, P, vx = self.soundWaveSolution(sim.x[0:ng], sim.t)
        sim.V[sim.DN, 0:ng, 0] = rho
        sim.V[sim.VX, 0:ng, 0] = vx
        if sim.track_pressure:
            sim.V[sim.PR, 0:ng, 0] = P
        sim.primitiveToConserved(sim.V[:, 0:ng, :], sim.U[:, 0:ng, :])
        
        return
    
    # ---------------------------------------------------------------------------------------------

    def trueSolution(self, sim, x, q_plot, plot_geometry):
        
        rho, P, vx = self.soundWaveSolution(x, sim.t)
       
        mask_wave = (x <= self.cs * sim.t)
        mask_flat = np.logical_not(mask_wave)

        sol_list = []
        for i in range(len(q_plot)):
            q = q_plot[i]
            sol = np.zeros((len(x)), float)
            if q == 'DN':
                sol[mask_wave] = rho[mask_wave]
                sol[mask_flat] = self.rho0
            elif q == 'VX':
                sol[mask_wave] = vx[mask_wave]
                sol[mask_flat] = 0.0
            elif q == 'PR': 
                sol[mask_wave] = P[mask_wave]
                sol[mask_flat] = self.P0
            elif q == 'ET':
                sol[mask_wave] = 0.5 * rho[mask_wave] * vx[mask_wave]**2 + P[mask_wave] / (self.eos_gamma - 1.0)
                sol[mask_flat] = self.P0 / (self.eos_gamma - 1.0)
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
                vmin.append(self.rho0 * (1.0 - self.amplitude * 1.4))
                vmax.append(self.rho0 * (1.0 + self.amplitude * 1.4))
            elif q in ['VX', 'VY']:
                vmin.append(-self.cs * self.amplitude * 1.4)
                vmax.append(self.cs * self.amplitude * 1.4)
            elif q in ['PR']:
                vmin.append(self.P0 * (1.0 - self.amplitude * 2.0))
                vmax.append(self.P0 * (1.0 + self.amplitude * 2.0))
            elif q == 'EI':
                vmin.append(0.0)
                vmax.append(2.0)
            else:
                vmin.append(None)
                vmax.append(None)
        
        return vmin, vmax, None

###################################################################################################
