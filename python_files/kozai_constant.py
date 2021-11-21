# Packages
import numpy as np
from amuse.lab import units
import matplotlib.pyplot as plt

''' The Kozai-constant Lz should be (approximately) conserved. This function will check this by computing Lz.
    Input: list of eccentricites and inclinations obtained from the integrate_system() function
    Returns: array of Lz's for each instance for each moon, and plots!
    Example: lz = check_lz(ecc, inc) '''
    
def check_lz(moons, ecc, inc, time_range, savefig=False, figname='kozai_constant'):
    
    # Lz=sqrt(1-e**2)*cos(i)
    lz = np.zeros_like(ecc)
    for i in range(len(lz[0])):
        for j in range(len(lz[0:])):
            x = np.sqrt(1 - ecc[j][i]**2) * np.cos(inc[j][i].value_in(units.rad))
            lz[j][i] = x
    
    # Standard deviations
    sdev = []
    for i in range(len(lz[0:])):
        y = np.std(lz[i:])
        sdev.append(y)

    # Plotting
    colours = ['r', 'g', 'b', 'm']     
    plt.rcParams.update({'font.size': 20})
    
    # Sizes of subplots are annoying
    if len(lz[0:]) < 4:
        figsize=[10,8]
    else:
        figsize=[10,12]
    
    fig, ax = plt.subplots(len(lz[0:]), 1, figsize=figsize, constrained_layout=True)    
    
    for i, ax in enumerate(fig.axes):
        ax.plot(time_range.value_in(units.yr), lz[i], '-o', color=colours[i], lw=1, label=moons[i])
        ax.plot([], [], ' ', label='std = '+str(round(sdev[i],3)))
        ax.legend(fontsize=16) 
        
    plt.suptitle('Lz vs Time')
    #plt.subplots_adjust(top=0.94)
    if savefig:
        plt.savefig(figname+'.png', facecolor='w', bbox_inches='tight')
    plt.show()
                           
    return lz