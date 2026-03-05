import os
import sys
import re
sys.path.append('')
# global imports
import numpy as np
# private imports from sys.path
from core.evolve import evolve
#private imports for earth system
from earth_sys.timing_no_enso import timing
from earth_sys.functions_earth_system_no_enso import global_functions
from earth_sys.earth_no_enso import earth_system

def run_example_simulation(earth_system_pass, GMT_series, coupling_strength=0.3, kk=[1.,0.,-1.]):
    
    """
    Run one example simulation for a single GMT_series and one coupling strength / link scenario.
    Returns time vector and system states.
    """
    duration = len(GMT_series)
    
    output = []
    initial_state = [-1, -1, -1, -1]
    
    for t in range(duration):
        effective_GMT = GMT_series[t]
        net = earth_system_pass.earth_network(effective_GMT, coupling_strength, kk[0], kk[1], kk[2])
        ev = evolve(net, initial_state)
        
        # timestep and integration
        timestep = 0.1
        t_end = 1.0
        ev.integrate(timestep, t_end)
        
        state = ev.get_timeseries()[1][-1]
        output.append([t, *state])
        initial_state = state  # for next step
    
    data = np.array(output)
    time = data[:,0]
    state_gis = data[:,1]
    state_thc = data[:,2]
    state_wais = data[:,3]
    state_amaz = data[:,4]
    
    # export values if needed
    return time, state_gis, state_thc, state_wais, state_amaz
