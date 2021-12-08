# Packages
import time
import numpy as np
import tidal_force as tf 
from amuse.lab import units
from amuse.couple import bridge
from set_up import make_moon_system
from amuse.units.constants import G
from amuse.units import units, constants
from amuse.lab import Huayno, nbody_system
from amuse.ext.orbital_elements import get_orbital_elements_from_binary


def integrate_system(moons, eccentricities, inclinations, kdt, dt, end_time, kozai=True):

    ''' Function to integrate the system over time using a gravity code.

    @Input: 
        list of Galileann Moon names in string format (any combination (but in order!) of: io, 
        europa, ganymede, callisto), eccentricities, inclinations, kdt, integration time step and
        end time.

    @Returns: 
        list of evolved eccentrities, inclinations, semimajor-axis values, total eneries, 
        energy dissipation, and  the time range at time step intervals.

    @Example: 
        ecc, inc, sma, Etot, Ediss, time_range = integrate_system(moons=['io'], 
        eccentricities=[0.3], inclinations=[50], 10|units.yr, 1000|units.yr) '''
        
    
    # Checking how long code takes to run
    start_time = time.time()
    
    # Getting system
    system = make_moon_system(moons, eccentricities, inclinations, kozai=kozai)
    
    # Converting Nbody
    converter = nbody_system.nbody_to_si(system.mass.sum(), system[1].position.length())
    
    # Gravity code
    gravity = Huayno(converter)
    gravity.particles.add_particles(system)
    
    # Eccentricities
    e_io = []
    e_eu = []
    e_ga = []
    e_ca = []
    
    # Inclinations
    i_io = [] | units.deg
    i_eu = [] | units.deg
    i_ga = [] | units.deg
    i_ca = [] | units.deg
    
    #Semimajor axes 
    a_io = [] | units.m
    a_eu = [] | units.m
    a_ga = [] | units.m
    a_ca = [] | units.m

    # Tidal force
    tides = tf.TidalForce(kdt=kdt)
    tides.add_particles(system)
    
    # Bridge for tidal effects
    our_bridge = bridge.Bridge(use_threading=False)    
    our_bridge.add_system(gravity, (tides,))
    
    # Channels
    channel_grav = gravity.particles.new_channel_to(system)
    channel_tf = tides.particles.new_channel_to(system)
    
    # Running gravity code
    dt = dt|units.yr
    end_time = end_time|units.yr
    model_time = np.arange(0, end_time.value_in(units.yr), dt.value_in(units.yr)) * 1|units.yr
    
    for tstep in model_time:
        
        if 'io' in moons:
            orbit_io = get_orbital_elements_from_binary(
                system[(system.name=='jupiter')|(system.name=='io')], G=constants.G)
            
        if 'europa' in moons:
            orbit_eu = get_orbital_elements_from_binary(
                system[(system.name=='jupiter')|(system.name=='europa')], G=constants.G)
            
        if 'ganymede' in moons:
            orbit_ga = get_orbital_elements_from_binary(
                system[(system.name=='jupiter')|(system.name=='ganymede')], G=constants.G)
            
        if 'callisto' in moons:
            orbit_ca = get_orbital_elements_from_binary(
                system[(system.name=='jupiter')|(system.name=='callisto')], G=constants.G)
        
        
        our_bridge.evolve_model(tstep)
        channel_grav.copy()
        channel_tf.copy()
        
        
        if 'io' in moons:
            a_io.append(orbit_io[2])
            e_io.append(orbit_io[3])
            i_io.append(orbit_io[5])
            
        
        if 'europa' in moons:
            a_eu.append(orbit_eu[2])
            e_eu.append(orbit_eu[3])
            i_eu.append(orbit_eu[5])
            
        
        if 'ganymede' in moons:
            a_ga.append(orbit_ga[2])
            e_ga.append(orbit_ga[3])
            i_ga.append(orbit_ga[5])
            
        
        if 'callisto' in moons:
            a_ca.append(orbit_ca[2])
            e_ca.append(orbit_ca[3])
            i_ca.append(orbit_ca[5])
        
        
    our_bridge.stop()
    
    
    ecc = []
    inc = [] | units.deg
    sma = [] | units.m
    
    if 'io' in moons:
        ecc.append(e_io)
        inc.append(i_io)
        sma.append(a_io)
        
    if 'europa' in moons:
        ecc.append(e_eu)
        inc.append(i_eu)
        sma.append(a_eu)
        
    if 'ganymede' in moons:
        ecc.append(e_ga)
        inc.append(i_ga)
        sma.append(a_ga)
        
    if 'callisto' in moons:
        ecc.append(e_ca)
        inc.append(i_ca)
        sma.append(a_ca)
        
    
    # Printing runtime
    print('Runtime: %s seconds' % (time.time() - start_time))
    
    return ecc, inc, sma, model_time