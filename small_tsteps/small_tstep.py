print('Beginning Script')

# Packages
import h5py
from amuse.lab import units
from evolve_model import integrate_system

# Defining system parameters
moons = ['io']
eccentricities = [0.2]
inclinations = [0]

# Evolving the system 
dt = 10
end_time = 1e3
kdt = 2e-2
ecc, inc, sma, model_time = integrate_system(moons, eccentricities, inclinations, 
	kdt, dt, end_time, kozai=False)

print('Model evolved, saving data')

# Saving data
filename  = 'small_tstep.hdf5'
d = h5py.File(filename, 'w')

d['ecc'] = ecc[0]
d['sma'] = sma[0].value_in(units.m)
d['time'] = model_time.value_in(units.yr)

d.close()
