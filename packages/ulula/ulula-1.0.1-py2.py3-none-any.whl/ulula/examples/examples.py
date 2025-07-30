###################################################################################################
#
# This file is part of the ULULA code.
#
# (c) Benedikt Diemer, University of Maryland
#
###################################################################################################

import matplotlib.pyplot as plt

import ulula.core.simulation as ulula_sim
import ulula.core.run as ulula_run

import ulula.setups.advection_1d as setup_advection_1d
import ulula.setups.advection_2d as setup_advection_2d
import ulula.setups.atmosphere as setup_atmosphere
import ulula.setups.cloud_crushing as setup_cloud_crushing
import ulula.setups.freefall as setup_freefall
import ulula.setups.gresho_vortex as setup_gresho_vortex
import ulula.setups.jeans_instability as setup_jeans_instability
import ulula.setups.kelvin_helmholtz as setup_kelvin_helmholtz
import ulula.setups.keplerian_disk as setup_keplerian_disk
import ulula.setups.merger as setup_merger
import ulula.setups.rayleigh_taylor as setup_rayleigh_taylor
import ulula.setups.sedov_taylor as setup_sedov_taylor
import ulula.setups.shocktube as setup_shocktube
import ulula.setups.soundwave as setup_soundwave
import ulula.setups.tidal_disruption as setup_tidal_disruption

###################################################################################################

def main():
    
    # ---------------------------------------------------------------------------------------------
    # 1D setups
    # ---------------------------------------------------------------------------------------------

    #runAdvection1D()
    
    #runSoundwave()
    
    #runShocktube()
    
    #runFreefall()

    #runAtmosphere()
    
    #runJeansInstability()

    # ---------------------------------------------------------------------------------------------
    # 2D setups
    # ---------------------------------------------------------------------------------------------
    
    #runAdvection2D()
    
    #runKelvinHelmholtz(movie = False)

    #runCloudCrushing()
    
    #runSedovTaylor()
    
    #runGreshoVortex()

    #runRayleighTaylor()
    
    #runTidalDisruption()

    #runKeplerianDisk()

    #runMerger(movie = False)
    
    return

###################################################################################################

def runAdvection1D():
    """
    Run the 1D advection test setup
    
    We run the advection test with different numerical algorithms. When using Euler (first-order) 
    time integration, the test may be unstable. We use a callback function to add labels to the 
    plots before they are saved.
    """

    def plotCallBackFunc(sim, fig, panels, plot_type):

        label = r'$'
        if alg_spatial == 'const':
            label += r'\mathrm{Constant}'
        elif alg_spatial == 'minmod':
            label += r'\mathrm{MinMod}'
        elif alg_spatial == 'mc':
            label += r'\mathrm{MC}'

        if alg_stepping == 'euler':
            label += r'+\mathrm{Euler}'
        else:
            label += r'+\mathrm{Hancock}'

        if alg_riemann == 'hll':
            label += r'+\mathrm{HLL}'
        elif alg_riemann == 'hllc':
            label += r'+\mathrm{HLLC}'
        label += r'$'
        ax = panels[0]
        plt.sca(ax)
        plt.text(0.04, 0.9, label, transform = ax.transAxes, fontsize = 16)
        ax.get_legend().remove()
        
        return

    setup = setup_advection_1d.SetupAdvection1D(shape = 'tophat')
    kwargs = dict(nx = 100, tmax = 1.1, plot_time = 1.1, q_plot = ['DN'], plot_ics = False, 
                  print_step = 1000, plot_callback_func = plotCallBackFunc)

    for alg_stepping in ['euler', 'hancock']:
        for alg_spatial in ['const', 'minmod', 'mc']:
            for alg_riemann in ['hll', 'hllc']:
                if alg_spatial == 'const':
                    alg_recon = 'const'
                    alg_lim = 'mc'
                    
                else:
                    alg_recon = 'linear'
                    alg_lim = alg_spatial
                suffix = '%s_%s_%s' % (alg_spatial, alg_stepping, alg_riemann)
                print(suffix)
                hs = ulula_sim.HydroScheme(time_integration = alg_stepping, 
                                           reconstruction = alg_recon, 
                                           limiter = alg_lim,
                                           riemann = alg_riemann)
                try:
                    ulula_run.run(setup, hydro_scheme = hs, plot_suffix = '_' + suffix, **kwargs)
                except Exception:
                    print('Failed.')

    return

###################################################################################################

def runSoundwave():
    """
    Run the sound wave setup
    """

    setup = setup_soundwave.SetupSoundwave(eos_mode = 'ideal', amplitude = 0.01)
    ulula_run.run(setup, nx = 300, tmax = 4.0, max_steps = 10000, plot_time = 0.5,
                q_plot = ['DN', 'VX'], plot_unit_l = 'm', plot_unit_t = 's', plot_unit_m = 'kg')
    
    return

###################################################################################################

def runShocktube():
    """
    Run the shock tube setup

    The function creates outputs for piecewise-constant states and piecewise-linear reconstruction.
    """

    setup = setup_shocktube.SetupShocktube()
    kwargs = dict(tmax = 0.2, nx = 100, plot_time = 0.2, q_plot = ['DN', 'VX', 'PR'], plot_ics = False)
    
    hs = ulula_sim.HydroScheme(reconstruction = 'const')
    ulula_run.run(setup, hydro_scheme = hs, plot_suffix = '_const', **kwargs)

    hs = ulula_sim.HydroScheme(limiter = 'vanleer')
    ulula_run.run(setup, hydro_scheme = hs, plot_suffix = '_linear_vl', **kwargs)

    hs = ulula_sim.HydroScheme(limiter = 'mc')
    ulula_run.run(setup, hydro_scheme = hs, plot_suffix = '_linear_mc', **kwargs)

    hs = ulula_sim.HydroScheme(limiter = 'vanleer', riemann = 'hllc')
    ulula_run.run(setup, hydro_scheme = hs, plot_suffix = '_linear_vl_hllc', **kwargs)
    
    return

###################################################################################################

def runFreefall():
    """
    Run the freefall setup
    """

    setup = setup_freefall.SetupFreefall()
    ulula_run.run(setup, nx = 300, tmax = 1.2, print_step = 100, plot_step = None, plot_time = 0.1, 
                q_plot = ['DN', 'VX'])

    return

###################################################################################################

def runAtmosphere():
    """
    Run the atmosphere setup
    
    In its default mode, this setup uses an isothermal equation of state, which means we cannot use
    the default HLLC Riemann solver.
    """

    setup = setup_atmosphere.SetupAtmosphere(eos_mode = 'isothermal')
    hs = ulula_sim.HydroScheme(riemann = 'hll')
    ulula_run.run(setup, hydro_scheme = hs,
                nx = 200, tmax = 10.0, print_step = 10000, 
                plot_step = None, plot_time = 0.5, q_plot = ['DN', 'VX', 'TK'],
                plot_unit_l = 'km', plot_unit_t = 'hr', plot_unit_m = 't')
    
    return

###################################################################################################

def runJeansInstability():
    """
    Run the Jeans instability setup

    This setup uses an isothermal equation of state, which means we cannot use the default HLLC 
    Riemann solver.
    """

    setup = setup_jeans_instability.SetupJeansInstability()
    hs = ulula_sim.HydroScheme(riemann = 'hll')
    ulula_run.run(setup, hydro_scheme = hs,
                  tmax = 1.0, nx = 100, q_plot = ['DN', 'PR', 'GP', 'GX'], plot_time = 0.1)
    
    return

###################################################################################################

def runAdvection2D():
    """
    Run the 2D advection test setup
    
    We run the advection test with different numerical algorithms. When using the MC limiter with 
    an Euler (first-order) time integration, the test fails spectacularly. We use a callback 
    function to add labels to the plots before they are saved.
    """

    def plotCallBackFunc(sim, fig, panels, plot_type):

        label = r'$'
        if alg_spatial == 'const':
            label += r'\mathrm{Constant}'
        elif alg_spatial == 'minmod':
            label += r'\mathrm{MinMod}'
        elif alg_spatial == 'mc':
            label += r'\mathrm{MC}'

        if alg_stepping == 'euler':
            label += r'+\mathrm{Euler}'
        else:
            label += r'+\mathrm{Hancock}'

        if alg_riemann == 'hll':
            label += r'+\mathrm{HLL}'
        elif alg_riemann == 'hllc':
            label += r'+\mathrm{HLLC}'
        label += r'$'
        plt.sca(panels[0][2])
        plt.text(0.04, 0.9, label, transform = panels[0][2].transAxes, fontsize = 16, color = 'w')
        
        return

    setup = setup_advection_2d.SetupAdvection2D()
    kwargs = dict(nx = 100, tmax = 2.3, plot_time = 2.3, q_plot = ['DN'], plot_ics = False, 
                  print_step = 1000, plot_callback_func = plotCallBackFunc)

    for alg_stepping in ['euler', 'hancock']:
        for alg_spatial in ['const', 'minmod', 'mc']:
            for alg_riemann in ['hll', 'hllc']:
                if alg_spatial == 'const':
                    alg_recon = 'const'
                    alg_lim = 'mc'
                    
                else:
                    alg_recon = 'linear'
                    alg_lim = alg_spatial
                suffix = '%s_%s_%s' % (alg_spatial, alg_stepping, alg_riemann)
                print(suffix)
                hs = ulula_sim.HydroScheme(time_integration = alg_stepping, 
                                           reconstruction = alg_recon, 
                                           limiter = alg_lim,
                                           riemann = alg_riemann)
                try:
                    ulula_run.run(setup, hydro_scheme = hs, plot_suffix = '_' + suffix, **kwargs)
                except Exception:
                    print('Failed.')

    return

###################################################################################################

def runKelvinHelmholtz(movie = False):
    """
    Run the Kelvin-Helmholtz setup

    This function demonstrates how to make movies with Ulula. By passing the ``movie`` parameter,
    the function outputs frames at a user-defined rate and combines them into a movie at the end
    of the simulation.
    
    Parameters
    ----------
    movie: bool
        Whether to produce plots or a movie.
    """
    
    setup = setup_kelvin_helmholtz.SetupKelvinHelmholtz(n_waves = 1)

    if movie:
        kwargs = dict(tmax = 4.0, movie = True, movie_length = 20.0, plot_ics = False)
    else:
        kwargs = dict(tmax = 3.0, plot_time = 1.0)

    ulula_run.run(setup, nx = 200, q_plot = ['DN'], **kwargs)

    return

###################################################################################################

def runCloudCrushing():
    """
    Run the cloud crushing setup
    """

    setup = setup_cloud_crushing.SetupCloudCrushing()
    ulula_run.run(setup, tmax = 14.0, nx = 300, q_plot = ['DN', 'VX'], plot_time = 1.0)

    return

###################################################################################################

def runSedovTaylor():
    """
    Run the Sedov-Taylor explosion setup
    
    This function demonstrates a style of 1D plotting where the solution is averaged in 
    radial bins.
    """

    setup = setup_sedov_taylor.SetupSedovTaylor()
    ulula_run.run(setup, tmax = 0.02, nx = 200, q_plot = ['DN', 'PR', 'VT'], plot_step = 1000, 
                plot_ics = False, plot_1d = True, plot_geometry = 'radius')

    return

###################################################################################################

def runGreshoVortex():
    """
    Run the Gresho vortex setup
    """

    setup = setup_gresho_vortex.SetupGreshoVortex()
    ulula_run.run(setup, nx = 200, tmax = 6.0, plot_time = 2.0, plot_step = None, print_step = 100, 
                plot_ghost_cells = False, save_plots = True, q_plot = ['DN', 'PR', 'VR', 'VA'],
                plot_1d = True, plot_2d = True, plot_geometry = 'radius')

    return

###################################################################################################

def runRayleighTaylor():
    """
    Run the Rayleigh-Taylor setup
    """

    setup = setup_rayleigh_taylor.SetupRayleighTaylor()
    ulula_run.run(setup, nx = 80, tmax = 6.0, print_step = 100, plot_time = 0.5, q_plot = ['DN', 'VY'])

    return

###################################################################################################

def runTidalDisruption():
    """
    Run the tidal disruption setup
    """

    setup = setup_tidal_disruption.SetupTidalDisruption()
    ulula_run.run(setup, nx = 120, tmax = 3.0, print_step = 100, plot_step = None, plot_time = 0.2, 
                q_plot = ['DN', 'GP'])

    return

###################################################################################################

def runKeplerianDisk():
    """
    Run the Keplerian disk setup
    """

    setup = setup_keplerian_disk.SetupKeplerianDisk()
    hs = ulula_sim.HydroScheme(limiter = 'vanleer', cfl = 0.8)
    ulula_run.run(setup, hydro_scheme = hs,
                nx = 150, tmax = 3.0, plot_time = 0.5, plot_step = None, print_step = 100, 
                q_plot = ['DN', 'PR', 'VR', 'VA', 'GP'], plot_1d = True, plot_2d = True, 
                plot_geometry = 'radius')

    return

###################################################################################################

def runMerger(movie = False):
    """
    Run the merger disk setup
    
    Parameters
    ----------
    movie: bool
        Whether to produce plots or a movie.
    """
    
    if movie:
        kwargs = dict(tmax = 20.0, nx = 100, plot_time = None, movie = True, movie_length = 30.0)
    else:
        kwargs = dict(tmax = 10.0, nx = 200, plot_time = 0.5)

    setup = setup_merger.SetupMerger()
    ulula_run.run(setup, q_plot = ['DN', 'GP', 'GX', 'GY'], print_step = 500, **kwargs)
    
    return

###################################################################################################
# Trigger
###################################################################################################

if __name__ == "__main__":
    main()
