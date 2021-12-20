# Packages
import numpy as np
from amuse.lab import units
import matplotlib.pyplot as plt

    
def check_lz(moons, ecc, inc, time_range, savefig=False, figname='kozai_constant'):
    
    ''' The Kozai-constant Lz should be (approximately) conserved for one moon.
        Approximate Law: Lz = sqrt(1 - e**2) * cos(i) 

        @input:
            List of moons, retrieved eccentricities, inclinations, semimajor-axes, and time range. 
            Option to save figure as a PNG if desired.

        @Output:
            Plot of the Kozai-constant for a given moon to check if this conservation law holds.

        Example:
            check_lz(moons, ecc, inc, time_range, savefig=True, figname='my_plot') '''
    

    t = time_range.value_in(units.yr)
    e = ecc[0]
    i = inc[0].value_in(units.rad)
    
    # Equation
    lz = np.sqrt(1 - np.array(e)**2) * np.cos(i)
    
    # Standard deviations
    sdev = np.std(lz)
    
    # Plotting
    plt.rcParams.update({'font.size': 25})
    
    fig, ax = plt.subplots(figsize=[14,7], tight_layout=True)    
    
    ax.set_title('Kozai-constant', pad=10)
    ax.plot(t, lz, '-o', c='tab:purple', lw=2)
    ax.plot([], [], ' ', label='std = '+str(round(sdev,5)))
    ax.set_ylabel(r'L$_{z}$', labelpad=10)
    ax.set_xlabel('time [yr]')
    ax.tick_params(direction='in', length=6, width=2, top=True, right=True)
    ax.legend(frameon=False) 
    
    if savefig:
        plt.savefig(figname+'.png', facecolor='w', bbox_inches='tight')
    
    plt.show()