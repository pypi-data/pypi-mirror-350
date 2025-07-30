###################################################################################################
#
# This file is part of the ULULA code.
#
# (c) Benedikt Diemer, University of Maryland
#
###################################################################################################

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec

import ulula.utils.utils as utils
import ulula.physics.units as units
import ulula.physics.constants as constants

###################################################################################################

fields = {}
"""
List of fields that can be extracted from the simulation and/or plotted.
"""

fields['DN']       = {'name': 'Density',            'label': r'\rho',                 'cmap': 'viridis'}
fields['VX']       = {'name': 'X-velocity',         'label': r'v_{\rm x}',            'cmap': 'RdBu_r'}
fields['VY']       = {'name': 'Y-velocity',         'label': r'v_{\rm y}',            'cmap': 'RdBu_r'}
fields['VT']       = {'name': 'Total velocity',     'label': r'v_{\rm tot}',          'cmap': 'viridis'}
fields['VR']       = {'name': 'Radial velocity',    'label': r'v_{\rm r}',            'cmap': 'RdBu_r'}
fields['VA']       = {'name': 'Azimuthal velocity', 'label': r'v_{\phi}',             'cmap': 'RdBu_r'}
fields['PR']       = {'name': 'Pressure',           'label': r'P',                    'cmap': 'viridis'}
fields['MX']       = {'name': 'X-momentum',         'label': r'm_{\rm x}',            'cmap': 'RdBu_r'}
fields['MY']       = {'name': 'Y-momentum',         'label': r'm_{\rm y}',            'cmap': 'RdBu_r'}
fields['ET']       = {'name': 'Energy',             'label': r'E',                    'cmap': 'viridis'}
fields['EI']       = {'name': 'Internal energy',    'label': r'\epsilon',             'cmap': 'viridis'}
fields['TK']       = {'name': 'Temperature',        'label': r'T',                    'cmap': 'viridis'}
fields['GP']       = {'name': 'Potential',          'label': r'\Phi',                 'cmap': 'viridis'}
fields['GX']       = {'name': 'Pot. gradient',      'label': r'{\rm d}\Phi/{\rm d}x', 'cmap': 'RdBu_r'}
fields['GY']       = {'name': 'Pot. gradient',      'label': r'{\rm d}\Phi/{\rm d}y', 'cmap': 'RdBu_r'}
fields['GU']       = {'name': 'User-added pot.',    'label': r'\Phi_{\rm user}',      'cmap': 'viridis'}

label_code_units = r'{\rm CU}'

###################################################################################################

def getQuantities(sim, q_list, unit_l = 'code', unit_t = 'code', unit_m = 'code'):
    """
    Extract fluid properties
    
    The fluid properties in an Ulula simulation are stored in separate arrays as primitive and 
    conserved variables. Some quantities, such as total velocity, need to be calculated after
    the simulation has finished. This function takes care of all related operations and returns
    a single array that has the same dimensions as the domain.
    
    Moreover, the function computes unit conversion factors if necessary and creates the 
    corresponding labels for plotting. One quantity that demands special treatment is temperature, 
    which cannot sensibly be plotted in code units. Instead we always convert to Kelvin, even if 
    code units are used.
    
    Parameters
    ----------
    sim: Simulation
        Object of type :data:`~ulula.core.simulation.Simulation`.
    q_list: array_like
        List of quantities to extract. Quantities are identified via the short strings given in the
        :data:`~ulula.core.plots.fields` dictionary.
    unit_l: str
        Length unit for returned arrays (see :mod:`~ulula.physics.units` for valid units). If other 
        than ``'code'``, ``unit_t`` and ``unit_m`` must also be changed from code units.
    unit_t: str
        Time unit for returned arrays (see :mod:`~ulula.physics.units` for valid units). If other 
        than ``'code'``, ``unit_l`` and ``unit_m`` must also be changed from code units.
    unit_m: str
        Mass unit for returned arrays (see :mod:`~ulula.physics.units` for valid units). If other 
        than ``'code'``, ``unit_l`` and ``unit_t`` must also be changed from code units.

    Returns
    -------
    q_array: array_like
        Array of fluid properties. Has dimensions of the number of quantities extracted times the
        domain.
    conv_factors: array_like
        Unit conversion factors. The returned ``q_array`` has already been multiplied by these 
        factors in order to bring it into the desired unit system, but they may be useful for other
        parts of the analysis or plotting. If code units are chosen, all factors are unity.
    q_labels: array_like
        List of latex-formatted labels for the fluid quantities.
    conv_l: float
        Unit conversion factor for length, which must be applied to the dimensions of any plot.
    label_l: float
        Unit label for lengths.
    """
    
    # Check that quantities are valid
    for q in q_list:
        if not q in fields:
            raise Exception('Unknown quantity, %s. Valid quantities are %s.' \
                        % (str(q), str(list(fields.keys()))))

    nq = len(q_list)
    q_array = np.zeros((nq, sim.nx + 2 * sim.nghost, sim.ny + 2 * sim.nghost), float)
    conv_factors = []
    q_labels = []

    # If we are converting units, we compute conversion factors between code units and the given
    # units once before applying them to all plotted quantities. We do not allow a mixture of
    # code and other units, since this becomes complicated for mixed quantities (e.g., density in
    # tons / code unit^3 are not intuitive). 
    do_convert = ((unit_l != 'code') or (unit_t != 'code') or (unit_m != 'code'))
    if do_convert:
        conv_l = 1.0
        conv_t = 1.0
        conv_m = 1.0
        if ((unit_l == 'code') or (unit_t == 'code') or (unit_m == 'code')):
            raise Exception('Found mixed code and other units (%s, %s, %s). Please select consistent unit system.' \
                        % (unit_l, unit_t, unit_m))
        if not unit_l in units.units_l:
            raise Exception('Unknown length unit, %s. Allowed are %s.' % (unit_l, str(list(units.units_l.keys()))))
        conv_l = sim.unit_l / units.units_l[unit_l]['in_cgs']
        unit_label_l = units.units_l[unit_l]['label']
        
        if not unit_t in units.units_t:
            raise Exception('Unknown time unit, %s. Allowed are %s.' % (unit_t, str(list(units.units_t.keys()))))
        conv_t = sim.unit_t / units.units_t[unit_t]['in_cgs']
        unit_label_t = units.units_t[unit_t]['label']

        if not unit_m in units.units_m:
            raise Exception('Unknown mass unit, %s. Allowed are %s.' % (unit_m, str(list(units.units_m.keys()))))
        conv_m = sim.unit_m / units.units_m[unit_m]['in_cgs']
        unit_label_m = units.units_m[unit_m]['label']
    else:
        conv_l = 1.0
        unit_label_l = label_code_units

    # Copy quantities from the simulation, and compute them if necessary. If the simulations was
    # run with an isothermal EOS, the pressure/total energy fields do not exist and need to be
    # reconstructed.
    for iq in range(nq):
        q = q_list[iq]
        if q in sim.q_prim:
            q_array[iq] = sim.V[sim.q_prim[q]]
        elif q in sim.q_cons:
            q_array[iq] = sim.U[sim.q_cons[q]]
        else:
            rho = sim.V[sim.q_prim['DN']]
            vx = sim.V[sim.q_prim['VX']]
            vy = sim.V[sim.q_prim['VY']]
            if q == 'VT':
                q_array[iq] = np.sqrt(vx**2 + vy**2)
            elif q == 'VR':
                x, y = sim.xyGrid()
                r = np.sqrt(x**2 + y**2)
                mask = (np.abs(r) > 1E-20)
                q_array[iq][mask] = (vx[mask] * x[mask] + vy[mask] * y[mask]) / r[mask]
            elif q == 'VA':
                x, y = sim.xyGrid()
                phi = np.arctan2(y, x)
                q_array[iq] = -np.sin(phi) * vx + np.cos(phi) * vy
            elif q in ['EI', 'TK']:
                if sim.track_pressure:
                    eint_rho = sim.U[sim.q_cons['ET']] - 0.5 * rho * (vx**2 + vy**2)
                    if sim.gravity_mode != 'none':
                        eint_rho -= rho * sim.V[sim.q_prim['GP']]
                    q_array[iq] = eint_rho / rho
                else:
                    q_array[iq, ...] = sim.eos_eint_fixed
                if q == 'TK':
                    if sim.eos_mu is None:
                        raise Exception('The mean particle weight mu must be set for temperature to be computed.')
                    eint_cgs = q_array[iq] * sim.unit_l**2 / sim.unit_t**2
                    q_array[iq] = eint_cgs * (sim.eos_gamma - 1.0) * sim.eos_mu * constants.mp_cgs / constants.kB_cgs
            elif not sim.track_pressure and q == 'PR':
                q_array[iq] = sim.eos_eint_fixed * rho * sim.eos_gm1
            elif not sim.track_pressure and q == 'ET':
                E_rho = 0.5 * (vx**2 + vy**2) + sim.eos_eint_fixed
                if sim.gravity_mode != 'none':
                    E_rho += sim.V[sim.q_prim['GP']]
                q_array[iq] = E_rho * rho
            elif sim.gravity_mode == 'fixed_pot' and q == 'GU':
                q_array[iq] = sim.V[sim.q_prim['GP']]
            else:
                raise Exception('Unknown quantity, %s.' % (str(q)))
        
        # Convert units and create combined labels, if necessary
        if do_convert:
            if q in ['DN']:
                conv_fac = conv_m / conv_l**3
                unit_label = unit_label_m + r'/' + unit_label_l + r'^3'
            elif q in ['VX', 'VY', 'VT', 'VR', 'VA']:
                conv_fac = conv_l / conv_t
                unit_label = unit_label_l + r'/' + unit_label_t
            elif q in ['MX', 'MY']:
                conv_fac = conv_m / conv_l**2 / conv_t
                unit_label = unit_label_m + r'/' + unit_label_l + r'^2/' + unit_label_t
            elif q in ['PR', 'ET']:
                conv_fac = conv_m / conv_l / conv_t**2
                unit_label = unit_label_m + r'/' + unit_label_l + r'/' + unit_label_t + r'^2'
            elif q in ['EI', 'GP', 'GU']:
                conv_fac = conv_l**2 / conv_t**2
                unit_label = unit_label_l + r'^2/' + unit_label_t + r'^2'
            elif q in ['GX', 'GY']:
                conv_fac = conv_l / conv_t**2
                unit_label = unit_label_l + r'/' + unit_label_t + r'^2'
            elif q in ['TK']:
                conv_fac = 1.0
                unit_label = r'K'
            else:
                raise Exception('Could not find conversion for plot quantity %s.' % (q))
            q_array[iq] *= conv_fac
            conv_factors.append(conv_fac)
        else:
            unit_label = label_code_units
            conv_factors.append(1.0)

        # Create label and unit label
        label = r'$' + fields[q]['label'] + r'\ (' + unit_label + r')$'
        q_labels.append(label)
    
    conv_factors = np.array(conv_factors)
    
    return q_array, conv_factors, q_labels, conv_l, unit_label_l

###################################################################################################

def plot1d(sim, q_plot = ['DN', 'VX', 'VY', 'PR'], 
        plot_unit_l = 'code', plot_unit_t = 'code', plot_unit_m = 'code',
        plot_ghost_cells = False, range_func = None, 
        # The following parameters are specific to 1D plotting
        true_solution_func = None, plot_geometry = 'line', invert_direction = False, 
        radial_bins_per_cell = 4.0, vertical = False):
    """
    Plot fluid state along a 1D line
    
    This function creates a multi-panel plot of the fluid variables along a 1D domain. For 2D 
    simulations, the plots can show fluid quantities along a line through the center of the domain
    or a radial average. The plot is created but not shown or saved to a file. These operations can 
    be completed using the returned matplotlib objects. Plots can also be edited before saving 
    via a callback function passed to the :func:`~ulula.core.run.run` function.
    
    Parameters
    ----------
    sim: Simulation
        Object of type :data:`~ulula.core.simulation.Simulation`.
    q_plot: array_like
        List of quantities to plot. Quantities are identified via the short strings given in the
        :data:`~ulula.core.plots.fields` dictionary.
    plot_unit_l: str
        Length unit to be plotted (see :mod:`~ulula.physics.units` for valid units). If other 
        than ``'code'``, ``plot_unit_t`` and ``plot_unit_m`` must also be changed from code units.
    plot_unit_t: str
        Time unit to be plotted (see :mod:`~ulula.physics.units` for valid units). If other 
        than ``'code'``, ``plot_unit_l`` and ``plot_unit_m`` must also be changed from code units.
    plot_unit_m: str
        Mass unit to be plotted (see :mod:`~ulula.physics.units` for valid units). If other 
        than ``'code'``, ``plot_unit_l`` and ``plot_unit_t`` must also be changed from code units.
    plot_ghost_cells: bool
        If ``True``, ghost cells are plotted and separated from the physical domain by a gray
        vertical line. This option is useful for debugging. Ignored if ``plot_geometry == 'radius'``.
    range_func: function
        If None, the plotting ranges are chosen automatically. Otherwise this parameter must be
        a function that can be called with the signature ``range_func(sim, q_plot, plot_geometry)``
        and that returns three lists with the same lengths as the number of plot quantities. The 
        lists give the minimum and maximum plot extents for each fluid variable, as well as whether 
        to use a log scale (if ``True`` is returned for a given quantity). Elements in the lists can 
        be None in which case ranges are chosen automatically. The range function is typically 
        implemented within a problem setup (see :doc:`setups`).
    true_solution_func: function
        If None, no true solution is plotted. Otherwise it must be a function that can be called
        with the signature ``true_solution_func(sim, x_plot, q_plot, plot_geometry)``, where 
        ``x_plot`` is an array of x-bins. The function must return a list with one element for each 
        of the quantities in ``q_plot``. If an element is None, no solution is plotted. Otherwise
        the element must be an array with the same dimensions as ``x_plot``. The true solution
        must be in code units, which are automatically converted if the user has chosen 
        different units for plotting. The true solution function is typically implemented within a
        problem setup (see :doc:`setups`).
    plot_geometry: str
        For 2D simulations, the type of cut through the domain that is plotted. Can be ``line`` or 
        ``radius`` (which creates a radially averaged plot from the center).
    invert_direction: bool
        If ``plot_geometry == 'line'``, the default is to for the plotted line to be along the 
        dimension (x or y) that has more cells, and along x if they have the same number of cells. 
        If ``True``, this parameter inverts the direction.
    radial_bins_per_cell: float
        If ``plot_geometry == 'radius'``, this parameter chooses how many radial bins per cell are
        plotted. The bins are averaged onto the radial annuli, so this number can be greater
        than unity.
    vertical: bool
        If True, panels are stacked vertically instead of being placed next to each other 
        horizontally.

    Returns
    -------
    fig: matplotlib figure
        The figure object.
    panels: array_like
        List of axes objects.
    """
     
    nq_plot = len(q_plot)
    q_array, conv_factors, q_labels, conv_l, unit_label_l = getQuantities(sim, q_plot, 
                                        unit_l = plot_unit_l, unit_t = plot_unit_t, unit_m = plot_unit_m)
    
    if plot_geometry == 'line':
        
        if sim.ny > sim.nx:
            idir = 1
        else:
            idir = 0
        if invert_direction:
            idir = int(not idir)
        if idir == 0:
            if plot_ghost_cells:
                slc1d = slice(0, sim.nx_tot)
            else:
                slc1d = slice(sim.xlo, sim.xhi + 1)
            slc2d = (slc1d, sim.ny // 2)
            x_plot = sim.x[slc1d]
            xlabel = r'$x\ (' + unit_label_l + r')$'
        elif idir == 1:
            if plot_ghost_cells:
                slc1d = slice(0, sim.ny_tot)
            else:
                slc1d = slice(sim.ylo, sim.yhi + 1)
            slc2d = (sim.nx // 2, slc1d)
            x_plot = sim.y[slc1d]
            xlabel = r'$y\ (' + unit_label_l + r')$'
        else:
            raise Exception('Unknown direction')
        xmin = x_plot[0]
        xmax = x_plot[-1]
        q_line = q_array[(slice(None), ) + slc2d]
        
    elif plot_geometry == 'radius':
        
        if not sim.is_2d:
            raise Exception('Radial plotting geometry makes sense only for 2D simulation.')
        if (sim.nx % 2 != 0) or (sim.ny % 2 != 0):
            raise Exception('For plot type radius, both nx and ny must be multiples of two (found %d, %d)' \
                        % (sim.nx, sim.ny))
        xlabel = r'$r\ (' + unit_label_l + r')$'
        slc1d = slice(None)

        # The smaller side of the domain limits the radius to which we can plot
        xmin = 0.0
        nx_half = sim.nx // 2 + sim.nghost
        ny_half = sim.ny // 2 + sim.nghost
        x_half = (sim.xmin + sim.xmax) * 0.5
        y_half = (sim.ymin + sim.ymax) * 0.5
        if sim.nx >= sim.ny:
            xmax = 0.5 * (sim.ymax - sim.ymin)
            n_cells = sim.nx
        else:
            xmax = 0.5 * (sim.xmax - sim.xmin)
            n_cells = sim.ny
        n_cells_half = n_cells // 2
        
        # Radial bins
        n_r = int(n_cells_half * radial_bins_per_cell)
        bin_edges = np.linspace(0.0, xmax, n_r + 1)
        x_plot = 0.5 * (bin_edges[:-1] + bin_edges[1:])

        # Compute weight in concentric circles
        slc_x = slice(nx_half - n_cells_half, nx_half + n_cells_half)
        slc_y = slice(ny_half - n_cells_half, ny_half + n_cells_half)
        cell_x, cell_y = sim.xyGrid()
        cell_x = cell_x[(slc_x, slc_y)]
        cell_y = cell_y[(slc_x, slc_y)]
        circle_weight = np.zeros((n_r, n_cells, n_cells), float)
        for i in range(n_r):
            circle_weight[i] = utils.circleSquareOverlap(x_half, y_half, bin_edges[i + 1], cell_x, cell_y, sim.dx)

        # Compute weight in bin annuli and normalize them 
        bin_weight = np.zeros((n_r, n_cells, n_cells), float)
        bin_weight[0] = circle_weight[0]
        for i in range(n_r - 1):
            bin_weight[i + 1] = circle_weight[i + 1] - circle_weight[i]
        bin_norm = np.sum(bin_weight, axis = (1, 2))

        # Create a square map that we use to measure the profile, then apply bin mask and sum
        q_2d = q_array[(slice(None), slc_x, slc_y)]
        q_line = np.sum(bin_weight[None, :, :, :] * q_2d[:, None, :, :], axis = (2, 3)) / bin_norm[None, :]

    else:
        raise Exception('Unknown plot geometry, %s.' % (plot_geometry))

    # Get true solution, if available
    q_true = None
    if true_solution_func is not None:
        q_true = true_solution_func(sim, x_plot, q_plot, plot_geometry)
        if q_true is not None:
            if len(q_true) != nq_plot:
                raise Exception('Found %d quantities in true solution, expected %d (%s).' \
                        % (len(q_true), nq_plot, str(q_plot)))
            for i in range(nq_plot):
                if q_true[i] is not None:
                    if len(q_true[i]) != len(x_plot):
                        raise Exception('Found %d values in true solution, expected %d.' \
                            % (len(q_true[i]), len(x_plot)))

    # Get min/max extent of plots
    ymin = None
    ymax = None
    if range_func is not None:
        ymin, ymax, ylog = range_func(q_plot, plot_geometry)
        if (ymin is not None) and (len(ymin) != nq_plot):
            raise Exception('Found %d fields in lower limits, expected %d (%s).' % (len(ymin), nq_plot, str(q_plot)))
        if (ymax is not None) and (len(ymax) != nq_plot):
            raise Exception('Found %d fields in upper limits, expected %d (%s).' % (len(ymax), nq_plot, str(q_plot)))
        if (ylog is not None) and (len(ylog) != nq_plot):
            raise Exception('Found %d fields in log, expected %d (%s).' % (len(ylog), nq_plot, str(q_plot)))

    # Prepare figure
    panel_size = 3.0
    space_lb = 1.1
    if vertical:
        space = 0.5
        fwidth  = space_lb + panel_size + space
        fheight = space_lb + (panel_size + space) * nq_plot
        fig = plt.figure(figsize = (fwidth, fheight))
        gs = gridspec.GridSpec(nq_plot, 1)
        plt.subplots_adjust(left = space_lb / fwidth, right = 1.0 - space / fwidth,
                    bottom = space_lb / fheight, top = 1.0 - space / fheight, 
                    hspace = space / panel_size, wspace = space_lb / panel_size)
    else:
        space = 0.3
        fwidth  = space_lb + panel_size * nq_plot + space_lb * (nq_plot - 1) + space
        fheight = space_lb + panel_size + space
        fig = plt.figure(figsize = (fwidth, fheight))
        gs = gridspec.GridSpec(1, nq_plot)
        plt.subplots_adjust(left = space_lb / fwidth, right = 1.0 - space / fwidth,
                    bottom = space_lb / fheight, top = 1.0 - space / fheight, 
                    hspace = space_lb / panel_size, wspace = space_lb / panel_size)

    # Create panels
    panels = []
    for i in range(nq_plot):
        panel = fig.add_subplot(gs[i])
        panels.append(panel)
        plt.xlim(xmin * conv_l, xmax * conv_l)
        if (ymin is not None) and (ymin[i] is not None) and (ymax is not None) and (ymax[i] is not None):
            if (ylog is not None) and ylog[i]:
                if ymin[i] <= 0.0 or ymax[i] <= 0.0:
                    raise Exception('Cannot create log plot for quantity %s with zero or negative limits (%.2e, %.2e).' \
                                % (q_plot[i], ymin[i], ymax[i]))
                plt.yscale('log')
            plt.ylim(ymin[i] * conv_factors[i], ymax[i] * conv_factors[i])
        if (not vertical) or (i == nq_plot - 1):
            plt.xlabel(xlabel)
        else:
            panel.set_xticklabels([])
        plt.ylabel(q_labels[i])
        if plot_ghost_cells:
            plt.axvline(sim.xmin, color = 'gray', lw = 0.3)
            plt.axvline(sim.xmax, color = 'gray', lw = 0.3)
    
    # Plot fluid variables
    for i in range(nq_plot):
        plt.sca(panels[i])
        plt.plot(x_plot * conv_l, q_line[i, :], 
                    color = 'darkblue', label = r'$\mathrm{Solution}, t=%.2f$' % (sim.t))
        if (q_true is not None) and (q_true[i] is not None):
            plt.plot(x_plot * conv_l, q_true[i] * conv_factors[i], 
                    ls = '--', color = 'deepskyblue', label = r'$\mathrm{True\ solution}$')

    # Finalize plot
    plt.sca(panels[0])
    plt.legend(loc = 1, labelspacing = 0.1)
    
    return fig, panels

###################################################################################################

def plot2d(sim, q_plot = ['DN', 'VX', 'VY', 'PR'], 
        plot_unit_l = 'code', plot_unit_t = 'code', plot_unit_m = 'code',
        plot_ghost_cells = False, range_func = None, 
        # The following parameters are specific to 2D plotting
        cmap_func = None, panel_size = 3.0):
    """
    Plot fluid state in 2D
    
    Create a multi-panel plot of the fluid variables in 2D. The plot is created but not shown or 
    saved to a file. These operations can be completed using the returned matplotlib objects. Plots 
    can also be edited before saving via a callback function passed to the 
    :func:`~ulula.core.run.run` function.
    
    Parameters
    ----------
    sim: Simulation
        Object of type :data:`~ulula.core.simulation.Simulation`.
    q_plot: array_like
        List of quantities to plot. Quantities are identified via the short strings given in the
        :data:`~ulula.core.plots.fields` dictionary.
    plot_unit_l: str
        Length unit to be plotted (see :mod:`~ulula.physics.units` for valid units). If other 
        than ``'code'``, ``plot_unit_t`` and ``plot_unit_m`` must also be changed from code units.
    plot_unit_t: str
        Time unit to be plotted (see :mod:`~ulula.physics.units` for valid units). If other 
        than ``'code'``, ``plot_unit_l`` and ``plot_unit_m`` must also be changed from code units.
    plot_unit_m: str
        Mass unit to be plotted (see :mod:`~ulula.physics.units` for valid units). If other 
        than ``'code'``, ``plot_unit_l`` and ``plot_unit_t`` must also be changed from code units.
    plot_ghost_cells: bool
        If ``True``, ghost cells are plotted and separated from the physical domain by a gray
        frame. This option is useful for debugging.
    range_func: function
        If None, the plotting ranges are chosen automatically. Otherwise this parameter must be
        a function that can be called with the signature ``range_func(sim, q_plot, '2d')``
        and that returns three lists with the same lengths as the number of plot quantities. The 
        lists give the minimum and maximum plot extents for each fluid variable, as well as whether 
        to use a log scale (if ``True`` is returned for a given quantity). Elements in the lists can 
        be None in which case ranges are chosen automatically. The range function is typically 
        implemented within a problem setup (see :doc:`setups`).
    cmap_func: function
        If None, the default colormaps are used. Otherwise this parameter must be a function
        that can be called with the signature``cmap_func(q_plot)`` and returns a list of color maps
        of the same length as the list of plotted quantities. The cmap function is typically 
        implemented within a problem setup (see :doc:`setups`).
    panel_size: float
        Size of each plotted panel in inches.

    Returns
    -------
    fig: matplotlib figure
        The figure object.
    panels: array_like
        List of axes objects.
    """

    # Constants
    space = 0.15
    space_lb = 0.8
    cbar_width = 0.2
    
    # Compute quantities
    nq_plot = len(q_plot)
    q_array, conv_factors, q_labels, conv_l, unit_label_l = getQuantities(sim, q_plot, 
                                    unit_l = plot_unit_l, unit_t = plot_unit_t, unit_m = plot_unit_m)

    # Get x-extent
    if not sim.is_2d:
        raise Exception('Cannot plot 1D simulation in 2D.')
    if plot_ghost_cells:
        xlo = 0
        xhi = sim.nx + 2 * sim.nghost - 1
        ylo = 0
        yhi = sim.ny + 2 * sim.nghost - 1
        
        xmin = sim.x[0] - 0.5 * sim.dx
        xmax = sim.x[-1] + 0.5 * sim.dx
        ymin = sim.y[0] - 0.5 * sim.dx
        ymax = sim.y[-1] + 0.5 * sim.dx
    else:
        xlo = sim.xlo
        xhi = sim.xhi
        ylo = sim.ylo
        yhi = sim.yhi
        
        xmin = sim.xmin
        xmax = sim.xmax
        ymin = sim.ymin
        ymax = sim.ymax

    # Apply units
    xmin *= conv_l
    xmax *= conv_l
    ymin *= conv_l
    ymax *= conv_l
    
    slc_x = slice(xlo, xhi + 1)
    slc_y = slice(ylo, yhi + 1)
    xext = xmax - xmin
    yext = ymax - ymin
    
    # Prepare figure; take the larger dimension and assign that the panel size; the smaller
    # dimension follows from that.
    if xext >= yext:
        panel_w = panel_size
        panel_h = yext / xext * panel_w
    else:
        panel_h = panel_size
        panel_w = xext / yext * panel_h
    
    fwidth  = space_lb + (panel_w + space) * nq_plot
    fheight = space_lb + panel_h + space + cbar_width + space_lb
    
    fig = plt.figure(figsize = (fwidth, fheight))
    gs = gridspec.GridSpec(3, nq_plot, height_ratios = [space_lb * 0.8, cbar_width, panel_h])
    plt.subplots_adjust(left = space_lb / fwidth, right = 1.0 - space / fwidth,
                    bottom = space_lb / fheight, top = 1.0 - space / fheight, 
                    hspace = space / fheight, wspace = space / panel_w)
    
    # Create panels
    panels = []
    for i in range(nq_plot):
        panels.append([])
        for j in range(3):
            panels[i].append(fig.add_subplot(gs[j, i]))
            
            if j == 0:
                plt.axis('off')
            elif j == 1:
                pass
            else:
                plt.xlim(xmin, xmax)
                plt.ylim(ymin, ymax)
                plt.xlabel(r'$x\ (' + unit_label_l + r')$')
                if i == 0:
                    plt.ylabel(r'$y\ (' + unit_label_l + r')$')
                else:
                    plt.gca().set_yticklabels([])
    
    # Check for plot limits and colormaps specific to the setup
    vmin = None
    vmax = None
    if range_func is not None:
        vmin, vmax, vlog = range_func(q_plot, '2d')
        if (vmin is not None) and (len(vmin) != nq_plot):
            raise Exception('Found %d fields in lower limits, expected %d (%s).' % (len(vmin), nq_plot, str(q_plot)))
        if (vmax is not None) and (len(vmax) != nq_plot):
            raise Exception('Found %d fields in upper limits, expected %d (%s).' % (len(vmax), nq_plot, str(q_plot)))
        if (vlog is not None) and (len(vlog) != nq_plot):
            raise Exception('Found %d fields in log, expected %d (%s).' % (len(vlog), nq_plot, str(q_plot)))
        
    cmaps = None
    if cmap_func is not None:
        cmaps = cmap_func(q_plot)
        if (cmaps is not None) and (len(cmaps) != nq_plot):
            raise Exception('Found %d fields in colormaps, expected %d (%s).' % (len(cmaps), nq_plot, str(q_plot)))
    
    # Plot fluid variables
    for i in range(nq_plot):
        plt.sca(panels[i][2])
        data = q_array[i, slc_x, slc_y]
        data = data.T[::-1, :]
        
        if (vmin is None) or (vmin[i] is None):
            vmin_ = np.min(data)
        else:
            vmin_ = vmin[i] * conv_factors[i]
        if (vmax is None) or (vmax[i] is None):
            vmax_ = np.max(data)
        else:
            vmax_ = vmax[i] * conv_factors[i]
        if (vlog is not None) and (vlog[i] is not None):
            log_ = vlog[i]
        else:
            log_ = False
        if (cmaps is None) or (cmaps[i] is None):
            cmap = plt.get_cmap(fields[q_plot[i]]['cmap'])
        else:
            cmap = cmaps[i]
            
        # Check that limits and log make sense
        if log_:
            if (vmin_ <= 0.0) or (vmax_ <= 0.0):
                raise Exception('Cannot use negative limits with in log space (quantity %s, limits %.2e, %.2e).' \
                            % (q_plot[i], vmin_, vmax_))
            vmin_ = np.log10(vmin_)
            vmax_ = np.log10(vmax_)
            if np.min(data) <= 0.0:
                raise Exception('Cannot plot zero or negative data in field %s on log scale.' % (q_plot[i]))
            data = np.log10(data)
            label_use = r'$\log_{10}$' + q_labels[i]
        else:
            label_use = q_labels[i]
            
        norm = mpl.colors.Normalize(vmin = vmin_, vmax = vmax_)
        plt.imshow(data, extent = [xmin, xmax, ymin, ymax], interpolation = 'none', 
                cmap = cmap, norm = norm, aspect = 'equal')

        ax = panels[i][1]
        plt.sca(ax)
        cb = mpl.colorbar.ColorbarBase(ax, orientation = 'horizontal', cmap = cmap, norm = norm)
        cb.set_label(label_use, rotation = 0, labelpad = 8)
        cb.ax.xaxis.set_ticks_position('top')
        cb.ax.xaxis.set_label_position('top')
        cb.ax.xaxis.set_tick_params(pad = 5)
        
        # Plot frame around domain if plotting ghost cells
        if plot_ghost_cells:
            plt.sca(panels[i][2])
            plt.plot([sim.xmin, sim.xmax, sim.xmax, sim.xmin, sim.xmin], 
                    [sim.ymin, sim.ymin, sim.ymax, sim.ymax, sim.ymin], '-', color = 'gray')
    
    return fig, panels

###################################################################################################
