print('Beginning Script')

# Packages
from kozai_constant import check_lz
from evolve_model import integrate_system
from plotting import plot_tracks

# Defining system parameters
moons = ['ganymede']
eccentricities = [0.3]
inclinations = [80]

# Evolving the system 
dt = 10
end_time = 1000
kdt = 360
ecc, inc, sma, model_time = integrate_system(moons, eccentricities, inclinations,
	dt, end_time, kdt, kozai=True)

# Evolved tracks
plot_tracks(moons, ecc, inc, sma, model_time)

# Kozai-constant
check_lz(moons, ecc, inc, model_time)