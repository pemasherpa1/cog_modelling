"""import the txt files to python"""

import glob
import pandas as pd
import pickle
import os
import re
import shutil


# defining constants

PATH_IN = 'data/' 
# Note to self: 
# This data folder is / should be pasted here and NOT in the imaginal buttleneck folder!
# C:\Users\pemas\OneDrive\Desktop\University\Master UOL\Research Project\Code Versions\with support mechanism nr1\Experiment Code\PS_experiment code\experiment_code_held2022-main\data
# (when running ACT-R it will save it in the imaginal b. folder but the analysis skript wants it in one level above, so I pasted it there)

PATH_OUT = 'analysis/ana01/' # Note: this will also be in the same level as the data folder - not in the imaginal bottleneck folder!
PATH_OUT_UNMATCHED = 'analysis/ana01/unmatched'
CONDITION = ['2backPS']

# Check if output directory exists, if not, create it
if not os.path.exists(PATH_OUT):
    os.makedirs(PATH_OUT)

# Check if unmatched directory exists, if not, create it
if not os.path.exists(PATH_OUT_UNMATCHED):
    os.makedirs(PATH_OUT_UNMATCHED)



# -------------- f import behavior data-------------------------------

def import_behavior_run(filename: str):
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
        data_B_run = []
        for line in lines:
            unformatted_str = line.split('|')
            output = []
            for word in enumerate(unformatted_str):
                if word != '':
                    output.append(word[1])
            data_B_run.append(output)

    data_B_run = pd.DataFrame(data_B_run[1:], columns=data_B_run[0])
    return data_B_run

# -------------- f import trace data--------------------------------

def import_trace_run(filename: str):
    print(f"Trying to open file: {filename}")  

    lines = []
    with open(filename) as f:
        for line in f.readlines():
            line = str(re.sub(' {2,}', '  ', line)).strip() # remove/replace white space
            line = line.split('  ', 3)
            lines.append(line)
    data_run = pd.DataFrame(lines, columns=('time', 'buffer', 'action')) 
    return data_run


# --------------- Start Preprocessing Data ----------------------------

if __name__ == '__main__':
    dict.fromkeys(CONDITION)

    for condition in CONDITION:
      
        current_path_behavior = PATH_IN + condition + '/*_behavior_???.txt'
        current_path_trace = PATH_IN + condition + '/*_trace_???.txt'
        #current_path_behavior = r"C:\Users\pemas\OneDrive\Desktop\University\Master UOL\Research Project\Code Versions\with support mechanism nr1\Experiment Code\PS_experiment code\experiment_code_held2022-main\imaginal_bottleneck\data\2backPS\*_behavior_???.txt"
        #current_path_trace = r"C:\Users\pemas\OneDrive\Desktop\University\Master UOL\Research Project\Code Versions\with support mechanism nr1\Experiment Code\PS_experiment code\experiment_code_held2022-main\imaginal_bottleneck\data\2backPS\*_trace_???.txt"

        print(f"\nSearching for behavior files in: {current_path_behavior}")
        print(f"Searching for trace files in: {current_path_trace}")


        all_runs_behavior = glob.glob(current_path_behavior)

        for i, run_behavior in enumerate(all_runs_behavior):
            formatted_run_behavior = import_behavior_run(run_behavior)
            last_time = float(formatted_run_behavior.iloc[-1]['time'])

            # Continue with the process only if the behavior run is long enough
            if last_time > 179.00:
                print(f"\nProcessing {condition}  Run {i + 1} - Behavior is long enough.")

                # Import trace data
                run_number = run_behavior.split('_')[-1].split('.')[0]
                run_trace_filename = f'{PATH_IN}{condition}/{condition}_trace_{int(run_number):03d}.txt'
                #run_trace_filename = f'{PATH_IN}{condition}/2backPS_trace_{int(run_number):03d}.txt'

                formatted_run_trace = import_trace_run(run_trace_filename)

                # Check if trace data has at least 6 occurrences of "notice support"
                notice_support_count = formatted_run_trace[formatted_run_trace['action'] == '** NOTICE-SUPPORT ** [goal1]'].shape[0]

                if notice_support_count >= 6:
                    print(f"Processing {condition} Run {i + 1} - Trace has {notice_support_count} occurrences of 'notice support'\n")
                    
                    # Save behavior file
                    behavior_filename = f'{PATH_OUT}{condition}_behavior_{int(run_number):03d}.p'
                    pickle.dump(formatted_run_behavior, open(behavior_filename, 'wb'))

                    # Save trace file
                    trace_filename = f'{PATH_OUT}{condition}_trace_{int(run_number):03d}.p'
                    pickle.dump(formatted_run_trace, open(trace_filename, 'wb'))
                else:
                    print(f"Skipping {condition}    Run {i + 1} - Trace has only {notice_support_count} occurrences of 'notice support'\n")
                    # Copy both unmatched files for a trial to PATH_OUT_UNMATCHED
                    shutil.copy(run_behavior, os.path.join(PATH_OUT_UNMATCHED, f'{condition}_behavior_{int(run_number):03d}.txt'))
                    shutil.copy(run_trace_filename, os.path.join(PATH_OUT_UNMATCHED, f'{condition}_trace_{int(run_number):03d}.txt'))

            else:
                print(f"Skipping {condition}, Run {i + 1} - Behavior is not long enough\n")

        print(f"Preprocessing of all files for the {condition} model + ' done!\n")
        
    # sort BEHAVIOR files into conditions
    files_all = glob.glob(PATH_OUT + '*_behavior_???.p')
    files_condition = dict.fromkeys(CONDITION)
    for condition in files_condition:
        files_condition[condition] = [file for file in files_all if (condition + '_') in file] #condition not unique see 'mild load' vs. 'mild load + warning'

    filename_behavior = '%sfiles_sorted_behavior.p' %(PATH_OUT)
    pickle.dump(files_condition, open(filename_behavior, 'wb'))
   
    # sort TRACE files into conditions
    files_all = glob.glob(PATH_OUT + '*_trace_??.p')
    files_condition = dict.fromkeys(CONDITION)
    for condition in files_condition:
        files_condition[condition] = [file for file in files_all if (condition + '_') in file] #condition not unique see 'mild load' vs. 'mild load + warning'

    filename_trace = '%sfiles_sorted_trace.p' %(PATH_OUT)
    pickle.dump(files_condition, open(filename_trace, 'wb'))

   # Load the pickled data
    #loaded_data = pickle.load(open(filename, 'rb'))

    # Print or inspect the loaded data
    #print(loaded_data)

# ----------------- just to check if and which were both saved (no functionality) -------------- 

if __name__ == '__main__':
    # Get all run numbers
    run_numbers = range(1, 250)  # Assuming you have 100 runs

    for run_number in run_numbers:
        behavior_filename = f'{PATH_OUT}2backPS_behavior_{run_number:03d}.p'
        trace_filename = f'{PATH_OUT}2backPS_trace_{run_number:03d}.p'

        # Check if both behavior and trace files exist
        if os.path.exists(behavior_filename) and os.path.exists(trace_filename):
            print(f"Saved both files for Run {run_number}")



#-----------------------------------------------------------------------------------------------

# Count and display the number of files in PATH_OUT and PATH_OUT_UNMATCHED
total_input_files = 250  # Assuming a constant total number 250 of input files

num_files_out = len(os.listdir(PATH_OUT)) // 2 - 1
num_files_unmatched = len(os.listdir(PATH_OUT_UNMATCHED)) // 2
matching_files_percentage = (num_files_out / total_input_files) * 100

print(f"\nNumber of files in {PATH_OUT}: {num_files_out}")
print(f"Number of files in {PATH_OUT_UNMATCHED}: {num_files_unmatched}")
print(f"Percentage of matching files: {matching_files_percentage:.2f}%\n")



#---------------------- Renumber files in PATH_OUT folder------------------------------------------

# path_out_behavior_files = glob.glob(os.path.join(PATH_OUT, '*_behavior_???.p'))
# path_out_trace_files = glob.glob(os.path.join(PATH_OUT, '*_trace_???.p'))

# for i, (behavior_path, trace_path) in enumerate(zip(path_out_behavior_files, path_out_trace_files), start=1):
#     _, behavior_extension = os.path.splitext(behavior_path)
#     _, trace_extension = os.path.splitext(trace_path)

#     new_behavior_filename = os.path.join(PATH_OUT, f'{condition}_behavior_{i:03d}{behavior_extension}')
#     new_trace_filename = os.path.join(PATH_OUT, f'{condition}_trace_{i:03d}{trace_extension}')

#     os.rename(behavior_path, new_behavior_filename)
#     os.rename(trace_path, new_trace_filename)

# # Renumber files in PATH_OUT_UNMATCHED folder
# path_out_unmatched_behavior_files = glob.glob(os.path.join(PATH_OUT_UNMATCHED, '*_behavior_???.txt'))
# path_out_unmatched_trace_files = glob.glob(os.path.join(PATH_OUT_UNMATCHED, '*_trace_???.txt'))

# for i, (behavior_path, trace_path) in enumerate(zip(path_out_unmatched_behavior_files, path_out_unmatched_trace_files), start=1):
#     _, behavior_extension = os.path.splitext(behavior_path)
#     _, trace_extension = os.path.splitext(trace_path)

#     new_behavior_filename = os.path.join(PATH_OUT_UNMATCHED, f'{condition}_behavior_{i:03d}{behavior_extension}')
#     new_trace_filename = os.path.join(PATH_OUT_UNMATCHED, f'{condition}_trace_{i:03d}{trace_extension}')