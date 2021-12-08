print('Beginning Script')

# Packages
import h5py
from amuse.lab import units
from evolve_model import integrate_system

# Defining system parameters
moons = ['europa']
eccentricities = [0.2]
inclinations = [0]

# Evolving the system 
dt = 100
end_time = 1e4
kdt = 360
ecc, inc, sma, Etot, Ediss, model_time = integrate_system(moons, eccentricities, inclinations, 
	kdt, dt, end_time, kozai=False)

print('Model evolved, saving data')

# Saving data
filename  = 'debug_test.hdf5'
d = h5py.File(filename, 'w')

d['inc'] = inc[0].value_in(units.deg)
d['ecc'] = ecc[0]
d['sma'] = sma[0].value_in(units.m)
d['etot'] = Etot
d['ediss'] = Ediss
d['time'] = model_time.value_in(units.yr)

d.close()
