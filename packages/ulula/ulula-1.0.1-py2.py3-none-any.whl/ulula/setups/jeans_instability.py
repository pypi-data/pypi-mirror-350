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

class SetupJeansInstability(setup_base.Setup):
    """
    Jeans instability

    In this setup, a background state with constant density and (isothermal) pressure is perturbed
    by a sine wave. Depending on the ratio of the wavenumber to the critical "Jeans wavenumber,"
    the perturbation is stable (if :math:`\\lambda < \\lambda_{\\rm J}`, meaning the fluid state
    oscillates) or unstable (if :math:`\\lambda > \\lambda_{\\rm J}`, meaning the perturbation 
    collapses). In practice, we seem to need :math:`\\lambda_{\\rm J} / \\lambda \\sim 1.5` for
    stability. This setup demonstrates
    
    * Self-gravity and run-away collapse
    * Stability criteria.
    
    Parameters
    ----------
    lam: float
        The wavelength of the initial perturbation, where unity corresponds to one wave across the
        domain.
    lam_J: float
        The critical Jeans wavelength for stability, which is determined by the balance between
        pressure and gravity. We set the gravitational constant according to this number.
    amplitude: float
        The amplitude of the initial perturbation as a fraction of the background density.
    unit_l: float
        Code unit for length in units of centimeters.
    unit_t: float
        Code unit for time in units of seconds.
    unit_m: float
        Code unit for mass in units of gram.
    """

    def __init__(self, lam = 1.0, lam_J = 1.3, amplitude = 0.01,
                 unit_l = 1.0, unit_t = 1.0, unit_m = 1.0):

        setup_base.Setup.__init__(self, unit_l = unit_l, unit_t = unit_t, unit_m = unit_m)

        self.rho0 = 1.0
        self.P0 = 1.0
        self.gamma = 5.0 / 3.0

        self.amplitude = amplitude
        self.k = 2.0 * np.pi / lam
        self.kJ = 2.0 * np.pi / lam_J
        self.eint_cu = self.P0 / self.rho0 / (self.gamma - 1.0)
        cs2 = self.P0 / self.rho0
        self.G = self.kJ**2 * cs2 / np.sqrt(4.0 * np.pi * self.rho0)
        
        print('Jeans instability setup: G = %.2e in code units.' % (self.G))

        return 

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'jeans'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialConditions(self, sim, nx):
        
        sim.setEquationOfState(eos_mode = 'isothermal', eint_fixed = self.eint_cu, gamma = self.gamma)
        sim.setGravityMode(gravity_mode = 'poisson', G = self.G)
        sim.setDomain(nx, 1, xmin = 0.0, xmax = 1.0, bc_type = 'periodic')

        x, _ = sim.xyGrid()
        sim.V[sim.q_prim['DN']] = self.rho0 * (1.0 + self.amplitude * np.sin(x * self.k))
        
        return

    # ---------------------------------------------------------------------------------------------

    def plotLimits(self, q_plot, plot_geometry):
        
        vmin = []
        vmax = []
        log = []

        for q in q_plot:
            if q == 'DN':
                vmin.append(1E-2)
                vmax.append(1E2)
                log.append(True)
            elif q in ['VX']:
                vmin.append(-0.5)
                vmax.append(0.5)
                log.append(False)
            elif q == 'PR':
                vmin.append(1E-2)
                vmax.append(1E2)
                log.append(True)
            elif q == 'GP':
                vmin.append(70.0)
                vmax.append(90.0)
                log.append(False)
            elif q == 'GX':
                vmin.append(-100.0)
                vmax.append(100.0)
                log.append(False)
            else:
                vmin.append(None)
                vmax.append(None)
                log.append(False)
        
        return vmin, vmax, log

###################################################################################################
