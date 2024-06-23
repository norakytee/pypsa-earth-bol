
import pypsa
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import subprocess
import os

# Function to perform Monte Carlo simulation for states and times
def mcs_ms(n_Hr, TRM, Initial_hour, state_now, state_next):
    n_com = len(TRM)
    n_state_com = np.zeros(n_com, dtype=int)
    for comp in range(n_com):
        n_state_com[comp] = len(TRM[comp])

    States_Raw = np.zeros((n_com, n_Hr))
    Times_Raw = np.zeros((n_com, n_Hr))

    for element in range(n_com):
        hour = int(Initial_hour[element])
        TTNE = np.zeros(n_state_com[element])
        while hour < n_Hr:
            # Calculate time to next event
            for i in range(n_state_com[element]):
                TTNE[i] = -np.log(np.random.rand()) / TRM[element][state_now[element] - 1, i]
            TTNE[TTNE <= 0] = np.nan
            if np.all(np.isnan(TTNE)):
                break
            Time, state_next[element] = np.nanmin(TTNE), np.nanargmin(TTNE) + 1
            Time = max(int(Time), 1)
            if Time != float('inf'):
                if hour + Time < n_Hr:
                    States_Raw[element, hour:hour + Time] = state_now[element] - 1
                    hour += Time
                    state_now[element] = state_next[element]
                else:
                    States_Raw[element, hour:n_Hr] = state_now[element] - 1
                    hour = n_Hr
            else:
                States_Raw[element, hour:n_Hr] = state_now[element] - 1
                hour = n_Hr

    return States_Raw, Times_Raw, Initial_hour, state_now, state_next

# Function to arrange states in time
def arrange_states_in_time(State_Raw, Time_Raw, n_Hr, n_com):
    A = Time_Raw.copy()
    
    # Calculate cumulative Times
    for j in range(n_com):
        for i in range(1, Time_Raw.shape[1] - 1):
            A[j, i] += A[j, i - 1]
        A[j, -1] = n_Hr
    
    # Sort and delete repetitive times
    B = np.sort(A, axis=None)
    C = np.unique(B)
    D = np.zeros((n_com + 1, len(C) + 1))
    D[n_com, 1:] = C
    
    # Calculate the states of the system with related times
    D[:n_com, 0] = State_Raw[:, 0]
    for i in range(len(C) - 1):
        D[:n_com, i + 1] = D[:n_com, i]
        rows, cols = np.where(A == C[i])
        if len(rows) == 1:
            D[rows[0], i + 1] = State_Raw[rows[0], cols[0] + 1]
        else:
            for j in range(len(rows)):
                D[rows[j], i + 1] = State_Raw[rows[j], cols[j] + 1]
    D[:n_com, -1] = D[:n_com, -2]
    
    # Delete similar consecutive states
    s = 1
    D1 = np.zeros((n_com, len(C) + 1))
    D1[:, 0] = D[:n_com, 0]
    for i in range(D.shape[1] - 1):
        if not np.array_equal(D[:n_com, i], D[:n_com, i + 1]):
            D1[:, s] = D[:n_com, i + 1]
            s += 1
    D1[:, s] = D[:n_com, -1]
    
    State_Time = D1[:, :s + 1]
    return State_Time

def run_monte_carlo_simulation(all_indices):
    # Parameters
    n_lines = 114
    n_CCGT = 12
    n_OCGT = 30
    n_solar = 83
    n_onwind = 83
    n_biomass = 6
    n_geo = 1
    n_ror = 19
    n_hydro = 12
    n_oil = 14
    n_ele = n_lines + n_oil + n_hydro + n_ror + n_geo + n_biomass + n_onwind + n_solar + n_OCGT + n_CCGT

    n_h = 8760
    Initial_hour = np.zeros(n_ele)
    state_now = np.ones(n_ele, dtype=int)
    state_next = np.ones(n_ele, dtype=int)

    # Defining TRM (transition rate matrix) for all elements
    TRM = [None] * n_ele

    fr_line = np.array([[-1/5000, 1/5000], [1/9.5, -1/9.5]])
    fr_OCGT = np.array([[-1/2190, 1/2190], [1/9.5, -1/9.5]])
    fr_biomass = np.array([[-1/2190, 1/2190], [1/9.5, -1/9.5]])
    fr_CCGT = np.array([[-1/2190, 1/2190], [1/9.5, -1/9.5]])
    fr_oil = np.array([[-1/2190, 1/2190], [1/9.5, -1/9.5]])
    fr_geo = np.array([[-1/2190, 1/2190], [1/9.5, -1/9.5]])
    fr_onwind = np.array([[-43/500000, 43/500000], [1/51.75, -1/51.75]]) #Source: https://www.sciencedirect.com/science/article/pii/S0960148110001904 | https://www.mdpi.com/1996-1073/10/11/1904
    fr_solar = np.array([[-397/11680, 397/11680], [1/11.2, -1/11.2]]) #Source: https://www.sciencedirect.com/science/article/pii/S0360544219313234
    fr_ror = np.array([[-1/4380, 1/4380], [1/9.5, -1/9.5]])
    fr_hydro = np.array([[-1/4380, 1/4380], [1/9.5, -1/9.5]])

    # fr_line = np.array([[-1/500000, 1/500000], [1/9.5, -1/9.5]])
    # fr_OCGT = np.array([[-1/219000, 1/219000], [1/9.5, -1/9.5]])
    # fr_biomass = np.array([[-1/219000, 1/219000], [1/9.5, -1/9.5]])
    # fr_CCGT = np.array([[-1/219000, 1/219000], [1/9.5, -1/9.5]])
    # fr_oil = np.array([[-1/219000, 1/219000], [1/9.5, -1/9.5]])
    # fr_geo = np.array([[-1/219000, 1/219000], [1/9.5, -1/9.5]])
    # fr_onwind = np.array([[-43/5000000, 43/5000000], [1/51.75, -1/51.75]]) #Source: https://www.sciencedirect.com/science/article/pii/S0960148110001904 | https://www.mdpi.com/1996-1073/10/11/1904
    # fr_solar = np.array([[-397/1168000, 397/1168000], [1/11.2, -1/11.2]]) #Source: https://www.sciencedirect.com/science/article/pii/S0360544219313234
    # fr_ror = np.array([[-1/438000, 1/438000], [1/9.5, -1/9.5]])
    # fr_hydro = np.array([[-1/438000, 1/438000], [1/9.5, -1/9.5]])

    line_file = pd.read_csv('/mnt/beegfs/users/noraky/pypsa-earth-2/pypsa-earth/resources/base_network/all_lines_build_network.csv')

    for i in range(n_lines):
        fr_aux = fr_line.copy()
        fr_aux[0, 1] *= line_file.loc[i, 'length']
        TRM[i] = fr_aux

    offset = n_lines
    for i in range(n_OCGT):
        TRM[offset + i] = fr_OCGT

    offset += n_OCGT
    for i in range(n_biomass):
        TRM[offset + i] = fr_biomass

    offset += n_biomass
    for i in range(n_CCGT):
        TRM[offset + i] = fr_CCGT

    offset += n_CCGT
    for i in range(n_oil):
        TRM[offset + i] = fr_oil

    offset += n_oil
    for i in range(n_geo):
        TRM[offset + i] = fr_geo

    offset += n_geo
    for i in range(n_onwind):
        TRM[offset + i] = fr_onwind

    offset += n_onwind
    for i in range(n_solar):
        TRM[offset + i] = fr_solar

    offset += n_solar
    for i in range(n_ror):
        TRM[offset + i] = fr_ror

    offset += n_ror
    for i in range(n_hydro):
        TRM[offset + i] = fr_hydro
            
    States_Raw, Times_Raw, Initial_hour, state_now, state_next = mcs_ms(n_h, TRM, Initial_hour, state_now, state_next)
    states_df = pd.DataFrame(States_Raw)
    states_df_transposed = states_df.T

    n_snapshots = 8760  
    start_time = datetime(2013, 1, 1)

    datetime_column = [start_time + timedelta(hours=i) for i in range(n_snapshots)]

    datetime_df = pd.DataFrame(datetime_column, columns=['datetime'])
    result_df = pd.concat([datetime_df, states_df_transposed.reset_index(drop=True)], axis=1)

    df_lines = result_df.iloc[:, :n_lines + 1]

    start_generators = n_lines + 1
    end_generators = start_generators + n_oil + n_ror + n_geo + n_biomass + n_onwind + n_solar + n_OCGT + n_CCGT
    df_generators = result_df.iloc[:, np.r_[0, start_generators:end_generators]]

    start_storage_units = end_generators
    end_storage_units = start_storage_units + n_hydro
    df_storage_units = result_df.iloc[:, np.r_[0, start_storage_units:end_storage_units]]

    mapping = {i: name for i, name in enumerate(all_indices)}

    df_lines.rename(columns=mapping, inplace=True)
    df_generators.rename(columns=mapping, inplace=True)
    df_storage_units.rename(columns=mapping, inplace=True)

    df_lines.to_csv('/mnt/beegfs/users/noraky/pypsa-earth-2/pypsa-earth/matrices/lines_matrix.csv', index=False)
    df_generators.to_csv('/mnt/beegfs/users/noraky/pypsa-earth-2/pypsa-earth/matrices/generators_matrix.csv', index=False)
    df_storage_units.to_csv('/mnt/beegfs/users/noraky/pypsa-earth-2/pypsa-earth/matrices/storage_units_matrix.csv', index=False)


def rename_results_file(iteration):
    current_location = '/mnt/beegfs/users/noraky/pypsa-earth-2/pypsa-earth/results/networks/'
    old_filename = "elec_s_all_ec_lcopt_Co2L-1H.nc"
    new_filename = f"network_{iteration}.nc"
    new_location = '/mnt/beegfs/users/noraky/pypsa-earth-2/pypsa-earth/monte_carlo_network/'

    # Create the full paths for the old and new files
    old_file_path = os.path.join(current_location, old_filename)
    new_file_path = os.path.join(new_location, new_filename)

    # Rename the file
    os.rename(old_file_path, new_file_path)

n_simulations = 10

start_date = '2013-01-01'

n = pypsa.Network('/mnt/beegfs/users/noraky/pypsa-earth-2/pypsa-earth/network_bnze_2040/BNZE_2040.nc')
line_indices = list(n.lines.index)
generators = n.generators[~n.generators.carrier.str.contains('load')].carrier.unique()
generator_indices = []
for carrier in generators:
    generator_indices += list(n.generators.query(f"carrier == '{carrier}'").index)
storage_unit_indices = list(n.storage_units.index)
all_indices = line_indices + generator_indices + storage_unit_indices

start_year = 2024
start_value = 2740892
end_year = 2050
end_value = 0

years = range(start_year, end_year + 1)
emissions = []

decrease_per_year = (start_value - end_value) / (end_year - start_year)

for i in years:
    emission = max(start_value - decrease_per_year * (i - start_year), end_value)
    emissions.append(emission)

index = np.arange(2024,2051)
emission_limit = dict(zip(index, emissions))
emission_limit

for iteration in range(n_simulations):
    n = pypsa.Network('/mnt/beegfs/users/noraky/pypsa-earth-2/pypsa-earth/network_bnze_2040/network_bnze_2040.nc')
    n.global_constraints.constant = emission_limit[2040]
    n.lines.loc[n.lines.index,"s_nom_extendable"] = False
    n.generators.loc[n.generators.index,"p_nom_extendable"] = False
    n.stores.loc[n.stores.index,"e_nom_extendable"] = False
    n.links.loc[n.links.index,"p_nom_extendable"] = False
    n.export_to_netcdf('/mnt/beegfs/users/noraky/pypsa-earth-2/pypsa-earth/networks/elec_s_all_ec_lcopt_Co2L-1H.nc')
    run_monte_carlo_simulation(all_indices)
    subprocess.run(['snakemake', '-j', '16', 'solve_all_networks'])
    rename_results_file(iteration+1)