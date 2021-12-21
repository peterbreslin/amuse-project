# Packages
import numpy as np
from amuse.lab import units
import matplotlib.pyplot as plt


def plot_tracks(moons, ecc, inc, sma, time_range, savefig=False, figname='evolved_tracks'):

    ''' Plotting evolutionary tracks for given moons.

        @input:
            List of moons, retrieved eccentricities, inclinations, semimajor-axes, and time range. 
            Option to save figure as a PNG if desired.

        @Output:
            Plot of the evolutionary tracks for the eccentricities, inclinations, semimajor-axes.

        Example:
            plot_tracks(moons, ecc, inc, time_range, savefig=True, figname='my_plot') '''

    
    plt.rcParams.update({'font.size': 25})
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=[25, 15], tight_layout=True, sharex=True)
    cb = ['#e41a1c', '#ff7f00', '#999999', '#377eb8']

    t = time_range.value_in(units.yr)
    inc = inc.value_in(units.deg)
    ecc = np.array(ecc)
    sma = sma.value_in(units.m)

    for i in range(len(moons)): 
        ax1.plot(t, ecc[i], color=cb[i], label=moons[i], lw=2)   
        ax2.plot(t, inc[i], color=cb[i], label=moons[i], lw=2) 
        ax3.plot(t, sma[i], color=cb[i], label=moons[i], lw=2)    
        
    ax1.set_ylabel('eccentricity', labelpad=10)
    ax2.set_ylabel('inclination [deg]', labelpad=10)
    ax3.set_ylabel('semimajor axis', labelpad=10)
    
    ax1.tick_params(direction='in', length=6, width=2, top=True, right=True)
    ax2.tick_params(direction='in', length=6, width=2, top=True, right=True)    
    ax3.tick_params(direction='in', length=6, width=2, top=True, right=True)
    
    ax1.legend()
    ax2.legend()
    ax3.legend()
  
    ax1.set_title('Model Evolution')
    ax3.set_xlabel('time [years]')

    #ax1.set_xlim([0,1000])
    #ax2.set_xlim([0,1000])
    #ax3.set_xlim([0,1000])

    if savefig:
        plt.savefig(figname+'.png', facecolor='w', bbox_inches='tight')

    plt.show()