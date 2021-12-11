# Packages
import numpy as np
from amuse.lab import Particles
from amuse.units.constants import G
from amuse.units import units, constants
from amuse.ext.orbital_elements import new_binary_from_orbital_elements


def make_moon_system(moons, eccentricities, inclinations, kozai=True, *args):

    ''' Function to create a particle system of the Galileann moon(s) with Jupiter and the Sun.
        
    @Input: 
        list of Galileann Moon names in string format (any combination of: io, europa, ganymede, 
        callisto), list of eccentricities, list of inclinations (dimensionless).
               
    @Returns: 
        Particle system of the given moon set with the Sun and Jupiter.
        
    @Example: 
        system = make_moon_system(moons=['io', 'europa'], eccentricities=[0.4, 0.6], 
        inclinations=[50, 60]) '''
  

    # Assigning our variables
    x = zip(eccentricities, inclinations)
    y = list(x)
    z = {}
    for i in range(len(moons)):
        z[moons[i]] = y[i]   
    
    
    # Initialising Sun and Jupiter
    Msun = 1.0|units.MSun
    Mjup = 1.0|units.MJupiter
    rSun = 696340|units.km
    rJup = 69911|units.km
    a_jup = 5.2|units.au
    e_jup = 0.0
    
    system = new_binary_from_orbital_elements(Msun, Mjup, a_jup, e_jup, G=constants.G)
    system[0].name = 'sun'
    system[1].name = 'jupiter'
    jupiter = system[system.name=='jupiter']
    jupiter.semimajor_axis = a_jup
    jupiter.radius = rJup
    sun = system[system.name=='sun']
    sun.radius = rSun
    
    if kozai != True:
        system.remove_particle(system[0]) #removing the Sun
        system.move_to_center()
    
    
    # Function to automate addition of particles
    def add_particle(particle, a, e, inc, m, r):
        
        binary = new_binary_from_orbital_elements(jupiter.mass, m, a, eccentricity=e, 
            inclination=inc, G=constants.G)
         
        system.add_particle(binary[1].as_set()) 
        system[-1].name = particle
        moon = system[system.name==particle] 
        
        moon.semimajor_axis = a
        moon.eccentricity = e
        moon.inclination = inc
        moon.radius = r
        moon.position = binary[1].position + jupiter.position
        moon.velocity = binary[1].velocity + jupiter.velocity
        
        system.move_to_center()
    
    
    # Add moons based on input
    if 'io' in moons:
        a = 421800|units.km
        e = z['io'][0]
        inc = z['io'][1]|units.deg
        m = 8.93E22|units.kg
        r = 1821.6|units.km
        add_particle('io', a, e, inc, m, r) 
    
    if 'europa' in moons:
        a = 671100|units.km
        e = z['europa'][0]
        inc = z['europa'][1]|units.deg
        m = 4.80E22|units.kg
        r = 1560.8|units.km
        add_particle('europa', a, e, inc, m, r)  

    if 'ganymede' in moons:
        a = 1070400|units.km
        e = z['ganymede'][0]
        inc = z['ganymede'][1]|units.deg
        m = 1.48E23|units.kg
        r = 2634.1|units.km
        add_particle('ganymede', a, e, inc, m, r)   
        
    if 'callisto' in moons:
        a = 1882700|units.km
        e = z['callisto'][0]
        inc = z['callisto'][1]|units.deg
        m = 1.08E23|units.kg
        r = 2410.3|units.km
        add_particle('callisto', a, e, inc, m, r)  
        
        
    print('Particle system created for: '+ str(system.name))
    return system