print('Beginning Script')

# Packages
import h5py
from amuse.lab import units
from evolve_model import integrate_system

# Defining system parameters
moons = ['io', 'europa', 'ganymede', 'callisto']
eccentricities = [0.2, 0.2, 0.2, 0.2]
inclinations = [50, 55, 60, 65]

# Evolving the system 
dt = 10
end_time = 1e6
kdt = 360
ecc, inc, sma, model_time = integrate_system(moons, eccentricities, inclinations, 
	kdt, dt, end_time, kozai=True)

print('Model evolved, saving data')

# Saving data
filename  = 'full_system.hdf5'
d = h5py.File(filename, 'w')

labels = ['io', 'eu', 'ga', 'ca']

for i in range(4):
	g = d.create_group(labels[i])
	g['inc'] = inc[i].value_in(units.deg)
	g['ecc'] = ecc[i]
	g['sma'] = sma[i].value_in(units.m)
	g['time'] = model_time.value_in(units.yr)

d.close()
