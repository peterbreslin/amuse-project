# Packages
import numpy as np
from amuse.units.constants import G
from amuse.units import units, constants


class TidalForce():

    ''' Class to update the gravitational accelerations due to tidal friction between Jupiter and
        a given moon. Tidal interactions between moons are ignored. 

        This tidal code gives the bridge system instantaneous kicks (based on position). The 
        equations are based on the Mignard weak-friction tidal model.

        Inspiration was taken from the paper, 'Tidal decay and orbit circularization in close-in
        two-planet systems' (https://doi.org/10.1111/j.1365-2966.2011.18861.x). 

        The kdt parameter absorbs the Love number --> k is the love number and dt is the constant 
        time lag. This has been obtained from the literature to be ~0.02 for the Jupiter - 
        Galilean system (https://doi.org/10.1051/0004-6361/201014337). '''


    def __init__(self, kdt=2e-2):
        self.kdt = kdt
        
    
    # Add our system of particles
    def add_particles(self, particle_set):
        self.particles = particle_set
    
    
    # Bridges to gravity code
    def get_gravity_at_point(self, eps, x, y, z):
        return self.tidal_acceleration(kdt=self.kdt) 
    

    def tidal_acceleration(self, kdt):

        ''' Note: the number of satellites (sun and moons) is needed to reshape the arrays such 
            that they can all be contracted in the correct way (eg. multiplication of vector arrays, 
            with arrays). '''

        num_sat = len(self.particles)-1
        mask = self.particles.name != 'jupiter' # exclude the force of Jupiter on itself
        
        # Initializing required constants
        M = (1|units.MJupiter).value_in(units.kg)
        G = constants.G.value_in( (units.m)**3 / (units.kg * units.s**2) )
        c = constants.c.value_in(units.m/units.s)
        
        # Satellite attributes (including sun for the stellar tides)
        m = (self.particles.mass.value_in(units.kg)[mask]).reshape((num_sat,1))
        R_sat = (self.particles.radius.value_in(units.m)[mask]).reshape((num_sat,1))
        
        # Relative positions
        r_vec = self.particles[mask].position.value_in(units.m) - \
                self.particles[~mask].position.value_in(units.m)

        # Distance between satellite and jupiter
        r = np.linalg.norm(r_vec, axis=1).reshape(num_sat,1)

        # Relative velocities 
        v_vec = self.particles[mask].velocity.value_in(units.m/units.s) - \
                self.particles[~mask].velocity.value_in(units.m/units.s)

        # Velocity (v**2 needed in f_rel)
        v = np.linalg.norm(v_vec, axis=1).reshape(num_sat,1)
        
        # Rotation angular velocity
        omega = np.cross(r_vec, v_vec) / r**2
        
        # Tidal force equation
        f = (-3 * kdt * G * M**2 * R_sat**5 / r**10) * (2 * r_vec * \
            np.sum(r_vec*v_vec, axis=1).reshape((num_sat,1)) + \
            (r**2) * (np.cross(r_vec, omega) + v_vec))
        
        # General relativity contribution
        f_rel = (G * m * M / (c**2 * r**3)) * ( ((4*G*M/r) - v**2)*r_vec + \
            4*(np.sum(r_vec*v_vec, axis=1).reshape(num_sat,1))*v_vec)

        #  The acceleration due to tidal effects (this will be added to the gravitational accel.)
        a = (M + m)*(f + f_rel) / (M * m) 

        ax = np.zeros(num_sat+1)
        ay = np.zeros(num_sat+1)
        az = np.zeros(num_sat+1)
        
        ax[mask] = a[:,0]
        ay[mask] = a[:,1]
        az[mask] = a[:,2]
        
        ax = ax | units.m/(units.s**2)
        ay = ay | units.m/(units.s**2)
        az = az | units.m/(units.s**2)
        
        return ax, ay, az