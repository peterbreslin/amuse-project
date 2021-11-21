# Packages
import numpy as np
from amuse.units.constants import G
from amuse.units import units, constants


# Tidal forces
class TidalForce():
    def __init__(self, alpha=0.1):
        self.alpha=alpha
        
    
    def add_particles(self, particle_set):
        self.particles = particle_set
    
    
    def tidal_acceleration(self, k, alpha):
        R = (1|units.RJupiter).value_in(units.m) 
        M = (1|units.MJupiter).value_in(units.kg)
        G = constants.G.value_in( (units.m)**3 / (units.kg * units.s**2) )
        r = np.sqrt(np.sum(np.square(self.particles.position.value_in(units.m) - \
                                     self.particles[1].position.value_in(units.m)), axis=1))
        
        abs_vel = np.sqrt(np.sum(np.square(self.particles.velocity.value_in(units.m*units.s**-1)), 
        	axis=1))
        abs_acc = np.zeros(len(self.particles))
        mask = np.arange(len(self.particles)) != 1
        abs_acc[mask] = -9*k*G*self.particles.mass[mask].value_in(units.kg)*(R**5)*\
        np.sin(2*alpha)/(4*r[mask]**7)
        abs_acc = abs_acc * 1|units.m*units.s**-2
                
        ax = abs_acc*(self.particles.vx.value_in(units.m*units.s**-1)/abs_vel)
        ay = abs_acc*(self.particles.vy.value_in(units.m*units.s**-1)/abs_vel)
        az = abs_acc*(self.particles.vz.value_in(units.m*units.s**-1)/abs_vel)
        
        return ax, ay, az
    
    
    def get_gravity_at_point(self, eps, x, y, z):
        return self.tidal_acceleration(k=0.565, alpha=self.alpha) #k from literature, alpha guess
    

def energy_dissipation(system, k=0.565, alpha=0.1):
    """ Calculates the total energy dissipation due to the tidal force for a particle system. The 
    	second particle in the particle set is the particle that exerts the tidal force. """

    # Defining some constants
    R = (1|units.RJupiter).value_in(units.m) #radius of Jupiter
    M = (1|units.MJupiter).value_in(units.kg)
    G = constants.G.value_in( (units.m)**3 / (units.kg * units.s**2) )
    
    # Getting some parameters/values from the particle set
    m = system.mass.value_in(units.kg)
    r = np.sqrt(np.sum(np.square(system.position.value_in(units.m) - \
                                 system[1].position.value_in(units.m)), axis=1))
    
    # To exclude the force of Jupiter on itself
    mask = np.arange(len(system)) != 1
    
    # The energy dissipation
    dE_dt = -9*k*G**(3/2)*M**(1/2)*m[mask]**2*R**5*np.sin(2*alpha)/(2*r[mask]**(15/2))
   
    return np.sum(dE_dt) * 1|units.J/units.s


def get_energies(system, timestep, k=0.565, alpha=0.1):
    """ Calculates the total energy of the system, along with the energy dissipation. """

    # Getting the kinetic and potential energy from the particle system
    E_kin = system.kinetic_energy()
    E_pot = system.potential_energy()
    E_tot = E_kin + E_pot
    
    # Getting the energy dissipation
    dE_dt = energy_dissipation(system)

    # Getting the total dissipated energy in the following timestep
    dE = dE_dt*timestep
    
    return E_tot, dE