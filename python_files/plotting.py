# Packages
import numpy as np
from amuse.lab import units
import matplotlib.pyplot as plt


def plot_tracks(moons, ecc, inc, sma, time_range, savefig=False, figname='evolved_tracks'):
    
    plt.rcParams.update({'font.size': 20})
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=[20, 15], tight_layout=True)
    colours = ['r', 'g', 'b', 'm']

    for i in range(len(moons)):
        ax1.plot(time_range.value_in(units.yr), inc[i].value_in(units.deg), color=colours[i], 
        	label=moons[i])   
    ax1.set_ylabel('Inclination [deg]')
    ax1.legend()

    for i in range(len(moons)):
        ax2.plot(time_range.value_in(units.yr), np.array(ecc[i]), color=colours[i], 
        	label=moons[i])   
    ax2.set_ylabel('Eccentricity')
    ax2.set_xlabel('Time [years]')
    ax2.legend()
    
    for i in range(len(moons)):
        ax3.plot(time_range.value_in(units.yr), sma[i].value_in(units.m), color=colours[i], 
        	label=moons[i])   
    ax3.set_ylabel('Semimajor Axis')
    ax3.set_xlabel('Time [years]')
    ax3.legend()    
    
<<<<<<< Updated upstream
    plt.suptitle('Huayno Code (dt=10yrs)')
    plt.subplots_adjust(top=0.94)
    if savefig:
    	plt.savefig(figname+'.png', facecolor='w', bbox_inches='tight')
    plt.show()


def plot_energy_evolution(moons, Etot, time_range, savefig=False, figname='energy_evolution'):
    
    colours = ['r', 'g', 'b', 'm']     
    plt.rcParams.update({'font.size': 20})
    
    # Sizes of subplots are annoying
    if len(moons) < 4:
        figsize=[10,8]
    else:
        figsize=[10,12]
    
    fig, ax = plt.subplots(len(moons), 1, figsize=figsize, constrained_layout=True)     
    
    for i, ax in enumerate(fig.axes):
        ax.plot(time_range.value_in(units.yr), Etot,'-o', color=colours[i], lw=1, label=moons[i])
        ax.legend(fontsize=16) 
        
    plt.suptitle('Total Energy vs Time')
    #plt.subplots_adjust(top=0.94)
    if savefig:
    	plt.savefig(figname+'.png', facecolor='w', bbox_inches='tight')
=======
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

>>>>>>> Stashed changes
    plt.show()