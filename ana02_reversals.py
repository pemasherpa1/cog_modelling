""""""

from ast import Constant
import pandas as pd
import pickle
import glob
import numpy as np

PATH_IN = 'analysis/ana01/'
PATH_OUT = 'analysis/ana02/'
#CONDITIONS = ['focused driving', 'MW + driving',  'mild load', 'intermediate load', 'warning', 'mild load + warning']
CONDITIONS = ['2backPS']

SRATE = 0.05

def count_reversals(data:str):

    # count steering reversal
    angles_all = np.array(data['steerAngle']).astype(float)
    reversals = 0
    for i,j in zip(angles_all, angles_all[1:]):
        reversals += 1 if i*j<0 else 0

    return reversals


if __name__ == '__main__':

    files_condition = pickle.load(open(PATH_IN + 'files_sorted_behavior.p', 'rb'))

    reversals_all = dict.fromkeys(CONDITIONS)
    reversals_avg = dict.fromkeys(CONDITIONS)

    for condition in CONDITIONS:


        reversals_condition = []
        
        for i, filename in enumerate(files_condition[condition]):
            
            data = pickle.load(open(filename, 'rb'))

            # per model run
            reversals = count_reversals(data)
            reversal_rate = reversals/len(data)/SRATE
            reversals_condition.append(reversal_rate)

        reversals_all[condition] = reversals_condition
        reversals_avg[condition] = np.mean(reversals_condition)
        print(f"\n{condition} Model - Calculation of reversal rates done!\n")


    # dump all reversals in one file
    filename = PATH_OUT + 'reversals_all.p'
    pickle.dump(reversals_all, open(filename, 'wb'))

    # save to csv
    pd.DataFrame.from_dict(data=reversals_avg, orient='index').to_csv(PATH_OUT + 'reversals.csv', header=False)




import pickle
import pandas as pd
# Load the pickled data
reversals_all = pickle.load(open(PATH_OUT + 'reversals_all.p', 'rb'))

# Print or inspect the loaded data
print(reversals_all)


# Read the CSV file into a DataFrame
reversals_df = pd.read_csv(PATH_OUT + 'reversals.csv', header=None)

# Print or inspect the DataFrame
print(reversals_df)
