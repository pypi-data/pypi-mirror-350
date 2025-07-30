###################################################################################################
#
# This file is part of the ULULA code.
#
# (c) Benedikt Diemer, University of Maryland
#
###################################################################################################

import numpy as np
import h5py

import ulula.utils.version as ulula_version
import ulula.utils.utils as utils

###################################################################################################

class HydroScheme():
    """
    Container class for hydro algorithms

    Parameters
    ----------
    reconstruction: string
        Reconstruction algorithm; see table for valid choices
    limiter: string
        Slope limiter algorithm; see table for valid choices
    riemann: string
        Riemann solver; see table for valid choices
    time_integration: string
        Time integration scheme; see table for valid choices
    cfl: float
        CFL number (must be between 0 and 1), which determines the maximum allowable timestep such 
        that the distance traveled by the maximum signal speed in the domain does not exceed the 
        CFL number times the size of a cell.
    cfl_max: float
        Maximum CFL number (must be between 0 and 1, and greater than ``cfl``). While each timestep
        is (typically) set to satisfy the CFL condition, each timestep actually consists of two
        sweeps in the two dimensions (x and y). Since the fluid state changes during the first 
        sweep, satisfying the CFL condition in the first sweep does not guarantee that it is still 
        satisfied during the second sweep. To avoid repeating the first sweep, we tolerate an actual, 
        updated CFL factor that is larger than ``cfl``, but it must still be smaller than
        ``cfl_max`` and smaller than unity, because exceeding unity will definitely break the hydro
        solver. Setting ``cfl_max`` to a value close to unity (e.g., 0.99) may still lead to 
        instabilities. On the other hand, choosing ``cfl`` and ``cfl_max`` to be close may mean 
        that more timesteps need to be repeated, which slows down the code.
    cfl_reduce_factor: float
        If ``cfl_max`` is exceeded during the second sweep, we reduce the previous estimate of the
        timestep by this factor. Must be larger than unity.
    cfl_max_attempts: int
        If we still encounter a CFL violation after reducing the timestep, we keep doing so
        ``cfl_max_attempts`` times. After the last attempt, the simulation is aborted.
    """
    
    def __init__(self, reconstruction = 'linear', limiter = 'mc', riemann = 'hllc', 
                time_integration = 'hancock', cfl = 0.8, 
                cfl_max = 0.95, cfl_reduce_factor = 1.2, cfl_max_attempts = 3):
        
        if (cfl >= 1.0):
            raise Exception('The CFL number must be smaller than 1.')
        if (cfl_max >= 1.0):
            raise Exception('The maximum CFL number must be smaller than 1.')
        if (cfl >= cfl_max):
            raise Exception('The maximum CFL number must be larger than the CFL number.')
        if (cfl_reduce_factor <= 1.0):
            raise Exception('The CFL reduction factor must be greater than 1.')

        self.reconstruction = reconstruction
        self.limiter = limiter
        self.riemann = riemann
        self.time_integration = time_integration
        self.cfl = cfl
        self.cfl_max = cfl_max
        self.cfl_reduce_factor = cfl_reduce_factor
        self.cfl_max_attempts = cfl_max_attempts
        
        return

###################################################################################################

class Simulation():
    """
    The Ulula hydro solver framework
    
    This class contains all simulation data and routines. The internal fields have the following 
    meaning:
    
    =======================  =====================
    Field                    Meaning
    =======================  =====================
    *Domain*
    ----------------------------------------------
    ``is_2d``                Whether we are running a 1D or 2D simulation
    ``dx``                   Width of cells (same in both x and y directions)
    ``nx``                   Number of cells in the x-direction
    ``ny``                   Number of cells in the y-direction
    ``nghost``               Number of ghost cells around each edge
    ``xlo``                  First index of physical grid in x-direction (without left ghost zone)
    ``xhi``                  Last index of physical grid in x-direction (without right ghost zone)
    ``ylo``                  First index of physical grid in y-direction (without bottom ghost zone)
    ``yhi``                  Last index of physical grid in y-direction (without top ghost zone)
    ``x``                    Array of x values at cell centers (dimensions [nx + 2 ng])
    ``y``                    Array of y values at cell centers (dimensions [ny + 2 ng])
    ``bc_type``              Type of boundary condition ('periodic', 'outflow', 'wall')
    ``domain_set``           Once the domain is set, numerous settings cannot be changed any more
    -----------------------  ---------------------
    *Fluid variables*
    ----------------------------------------------
    ``track_pressure``       Whether we need to explicitly track pressure
    ``nq_hydro``             Number of hydro fluid variables (typically 4 for rho, vx, vy, P)
    ``nq_all``               Total number of fluid variables (including gravitational pot.)
    ``q_prim``               Dictionary containing the indices of the primitive fluid variables in the ``V`` array
    ``q_cons``               Dictionary containing the indices of the conserved fluid variables in the ``U`` array
    ``U``                    Vector of conserved fluid variables (dimensions [nq, nx + 2 ng, ny + 2 ng])
    ``V``                    Vector of primitive fluid variables (dimensions [nq, nx + 2 ng, ny + 2 ng])
    ``V_im12``               Cell-edge states at left side (same dimensions as V)
    ``V_ip12``               Cell-edge states at right side (same dimensions as V)
    -----------------------  ---------------------
    *Hydro scheme and timestepping*
    ----------------------------------------------
    ``hs``                   HydroScheme object
    ``use_source_term``      Whether any source terms are active (gravity etc.)
    ``t``                    Current time of the simulation
    ``step``                 Current step counter
    ``last_dir``             Direction of last sweep in previous timestep (x=0, y=1)
    -----------------------  ---------------------
    *Equation of state*
    ----------------------------------------------
    ``eos_mode``             Type of equation of state ('ideal', 'isothermal)
    ``eos_gamma``            Adiabatic index 
    ``eos_gm1``              gamma - 1
    ``eos_gm1_inv``          1 / (gamma - 1)
    ``eos_mu``               Mean particle mass in proton masses (can be None)
    ``eos_eint_fixed``       Fixed internal energy per unit mass (if isothermal)
    ``eos_pressure_floor``   Optional minimum pressure
    -----------------------  ---------------------
    *Code units*
    ----------------------------------------------
    ``unit_l``               Code unit length in centimeters
    ``unit_t``               Code unit time in seconds
    ``unit_m``               Code unit mass in grams
    -----------------------  ---------------------
    *Gravity*
    ----------------------------------------------
    ``gravity_mode``         Type of gravity ('none', 'fixed_acc', 'fixed_pot', 'poisson', 'fixed+poisson')
    ``gravity_dir``          Direction of fixed acceleration (0 for x, 1 for y)
    ``gravity_g``            Gravitational acceleration (for mode 'fixed_acc')
    ``gravity_G``            Gravitational constant (for mode 'poisson' or 'fixed+poisson')
    -----------------------  ---------------------
    *User-defined boundary and update functions*
    ----------------------------------------------
    ``do_user_updates``      True if the user has supplied a custom domain update function
    ``do_user_bcs``          True if the user has supplied a custom boundary condition function
    ``user_update_func``     A function to be called before the boundary conditions are enforced
    ``user_bc_func``         A function to be called after the boundary conditions are enforced
    =======================  =====================
    """

    def __init__(self):

        # The domain has not yet been set, which will be verified in functions below.    
        self.domain_set = False

        # Set all settings to their defaults
        self.setHydroScheme()
        self.setEquationOfState()
        self.setCodeUnits()
        self.setGravityMode()
        self.setUserUpdateFunction()
        self.setUserBoundaryConditions()
        
        return
    
    # ---------------------------------------------------------------------------------------------

    def setHydroScheme(self, hydro_scheme = None):
        """
        Set the hydro solver scheme
        
        This function must be executed before the :func:`~ulula.core.simulation.Simulation.setDomain` 
        function.
        
        Parameters
        ----------
        hydro_scheme: HydroScheme
            :class:`HydroScheme` object that contains the settings for the hydro solver.
        """
    
        if self.domain_set:
            raise Exception('The setHydroScheme() function must be called before setDomain().')
    
        if hydro_scheme is None:
            hydro_scheme = HydroScheme()
        self.hs = hydro_scheme
    
        # Set functions based on reconstruction scheme. If we are reconstructing, we need two
        # ghost zones instead of one due to slope calculations.
        if self.hs.reconstruction == 'const':
            self.reconstruction = self.reconstructionConst
            self.nghost = 1
        elif self.hs.reconstruction == 'linear':
            self.reconstruction = self.reconstructionLinear
            self.nghost = 2
        else:
            raise Exception('Unknown reconstruction scheme, %s.' % (self.hs.reconstruction))

        # Set limiter
        if self.hs.limiter == 'none':
            self.limiter = self.limiterNone
        elif self.hs.limiter == 'minmod':
            self.limiter = self.limiterMinMod
        elif self.hs.limiter == 'vanleer':
            self.limiter = self.limiterVanLeer
        elif self.hs.limiter == 'mc':
            self.limiter = self.limiterMC
        else:
            raise Exception('Unknown limiter, %s.' % (self.hs.limiter))
        
        # Set Riemann solver        
        if self.hs.riemann == 'hll':
            self.riemannSolver = self.riemannSolverHLL
        elif self.hs.riemann == 'hllc':
            self.riemannSolver = self.riemannSolverHLLC
        else:
            raise Exception('Unknown Riemann solver, %s.' % self.hs.riemann)

        # Check the time integration scheme for invalid values    
        if not self.hs.time_integration in ['euler', 'hancock', 'hancock_cons']:
            raise Exception('Unknown time integration scheme, %s.' % self.hs.time_integration)

        return
    
    # ---------------------------------------------------------------------------------------------

    def setEquationOfState(self, eos_mode = 'ideal', gamma = 5.0 / 3.0, mu = None, eint_fixed = None,
                           pressure_floor = None):
        """
        Choose an equation of state
        
        The equation of state (EOS) captures the microphysics of the gas that is being simulated.
        This function must be executed before the :func:`~ulula.core.simulation.Simulation.setDomain` 
        function.
        
        The default is an ideal gas EOS with :math:`\\gamma = 5/3`. If an isothermal EOS is chosen,
        the fixed temperature must be specified as an internal energy per unit mass, which can be
        computed from temperature using the 
        :func:`~ulula.core.setup_base.Setup.internalEnergyFromTemperature` function.
        
        Parameters
        ----------
        eos_mode: str
            Can be ``'ideal'`` or ``'isothermal'``.
        gamma: float
            Adiabatic index of the ideal gas to be simulated; should be 5/3 for atomic gases or
            7/5 for diatomic molecular gases.
        mu: float
            Mean particle mass in units of proton masses. Must be specified if temperature is to 
            be plotted, regardless of the EOS.
        eint_fixed: float
            A fixed internal energy per unit mass in code units for an isothermal EOS, ignored
            otherwise.
        pressure_floor: float
            If not None, this pressure (in code units) is enforced as a minimum. Such a pressure
            floor can be helpful in simulations where the pressure becomes negative due to 
            numerical errors. However, energy is no longer conserved since the pressure floor 
            may effectively add thermal energy.
        """

        if self.domain_set:
            raise Exception('The setEquationOfState() function must be called before setDomain().')
    
        self.eos_mode = eos_mode
        self.eos_gamma = gamma
        self.eos_mu = mu
        self.eos_gm1 = self.eos_gamma - 1.0
        self.eos_gm1_inv = 1.0 / self.eos_gm1
        self.eos_pressure_floor = pressure_floor
    
        # To avoid repeated string comparisons, we set the track_pressure field which indicates 
        # whether we need to explicitly track pressure and energy in the code. In practice, we 
        # assume an ideal equation of state if track_pressure == True and an isothermal one if 
        # track_pressure == False because those are the only EOSs implemented.
        if self.eos_mode == 'ideal':
            self.track_pressure = True
            self.eos_eint_fixed = None
            self.eos_T_fixed = None
        elif self.eos_mode == 'isothermal':
            if eint_fixed is None:
                raise Exception('In isothermal EOS mode, eint_fixed must be set.')
            self.eos_eint_fixed = eint_fixed
            self.track_pressure = False
        else:
            raise Exception('Unknown EOS mode, %s.' % (eos_mode))
    
        return
    
    # ---------------------------------------------------------------------------------------------

    def setCodeUnits(self, unit_l = 1.0, unit_t = 1.0, unit_m = 1.0):
        """
        Define the meaning of the internal units
        
        The pure Euler equations (i.e., ignoring viscosity, cooling, etc.) are invariant under 
        multiplications of up to three scale quantities, meaning that the solution of a hydro 
        problem remains unchanged independent of what physical length, time, and mass scales the 
        given numbers represent. One can alternatively think of rescalings in other, combined 
        quantities such as density, pressure, and so on. 

        This function lets the user define the meaning of the internal length, time, and mass 
        scales. The solution will not change unless the problem in question depends on physics 
        beyond the pure Euler equations, such as gravity. As a result, the values of the code units 
        are not used at all in the simulation class. However, plots of the solution will change if 
        a unit system other than code units is used.
        
        The code units are given in cgs units. Some common units are defined in the 
        :mod:`~ulula.physics.units` module. For example, to set time units of years, 
        ``unit_t = units.units_t['yr']['in_cgs']``. However, the code units can take on any 
        positive, non-zero value chosen by the user.
        
        This function must be executed before the :func:`~ulula.core.simulation.Simulation.setDomain` 
        function.
        
        Parameters
        ----------
        unit_l: float
            Code unit for length in units of centimeters.
        unit_t: float
            Code unit for time in units of seconds.
        unit_m: float
            Code unit for mass in units of gram.
        """

        if self.domain_set:
            raise Exception('The setCodeUnits() function must be called before setDomain().')
        
        self.unit_l = unit_l
        self.unit_t = unit_t
        self.unit_m = unit_m
        
        return

    # ---------------------------------------------------------------------------------------------

    def setGravityMode(self, gravity_mode = 'none', gravity_dir = 1, g = 1.0, G = 1.0):
        """
        Add gravity to the simulation
        
        If gravity is to be part of the setup, this function must be executed before the 
        :func:`~ulula.core.simulation.Simulation.setDomain` function. Once the domain is set, the 
        function :func:`~ulula.core.simulation.Simulation.solveGravity` must be called with 
        ``'initial_setup = True'`` to initialize potential and gradients. The 
        :class:`~ulula.core.setup_base.Setup` class performs this step automatically. The user 
        has a choice between a number of gravity modes. 
        
        If ``'fixed_acc'`` is chosen, an acceleration ``g`` is uniformly applied. If the simulation is 
        1D, we interpret a constant acceleration as pointing to the negative x-direction, otherwise 
        in the negative y-direction. 
        
        If the chosen mode is ``'fixed_pot'``, the user must subsequently set the initial
        potential at the same time as the other initial conditions. Ulula will take the gradients
        of this potential and apply them uniformly.
        
        If ``'poisson'`` is chosen, the Poisson equation is solved at each timestep so that the 
        density field in the simulation generates a gravitational field with a gravitational 
        constant ``G``. This mode works only with periodic boundary conditions. 
        
        The ``'fixed+poisson'`` mode is the same as ``'poisson'``, but the user additionally provides
        a fixed potential as in the ``'fixed_pot'`` mode. This potential is added to the Poisson
        potential at each timestep.

        Parameters
        ----------
        gravity_mode: str
            The type of gravity to be added. Can be ``'fixed_acc'``, ``'fixed_pot'``, ``'poisson'``, or
            ``'fixed+poisson'``.
        gravity_dir: int
            The direction of a fixed acceleration, 0 meaning x and 1 meaning y. For a 1D 
            simulation, the direction is forced to be x. For a 2D simulation, the direction is 
            typically 1 (y) so that gravity points downwards.
        g: float
            If ``gravity_mode`` is ``'fixed_acc'``, then ``g`` gives the constant acceleration in code
            units.
        G: float
            If ``gravity_mode`` is ``'poisson'`` or ``'fixed+poisson'``, then ``G`` is the 
            gravitational constant in code units.
        """

        if self.domain_set:
            raise Exception('The setGravityMode() function must be called before setDomain().')
        if not gravity_mode in ['none', 'fixed_acc', 'fixed_pot', 'poisson', 'fixed+poisson']:
            raise Exception('Unknown gravity mode, %s.' % (gravity_mode))
        
        self.gravity_mode = gravity_mode
        self.gravity_g = g
        self.gravity_G = G
        if not gravity_dir in [0, 1]:
            raise Exception('Invalid direction for gravity (%d), must be 0 (x) or 1 (y).' % (gravity_dir))
        self.gravity_dir = gravity_dir
        self.gravity_is_on = (self.gravity_mode != 'none')
        self.gravity_fixed_acc = (self.gravity_mode == 'fixed_acc')
        self.gravity_fixed_pot = (self.gravity_mode == 'fixed_pot')
        self.gravity_poisson = (self.gravity_mode in ['poisson', 'fixed+poisson'])
        self.gravity_fixed_poisson = (self.gravity_mode == 'fixed+poisson')

        self.use_source_terms = self.gravity_is_on
        
        return

    # ---------------------------------------------------------------------------------------------

    def setUserUpdateFunction(self, user_update_func = None):
        """
        Set user-defined updates in the domain
        
        If a function is passed for ``user_update_func``, that function will be called with the 
        simulation object as an argument before boundary conditions are enforced. This 
        mechanism allows the phyiscal setup to influence the simulation at runtime, while
        the boundary conditions are still automatically enforced. The 
        :class:`~ulula.core.setup_base.Setup` base class contains such a function, which becomes 
        active if it is overwritten by a child class.
        
        The code does not check that what a user update function does makes any sense! If the 
        function implements unphysical behavior, an unphysical simulation will result. For example,
        the update function must ensure that primitive and conserved variables are consistent after 
        the function call.

        Parameters
        ----------
        user_update_func: func
            Function pointer that takes the simulation object as an argument.
        """
        
        self.user_update_func = user_update_func
        self.do_user_updates = (self.user_update_func is not None)
        
        return

    # ---------------------------------------------------------------------------------------------

    def setUserBoundaryConditions(self, user_bc_func = None):
        """
        Set user-defined boundary conditions
        
        If a function is passed for ``user_bc_func``, that function will be called with the 
        simulation object as an argument every time after boundary conditions have been enforced. 
        This mechanism allows for custom boundary conditions such as a flow entering the domain
        from a certain side. The :class:`~ulula.core.setup_base.Setup` base class contains such a 
        function, which becomes active if it is overwritten by a child class.
        
        The code does not check that what a user update function does makes any sense! If the 
        function implements unphysical behavior, an unphysical simulation will result. For example,
        the update function must ensure that primitive and conserved variables are consistent after 
        the function call.

        Parameters
        ----------
        user_bc_func: func
            Function pointer that takes the simulation object as an argument.
        """
        
        self.user_bc_func = user_bc_func
        self.do_user_bcs = (self.user_bc_func is not None)
        
        return

    # ---------------------------------------------------------------------------------------------

    def setDomain(self, nx, ny, xmin = 0.0, xmax = 1.0, ymin = 0.0, bc_type = 'periodic'):
        """
        Set the physical and numerical domain
        
        This function creates the memory structure for the simulation as well as pre-computed 
        slices that index the variable arrays.

        Parameters
        ----------
        nx: int
            Number of grid points in x-direction. Must be at least 2.
        ny: int
            Number of grid points in y-direction. Choosing ``ny = 1`` leads to a 1D simulation.
        xmin: float
            Left edge in physical coordinates (in code units).
        xmax: float
            Right edge in physical coordinates (in code units).
        ymin: float
            Bottom edge in physical coordinates (in code units).
        ymax: float
            Top edge in physical coordinates (in code units).
        bc_type: string
            Type of boundary conditions, which can be ``'periodic'``, ``'outflow'``, or ``'wall'``. 
            With periodic boundary conditions, the domain wraps around, meaning that flows out of 
            the right edge re-enter on the left and so on. Outflow means that flows at the domain
            edge continue. Be careful with ouflow BCs! They do not conserved mass, energy, or 
            momentum, and they can lead to weird effects if the flow is not actually out of 
            the domain. For example, if there is a flow into the domain at an edge, this flow will 
            continue adding mass indefinitely unless it is stopped by counter-acting pressures 
            (which may or may not be desired). Finally, wall boundary conditions reflect the fluid 
            flow. They conserve mass and energy but not momentum.
        """

        # Make sure choices set so far have been consistent
        if (self.hs.riemann == 'hllc') and (not self.track_pressure):
            raise Exception('Cannot combine HLLC Riemann solver and isothermal EOS; use HLL instead.')
        if self.gravity_poisson and (bc_type != 'periodic'):
            raise Exception('The current Poisson solver only works with periodic boundary conditions.')

        # Compute dimensions. We ensure that the domain spans integer numbers of cells in each
        # dimension.
        if not isinstance(nx, int):
            raise Exception('Got nx = %s, expected integer.' % (str(nx)))
        if not isinstance(ny, int):
            raise Exception('Got ny = %s, expected integer.' % (str(ny)))
        if nx < 2:
            raise Exception('Got nx = %d, must be at least 2.' % (nx))
        if ny < 1:
            raise Exception('Got ny = %d, expected a positive number.' % (ny))
        
        self.nx = nx
        self.xmin = xmin
        self.xmax = xmax
        self.dx = (xmax - xmin) / float(nx)
        
        self.ny = ny
        self.ymin = ymin
        self.ymax = self.ymin + ny * self.dx
        
        print('Grid setup %d x %d, dimensions x = [%.2e .. %.2e] y =  [%.2e .. %.2e]' \
            % (self.nx, self.ny, self.xmin, self.xmax, self.ymin, self.ymax))

        # Set indices for lower and upper domain boundaries.
        ng = self.nghost
        self.xlo = ng
        self.xhi = ng + self.nx - 1
        self.nx_tot = self.nx + 2 * ng
        self.x = xmin + (np.arange(self.nx_tot) - ng) * self.dx + 0.5 * self.dx
        
        # If the domain is 1D, we do not create ghost cells in the y-direction.
        self.is_2d = (ny > 1)
        if self.is_2d:
            self.ylo = ng
            self.yhi = ng + self.ny - 1
            self.ny_tot = self.ny + 2 * ng
            self.y = ymin + (np.arange(self.ny_tot) - ng) * self.dx + 0.5 * self.dx
        else:
            self.ylo = 0
            self.yhi = 1
            self.ny_tot = 1
            self.y = np.array([ymin + 0.5 * self.dx])

        self.bc_type = bc_type

        # Create the indexing of the variable vectors. This is kept general because the tracked
        # fluid variables depend on the EOS, gravity, and so on. We store the indices of the 
        # primitive and conserved fields in dictionaries, which can be used by routines such as 
        # plotting. Density and velocity/momentum are always part of the variable vector.
        self.q_prim = {}
        self.q_cons = {}

        idx = 0
        self.DN = self.MS = idx
        self.q_prim['DN'] = self.DN
        self.q_cons['MS'] = self.DN
        
        idx += 1
        self.VX = self.MX = idx
        self.q_prim['VX'] = self.VX
        self.q_cons['MX'] = self.MX

        idx += 1
        self.VY = self.MY = idx
        self.q_prim['VY'] = self.VY
        self.q_cons['MY'] = self.MY
        
        # Pressure and energy can be computed from density for a barotropic EOS, so the pressure
        # and conserved energy fields only exist for non-barotropic EOSs.
        if self.track_pressure:
            idx += 1
            self.PR = self.ET = idx
            self.q_prim['PR'] = self.PR
            self.q_cons['ET'] = self.ET

        # Record the length of the state vector and which of those variables are hydro variables in
        # the sense that they represent one of the Euler equations and should thus have their 
        # fluxes advected. The latter is not true for the gravitational potential, even though it 
        # needs to be part of the (primitive) state vector.
        self.nq_hydro = len(self.q_prim)
        self.nq_state = self.nq_hydro
        
        # If gravity is on, we add a potential field and possibly gradients.
        self.GP = self.GX = self.GY = None
        if self.gravity_is_on:
            idx += 1
            self.GP = idx
            self.q_prim['GP'] = self.GP
            self.nq_state = len(self.q_prim)
            if self.gravity_fixed_acc:
                pass
            else:
                idx += 1
                self.GX = idx
                self.q_prim['GX'] = self.GX
                idx += 1
                self.GY = idx
                self.q_prim['GY'] = self.GY
                if self.gravity_fixed_poisson:
                    idx += 1
                    self.GU = idx
                    self.q_prim['GU'] = self.GU
        
        # Record the length of the total (primitive) vector of variables
        self.nq_all = len(self.q_prim)

        # Storage for the primitive and conserved fluid variables and other arrays. We create a
        # duplicate backup array for each where the solution at the beginning of a timestep is 
        # stored so that we can restore it if an error occurs.
        self.V = np.zeros((self.nq_all, self.nx_tot, self.ny_tot), float)
        self.V_cpy = np.zeros((self.nq_all, self.nx_tot, self.ny_tot), float)
        self.U = np.zeros((self.nq_hydro, self.nx_tot, self.ny_tot), float)
        self.U_cpy = np.zeros((self.nq_hydro, self.nx_tot, self.ny_tot), float)
    
        # Storage for the cell-edge states and conservative fluxes. If we are using 
        # piecewise-constant, both states are the same (and the same as the cell centers).
        if self.hs.reconstruction == 'const':
            self.V_im12 = self.V
            self.V_ip12 = self.V
        elif self.hs.reconstruction == 'linear':
            self.V_im12 = np.zeros((self.nq_state, self.nx_tot, self.ny_tot), float)
            self.V_ip12 = np.zeros((self.nq_state, self.nx_tot, self.ny_tot), float)
        else:
            raise Exception('Unknown reconstruction scheme, %s.' % (self.hs.reconstruction))
        
        # Prepare slices that can be reused. The simplest slice is one that makes no selection.
        self.slc_aa = slice(None)

        # Slices for the first dimension of the variable vector, i.e., the fluid variables. We 
        # again distinguish hydro variables (equations), state variables, and all variables.
        self.slc_qh = slice(0, self.nq_hydro)
        self.slc_qs = slice(0, self.nq_state)
        self.slc_qa = slice(0, self.nq_all)
        
        # Slices that include all cells except edges.
        self.slc_01 = slice(0, -1)
        self.slc_02 = slice(0, -2)
        self.slc_10 = slice(1, None)
        self.slc_11 = slice(1, -1)
        self.slc_20 = slice(2, None)

        # Slices that include the domain (c) or left/right (lr) cells, not including ghost cells.
        self.slc_lx = slice(self.xlo - 1, self.xhi + 1)
        self.slc_ly = slice(self.ylo - 1, self.yhi + 1)
        self.slc_rx = slice(self.xlo, self.xhi + 2)
        self.slc_ry = slice(self.ylo, self.yhi + 2)
        self.slc_cx = slice(self.xlo, self.xhi + 1)
        self.slc_cy = slice(self.ylo, self.yhi + 1)

        # Slice over the full domain without ghost cells (in 1D or 2D)
        if self.is_2d:
            self.slc_dom = (self.slc_cx, self.slc_cy)
        else:
            self.slc_dom = (self.slc_cx)

        # Time
        self.t = 0.0
        self.step = 0
        self.last_dir = -1
        
        # We are done setting up the domain. After this point, the fundamental settings cannot be
        # changed any more.
        self.domain_set = True
        
        return
    
    # ---------------------------------------------------------------------------------------------

    def xyGrid(self):
        """
        Get a grid of the x and y cell center positions
        
        This function returns two arrays with the x and y positions at each grid point.

        Returns
        -------
        x: array_like
            2D array with x positions of all cells (including ghost cells).
        y: array_like
            2D array with x positions of all cells (including ghost cells).
        """
    
        return np.meshgrid(self.x, self.y, indexing = 'ij')

    # ---------------------------------------------------------------------------------------------
    
    def enforceBoundaryConditions(self, a = None, slc_q = None):
        """
        Enforce boundary conditions after changes
        
        This function fills the ghost cells with values from the physical domain to achieve certain
        behaviors. It is executed at each timestep. In particular:

        * Periodic: cells are rolled over from the other side of the domain so that it looks to the
          hydro solver as if the domain just continues on the other side.
        * Outflow: we take the value of the physical cells at the edge and copy them into the 
          adjacent ghost cells, leading to flows that just continue across the edge.
        * Wall: the goal is to ensure that no mass or energy flux moves across the boundary. We 
          achieve this condition by setting the ghost cells to a mirror image of the adjacent cells
          in the domain and inverting the perpendicular velocity, creating a counter-flow that 
          balances any motion onto the edge.

        Parameters
        ----------
        a: array_like
            List of arrays to set boundary conditions in. If None, the function sets BCs for the
            hydro variables in the default primitive and conserved arrays. If not None, BCs are 
            set in the given array. In that case, the user-defined BC and update functions are not 
            executed.
        slc_q: slice
            If ``a`` is not None, this slice chooses which variables the BCs are set for. 
        """
        
        default_bcs = (a is None)
        if default_bcs:
            a = [self.V, self.U]
            slc_q = self.slc_qh
        
        if self.do_user_updates and default_bcs:
            self.user_update_func(self)

        ng = self.nghost
        xlo = self.xlo
        xhi = self.xhi
        ylo = self.ylo
        yhi = self.yhi
        slc_x = self.slc_cx
        slc_y = self.slc_cy
        
        for v in a:
            
            if self.bc_type == 'periodic':
                # Left/right ghost
                v[slc_q, 0:ng, slc_y] = v[slc_q, xhi-ng+1:xhi+1, slc_y]
                v[slc_q, -ng:, slc_y] = v[slc_q, xlo:xlo+ng,     slc_y]
                if self.is_2d:
                    # Bottom/top ghost
                    v[slc_q, slc_x, 0:ng] = v[slc_q, slc_x, yhi-ng+1:yhi+1]        
                    v[slc_q, slc_x, -ng:] = v[slc_q, slc_x, ylo:ylo+ng]
                    # Corners
                    v[slc_q, 0:ng,  0:ng] = v[slc_q, xhi-ng+1:xhi+1, yhi-ng+1:yhi+1]
                    v[slc_q, 0:ng,  -ng:] = v[slc_q, xhi-ng+1:xhi+1, ylo:ylo+ng]
                    v[slc_q, -ng:,  0:ng] = v[slc_q, xlo:xlo+ng,     yhi-ng+1:yhi+1]
                    v[slc_q, -ng:,  -ng:] = v[slc_q, xlo:xlo+ng,     ylo:ylo+ng]
            
            elif self.bc_type == 'outflow':
                # Left/right ghost
                v[slc_q, 0:ng, slc_y] = v[slc_q, xlo, slc_y][:, None, :]
                v[slc_q, -ng:, slc_y] = v[slc_q, xhi, slc_y][:, None, :]
                if self.is_2d:
                    # Bottom/top ghost
                    v[slc_q, slc_x, 0:ng] = v[slc_q, slc_x, ylo][:, :, None]
                    v[slc_q, slc_x, -ng:] = v[slc_q, slc_x, yhi][:, :, None]
                    # Corners
                    v[slc_q, 0:ng, 0:ng]  = v[slc_q, xlo, ylo][:, None, None]
                    v[slc_q, 0:ng, -ng:]  = v[slc_q, xlo, yhi][:, None, None]
                    v[slc_q, -ng:, 0:ng]  = v[slc_q, xhi, ylo][:, None, None]
                    v[slc_q, -ng:, -ng:]  = v[slc_q, xhi, yhi][:, None, None]

            elif self.bc_type == 'wall':
                # Left/right ghost
                v[slc_q, 0:ng, slc_y] = v[slc_q, xlo+ng-1:xlo-1:-1, slc_y]
                v[slc_q, -ng:, slc_y] = v[slc_q, xhi:xhi-ng:-1,     slc_y]
                if self.is_2d:
                    # Bottom/top ghost
                    v[slc_q, slc_x, 0:ng] = v[slc_q, slc_x, ylo+ng-1:ylo-1:-1]
                    v[slc_q, slc_x, -ng:] = v[slc_q, slc_x, yhi:yhi-ng:-1]
                    # Corners
                    v[slc_q, 0:ng, 0:ng]  = v[slc_q, xlo+ng-1:xlo-1:-1, ylo+ng-1:ylo-1:-1]
                    v[slc_q, 0:ng, -ng:]  = v[slc_q, xlo+ng-1:xlo-1:-1, yhi:yhi-ng:-1]
                    v[slc_q, -ng:, 0:ng]  = v[slc_q, xhi:xhi-ng:-1,     ylo+ng-1:ylo-1:-1]
                    v[slc_q, -ng:, -ng:]  = v[slc_q, xhi:xhi-ng:-1,     yhi:yhi-ng:-1]
                # Invert velocities
                v[self.VX, 0:ng, :] *= -1
                v[self.VX, -ng:, :] *= -1
                if self.is_2d:
                    v[self.VY, :, 0:ng] *= -1
                    v[self.VY, :, -ng:] *= -1
                
            else:
                raise Exception('Unknown type of boundary condition, %s.' % (self.bc_type))
        
        if self.do_user_bcs and default_bcs:
            self.user_bc_func(self)
        
        return

    # ---------------------------------------------------------------------------------------------

    def primitiveToConserved(self, V, U):
        """
        Convert primitive to conserved variables
        
        This function takes the input and output arrays as parameters instead of assuming that it
        should use the main ``V`` and ``U`` arrays. In some cases, conversions need to be performed 
        on other fluid states.

        Parameters
        ----------
        V: array_like
            Input array of primitive fluid variables with first dimension ``nq_all``.
        U: array_like
            Output array of conserved fluid variables.
        """
                            
        rho = V[self.DN]
        vx = V[self.VX]
        vy = V[self.VY]
        
        U[self.MS] = rho
        U[self.MX] = vx * rho
        U[self.MY] = vy * rho        

        if self.track_pressure:
            U[self.ET] = 0.5 * (vx**2 + vy**2) * rho + V[self.PR] * self.eos_gm1_inv
            if self.gravity_is_on:
                U[self.ET] += rho * V[self.GP]
            
        return

    # ---------------------------------------------------------------------------------------------
    
    def primitiveToConservedRet(self, V):
        """
        Convert primitive to new conserved array
        
        Same as :func:`primitiveToConserved`, but creating a new array for the output conserved 
        variables.

        Parameters
        ----------
        V: array_like
            Input array of primitive fluid variables with first dimension ``nq_all``.

        Returns
        -------
        U: array_like
            Array of fluid variables with first dimension ``nq_hydro`` and otherwise same dimensions 
            as the input array.
        """
        
        U = np.zeros((self.nq_hydro, V.shape[1], V.shape[2]), dtype = V.dtype)
        self.primitiveToConserved(V, U)
        
        return U

    # ---------------------------------------------------------------------------------------------
    
    def conservedToPrimitive(self, U, V):
        """
        Convert conserved to primitive variables
        
        This function takes the input and output arrays as parameters instead of assuming that it
        should use the main ``U`` and ``V`` arrays, since in some cases, conversions need to be 
        performed on other fluid variables. Note that gravitational potentials are stored only in 
        the primitive variable vector, so that ``V`` must contain the correct potential even if 
        ``U`` is technically the input.

        Parameters
        ----------
        U: array_like
            Input array of conserved fluid variables with first dimension ``nq_hydro``.
        V: array_like
            Output array of primitive fluid variables with first dimension ``nq_all``, which must
            already contain the gravitational potential if gravity is on.
        """

        rho = U[self.DN]
        rho_inv = 1.0 / rho
        vx = U[self.MX] * rho_inv
        vy = U[self.MY] * rho_inv
        
        V[self.DN] = rho
        V[self.VX] = vx
        V[self.VY] = vy
        
        if self.track_pressure:
            e_int_rho = U[self.ET] - 0.5 * rho * (vx**2 + vy**2)
            if self.gravity_is_on:
                e_int_rho -= rho * V[self.GP]
            V[self.PR] = e_int_rho * self.eos_gm1
            self.checkPressure(V)
            
        return

    # ---------------------------------------------------------------------------------------------

    def checkPressure(self, V):
        """
        Check for zero or negative pressures
        
        Physically, pressure can never be negative. Numerically, however, negative pressures can
        when we compute pressure from conserved variables (by subtracting kinetic energy from total
        energy) or when we evolve it otherwise. After such operations, this function is called to 
        either raise an error or enforce a user-defined pressure floor.

        Parameters
        ----------
        V: array_like
            Input array of primitive fluid variables with first dimension ``nq_all``.
        """

        if np.any(V[self.PR] <= 0.0):
            if self.eos_pressure_floor is None:
                raise Exception('Zero or negative pressure found. Consider lowering the CFL number and/or imposing a pressure floor.')
            else:
                V[self.PR][V[self.PR] < self.eos_pressure_floor] = self.eos_pressure_floor
        
        return

    # ---------------------------------------------------------------------------------------------

    def fluxVector(self, idir, V):
        """
        Compute the flux vector F(V)
        
        The flux of the conserved quantities density, momentum, and total energy as a function of 
        a primitive fluid state.

        Parameters
        ----------
        idir: int
            Direction of sweep (0 = x, 1 = y).
        V: array_like
            Input array of primitive fluid variables with first dimension ``nq_all``.

        Returns
        -------
        F: array_like
            Array of fluxes with first dimension ``nq_hydro`` and otherwise same dimensions as input 
            array.
        """

        F = np.zeros((self.nq_hydro, V.shape[1], V.shape[2]), dtype = V.dtype)

        DN = self.DN
        VX = self.VX
        idir2 = (idir + 1) % 2
        
        rho = V[DN]
        v1 = V[VX + idir]
        v2 = V[VX + idir2]
        rho_v1 = rho * v1
        
        if self.track_pressure:
            P = V[self.PR]
            etot = 0.5 * rho * (v1**2 + v2**2) + P * self.eos_gm1_inv
            if self.gravity_is_on:
                etot += rho * V[self.GP]
        else:
            P = rho * self.eos_eint_fixed * self.eos_gm1
            
        F[DN] = rho_v1
        F[VX + idir] = rho_v1 * v1 + P
        F[VX + idir2] = rho_v1 * v2
        if self.track_pressure:
            F[self.ET] = (etot + P) * v1
        
        return F

    # ---------------------------------------------------------------------------------------------

    def primitiveEvolution(self, idir, V, dV_dx):
        """
        Linear approximation of the Euler equations
        
        Instead of the usual conservation-law form, we can also think of the Euler equations in 1D 
        as a change 
        :math:`\\partial {\\pmb V}/ \\partial t + A_x({\\pmb V})\\ \\partial {\\pmb V} / \\partial x = {\\pmb S}`. 
        This function returns :math:`\\Delta {\\pmb V} / \\Delta t` given an input state 
        :math:`{\\pmb V}` and a vector of spatial derivatives :math:`\\Delta {\\pmb V} / \\Delta x`. 
        The result is used in the Hancock step.

        Parameters
        ----------
        idir: int
            Direction of sweep (0 = x, 1 = y).
        V: array_like
            Array of primitive fluid variables with first dimension at least ``nq_hydro``.
        dV_dx: array_like
            Array of spatial derivatives of the fluid variables with first dimension at least 
            ``nq_hydro``.

        Returns
        -------
        dV_dt: array_like
            Array of linear approximations to time evolution of fluid variables, with same 
            dimensions as input arrays.
        """
        
        DN = self.DN
        idir2 = (idir + 1) % 2
        V1 = self.VX + idir
        V2 = self.VX + idir2

        if self.track_pressure:
            PR = self.PR
            dP_dx = dV_dx[PR]
        else:
            dP_dx = dV_dx[DN] * self.eos_eint_fixed * self.eos_gm1
        
        dV_dt = np.zeros_like(dV_dx)
        dV_dt[DN] = -(V[V1] * dV_dx[DN] + dV_dx[V1] * V[DN])
        dV_dt[V1] = -(V[V1] * dV_dx[V1] + dP_dx / V[DN])
        dV_dt[V2] = -(V[V1] * dV_dx[V2])
        if self.track_pressure:
            dV_dt[PR] = -(V[V1] * dP_dx + dV_dx[V1] * V[PR] * self.eos_gamma)

        return dV_dt

    # ---------------------------------------------------------------------------------------------

    def soundSpeed(self, V):
        """
        Sound speed
        
        Parameters
        ----------
        V: array_like
            Input array of primitive fluid variables.

        Returns
        -------
        cs: array_like
            Array of sound speed with same dimensions as input array (for a single variable).
        """

        if self.eos_mode == 'ideal':
            cs = np.sqrt(self.eos_gamma * V[self.PR] / V[self.DN])
        elif self.eos_mode == 'isothermal':
            cs = np.ones_like(V[self.DN]) * np.sqrt(self.eos_eint_fixed * self.eos_gm1)
        else:
            raise Exception('Unknown EOS mode, %s.' % (self.eos_mode))
        
        if np.any(np.isnan(cs)):
            raise Exception('Encountered invalid inputs while computing sound speed (input min DN %.2e, min PR %.2e). Try reducing the CFL number.' \
                        % (np.min(V[self.DN]), np.min(V[self.PR])))
        
        return cs

    # ---------------------------------------------------------------------------------------------

    def maxSpeedInDomain(self):
        """
        Largest signal speed in domain
        
        This function returns the largest possible signal speed anywhere in the domain. It
        evaluates the sound speed and adds it to the absolute x and y velocities. We do not need to
        add those velocities in quadrature since we are taking separate sweeps in the x and y 
        directions. Thus, the largest allowed timestep is determined by the largest speed in 
        either direction.
        
        Parameters
        ----------
        V: array_like
            Input array of primitive fluid variables.

        Returns
        -------
        c_max: float
            Largest possible signal speed in the domain.
        """
        
        cs = self.soundSpeed(self.V)
        c_max = np.max(np.maximum(np.abs(self.V[self.VX]), np.abs(self.V[self.VY])) + cs)
        
        if np.isnan(c_max):
            raise Exception('Could not compute fastest speed in domain. Aborting.')
        
        return c_max

    # ---------------------------------------------------------------------------------------------

    def reconstructionConst(self, idir, dt):
        """
        Piecewise-constant reconstruction
        
        The term "piecewise-constant" means that the fluid state at the cell center is interpreted
        as representing the entire cell, meaning that we perform no reconstruction. If this option
        is chosen, the left/right cell edge arrays already point to the cell-centered values so that 
        this function does nothing at all. It merely serves as a placeholder to which the 
        reconstruction function pointer can be set.
        
        Parameters
        ----------
        idir: int
            Direction of sweep (0 = x, 1 = y).
        dt: float
            Timestep.
        """
        
        return

    # ---------------------------------------------------------------------------------------------

    def reconstructionLinear(self, idir, dt):
        """
        Piecewise-linear reconstruction
        
        This function creates left and right cell-edge states based on the cell-centered states. It
        first computes the left and right slopes, uses a slope limiter to determine the limited
        slope to use, and interpolates linearly within each cell. This interpolation leads to
        2nd-order convergence in space.
        
        If the Hancock time integration scheme is chosen, the reconstructed edge states are also 
        advanced by half a timestep to get 2nd-order convergence in time. There are two ways 
        to perform the Hancock step. The more conventionally described way is to take the fluxes 
        according to the L/R states as an approximation for the flux differential across the cell 
        (the ``'hancock_cons'`` integration scheme). The differential is then used to updated the 
        conserved cell-edge states. However, this method necessitates a 
        primitive->conserved->primitive conversion and a flux calculation. By contrast, the 
        so-called primitive Hancock method uses the Euler equations in primitive variables to 
        estimate the change in time from the change across the cell (see 
        :func:`primitiveEvolution`). The two methods should give almost identical results, but the 
        primitive version is noticeably faster.
        
        Parameters
        ----------
        idir: int
            Direction of sweep (0 = x, 1 = y).
        dt: float
            Timestep.
        """
        
        # Compute slices. We set left and right edge states in each cell except one layer of ghost
        # cells, and only for the hydro variables.
        if idir == 0:
            slc3aL = (self.slc_qh, self.slc_02, self.slc_aa)
            slc3aR = (self.slc_qh, self.slc_20, self.slc_aa)
            slc3aC = (self.slc_qh, self.slc_11, self.slc_aa)
        else:
            slc3aL = (self.slc_qh, self.slc_aa, self.slc_02)
            slc3aR = (self.slc_qh, self.slc_aa, self.slc_20)
            slc3aC = (self.slc_qh, self.slc_aa, self.slc_11)

        # Compute undivided derivatives and apply slope limiter.
        sL = (self.V[slc3aC] - self.V[slc3aL])
        sR = (self.V[slc3aR] - self.V[slc3aC])
        slim = np.zeros_like(sL)
        self.limiter(sL, sR, slim)
        
        # Copy all fields, including any that are not hydro variables but are needed for the state
        # vector (e.g., gravitational potential).
        self.V_im12[...] = self.V[self.slc_qs, :, :]
        self.V_ip12[...] = self.V[self.slc_qs, :, :]
        
        # Apply limited derivative. 
        self.V_im12[slc3aC] -= slim * 0.5
        self.V_ip12[slc3aC] += slim * 0.5
        
        # The Hancock step advances the left/right cell edge states by 1/2 timestep to get 2nd
        # order in the flux calculation. There are two ways to perform the Hancock step. The more
        # conventionally quoted way is to take the fluxes according to the L/R states as an
        # approximation for the flux differential across the cell ('hancock_cons'). We use the 
        # differential to update the conserved cell-edge states. However, this method necessitates
        # a prim->cons->prim conversion and a flux calculation. By contrast, the "primitive 
        # Hancock" method uses the Euler equations in primitive variables to estimate the change in
        # time from the change across the cell. Both methods give identical results, but the 
        # primitive version is noticeably faster. We could in principle compute the primitive 
        # time evolution based on the spatially reconstructed states V_im12/V_ip12, but this makes
        # virtually no difference in practice.
        if self.hs.time_integration == 'hancock':
            delta_V = 0.5 * dt / self.dx * self.primitiveEvolution(idir, self.V[slc3aC], slim)
            self.V_im12[slc3aC] += delta_V
            self.V_ip12[slc3aC] += delta_V
            if self.track_pressure:
                self.checkPressure(self.V_im12)
                self.checkPressure(self.V_ip12)
            
        elif self.hs.time_integration == 'hancock_cons':
            slc3aCs = (self.slc_qs, self.slc_aa, self.slc_11)
            U_im12 = self.primitiveToConservedRet(self.V_im12[slc3aCs])
            U_ip12 = self.primitiveToConservedRet(self.V_ip12[slc3aCs])
            F_im12 = self.fluxVector(idir, self.V_im12[slc3aCs])
            F_ip12 = self.fluxVector(idir, self.V_ip12[slc3aCs])
            delta_U = 0.5 * dt / self.dx * (F_im12 - F_ip12)
            U_im12 += delta_U
            U_ip12 += delta_U
            self.conservedToPrimitive(U_im12, self.V_im12[slc3aCs])
            self.conservedToPrimitive(U_ip12, self.V_ip12[slc3aCs])

        return

    # ---------------------------------------------------------------------------------------------

    def limiterNone(self, sL, sR, slim):
        """
        No limiter (central derivative)
        
        This limiter is the absence thereof: it does not limit the left and right slopes but 
        returns their average (the central derivative). This generally produces unstable schemes
        but is implemented for testing and demonstration purposes.
        
        Parameters
        ----------
        sL: array_like
            Array of left slopes.
        sR: array_like
            Array of right slopes. Must have same dimensions as ``sL``.
        slim: array_like
            Output array of limited slope. Must have same dimensions as ``sL`` and ``sR``.
        """
            
        slim[:] = 0.5 * (sL + sR)    
        
        return

    # ---------------------------------------------------------------------------------------------

    def limiterMinMod(self, sL, sR, slim):
        """
        Minimum-modulus limiter
        
        The most conservative limiter, which always chooses the shallower out of the left and 
        right slopes.
        
        Parameters
        ----------
        sL: array_like
            Array of left slopes.
        sR: array_like
            Array of right slopes. Must have same dimensions as ``sL``.
        slim: array_like
            Output array of limited slope. Must have same dimensions as ``sL`` and ``sR``.
        """
        
        sL_abs = np.abs(sL)
        sR_abs = np.abs(sR)
        mask = (sL * sR > 0.0) & (sL_abs <= sR_abs)
        slim[mask] = sL[mask]
        mask = (sL * sR > 0.0) & (sL_abs > sR_abs)
        slim[mask] = sR[mask]        
        
        return

    # ---------------------------------------------------------------------------------------------

    def limiterVanLeer(self, sL, sR, slim):
        """
        The limiter of van Leer
        
        An intermediate limiter that is less conservative than minimum modulus but more 
        conservative than monotonized central.
        
        Parameters
        ----------
        sL: array_like
            Array of left slopes.
        sR: array_like
            Array of right slopes. Must have same dimensions as ``sL``.
        slim: array_like
            Output array of limited slope. Must have same dimensions as ``sL`` and ``sR``.
        """
        
        mask = (sL * sR > 0.0)
        slim[mask] = 2.0 * sL[mask]* sR[mask] / (sL[mask] + sR[mask])    
        
        return

    # ---------------------------------------------------------------------------------------------

    def limiterMC(self, sL, sR, slim):
        """
        Monotonized-central limiter
        
        As the name suggests, this limiter chooses the central derivative wherever possible, but 
        reduces its slope where it would cause negative cell-edge values. This limiter leads to the
        sharpest solutions but is also the least stable.
        
        Parameters
        ----------
        sL: array_like
            Array of left slopes.
        sR: array_like
            Array of right slopes. Must have same dimensions as ``sL``.
        slim: array_like
            Output array of limited slope. Must have same dimensions as ``sL`` and ``sR``.
        """
        
        sC = (sL + sR) * 0.5
        sL_abs = np.abs(sL)
        sR_abs = np.abs(sR)
        mask = (sL * sR > 0.0) & (sL_abs <= sR_abs)
        slim[mask] = 2.0 * sL[mask]
        mask = (sL * sR > 0.0) & (sL_abs > sR_abs)
        slim[mask] = 2.0 * sR[mask]
        mask = np.abs(slim) > np.abs(sC)
        slim[mask] = sC[mask]
        
        return

    # ---------------------------------------------------------------------------------------------
    
    def riemannSolverHLL(self, idir, VL, VR):
        """
        The HLL Riemann solver
        
        A Riemann solver computes the fluxes across cell interfaces given two discontinuous 
        states on the left and right sides of each interface. The Harten-Lax-van Leer (HLL) 
        Riemann solver is one of the simplest such algorithms. It takes into account the 
        fastest waves traveling to the left and to the right, but it takes into account only a 
        single possible intermediate state, which ignores contact discontinuities.
        
        Parameters
        ----------
        idir: int
            Direction of sweep (0 = x, 1 = y).
        VL: array_like
            Array of primitive fluid variables on the left sides of the interfaces.
        VR: array_like
            Array of primitive fluid variables on the right sides of the interfaces. Must have 
            the same dimensions as ``VL``.
    
        Returns
        -------
        flux: array_like
            Array of conservative fluxes across interfaces. Has the same dimensions as ``VL`` and 
            ``VR``.
        """
    
        # Sound speed to the left and right of the interface
        csL = self.soundSpeed(VL)
        csR = self.soundSpeed(VR)
        
        # Maximum negative velocity to the left and positive velocity to the right
        SL = VL[self.VX + idir] - csL
        SR = VR[self.VX + idir] + csR
        
        # Get conserved states for left and right states
        UL = self.primitiveToConservedRet(VL)
        UR = self.primitiveToConservedRet(VR)
        
        # F(V) on the left and right
        FL = self.fluxVector(idir, VL)
        FR = self.fluxVector(idir, VR)
        
        # Formula for the HLL Riemann solver. We first set all fields to the so-called HLL flux, i.e.,
        # the flux in the intermediate state between the two fastest waves SL and SR. If even SL is 
        # positive (going to the right), then we take the flux from the left cell, FL. If even SR is
        # going to the left, we take the right flux. Since these cases can be rare in some problems,
        # we first do a quick check whether there are any cells that match the condition before setting
        # them to the correct fluxes.
        flux = (SR * FL - SL * FR + SL * SR * (UR - UL)) / (SR - SL)

        # Check for cases where all speeds are on one side of the fan, in which case we overwrite
        # the values computed above. This may seem a little wasteful, but in practice, excuting the
        # operation above only for the needed entries costs more time than is typically saved.    
        if np.any(SL >= 0.0):
            mask_L = (SL >= 0.0)
            flux[:, mask_L] = FL[:, mask_L]
        if np.any(SR <= 0.0):
            mask_R = (SR <= 0.0)
            flux[:, mask_R] = FR[:, mask_R]

        return flux

    # ---------------------------------------------------------------------------------------------
    
    def riemannSolverHLLC(self, idir, VL, VR):
        """
        The HLLC Riemann solver
        
        Similar to the HLL Riemann solver, but with an additional distinction of whether the 
        interfaces lie to the left or right of contact discontinuities. The implementation follows
        Chapter 10.4 in Toro 2009.
        
        This Riemann solver explicitly uses pressure and total energy in its calculations and is 
        thus not compatible with an isothermal EOS where we do not track those variables. This is,
        in some sense, by construction: in an isothermal gas, there are no contact discontinuities,
        and the HLLC solver yields no advantage over HLL.
        
        Parameters
        ----------
        idir: int
            Direction of sweep (0 = x, 1 = y).
        VL: array_like
            Array of primitive fluid variables on the left sides of the interfaces.
        VR: array_like
            Array of primitive fluid variables on the right sides of the interfaces. Must have 
            the same dimensions as ``VL``.
    
        Returns
        -------
        flux: array_like
            Array of conservative fluxes across interfaces. Has the same dimensions as ``VL`` and 
            ``VR``.
        """
    
        # Shortcuts to indices
        idir2 = (idir + 1) % 2
        iDN = self.DN
        iU1 = self.VX + idir
        iU2 = self.VX + idir2
        iPR = self.PR
        iET = self.ET
    
        # The first steps are the same as for the HLL Riemann solver
        csL = self.soundSpeed(VL)
        csR = self.soundSpeed(VR)
        SL = VL[iU1] - csL
        SR = VR[iU1] + csR
        UL = self.primitiveToConservedRet(VL)
        UR = self.primitiveToConservedRet(VR)
        FL = self.fluxVector(idir, VL)
        FR = self.fluxVector(idir, VR)
        
        # Calculate the velocity of a contact discontinuity between the left and right star states
        rhoL = VL[iDN]
        rhoR = VR[iDN]
        uL = VL[iU1]
        uR = VR[iU1]
        PL = VL[iPR]
        PR = VR[iPR]
        rhoL_SL_m_uL = rhoL * (SL - uL)
        rhoR_SR_m_uR = rhoR * (SR - uR)
        Sstar = (PR - PL + uL * rhoL_SL_m_uL - uR * rhoR_SR_m_uR) / (rhoL_SL_m_uL - rhoR_SR_m_uR)
        
        # Construct star states. Since the computation is relatively involved, we only do it for those 
        # cells where it is actually needed.
        flux = np.zeros_like(UL)
        
        mask = (SL >= 0.0)
        if np.any(mask):
            flux[:, mask] = FL[:, mask]
        
        mask = (SL < 0.0) & (Sstar >= 0.0)
        if np.any(mask):
            UL_star = np.zeros_like(UL[:, mask])
            rho_star_L = rhoL_SL_m_uL[mask] / (SL[mask] - Sstar[mask])
            UL_star[iDN] = rho_star_L
            UL_star[iU1] = rho_star_L * Sstar[mask]
            UL_star[iU2] = rho_star_L * VL[iU2][mask]
            UL_star[iET] = rho_star_L * (UL[iET][mask] / rhoL[mask] + (Sstar[mask] - uL[mask]) * (Sstar[mask] + PL[mask] / rhoL_SL_m_uL[mask]))
            flux[:, mask] = FL[:, mask] + SL[mask] * (UL_star - UL[:, mask])
        
        mask = (SR > 0.0) & (Sstar < 0.0)
        if np.any(mask):
            UR_star = np.zeros_like(UL[:, mask])
            rho_star_R = rhoR_SR_m_uR[mask] / (SR[mask] - Sstar[mask])
            UR_star[iDN] = rho_star_R
            UR_star[iU1] = rho_star_R * Sstar[mask]
            UR_star[iU2] = rho_star_R * VR[iU2][mask]
            UR_star[iET] = rho_star_R * (UR[iET][mask] / rhoR[mask] + (Sstar[mask] - uR[mask]) * (Sstar[mask] + PR[mask] / rhoR_SR_m_uR[mask]))
            flux[:, mask] = FR[:, mask] + SR[mask] * (UR_star - UR[:, mask])
            
        mask = (SR <= 0.0)
        if np.any(mask):
            flux[:, mask] = FR[:, mask]
        
        return flux

    # ---------------------------------------------------------------------------------------------

    def cflCondition(self):
        """
        Compute the size of the next timestep
        
        This function computes the maximum signal speed anywhere in the domain and sets a timestep
        based on the CFL condition.
        
        Returns
        -------
        dt: float
            The next timestep.
        """
        
        u_max = self.maxSpeedInDomain()
        dt = self.hs.cfl * self.dx / u_max
        
        return dt
            
    # ---------------------------------------------------------------------------------------------

    def solveGravity(self, initial_setup = False):
        """
        Compute gravitational potentials
        
        This function computes the gravitational potential from density (if necessary) and the
        gradients of the potential. It must be executed once after the initial setup, i.e., after
        :func:`~ulula.core.simulation.Simulation.setDomain` but before the simulation is run. The 
        :class:`~ulula.core.setup_base.Setup` class performs this step automatically. In 
        this first step, the function computes the potential that corresponds to a fixed 
        acceleration (for ``'fixed_acc'`` gravity), or the fixed gradients (for ``'fixed_pot'`` 
        gravity), or the initial potential and gradients from the density field (for ``'poisson'`` 
        gravity). In the latter case, the calculation needs to be repeated each time the gravity
        source term is added to the conserved fluid variables.
        
        The Poisson equation is solved via Fourier transform because the Laplacian reduces to a
        multiplication by a "Green's function" in Fourier space (which only works with periodic
        BCs due to the periodic nature of the sine/cosine basis functions). The Green's function
        is specific to the discretization of the Laplacian derivative. We assume a standard
        discretized second derivative, 
        :math:`\\partial^2 \\phi / \\partial x^2 \\approx (\\phi_{i-1} - 2 \\phi_i + \\phi_{i+1}) / 2 \\Delta x`.
        See e.g. Section 9.2 in the 
        `book by Mike Zingale <https://open-astrophysics-bookshelf.github.io/numerical_exercises>`_ 
        for a derivation. 
        
        Parameters
        ----------
        initial_setup: bool
            Whether this is the first time the function is called.
        """
        
        if initial_setup:
            if self.gravity_fixed_acc:
                x, y = self.xyGrid()
                if not self.is_2d:
                    self.gravity_dir = 0
                if self.gravity_dir == 0:
                    self.V[self.GP] = self.gravity_g * x
                else:
                    self.V[self.GP] = self.gravity_g * y
            
            elif self.gravity_fixed_pot:
                self.V[self.GX, 1:-1, :] = (self.V[self.GP, 2:, :] - self.V[self.GP, :-2, :]) / (2.0 * self.dx)
                if self.is_2d:
                    self.V[self.GY, :, 1:-1] = (self.V[self.GP, :, 2:] - self.V[self.GP, :, :-2]) / (2.0 * self.dx)                
            
            elif self.gravity_poisson:
                
                # The longest-wavelength mode, i.e., a frequency of zero, is called the DC mode and
                # corresponds to the normalization of the input density field. For that frequency, 
                # the inverse of our Green's function is zero. The Green's function is not defined 
                # because the normalization of the potential does not change its Laplacian. We 
                # maintain the input normalization to keep the overall normalization of the potential 
                # constant. 
                kx = np.fft.fftfreq(self.nx)
                if self.is_2d:
                    ky = np.fft.fftfreq(self.ny)
                    kx_grid, ky_grid = np.meshgrid(kx, ky, indexing = 'ij')
                    self.gravity_gf = 2.0 / self.dx**2 * (np.cos(2.0 * np.pi * kx_grid) +
                                                          np.cos(2.0 * np.pi * ky_grid) - 2.0)
                    self.gravity_gf[0, 0] = 1.0
                else:
                    self.gravity_gf = 2.0 / self.dx**2 * (np.cos(2.0 * np.pi * kx) - 1.0)
                    self.gravity_gf[0] = 1.0
                self.gravity_gf = 1.0 / self.gravity_gf
                
                if self.gravity_fixed_poisson:
                    self.V[self.GU][...] = self.V[self.GP][...]
                    
        if self.gravity_poisson:
            
            # For the 1D case, we change to a 1D array because the FFT routine interprets a shape 
            # of (nx, 1) incorrectly.
            poisson_rhs = 4.0 * np.pi * self.gravity_G * self.V[self.DN][self.slc_dom]
            if self.is_2d:
                phi = np.fft.fft2(poisson_rhs)
                phi *= self.gravity_gf
                phi = np.real(np.fft.ifft2(phi))
            else:
                phi = np.fft.fft(poisson_rhs[:, 0])
                phi *= self.gravity_gf
                phi = np.real(np.fft.ifft(phi))
                phi = np.reshape(phi, (self.nx, 1))
            
            if self.gravity_fixed_poisson:
                phi += self.V[self.GU][self.slc_dom]
            self.V[self.GP][self.slc_dom] = phi
            self.V[self.GX][self.slc_dom] = -(np.roll(phi, +1, axis = 0) \
                                - np.roll(phi, -1, axis = 0)) / (2.0 * self.dx)
            self.enforceBoundaryConditions(a = [self.V], slc_q = slice(self.GP, self.GX + 1))
            if self.is_2d:
                self.V[self.GY][self.slc_dom] = -(np.roll(phi, +1, axis = 1) \
                                - np.roll(phi, -1, axis = 1) ) / (2.0 * self.dx)
                self.enforceBoundaryConditions(a = [self.V], slc_q = slice(self.GY, self.GY + 1))
        
        return

    # ---------------------------------------------------------------------------------------------    
    
    def addSourceTerms(self, dt):
        """
        Add source terms to conserved quantities

        This function implements the source terms in the equations above, meaning that it adds
        :math:`{\\pmb U} \\rightarrow {\\pmb U} + {\\pmb S} \\Delta t` to the conserved fluid
        variables. For fixed-acceleration gravity, we only set add the acceleration in the appropriate
        dimension. It might seem counter-intuitive that we are adding to the momentum but not to the 
        energy. However, changes in momentum are balanced by "falling," i.e., by changes in the 
        gravitational potential. If the gravitational potential is changing (namely, for 
        ``'poisson'`` gravity), we also add the change in potential to the total energy.
        
        Parameters
        ----------
        dt: float
            The time over which the source term should be integrated.
        """
        
        if self.gravity_fixed_acc:
            self.U[self.MX + self.gravity_dir] -= self.U[self.MS] * self.gravity_g * dt
        else:
            if self.gravity_poisson:
                phi_old = np.array(self.V[self.GP])
                self.solveGravity()
                if self.track_pressure:
                    delta_phi = self.V[self.GP] - phi_old
                    self.U[self.ET] += self.U[self.MS] * delta_phi   
            self.U[self.MX] -= self.U[self.MS] * self.V[self.GX] * dt
            self.U[self.MY] -= self.U[self.MS] * self.V[self.GY] * dt
            
        return

    # ---------------------------------------------------------------------------------------------
    
    def timestep(self, dt = None):
        """
        Advance the fluid state by a timestep dt
        
        This timestepping routine implements a dimensionally split scheme, meaning that we execute
        two sweeps in the two dimensions. We alternate the ordering of the sweeps with each timestep 
        (xy-yx-xy and so on). This so-called Strang splitting maintains 2nd-order accuracy, but only 
        if the timestep is the same for the two sweeps.

        The function internally handles the case of a CFL violation during the second sweep, which 
        can occur even if the timestep was initially set to obey the CFL criterion. In this case,
        the returned timestep will be different from the input timestep (if given).
        
        In each direction, we reconstruct the cell-edge states, compute the conservative Godunov 
        fluxes with the Riemann solver, and add the flux difference to the converved fluid variables.
        Any source terms are added in two half-timesteps before and after the hydrodynamical sweeps.
        
        Parameters
        ----------
        dt: float
            Size of the timestep to be taken. If None, the timestep is computed based on the CFL
            condition using the :func:`~ulula.core.simulation.Simulation.cflCondition` function. This 
            timestep should be used in most circumstances, but sometimes we wish to manually set a
            smaller timestep, for example, to output a file or plot at a particular time. The user 
            is responsible for ensuring that a manually chosen ``dt`` does not exceed the CFL 
            criterion!
        
        Returns
        -------
        dt: float
            The timestep taken.
        """
        
        # Copy current state in case an error occurs.
        self.V_cpy[...] = self.V[...]
        self.U_cpy[...] = self.U[...]

        # If the initial timestep is not given, compute it from the CFL condition
        if dt is None:
            dt = self.cflCondition()

        # Use Strang splitting to maintain 2nd order accuracy; we go xy-yx-xy-yx and so on. For a 
        # 1D simulation, there is no need to perform the y-sweep.
        is_2d = self.is_2d
        if is_2d:
            sweep_idxs = [0, 1]
            if self.last_dir == 0:
                sweep_dirs = [0, 1]
            else:
                sweep_dirs = [1, 0]
        else:
            sweep_idxs = [0]
            sweep_dirs = [0]
        
        # Iterate until we obtain a valid solution. Hopefully, the while loop should only be
        # executed once, but we might run into a CFL violation on the second sweep.
        success = False
        i_try = 0
        while not success:
        
            # We are fundamentally solving the conserved hydro equation dU / dt + div(F(U)) = S(U). 
            # If S(U) != 0, we need to add the time integral of S(U) to U (since it is not obvious
            # that we can pull it into the flux vector, given the div(F(U)) term). In order to
            # maintain 2nd-order accuracy, we do not add the entire source term before or after the
            # other operations but split it into two half-timesteps. 
            if self.use_source_terms:
                self.addSourceTerms(0.5 * dt)
                self.conservedToPrimitive(self.U, self.V)
                self.enforceBoundaryConditions()

            # Now perform the hydro step (without source terms) by sweeping in the two dimensions.
            for sweep_idx in sweep_idxs:
                sweep_dir = sweep_dirs[sweep_idx]

                # If we are on the second sweep, there is a possibility that we are violating the
                # CFL condition, i.e., that the maximum measured CFL number exceeds the maximum. 
                # If so, we re-set the solution, reduce the timestep, and try again.
                if sweep_idx == 1:
                    u_max = self.maxSpeedInDomain()
                    cfl_real = dt * u_max / self.dx
                    if (cfl_real > self.hs.cfl_max):
                        reduce_factor = cfl_real / self.hs.cfl_max * self.hs.cfl_reduce_factor
                        i_try += 1
                        if i_try >= self.hs.cfl_max_attempts:
                            raise Exception('Could not find solution after %d iterations.' % (i_try))
                        print('WARNING: CFL violation on timestep %4d, iteration %d, reducing dt by %.2f from %2e to %.2e.' \
                            % (self.step, i_try, reduce_factor, dt, dt / reduce_factor))
                        dt = dt / reduce_factor
                        self.V[...] = self.V_cpy[...]
                        self.U[...] = self.U_cpy[...]
                        continue
                    else:
                        success = True
                elif not is_2d:
                    success = True

                # Load slices for this dimension
                if sweep_dir == 0:
                    slc3dL = (self.slc_qs, self.slc_lx, self.slc_aa)
                    slc3dR = (self.slc_qs, self.slc_rx, self.slc_aa)
                    slc3fL = (self.slc_qh, self.slc_01, self.slc_aa)
                    slc3fR = (self.slc_qh, self.slc_10, self.slc_aa)
                    slc3fC = (self.slc_qh, self.slc_cx, self.slc_aa)
                else:
                    slc3dL = (self.slc_qs, self.slc_aa, self.slc_ly)
                    slc3dR = (self.slc_qs, self.slc_aa, self.slc_ry)
                    slc3fL = (self.slc_qh, self.slc_aa, self.slc_01)
                    slc3fR = (self.slc_qh, self.slc_aa, self.slc_10)
                    slc3fC = (self.slc_qh, self.slc_aa, self.slc_cy)
            
                # Reconstruct states at left and right cell edges.
                self.reconstruction(sweep_dir, dt)
                
                # Use states at cell edges (right edges in left cells, left edges in right cells) as 
                # input for the Riemann solver, which computes the Godunov fluxes at the interface 
                # walls. Here, we call interface i the interface between cells i-1 and i.
                flux = self.riemannSolver(sweep_dir, self.V_ip12[slc3dL], self.V_im12[slc3dR])
            
                # Update conserved fluid state. We are using Godunov's scheme, as in, we difference the 
                # fluxes taken from the Riemann solver. Note the convention that index i in the flux array
                # means the left interface of cell i, and i+1 the right interface of cell i.
                self.U[slc3fC] = self.U[slc3fC] + dt / self.dx * (flux[slc3fL] - flux[slc3fR])
                
                # If necessary, we perform the second source term addition here during the second
                # sweep so that we do not convert to primitive variables twice.
                if self.use_source_terms and (sweep_idx == 1 or (not is_2d)):
                    self.addSourceTerms(0.5 * dt)
                
                # Convert U -> V; this way, we are sure that plotting functions etc find both the correct
                # conserved and primitive variables.
                self.conservedToPrimitive(self.U, self.V)
            
                # Impose boundary conditions. This needs to happen after each dimensional sweep rather
                # than after each timestep, otherwise the second sweep will encounter some less 
                # advanced cells near the boundaries.
                self.enforceBoundaryConditions()
            
        # Increase timestep
        self.t += dt
        self.step += 1
        self.last_dir = sweep_dir
    
        return dt

    # ---------------------------------------------------------------------------------------------
    
    def save(self, filename = None):
        """
        Save the current state of a simulation
        
        Ulula uses the hdf5 format so save snapshots of a simulation.
        
        Parameters
        ----------
        filename: str
            Output filename. Auto-generated if None.
        """
        
        if filename is None:
            filename = 'ulula_%04d.hdf5' % (self.step)
    
        print('Saving to file %s' % (filename))
    
        f = h5py.File(filename, 'w')

        f.create_group('code')
        f['code'].attrs['file_version'] = ulula_version.__version__
        
        f.create_group('hydro_scheme')
        f['hydro_scheme'].attrs['reconstruction'] = self.hs.reconstruction
        f['hydro_scheme'].attrs['limiter'] = self.hs.limiter
        f['hydro_scheme'].attrs['riemann'] = self.hs.riemann
        f['hydro_scheme'].attrs['time_integration'] = self.hs.time_integration
        f['hydro_scheme'].attrs['cfl'] = self.hs.cfl
        f['hydro_scheme'].attrs['cfl_max'] = self.hs.cfl_max
        f['hydro_scheme'].attrs['cfl_reduce_factor'] = self.hs.cfl_reduce_factor
        f['hydro_scheme'].attrs['cfl_max_attempts'] = self.hs.cfl_max_attempts
    
        f.create_group('eos')
        f['eos'].attrs['eos_mode'] = self.eos_mode
        f['eos'].attrs['eos_gamma'] = self.eos_gamma
        if self.eos_mu is None:
            f['eos'].attrs['eos_mu'] = 0.0
        else:
            f['eos'].attrs['eos_mu'] = self.eos_mu
        if self.eos_mode == 'isothermal':
            f['eos'].attrs['eos_eint_fixed'] = self.eos_eint_fixed
        if self.eos_pressure_floor is None:
            f['eos'].attrs['eos_pressure_floor'] = 0.0
        else:
            f['eos'].attrs['eos_pressure_floor'] = self.eos_pressure_floor

        f.create_group('units')
        f['units'].attrs['unit_l'] = self.unit_l
        f['units'].attrs['unit_t'] = self.unit_t
        f['units'].attrs['unit_m'] = self.unit_m

        f.create_group('gravity')
        f['gravity'].attrs['gravity_mode'] = self.gravity_mode
        f['gravity'].attrs['gravity_dir'] = self.gravity_dir
        f['gravity'].attrs['gravity_g'] = self.gravity_g
        f['gravity'].attrs['gravity_G'] = self.gravity_G

        f.create_group('user_bcs')
        f['user_bcs'].attrs['do_user_updates'] = self.do_user_updates
        f['user_bcs'].attrs['do_user_bcs'] = self.do_user_bcs
    
        f.create_group('domain')
        f['domain'].attrs['is_2d'] = self.is_2d
        f['domain'].attrs['xmin'] = self.xmin
        f['domain'].attrs['xmax'] = self.xmax
        f['domain'].attrs['ymin'] = self.ymin
        f['domain'].attrs['ymax'] = self.ymax
        f['domain'].attrs['dx'] = self.dx
        f['domain'].attrs['nx'] = self.nx
        f['domain'].attrs['ny'] = self.ny
        f['domain'].attrs['nghost'] = self.nghost
        f['domain'].attrs['bc_type'] = self.bc_type
    
        f.create_group('run')
        f['run'].attrs['t'] = self.t
        f['run'].attrs['step'] = self.step
        f['run'].attrs['last_dir'] = self.last_dir
        
        f.create_group('grid')
        for q in self.q_prim:
            f['grid'][q] = self.V[self.q_prim[q], :, :]
        
        f.close()
        
        return

###################################################################################################

def load(filename, user_update_func = None, user_bc_func = None):
    """
    Load a snapshot file into a simulation object
    
    A simulation can be exactly restored from a file, with the exception of user-defined function
    pointers which cannot be saved to file. If such pointers were given to the original simulation, 
    the same functions must be passed to the loaded simulation object.
    
    Parameters
    ----------
    filename: str
        Input filename.
    user_update_func: func
        Function pointer that takes the simulation object as an argument. See 
        :func:`~ulula.core.simulation.Simulation.setUserUpdateFunction`.
    user_bc_func: func
        Function pointer that takes the simulation object as an argument. See 
        :func:`~ulula.core.simulation.Simulation.setUserBoundaryConditions`.

    Returns
    -------
    sim: Simulation
        Object of type :data:`~ulula.core.simulation.Simulation`.
    """

    print('Loading simulation from file %s' % (filename))

    f = h5py.File(filename, 'r')
    
    # The current file version is written to each Ulula file. If the code tries to open a file that
    # is too old to be compatible, an error is thrown.
    file_version_oldest = '1.0.0'
    file_version = f['code'].attrs['file_version']
    if utils.versionIsOlder(file_version_oldest, file_version):
        raise Exception('Cannot load simulation from file %s because version %s is too old (allowed %s).' \
                    % (filename, file_version, file_version_oldest))

    # Create simulation object
    sim = Simulation()

    # Load hydro scheme parameters
    hs_pars = {}
    hs_pars['reconstruction'] = f['hydro_scheme'].attrs['reconstruction']
    hs_pars['limiter'] = f['hydro_scheme'].attrs['limiter']
    hs_pars['riemann'] = f['hydro_scheme'].attrs['riemann']
    hs_pars['time_integration'] = f['hydro_scheme'].attrs['time_integration']
    hs_pars['cfl'] = f['hydro_scheme'].attrs['cfl']
    hs_pars['cfl_max'] = f['hydro_scheme'].attrs['cfl_max']
    hs_pars['cfl_reduce_factor'] = f['hydro_scheme'].attrs['cfl_reduce_factor']
    hs_pars['cfl_max_attempts'] = f['hydro_scheme'].attrs['cfl_max_attempts']
    hs = HydroScheme(**hs_pars)    
    sim.setHydroScheme(hs)
    
    # Load fluid parameters
    eos_mode = f['eos'].attrs['eos_mode']
    eos_gamma = f['eos'].attrs['eos_gamma']
    eos_mu = f['eos'].attrs['eos_mu']
    if eos_mu == 0.0:
        eos_mu = None
    if eos_mode == 'isothermal':
        eos_eint_fixed = f['eos'].attrs['eos_eint_fixed']
    else:
        eos_eint_fixed = None
    eos_pressure_floor = f['eos'].attrs['eos_pressure_floor']
    if eos_pressure_floor == 0.0:
        eos_pressure_floor = None
    sim.setEquationOfState(eos_mode = eos_mode, gamma = eos_gamma, eint_fixed = eos_eint_fixed,
                           mu = eos_mu, pressure_floor = eos_pressure_floor)
    
    # Load code units
    unit_l = f['units'].attrs['unit_l']
    unit_t = f['units'].attrs['unit_t']
    unit_m = f['units'].attrs['unit_m']
    sim.setCodeUnits(unit_l = unit_l, unit_t = unit_t, unit_m = unit_m)

    # Load gravity parameters
    gravity_mode = f['gravity'].attrs['gravity_mode']
    gravity_dir = f['gravity'].attrs['gravity_dir']
    gravity_g = f['gravity'].attrs['gravity_g']
    gravity_G = f['gravity'].attrs['gravity_G']
    sim.setGravityMode(gravity_mode = gravity_mode, gravity_dir = gravity_dir, g = gravity_g, 
                       G = gravity_G)

    # Load user BC settings. If a function was passed, we cannot restore it at this point.
    if f['user_bcs'].attrs['do_user_updates'] and user_update_func is None:
        raise Exception('Simulation loaded from file %s has user-defined update function; need user_update_func parameter to restore the simulation.' \
                        % (filename))
    sim.setUserUpdateFunction(user_update_func)
    if f['user_bcs'].attrs['do_user_bcs'] and user_bc_func is None:
        raise Exception('Simulation loaded from file %s has user-defined boundary conditions; need user_bc_func parameter to restore the simulation.' \
                        % (filename))
    sim.setUserBoundaryConditions(user_bc_func)

    # Load domain parameters and initialize domain
    nx = int(f['domain'].attrs['nx'])
    ny = int(f['domain'].attrs['ny'])
    xmin = f['domain'].attrs['xmin']
    xmax = f['domain'].attrs['xmax']
    ymin = f['domain'].attrs['ymin']
    bc_type = f['domain'].attrs['bc_type']
    sim.setDomain(nx, ny, xmin = xmin, xmax = xmax, ymin = ymin, bc_type = bc_type)

    # Ensure gravitational potentials are set
    sim.solveGravity(initial_setup = True)

    # Load and reset time and step
    sim.t = f['run'].attrs['t']
    sim.step = f['run'].attrs['step']
    sim.last_dir = f['run'].attrs['last_dir']
    
    # Set grid variables
    for q in sim.q_prim:
        sim.V[sim.q_prim[q], :, :] = f['grid'][q]
        
    # Initialize the conserved variables and ghost cells
    sim.primitiveToConserved(sim.V, sim.U)
    sim.enforceBoundaryConditions()

    f.close()
    
    return sim

###################################################################################################
