###################################################################################################
#
# This file is part of the ULULA code.
#
# (c) Benedikt Diemer, University of Maryland
#
###################################################################################################

import os
import subprocess
import glob
from matplotlib import pyplot as plt
import copy
import time
import math
import numpy as np
import inspect

import ulula.core.simulation as ulula_sim
import ulula.core.plots as ulula_plots

###################################################################################################

def run(setup, 
            hydro_scheme = None, nx = 200, tmax = 1.0, max_steps = None, restart_file = None,
            print_step = 100, check_conservation = True,
            output_step = None, output_time = None, output_suffix = '',
            plot_step = None, plot_time = None, plot_ics = True, plot_1d = False, plot_2d = True, 
            save_plots = True, plot_suffix = '', plot_file_ext = 'pdf', plot_dpi = 300,
            plot_callback_func = None,
            movie = False, movie_1d = False, movie_length = 4.0, movie_file_ext = 'mp4', movie_fps = 25,
            movie_dpi = 200,
            **kwargs):
    """
    Runtime environment for Ulula.
    
    This function executes the hydro solver for a given problem setup and user-defined parameters. 
    Depending on user choices, it produces output files, plots, and movies. Customizations that are 
    implemented in the setup class (e.g., which variables to plot with which colormaps) are automatically 
    routed to the respective plotting routines. 
    
    Parameters
    ----------
    setup: Setup
        Setup object. See :doc:`setups` for how to create this object.
    hydro_scheme: HydroScheme
        :class:`~ulula.core.simulation.HydroScheme` object that contains choices for the hydro
        solver, the CFL number, and so on. If None, the standard scheme is used. See 
        :doc:`simulation` for details.
    nx: int
        Number of cells in the x-direction. The ratio of x and y is determined by the problem 
        setup.
    tmax: float
        Time when the simulation should be stopped (in code units).
    max_steps: int
        Maximum number of steps to take. If None, no limit is imposed and the code is run to 
        a time ``tmax``. 
    restart_file: str
        If not None, the simulation is loaded from this filename and restarted at the step
        where it was saved.
    print_step: int
        Print a line to the console every ``print_step`` timesteps.
    check_conservation: bool
        If True, we compute the total mass, energy and so on each ``print_step`` timesteps and
        compare it to the initial energy. Note that the conserved quantities depend on the 
        boundary conditions of the simulation setup: mass, energy and momentum are conserved in
        periodic BCs, only mass and energy in wall BCs, and nothing is conserved in outflow BCs.
        Similarly, gravity can break the conservation laws.
    output_step: int
        Output a snapshot/restart file every ``output_step`` timesteps. Note that this spacing 
        probably does not correspond to fixed times. If the latter is desired, use 
        ``output_time``. Both ``output_step`` and ``output_time`` can be used at the same time 
        to produce two sets of files.
    output_time: float
        Produce output files in time intervals of size ``output_time`` (given in code units). This 
        parameter should not change the progression of the simulation because the timesteps taken
        to arrive at the desired times are not used for the actual simulation.
    output_suffix: string
        String to add to all output filenames.
    plot_step: int
        Produce a plot every ``plot_step`` timesteps. Note that this spacing probably does not
        correspond to fixed times. If the latter is desired, use ``plot_time``. Both ``plot_step``
        and ``plot_time`` can be used at the same time to produce two sets of plots.
    plot_time: float
        Produce plots in time intervals of size ``plot_time`` (given in code units). This 
        parameter should not change the progression of the simulation because the timesteps taken
        to arrive at the desired times are not used for the actual simulation.
    plot_ics: bool
        Produce a plot of the initial conditions (if ``plot_step`` and/or ``plot_time`` are set).
    plot_1d: bool
        If ``True``, the 1D plotting routine is called at the specified time or step intervals.
        This parameter is ignored for 1D simulations.
    plot_2d: bool
        If ``True``, the 2D plotting routine is called at the specified time or step intervals.
        This parameter is ignored for 1D simulations.
    save_plots: bool
        If ``True``, plots are saved to a file (see also ``plot_suffix``, ``plot_file_ext``,
        and ``plot_dpi``). If ``False``, plots are shown in an interactive matplotlib window. Note
        that this can happen many times during a simulation depending on the values of ``plot_step`` 
        and/or ``plot_time``.
    plot_suffix: string
        String to add to all plot filenames (only active if ``save_plots == True``).
    plot_file_ext: string
        File extension for plots. Can be ``png``, ``pdf``, or any other extension supported by 
        the matplotlib library (only active if ``save_plots == True``).
    plot_dpi
        Dots per inch for png figures or other bitmap-like image formats (only active if 
        ``save_plots == True`` and ``plot_file_ext == 'png'``).
    plot_callback_func: function
        If not None, this must be a function that can be called with the signature
        ``plot_callback_func(sim, fig, panels, plot_type)``, meaning that it accepts as parameters a
        simulation object, a matplotlib figure, a list of matplotlib axes objects, and a string 
        that may be ``'1d'``, ``'2d'``, or ``'movie'`` to identify what kind of plot has been created. 
        The function is called after every time a plot is created and before it is saved or shown.
    movie: bool
        If ``True``, a movie is created by outputting frames at equally spaced times and running 
        a tool to combine them (see ``movie_file_ext``).
    movie_1d: bool
        If ``True``, the 1D plotting routine is called instead of the 2D plotting routine for a
        2D simulation. This parameter is ignored for 1D simulations.
    movie_length: float
        Length of the movie in seconds (not code units!).
    movie_file_ext: str
        Movie format, which can be ``'mp4'`` or ``'gif'``. If ``'mp4'``, the ffmpeg software must
        be installed to compile image files into a movie. If ``'gif'``, the python package pillow is used.
        The mp4 format offers much better compression (and thus smaller file size) at fixed 
        quality.
    movie_fps: int
        Framerate of the movie (25 is typical). The code can output at most one frame per 
        simulation timestep, which should not normally be an issue. A movie with a finer time 
        resolution could be produced by lowering the CFL number to force smaller timesteps and 
        increasing the framerate.
    movie_dpi: int
        Resolution of the png files used to create the movie.
    kwargs: kwargs
        Additional keyword arguments that are passed to the Ulula plotting functions 
        :func:`~ulula.core.plots.plot1d` and/or :func:`~ulula.core.plots.plot2d`. Keyword arguments 
        must appear in either function signature.
        
    Returns
    -------
    sim: Simulation
        Object of type :data:`~ulula.core.simulation.Simulation`
    """
    
    # First we create the simulation object. If a restart file is given, we load it and start the 
    # simulation from the respective snapshot. If not, we create a new simulation object, set the 
    # hydro scheme, and let the setup determine the initial conditions and settings such as gravity, 
    # EOS, and so on.
    if restart_file is not None:
        if setup.hasUserBoundaryConditions():
            user_bc_func = setup.setBoundaryConditions
        else:
            user_bc_func = None
        sim = ulula_sim.load(restart_file, user_bc_func = user_bc_func)
        if sim.t >= tmax:
            raise Exception('The final time tmax (%.2e) must be greater than the time in the restart file (%.2e).' \
                        % (tmax, sim.t))
    else:
        sim = ulula_sim.Simulation()
        sim.setHydroScheme(hydro_scheme)
        setup.initialConditions(sim, nx)
    
    # Set some times and variables that are used by the functions below.
    next_time_output = None
    next_time_plot = None
    next_time_movie = None
    
    if movie:
        step_movie = 0
        movie_time = tmax / (movie_length * movie_fps - 1)
    else:
        step_movie = None
        movie_time = None
        
    setup_name = setup.shortName()

    # ---------------------------------------------------------------------------------------------
    
    # Compute the next time when a certain operation needs to happen given the current time and the
    # operation's time interval.
    
    def nextTime(sim, interval):
        
        if interval is None:
            next_time = None
        else:
            n_t = math.floor(sim.t / interval)
            next_time = interval * (n_t + 1)

        return next_time

    # ---------------------------------------------------------------------------------------------

    def doPlotting(sim, fn_str):

        if do_plot_1d:
            fig, panels = ulula_plots.plot1d(sim, **plot_kwargs_1d)
            if plot_callback_func is not None:
                plot_callback_func(sim, fig, panels, '1d')
            if save_plots:
                plt.savefig('ulula_%s_1d_%s%s.%s' % (setup_name, fn_str, plot_suffix, plot_file_ext),
                            dpi = plot_dpi)
                plt.close()
            else:
                plt.show()
        
        if do_plot_2d:
            fig, panels = ulula_plots.plot2d(sim, **plot_kwargs_2d)
            if plot_callback_func is not None:
                plot_callback_func(sim, fig, panels, '2d')
            if save_plots:
                plt.savefig('ulula_%s_%s%s.%s' % (setup_name, fn_str, plot_suffix, plot_file_ext),
                            dpi = plot_dpi)
                plt.close()
            else:
                plt.show()
        
        return

    # ---------------------------------------------------------------------------------------------

    # Perform step-based saving and plotting operations
        
    def checkOutputStep(sim, final_step = False):
        
        if (output_step is not None) and (sim.step % output_step == 0):
            sim.save(filename = 'ulula_step_%04d%s.hdf5' % (sim.step, output_suffix))
        
        if (plot_step is not None) and ((sim.step % plot_step == 0) or final_step) \
            and not ((sim.step == 0) and (plot_ics == False)):
            doPlotting(sim, 'step_%04d' % (sim.step))

        return

    # ---------------------------------------------------------------------------------------------

    # If a particular operation needs to happen at t_next and that time is within the next 
    # timestep, we need to return the simulation at time t_next. To avoid messing with the actual
    # simulation run by inserting an artificially small timestep, we copy the entire simulation 
    # object and advance it by the desired timestep. This operation has some memory overhead but
    # is cleaner than trying to restore the previous state to the main simulation object.
    #
    # We need to be careful though since the timestep taken can be smaller than the intended
    # timestep if there is a CFL violation. Thus, we check a second time whether the intended 
    # time was actually reached. 

    def getSimAtTime(sim, dt_next, t_next):
        
        if (t_next is None):
            return False, None
        
        do_operation = (sim.t + dt_next >= t_next)
        
        if do_operation:
            if abs(t_next - sim.t) < 1E-7 * tmax:
                sim_copy = sim
            else:
                sim_copy = copy.copy(sim)
                while sim_copy.t < t_next - 1E-6:
                    dt_needed = t_next - sim_copy.t
                    sim_copy.timestep(dt = dt_needed)
                if abs(t_next - sim_copy.t) > 1E-6:
                    raise Exception('Could not run copy of simulation to t = %.4e.' % (t_next))
        else:
            sim_copy = None
            
        return do_operation, sim_copy

    # ---------------------------------------------------------------------------------------------

    # Add up the grid of conserved quantities in the simulation, leaving out the ghost cells.

    def getConservedQuantities(sim):
        
        U_tot = np.sum(sim.U[:, sim.xlo:sim.xhi + 1, sim.ylo:sim.yhi + 1], axis = (1, 2))
        
        return U_tot

    # ---------------------------------------------------------------------------------------------

    # Plotting settings. Since we allow plotting both in 1D and 2D, the correct keyword arguments 
    # must be routed to both plotting functions.
    plot_kwargs = copy.copy(kwargs)
    plot_kwargs.update(dict(range_func = setup.plotLimits, true_solution_func = setup.trueSolution,
                            cmap_func = setup.plotColorMaps))
    plot_kwargs_1d = {}
    plot_kwargs_2d = {}
    signature_1d = inspect.signature(ulula_plots.plot1d).parameters
    signature_2d = inspect.signature(ulula_plots.plot2d).parameters
    for k in plot_kwargs:
        if (not k in signature_1d) and (not k in signature_2d):
            raise Exception('Keyword argument "%s" does not match either 1D or 2D plotting functions.' % (k))
        if k in signature_1d:
            plot_kwargs_1d[k] = plot_kwargs[k]
        if k in signature_2d:
            plot_kwargs_2d[k] = plot_kwargs[k]
    if not sim.is_2d:
        do_plot_1d = True
        do_plot_2d = False
        if movie:
            plotFunctionMovie = ulula_plots.plot1d
            plot_kwargs_movie = plot_kwargs_1d
    else:
        do_plot_1d = plot_1d
        do_plot_2d = plot_2d
        if movie:
            if movie_1d:
                plotFunctionMovie = ulula_plots.plot1d
                plot_kwargs_movie = plot_kwargs_1d
            else:
                plotFunctionMovie = ulula_plots.plot2d
                plot_kwargs_movie = plot_kwargs_2d

    # Now we can use the helper functions above.
    if restart_file is not None:
        next_time_output = nextTime(sim, output_time)
        next_time_plot = nextTime(sim, plot_time)
        next_time_movie = nextTime(sim, movie_time)
    else:
        # Plot/save initial conditions and reset the next operation times to 0 so that time-based
        # saving/plotting is also performed at t = 0.
        checkOutputStep(sim)
        if output_time is not None:
            next_time_output = 0.0
        if plot_time is not None:
            if plot_ics:
                next_time_plot = 0.0
            else:
                next_time_plot = plot_time
        if movie_time is not None:
            next_time_movie = 0.0

    # If we are checking the conservation of supposedly conserved quantities, we measure their
    # initial values now. If the simulation has outflow BCs, this makes no sense since nothing is
    # conserved. While mass and energy can only be positive and thus always have a finite value,
    # momentum can easily be set up such that the net momentum is zero. We thus only check momentum
    # conservation if there was some appreciable initial momentum (in code units).
    if check_conservation and (sim.bc_type == 'outflow'):
        check_conservation = False
    if check_conservation:
        MS = sim.q_cons['MS']
        MX = sim.q_cons['MX']
        MY = sim.q_cons['MY']
        if sim.track_pressure:
            ET = sim.q_cons['ET']
        U_tot_ini = getConservedQuantities(sim)
        check_mom_x = (sim.bc_type == 'periodic') and (np.abs(U_tot_ini[MX]) > 1E-6)
        check_mom_y = (sim.bc_type == 'periodic') and (np.abs(U_tot_ini[MY]) > 1E-6)
    
    # Main loop over timesteps. We record the starting timestep as it may not be zero if we
    # are restarting from a file.
    t0 = time.process_time()
    step_start = sim.step
    
    while sim.t < tmax:

        # Compute timestep. We check that the timestep has not gone to zero, which can indicate
        # that something has become unphyiscal and led to extremely high sound speeds.
        dt = sim.cflCondition()
        if dt < 1E-10:
            cs = sim.soundSpeed(sim.V)
            idx = np.unravel_index(np.argmax(cs, axis = None), cs.shape)
            raise Exception('Timestep has effectively gone to zero (dt %.1e, cs_max %.1e), something is wrong.' \
                            % (dt, cs[idx]))
        
        # Check whether we need to output a snapshot file during the next timestep
        do_output, sim_copy = getSimAtTime(sim, dt, next_time_output)
        if do_output:
            sim_copy.save(filename = 'ulula_time_%.4f%s.hdf5' % (sim_copy.t, output_suffix))
        
        # Check whether we need to create a plot during the next timestep
        do_plot, sim_copy = getSimAtTime(sim, dt, next_time_plot)
        if do_plot:
            doPlotting(sim, 'time_%.4f' % sim_copy.t)

        # Check whether we need to output a movie frame during the next timestep
        do_movie, sim_copy = getSimAtTime(sim, dt, next_time_movie)
        if do_movie:
            fig, panels = plotFunctionMovie(sim_copy, **plot_kwargs_movie)
            if plot_callback_func is not None:
                plot_callback_func(sim, fig, panels, 'movie')
            plt.savefig('frame_%04d.png' % (step_movie), dpi = movie_dpi)
            plt.close()
            step_movie += 1
        
        # Perform the actual timestep
        sim.timestep(dt = dt)
        
        # Print output if desired
        if sim.step % print_step == 0:
            msg = 'Timestep %5d, t = %.2e, dt = %.2e' % (sim.step, sim.t, dt)
            if check_conservation:
                U_tot_cur = getConservedQuantities(sim)
                ratio_m = U_tot_cur[MS] / U_tot_ini[MS] - 1.0
                msg += '; conservation of mass to %8.1e' % (ratio_m)
                if sim.track_pressure:
                    ratio_e = U_tot_cur[ET] / U_tot_ini[ET] - 1.0
                    msg += ', energy %8.1e' % (ratio_e)
                if check_mom_x:
                    msg += ', X-mom %8.1e' % (U_tot_cur[MX] / U_tot_ini[MX] - 1.0)
                if check_mom_y:
                    msg += ', Y-mom %8.1e' % (U_tot_cur[MY] / U_tot_ini[MY] - 1.0)
            print(msg)
        
        # Set the next times for output/plotting/movie frames
        if do_output:
            next_time_output = nextTime(sim, output_time)
        if do_plot:
            next_time_plot = nextTime(sim, plot_time)
        if do_movie:
            next_time_movie = nextTime(sim, movie_time)
        
        # Save and/or plot at this step if necessary
        checkOutputStep(sim)

        # Check for abort conditions
        if (max_steps is not None) and (sim.step >= max_steps):
            break

    # Print timing info
    ttot = time.process_time() - t0
    steps_taken = sim.step - step_start
    print('Simulation finished. Took %d steps, %.1f seconds, %.3f s/step, %.2f steps/s.' % \
        (steps_taken, ttot, ttot / steps_taken, steps_taken / ttot))

    # Render movie. If the chosen file extension is mp4, we use the ffmpeg library via the command
    # line to combine the png files. As a pure-python alternative, we can use the pillow library 
    # to combine the files to a gif. 
    if movie:
        movie_name = 'ulula_%s%s.%s' % (setup_name, plot_suffix, movie_file_ext)
        
        frame_fns = sorted(glob.glob('frame*.png'))
        
        if movie_file_ext == 'mp4':
            cmd_str = 'ffmpeg -i frame_%04d.png -pix_fmt yuv420p -y' 
            cmd_str += ' -framerate %d ' % (movie_fps)
            cmd_str += movie_name
            subprocess.run(cmd_str, shell = True)
        
        elif movie_file_ext == 'gif':
            try:
                import PIL
            except:
                raise Exception('Could not import pillow library (PIL) to make gif movie. Please make sure it is installed.')
            images = []
            for frame in frame_fns:
                # We need to make copies due to pillow bug (issue #1237)
                try:
                    image = PIL.Image.open(frame)
                    cp = image.copy() 
                    images.append(cp)
                    image.close()
                except Exception as e:
                    print('WARNING: Could not load image file %s, pillow exception %s.' % (frame, str(e)))
            images[0].save(movie_name, save_all = True, append_images = images[1:], 
                  loop = 0, duration = int(1000 / movie_fps))
            
        else:
            raise Exception('Unknown movie file extension, %s (must be mp4 or gif).' % (movie_file_ext))

        # Delete frame files
        for frame in frame_fns:
            try:
                os.remove(frame)
            except OSError:
                pass
    
    # Plot final state
    checkOutputStep(sim, final_step = True)

    return sim

###################################################################################################
