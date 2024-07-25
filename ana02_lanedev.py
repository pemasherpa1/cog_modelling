""""""

import pandas as pd
import pickle
import glob
import numpy as np
import os



PATH_IN = 'analysis/ana01/'
PATH_OUT = 'analysis/ana02/'
CONDITIONS = ['2backPS']
SRATE = 0.05


print(os.getcwd())

# Pema -------------------------------------------------------------------------------

# Check if output directory exists, if not, create it

PATH_OUT = 'analysis/ana02/'
if not os.path.exists(PATH_OUT):
    os.makedirs(PATH_OUT)


# ---------------- F CALCULATE DEVIATION ----------------------------------------------

def calc_deviation(data: str):

    # calc lane deviation
    
    lanepos = np.array(data['lanepos']).astype(float)

    deviation = np.abs(lanepos - 2.5)*2.5
    deviation = np.mean(deviation)

    return deviation

# ---------------- F CALCULATE STD OF LAT. POSITION--------------------------------------

def calc_sdlp(data: str):
    """calculates standard deviation of the lateral position"""

    lanepos = np.array(data['lanepos']).astype(float)

    sdlp = np.std(lanepos)

    return sdlp

#----------------------------------------------------------------------------------------





if __name__ == '__main__':

    files_condition = pickle.load(open(PATH_IN + 'files_sorted_behavior.p', 'rb'))
    
    # initialise dictionaries
    deviation_all = dict.fromkeys(CONDITIONS)
    deviation_avg = dict.fromkeys(CONDITIONS)
    sdlp_all = dict.fromkeys(CONDITIONS)
    sdlp_avg = dict.fromkeys(CONDITIONS)

    for condition in CONDITIONS: # for "2backPS" only once

        # calculate average steering reversal for each condition
        deviation_condition = [] 
        sdlp_condition = []

        for filename in files_condition[condition]:
            # load data from the current file
            data = pickle.load(open(filename, 'rb'))

            # calculate average lane deviation per run
            deviation = calc_deviation(data)
            # append the calculated values to the list
            deviation_condition.append(deviation)

            # calculate sdlp
            sdlp = calc_sdlp(data)
            # append the calculated values to the list
            sdlp_condition.append(sdlp)

        # caculate and store average lane deviation and sdlp 
        deviation_all[condition] = deviation_condition
        deviation_avg[condition] = np.mean(deviation_condition) # calc average
        sdlp_all[condition] = sdlp_condition
        sdlp_avg[condition] = np.mean(sdlp_condition)           # calc average

        print(f"\n{condition} Model - Calculation of lane deviation and STD of lateral position done!\n")

    # dump all ld, sdlp into one file
    pickle.dump(deviation_all, open(PATH_OUT + 'lanedev_all.p', 'wb')) # lanedev_all.p will contain all lane devs for each of the 130 trials
    pickle.dump(sdlp_all, open(PATH_OUT + 'sdlp_all.p', 'wb'))  # sdlp_all.p will contain all the SDLPs for all 130 trials

    # save to csv
    pd.DataFrame.from_dict(data=deviation_avg, orient='index').to_csv(
        PATH_OUT + 'lanedev.csv', header=False) # lanedev.csv contains the average deviation for ALL trials with the same model
    pd.DataFrame.from_dict(data=sdlp_avg, orient='index').to_csv(
        PATH_OUT + 'sdlp.csv', header=False) # sdlp.csv contains the average of ALL average lane deviations for ALL trials with the same model
