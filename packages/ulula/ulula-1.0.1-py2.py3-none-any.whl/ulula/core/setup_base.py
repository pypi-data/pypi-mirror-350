###################################################################################################
#
# This file is part of the ULULA code.
#
# (c) Benedikt Diemer, University of Maryland
#
###################################################################################################

import six
import abc
import numpy as np

import ulula.physics.constants as constants

###################################################################################################

@six.add_metaclass(abc.ABCMeta)
class Setup():
    """
    General setup class
    
    This abstract container class serves as the basis for any problem setup in Ulula. Only two 
    routines must be overwritten, namely those setting a short name and that set the initial 
    conditions (:func:`~ulula.core.setup_base.Setup.shortName` and 
    :func:`~ulula.core.setup_base.Setup.setInitialConditions`). However, default implementations 
    for numerous other routines are provided and can be overwritten if desired. For example, some 
    routines determine the style of plots and are automatically passed to the plotting module when 
    using the :func:`~ulula.core.run.run` function.

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

        self.unit_l = unit_l
        self.unit_t = unit_t
        self.unit_m = unit_m
        
        return

    # ---------------------------------------------------------------------------------------------

    @abc.abstractmethod
    def shortName(self):
        """
        Short identifier for filenames (must be overwritten)
        """
        
        return

    # ---------------------------------------------------------------------------------------------
    
    def initialConditions(self, sim, nx):
        """
        Wrapper function for setting initial data
        
        This function provides a framework to make setting the initial conditions easier. It calls
        the user-defined routine to set the ICs in primitive variables, but it also sets code units, 
        checks for erroneous input such as negative densities, initializes gravitational potentials,
        and converts primitive to conserved variables.
        
        Parameters
        ----------
        sim: Simulation
            Object of type :data:`~ulula.core.simulation.Simulation`.
        nx: int
            Number of cells in the x-direction.
        """
        
        # Code units are handled in this base class, set them now
        sim.setCodeUnits(unit_l = self.unit_l, unit_t = self.unit_t, unit_m = self.unit_m)

        # Call the user-defined function to set the initial conditions. Make sure the child class
        # didn't contain bugs that led to blatantly unphysical ICs.
        self.setInitialConditions(sim, nx)
        if np.any(sim.V[sim.q_prim['DN'], sim.xlo:sim.xhi+1, sim.ylo:sim.yhi+1] <= 0.0):
            raise Exception('Found zero or negative densities in initial conditions.')
        if 'PR' in sim.q_prim:
            if np.any(sim.V[sim.q_prim['PR'], sim.xlo:sim.xhi+1, sim.ylo:sim.yhi+1] <= 0.0):
                raise Exception('Found zero or negative pressure in initial conditions.')

        # User-defined domain update function. We check whether the child class has overwritten the
        # base class method.
        if self.hasUserUpdateFunction():
            user_update_func = self.updateFunction
        else:
            user_update_func = None
        sim.setUserUpdateFunction(user_update_func = user_update_func)
        
        # User-defined boundary conditions. We check whether the child class has overwritten the
        # base class method.
        if self.hasUserBoundaryConditions():
            user_bc_func = self.setBoundaryConditions
        else:
            user_bc_func = None
        sim.setUserBoundaryConditions(user_bc_func = user_bc_func)

        # We need to set the gravitational fields before any prim-cons conversions
        sim.solveGravity(initial_setup = True)
        
        # Now create the correct conserved initial conditions and BCs
        sim.primitiveToConserved(sim.V, sim.U)
        sim.enforceBoundaryConditions()
        
        return

    # ---------------------------------------------------------------------------------------------

    @abc.abstractmethod
    def setInitialConditions(self, sim, nx):
        """
        Set the initial conditions (must be overwritten)

        In this function, the user sets the initial conditions for the simulation in primitive 
        variables and choose the settings for the simulation such the equation of state, gravity
        mode, and so on (see :doc:`simulation`). The wrapper function 
        :func:`~ulula.core.setup_base.Setup.initialConditions` takes care of any other necessary 
        steps.

        Parameters
        ----------
        sim: Simulation
            Object of type :data:`~ulula.core.simulation.Simulation`.
        nx: int
            Number of cells in the x-direction.
        """
        
        return

    # ---------------------------------------------------------------------------------------------

    def trueSolution(self, sim, x, q_plot, plot_geometry):
        """
        Return a true solution for this setup
        
        If overwritten, this function is passed to the Ulula 1D plotting routine 
        :func:`~ulula.core.plots.plot1d`. The function must return a list with one element for each 
        of the quantities in ``q_plot``. If an element is None, no solution is plotted. Otherwise
        the element must be an array with the same dimensions as ``x_plot``. The true solution
        must be in code units.

        Parameters
        ----------
        sim: Simulation
            Object of type :data:`~ulula.core.simulation.Simulation`.
        x: array_like
            The coordinates where the true solution is to be computed.
        q_plot: array_like
            List of quantities for which to return the true solution. Quantities are identified via 
            the short strings given in the :data:`~ulula.core.plots.fields` dictionary.
        plot_geometry: str
            If the setup is 2D, the type of cut through the domain that the solution is desired 
            for. Can be ``'line'`` or ``'radius'`` (a radially averaged plot from the center). See 
            the documentation of :func:`~ulula.core.plots.plot1d` for details.

        Returns
        -------
        solution: array_like
            A list of length ``len(q_plot)``, with elements that are either None or an array with 
            the same length as ``x``.
        """
        
        return

    # ---------------------------------------------------------------------------------------------

    def plotLimits(self, q_plot, plot_geometry):
        """
        Return min/max limits for plotted quantities
        
        If overwritten, this function is passed to the Ulula plotting routines. By default, no 
        limits are returned, which means the plotting functions automatically select limits. The 
        limits must be in code units.

        Parameters
        ----------
        q_plot: array_like
            List of quantities for which to return the plot limits. Quantities are identified via 
            the short strings given in the :data:`~ulula.core.plots.fields` dictionary.
        plot_geometry: str
            For 2D plots, this parameter is ``'2d'``. For 1D plots in a 1D simulation, it is ``'line'``.
            If the setup is 2D but a 1D plot is created, this parameter gives the cut through the 
            domain, which can be ``'line'`` or ``'radius'`` (a radially averaged plot from the center). 
            See the documentation of :func:`~ulula.core.plots.plot1d` for details. 

        Returns
        -------
        limits_lower: array_like
            List of lower limits for the given plot quantities. If None, a limit is chosen 
            automatically. Individual items can also be None.
        limits_upper: array_like
            List of upper limits for the given plot quantities. If None, a limit is chosen 
            automatically. Individual items can also be None.
        log: array_like
            List of True/False values that determine whether to plot the given quantities in log 
            space. If None, all quantities are plotted in linear space. If log is chosen, the 
            limits must be positive.
        """
        
        return None, None, None

    # ---------------------------------------------------------------------------------------------

    def plotColorMaps(self, q_plot):
        """
        Return colormaps for plotted quantities
        
        If overwritten, this function is passed to the Ulula plotting routines. By default, 
        quantities that can be negative (such as velocities) are displayed with divergent colormaps
        whereas positive-only quantities such as density are displayed with perceptually uniform 
        colormaps.

        Parameters
        ----------
        q_plot: array_like
            List of quantities for which to return the colormaps. Quantities are identified via 
            the short strings given in the :data:`~ulula.core.plots.fields` dictionary.

        Returns
        -------
        cmaps: array_like
            List of colormaps for the given quantities. If None, a colormap is chosen 
            automatically. Individual items can also be None.
        """
        
        return None

    # ---------------------------------------------------------------------------------------------

    def updateFunction(self, sim):
        """
        Interact with the simulation at run-time

        If this function is overwritten by a child class, it will be executed by the Ulula 
        simulation before boundary conditions are enforced. During that time, the setup can
        change the fluid variables in the domain.

        Note that the simulation does not check whether what this function does makes any sense! 
        If the function implements unphysical behavior, an unphysical simulation will result. The 
        overwriting function can manipulate either primitive or conserved variables and thus must
        ensure that primitive and conserved variables are consistent after the function call.
        
        Derived classes should not return any values (and must not return False like this base
        class implementation, because that value is used to determine whether a user function is
        provided in a given setup).
        
        Parameters
        ----------
        sim: Simulation
            Object of type :data:`~ulula.core.simulation.Simulation`.
        """
        
        return False

    # ---------------------------------------------------------------------------------------------

    def setBoundaryConditions(self, sim):
        """
        Set boundary conditions at run-time

        If this function is overwritten by a child class, it will be executed by the Ulula 
        simulation after the boundary conditions are enforced. During that time, the setup can
        overwrite the boundary conditions.

        Note that the simulation does not check whether what this function does makes any sense! 
        If the function implements unphysical behavior, an unphysical simulation will result. The 
        overwriting function can manipulate either primitive or conserved variables and thus must
        ensure that primitive and conserved variables are consistent after the function call.
        
        Derived classes should not return any values (and must not return False like this base
        class implementation, because that value is used to determine whether user BCs are
        provided in a given setup).
        
        Parameters
        ----------
        sim: Simulation
            Object of type :data:`~ulula.core.simulation.Simulation`.
        """
        
        return False

    # ---------------------------------------------------------------------------------------------

    def hasUserUpdateFunction(self):
        """
        Check whether setup provides update function

        An internal function that determines whether a child class has overwritten 
        :func:`updateFunction`. 
        
        Parameters
        ----------
        has_user_updates: bool
            True if an setup implementation is providing a user-defined update function, False 
            otherwise.
        """

        has_user_updates = True
        try:
            ret = self.updateFunction(None)
            if ret == False:
                has_user_updates = False
        except:
            pass
        
        return has_user_updates

    # ---------------------------------------------------------------------------------------------

    def hasUserBoundaryConditions(self):
        """
        Check whether setup provides BCs

        An internal function that determines whether a child class has overwritten 
        :func:`setBoundaryConditions`. 
        
        Parameters
        ----------
        has_user_bcs: bool
            True if an setup implementation is providing user-defined BCs, False otherwise.
        """

        has_user_bcs = True
        try:
            ret = self.setBoundaryConditions(None)
            if ret == False:
                has_user_bcs = False
        except:
            pass
        
        return has_user_bcs

    # ---------------------------------------------------------------------------------------------

    def internalEnergyFromTemperature(self, T, mu, gamma):
        """
        Conversion for isothermal EOS
        
        If you are choosing an isothermal EOS, you need to pass the temperature in the form of an
        equivalent internal energy in code units, which can be a little tedious to compute. This
        function takes care of the calculation. The result can be passed as the ``eint_fixed`` 
        parameter to the :func:`~ulula.core.simulation.Simulation.setEquationOfState` function.

        Parameters
        ----------
        T: float
            Temperature in Kelvin.
        mu: float
            Mean particle weight in proton masses.

        Returns
        -------
        eint: float
            Internal energy in code units corresponding to the given temperature.
        """
        
        eint = constants.kB_cgs * T / ((gamma - 1.0) * mu * constants.mp_cgs)
        eint *= self.unit_t**2 / self.unit_l**2
        
        return eint

###################################################################################################
