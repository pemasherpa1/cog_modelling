"""custom script for different plots"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pickle
import numpy as np
import csv
import itertools



PATH_IN = 'analysis/ana02/'
PATH_OUT = 'analysis/ana03/'


# --------------------------- Pema ------------------------------
# Check if output directory exists, if not, create it
import os 

PATH_OUT = 'analysis/ana03/'
if not os.path.exists(PATH_OUT):
    os.makedirs(PATH_OUT)


# _____________________ VIOLIN PLOT _______________________________________________

def my_violinplot(datadict: dict, x_label: str, title: str='', color: str='skyblue'):

    """ Generate a violin plot for the given data.
    Parameters:
    - datadict  (dict):  Dictionary containing data for the plot
    - x_label   (str):   Label for the x-axis
    - title     (str):   Title for the plot
    - color (str): Color for the violin plot


    Returns:
    - fig, ax: Figure and axis objects."""

    # unfortunately this is necessary as sns likes a different format for the data
    dat = []
    dat_label = []
    for key in datadict:
        for data in datadict[key]:
            dat.append(data)
            dat_label.append(key)

    df = pd.DataFrame({x_label: dat,
                       'Model': dat_label})

    # Set the font properties
    plt.rc('axes', unicode_minus=False)
    plt.rcParams['font.family'] = 'Gill Sans MT'
    COLOR = 'black'
    plt.rcParams['text.color'] = COLOR
    plt.rcParams['axes.labelcolor'] = COLOR
    plt.rcParams['xtick.color'] = COLOR
    plt.rcParams['ytick.color'] = COLOR
    plt.rcParams['axes.edgecolor'] = COLOR
    my_fontsize = 20

    # create figure
    fig, ax = plt.subplots()

    # Set the labels font
    ax.tick_params(axis='both', labelsize=18)
    ax.set_title('', fontsize=my_fontsize)
    ax.set_xlabel('', fontsize=my_fontsize)
    ax.set_ylabel('', fontsize=my_fontsize)

    # plot/components/mail/mail.html
    # violin_color = '#dcedc1'

    # plot/components/mail/mail.html
    sns.violinplot(data=df, x=x_label, y='Model', width=0.9,
                saturation=1, color=color, inner='box', density_norm='width', linewidth=1, legend=False).set_title(title, fontsize=my_fontsize)

    sns.despine(ax=ax, offset=1, trim=True) # removes the borders of the plot

    return fig, ax


# _____________________ STEERING REVERSAL RATE _______________________________________________

def plot_srr(): 
    filename = PATH_IN + 'reversals_all.p'
    datadict = pickle.load(open(filename, 'rb'))
    fig, ax = my_violinplot(datadict, 'Average steering reversal rate in [Hz]',color='skyblue')
    start = 0 # 0.3
    stop = 1 # 0.9
    step = 0.1
    ax.spines['bottom'].set_bounds(start, stop)
    xticks = np.arange(start, stop + 0.00001, step)
    ax.set_xticks(xticks)
    
    plt.savefig(PATH_OUT + 'steering_reversals.png', bbox_inches='tight')



# __________________________ AVG LANE DEVIATION _____________________________________________
def plot_lanedev():
    filename = PATH_IN + 'lanedev_all.p'
    datadict = pickle.load(open(filename, 'rb'))
    fig, ax = my_violinplot(datadict, 'Average lane deviation',color='lightcoral')
    start = 0
    stop = 10 #0.8
    step = 1
    ax.spines['bottom'].set_bounds(start, stop)
    xticks = np.arange(start, stop + 0.00001, step)
    ax.set_xticks(xticks)

    plt.savefig(PATH_OUT + 'lane_deviation.png', bbox_inches='tight')


# _____________________ STANDARD DEVIATION OF LATERAL POSITION____________________________

def plot_sdlp():
    filename = PATH_IN + 'sdlp_all.p'
    datadict = pickle.load(open(filename, 'rb'))
    fig, ax = my_violinplot(datadict, 'Standard deviation of lateral position', title='Driving Performance',color='lightgreen')
    start = -1  # 0
    stop = 3    # 0.35
    step = 0.5
    ax.spines['bottom'].set_bounds(start, stop)
    xticks = np.arange(start, stop + 0.00001, step)
    ax.set_xticks(xticks)

    plt.savefig(PATH_OUT + 'std_lat_pos.png', bbox_inches='tight')


# ----------------------------------FUNCTION CALLS --------------------------------------------


if __name__ == '__main__':

    plot_srr()          # steering reversal rate
    plot_sdlp()         # std of lateral position
    plot_lanedev()      # lane deviation
    
    plt.show()          # show the plots



























# ---------------------- MINDWANDERING PLOTS (not needed)
 # Mindwandering Plot:
    #plot_mw_count()
    #plot_mw_length()
    #plot_mw_stops()    



# _____________________ BAR PLOT _______________________________________________

# def my_barplot(datadict: dict, x_label: str):

#     df = pd.DataFrame(datadict, index=[0])
    
#     # Set the font properties
#     plt.rc('axes', unicode_minus=False)
#     plt.rcParams['font.family'] = 'Gill Sans'
#     my_fontsize = 20

#     # create figure
#     fig, ax = plt.subplots()

#     # Set the labels font
#     ax.tick_params(axis='both', labelsize=16)
#     ax.set_title('', fontsize=my_fontsize)
#     ax.set_xlabel('', fontsize=my_fontsize)
#     ax.set_ylabel('', fontsize=my_fontsize)

#     # plot/components/mail/mail.html
#     sns.barplot(df, x=x_label, width=0.8,saturation=1, palette='Set2')
#     sns.despine(ax=ax, offset=1, trim=True)
#     return fig, ax

    
# def plot_mw_count():
#     filename = PATH_IN + 'mw_count_all.p'
#     datadict = pickle.load(open(filename, 'rb'))
#     fig, ax = my_violinplot(
#         datadict, 'Average number of mind-wandering productions', title='Prevalence of MW')
    
#     plt.savefig(PATH_OUT + 'mw_count.eps', bbox_inches='tight', transparent=True)


# def plot_mw_length():
#     filename = PATH_IN + 'mw_length_all.p'
#     datadict = pickle.load(open(filename, 'rb'))
#     fig, ax = my_violinplot(
#         datadict, 'Average length of each mind-wandering episode')
    
#     plt.savefig(PATH_OUT + 'mw_length.eps', bbox_inches='tight', transparent=True)


# def plot_mw_stops():
#     filename = PATH_IN + 'stops_count_avg.csv'
#     reader = csv.reader(open(filename, 'r'))
#     datadict = {}
#     for key, value in reader:
#         datadict[key] = value

#     fig, ax = my_barplot(datadict, 'Average percentage of mind-wandering being stopped by lateral position')
    
#     plt.savefig(PATH_OUT + 'mw_stops.eps', bbox_inches='tight')