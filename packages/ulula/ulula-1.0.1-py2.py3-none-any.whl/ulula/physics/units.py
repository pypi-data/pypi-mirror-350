###################################################################################################
#
# This file is part of the ULULA code.
#
# (c) Benedikt Diemer, University of Maryland
#
###################################################################################################

units_l = {}
"""
List of length units that can be used in the plotting functions.
"""

units_l['nm']   = {'in_cgs': 1E-7,              'label': r'{\rm nm}'}
units_l['mum']  = {'in_cgs': 1E-4,              'label': r'{\rm \mu m}'}
units_l['mm']   = {'in_cgs': 1E-1,              'label': r'{\rm mm}'}
units_l['cm']   = {'in_cgs': 1.0,               'label': r'{\rm cm}'}
units_l['m']    = {'in_cgs': 1E2,               'label': r'{\rm m}'}
units_l['km']   = {'in_cgs': 1E5,               'label': r'{\rm km}'}
units_l['au']   = {'in_cgs': 1.495978707E13,    'label': r'{\rm AU}'}
units_l['pc']   = {'in_cgs': 3.08567758149E18,  'label': r'{\rm pc}'}
units_l['kpc']  = {'in_cgs': 3.08567758149E21,  'label': r'{\rm kpc}'}
units_l['Mpc']  = {'in_cgs': 3.08567758149E24,  'label': r'{\rm Mpc}'}
units_l['Gpc']  = {'in_cgs': 3.08567758149E27,  'label': r'{\rm Gpc}'}

units_t = {}
"""
List of time units that can be used in the plotting functions.
"""

units_t['ns']   = {'in_cgs': 1E-9,              'label': r'{\rm ns}'}
units_t['mus']  = {'in_cgs': 1E-6,              'label': r'{\rm \mu s}'}
units_t['ms']   = {'in_cgs': 1E-3,              'label': r'{\rm ms}'}
units_t['s']    = {'in_cgs': 1.0,               'label': r'{\rm s}'}
units_t['min']  = {'in_cgs': 60.0,              'label': r'{\rm min}'}
units_t['hr']   = {'in_cgs': 3600.0,            'label': r'{\rm hr}'}
units_t['yr']   = {'in_cgs': 3.15569252E7,      'label': r'{\rm yr}'}
units_t['kyr']  = {'in_cgs': 3.15569252E10,     'label': r'{\rm kyr}'}
units_t['Myr']  = {'in_cgs': 3.15569252E13,     'label': r'{\rm Myr}'}
units_t['Gyr']  = {'in_cgs': 3.15569252E16,     'label': r'{\rm Gyr}'}

units_m = {}
"""
List of mass units that can be used in the plotting functions.
"""

units_m['u']    = {'in_cgs': 1.66054E-24,       'label': r'{\rm u}'}
units_m['mp']   = {'in_cgs': 1.672621898E-24,   'label': r'm_{\rm p}'}
units_m['ng']   = {'in_cgs': 1E-9,              'label': r'{\rm ng}'}
units_m['mug']  = {'in_cgs': 1E-6,              'label': r'{\rm \mu g}'}
units_m['mg']   = {'in_cgs': 1E-3,              'label': r'{\rm mg}'}
units_m['g']    = {'in_cgs': 1.0,               'label': r'{\rm g}'}
units_m['kg']   = {'in_cgs': 1E3,               'label': r'{\rm kg}'}
units_m['t']    = {'in_cgs': 1E6,               'label': r'{\rm t}'}
units_m['Mear'] = {'in_cgs': 5.972E27,          'label': r'M_{\oplus}'}
units_m['Msun'] = {'in_cgs': 1.988475415338E33, 'label': r'M_{\odot}'}
