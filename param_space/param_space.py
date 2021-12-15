print('Beginning Script')

# Packages
import h5py
import numpy as np
from amuse.lab import units
from evolve_model import integrate_system

# Defining system parameters
moons = ['io', 'europa', 'ganymede', 'callisto']

filename  = 'p_space.hdf5'
results = h5py.File(filename, 'w')

dt = 1
end_time = 1000
kdt = 360

for k in range(10):
	print(k)
	recc = []
	rinc = []

	for i in range(4):
		re = np.random.randint(40, 140)
		ri = round(np.random.uniform(0.1, 0.9), 1)
		recc.append(re)
		rinc.append(ri)

	g1 = results.create_group(str(k))
	g2 = g1.create_group('init') 
	g2['e'] = recc
	g2['i'] = rinc

	ecc, inc, sma, model_time = integrate_system(moons, recc, rinc, 
		kdt, dt, end_time, kozai=True)

	# Time for ease
	g2['t'] = model_time.value_in(units.yr)

	labels = ['io', 'eu', 'ga', 'ca']

	for i in range(4):
		g3 = g1.create_group(labels[i])
		g3['inc'] = inc[i].value_in(units.deg)
		g3['ecc'] = ecc[i]
		g3['sma'] = sma[i].value_in(units.m)

	print('')

results.close()
