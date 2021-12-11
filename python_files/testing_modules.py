print('Beginning Script')

# Packages
from kozai_constant import check_lz
from evolve_model import integrate_system
from plotting import plot_tracks, plot_energy_evolution

# Defining system parameters
moons = ['io', 'europa', 'ganymede', 'callisto']
eccentricities = [0.3, 0.4, 0.5, 0.6]
inclinations = [60, 70, 80, 90]

# Evolving the system 
dt = 10
end_time = 1000
kdt = 360
ecc, inc, sma, model_time = integrate_system(moons, eccentricities, inclinations, 
	kdt, dt, end_time, kozai=True)

print('Model fully evolved')

# Evolved tracks
plot_tracks(moons, ecc, inc, sma, model_time)

# Energy evolution
#plot_energy_evolution(moons, Etot, model_time)

# Kozai-constant
lz = check_lz(moons, ecc, inc, model_time)

