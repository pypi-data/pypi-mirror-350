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

class SetupRayleighTaylor(setup_base.Setup):
    """
    Rayleigh-Taylor instability

    In this well-known setup, a denser fluid sits on top of a less dense fluid. As the boundary 
    is perturbed with a small velocity, a mushroom-like structure forms. The default setup 
    corresponds to a single peak in velocity at the center of the center of the domain, but the 
    user can investigate multiple linearly added perturbations as well. This setup demonstrates:
    
    * Fixed-acceleration gravity in 2D with wall boundary conditions
    * Instabilities at a two-fluid interface, including their dependence on the scale of 
      perturbations.

    Parameters
    ----------
    aspect_ratio: float
        The ratio of y to x extent of the domain.
    amplitude: float
        The amplitude of the initial y-velocity at the interface.
    frequency: float
        The number of sine wave periods by which the boundary between fluids is perturbed. Unity 
        corresponds to one full wave across the x-range of the domain, one-half corresponds to 
        a single wave peak.
    phase: float
        A phase to add to the sine wave argument, where unity corresponds to a shift by a full
        wavelength (:math:`2 \\pi` radians).
    amplitude_2: float
        Like ``amplitude``, but for a second wave that can optionally be added on top of the first
        to study the behavior of the RT instability for different perturbations.
    frequency_2: float
        Like ``frequency`` but for the second wave.
    phase_2: float
        Like ``phase`` but for the second wave.
    unit_l: float
        Code unit for length in units of centimeters.
    unit_t: float
        Code unit for time in units of seconds.
    unit_m: float
        Code unit for mass in units of gram.
    """
    
    def __init__(self, aspect_ratio = 3.0, amplitude = 0.1, frequency = 0.5, phase = 0.0,
                 amplitude_2 = 0.0, frequency_2 = 0.0, phase_2 = 0.0,
                 unit_l = 1.0, unit_t = 1.0, unit_m = 1.0):

        setup_base.Setup.__init__(self, unit_l = unit_l, unit_t = unit_t, unit_m = unit_m)

        self.aspect_ratio = aspect_ratio
        self.rho_up = 2.0
        self.rho_dn = 1.0
        self.P0 = 1.0
        self.g = 1.0
        self.delta_y =  0.05
        
        self.amplitude_1 = amplitude
        self.frequency_1 = frequency
        self.phase_1 = phase
        
        self.amplitude_2 = amplitude_2
        self.frequency_2 = frequency_2
        self.phase_2 = phase_2
    
        return

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'rt'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialConditions(self, sim, nx):
        
        sim.setGravityMode(gravity_mode = 'fixed_acc', g = self.g)
        sim.setDomain(nx, int(nx * self.aspect_ratio), xmin = 0.0, xmax = 1.0 / self.aspect_ratio, 
                      ymin = 0.0, bc_type = 'wall')

        DN = sim.q_prim['DN']
        VX = sim.q_prim['VX']
        VY = sim.q_prim['VY']
        PR = sim.q_prim['PR']

        # Split the domain in density        
        x, y = sim.xyGrid()
        sim.V[DN][y > 0.5] = self.rho_up
        sim.V[DN][y <= 0.5] = self.rho_dn
        sim.V[VX] = 0.0

        # Create sine waves in y-velocity at the interface
        x_unity = x * self.aspect_ratio
        soft_y = np.exp(-0.5 * (y - 0.5)**2 / self.delta_y**2)
        sim.V[VY] =  self.amplitude_1 * np.sin(2.0 * np.pi * (self.phase_1 + x_unity * self.frequency_1)) * soft_y
        sim.V[VY] += self.amplitude_2 * np.sin(2.0 * np.pi * (self.phase_2 + x_unity * self.frequency_2)) * soft_y

        # Integrate a hydrostatic pressure from the top
        for i in range(sim.ny):
            idx = sim.ylo + sim.ny - i - 1
            if i == 0:
                P = self.P0
            else:
                dP = self.g * sim.V[DN][:, idx] * sim.dx
                P = sim.V[PR][:, idx + 1] + dP
            sim.V[PR][:, idx] = P

        return
    
    # ---------------------------------------------------------------------------------------------

    def plotLimits(self, q_plot, plot_geometry):
        
        vmin = []
        vmax = []

        for q in q_plot:
            if q == 'DN':
                vmin.append(self.rho_dn * 0.9)
                vmax.append(self.rho_up * 1.1)
            elif q in ['VX', 'VY']:
                vmin.append(-0.6)
                vmax.append(0.6)
            elif q == 'PR':
                vmin.append(self.P0 * 0.7)
                vmax.append(self.P0 * 1.3)
            else:
                vmin.append(None)
                vmax.append(None)
        
        return vmin, vmax, None

###################################################################################################
