# Packages
from evolve_model import integrate_system


def main():

	""" This Python script gives an example of how to use our code and illustrates a sample of the 
		results. 

		When this file is executed the user will be prompted to input an integer number of moons
		to simulate ranging from 1, 2, 3, or 4. """


	# Defining system parameters based on user input for the moons
	while True:
		try:
			selection = input('Please choose how many moons to simulate (input 1, 2, 3, or 4): ')

			if selection in ['1']:
				moons = ['io']
				ecc = [0.3]
				inc = [70]
				dt = 1
				end_time = 101
				break;

			if selection in ['2']:
				moons = ['io', 'europa']
				ecc = [0.2, 0.3]
				inc = [80, 70]
				dt = 1
				end_time = 101
				break;	

			if selection in ['2']:
				moons = ['io', 'europa', 'ganymede']
				ecc = [0.2, 0.3, 0.4]
				inc = [80, 70, 60]
				dt = 1
				end_time = 101
				break;		

			if selection in ['4']:
				moons = ['io', 'europa', 'ganymede', 'callisto']
				ecc = [0.2, 0.3, 0.4, 0.5]
				inc = [80, 70, 60, 50]
				dt = 1
				end_time = 101
				break;

			else:
				print('Input must be an integer number from the range [1, 2, 3, 4]')

		except:
			continue


	# Evolving the system 
	kdt = 360
	e, i, a, model_time = integrate_system(moons, ecc, inc, dt, end_time, kdt, kozai=True)

	# Evolved tracks
	from plotting import plot_tracks
	print('Plotting the evolutionary tracks of the eccentricities, inclinations and semimajor-axes')
	plot_tracks(moons, e, i, a, model_time)

	# Kozai-constant
	if selection in ['1']:
		from kozai_constant import check_lz
		print('Plotting the Kozai-constant')
		check_lz(moons, e, i, model_time)


if __name__ == "__main__":
    main()