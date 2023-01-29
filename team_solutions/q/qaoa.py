import numpy as np
import json
import matplotlib.pyplot as plt
from pprint import pprint as pp
import networkx as nx
from scipy.optimize import minimize

from braket.aws import AwsDevice
from braket.devices import LocalSimulator

from quera_ahs_utils.plotting import show_global_drive
from quera_ahs_utils.drive import get_drive 

from braket.ahs.analog_hamiltonian_simulation import AnalogHamiltonianSimulation

qpu = AwsDevice("arn:aws:braket:us-east-1::device/qpu/quera/Aquila")

# Capabilities, constraints and performance metrics are stored as 'paradigm' attribute of AwsDevice.
capabilities = qpu.properties.paradigm

# get C6 coefficient in rad m^6/sec Pull from capabilities attribute
C6 = float(capabilities.rydberg.dict()['c6Coefficient'])

# Some variables storing device information
max_time = float(capabilities.rydberg.dict()['rydbergGlobal']['timeMax'])
time_res = float(capabilities.rydberg.dict()['rydbergGlobal']['timeResolution'])

max_rabi = float(capabilities.rydberg.dict()['rydbergGlobal']['rabiFrequencyRange'][1])
rabi_res = float(capabilities.rydberg.dict()['rydbergGlobal']['rabiFrequencyResolution'])

max_detuning = float(capabilities.rydberg.dict()['rydbergGlobal']['detuningRange'][1])
detuning_res = float(capabilities.rydberg.dict()['rydbergGlobal']['detuningResolution'])

max_slew_rate = min(
    float(capabilities.rydberg.dict()['rydbergGlobal']['detuningSlewRateMax']),
    float(capabilities.rydberg.dict()['rydbergGlobal']['rabiFrequencySlewRateMax'])
)
ramp_time = max_rabi/max_slew_rate # run = slope/rise. This is greater than time res

def get_ham_values(params):
    '''
    Generates the time-dependent values of the parameters of the Hamiltonian
    params: The parameters storing the duration of each pulse
    
    Returns
    time_points: :ist of points along the t-axis where the value of a Hamiltonian paramter changes
    amplitude_values: the values of omega at key points in time
    detuning_values: the values of delta at key points in time
    phase_values: the value of the phase at key points in time
    '''
    
    # Based on device
    max_rabi = 15800000.0 
    max_detuning = 125000000.0
    ramp_time = max_rabi/2500000000000000.0
    
    # Initialize variables
    p = int(len(params)/2)
    time_points = [0]
    amplitude_values = [0]
    detuning_values = [max_detuning]
    phase_values = [0]
    time_count = 0
    
    # Fill in lists according to params
    for i in range(0,p,2):
        time_points.extend([
            time_count+ramp_time, time_count+ramp_time + params[i], 
            time_count+ramp_time+params[i] + ramp_time, time_count+ramp_time+params[i] + ramp_time + params[i+1]
        ])

        time_count = time_points[-1]

        amplitude_values.extend([max_rabi*(i+1)/p, max_rabi*(i+1)/p, 0, 0])
        detuning_values.extend([0, 0, max_detuning*(i+1)/p, max_detuning*(i+1)/p])
        phase_values.extend([np.pi*(i+1)/p, 0, -1*np.pi*(i+1)/p, 0])
        
    return time_points, amplitude_values, detuning_values, phase_values


def objective(params):
    '''
    The objective function that the classical optimizer minimzes the parameters of.
    Runs evolution by given paramters
    
    params: a list of points in time, in picoseconds (so that the number is large enough for scipy to optimize). 
    '''
    
    scaled_params = [elem*10**(-6) for elem in params] # convert to microseconds
    time_points, amplitude_values, detuning_values, phase_values = get_ham_values(scaled_params)
    # Define the drive
    drive = get_drive(time_points, amplitude_values, detuning_values, phase_values)
    #show_global_drive(drive);
    
    small_ahs_program = AnalogHamiltonianSimulation(
        register=small_register, 
        hamiltonian=drive
    )
    
    # Define Device
    device = LocalSimulator("braket_ahs")
    small_ahs_run = device.run(small_ahs_program, shots=1000)
    
    # Run
    result  = small_ahs_run.result()
    
    # Store results in json string
    result_dict = {"measurements":[]}
    for measurement in result.measurements:
        shot_result = {
            "pre_sequence":[int(qubit) for qubit in measurement.pre_sequence],
            "post_sequence":[int(qubit) for qubit in measurement.post_sequence]
                      } 
        result_dict["measurements"].append(shot_result)
        
    #json.dumps(result_dict,io,indent=2) # dumps instead of dump to avoid saving file
    
    IS_sizes,pp_bitstrings = analysis_MIS(small_G,result_dict, print_extra=False)
    return -1*IS_sizes.mean() # Multiply by -1 since we want to minimze rather than maximize

# Constraint to ensure total time falls within maximum allowable time
def enforce_time_bound(x):
    return 0.000004*(10**6) - (sum(x) + (15800000.0*(10**6)/250000000000000.0)*(len(x)))

# Constraint to ensure all time durations are positive
def enforce_positive_params(x):
    for elem in x:
        if elem < 0:
            return -1 # penalty for negative parameter
    
    return 1

# Constraint Dictionary
cons = (
    {
        'type': 'ineq', 
        'fun': enforce_time_bound # sum of times must be less than max time
    },
    {
        'type': 'ineq',
        'fun': enforce_positive_params
    }
)

if __name__ == '__main__':
    pp(capabilities.dict())