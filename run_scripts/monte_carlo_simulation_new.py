
import pypsa
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import subprocess
import os


def monte_carlo_simulation_multi_component(n_Hr, lambdas_ttf, lambdas_ttr):
    """
    Perform a Monte Carlo simulation of multiple system components' reliability for a single simulation run.

    Parameters:
    - n_Hr : int
        Total hours to simulate.
    - lambdas_ttf : array_like
        Rate parameters for the exponential distribution of time to failure for each component.
    - lambdas_ttr : array_like
        Rate parameters for the exponential distribution of time to repair for each component.
        
    Returns:
    - states_record : np.array
        A 2D array recording the binary state (1 = operational, 0 = failed) of each component over time.
    """
    n_components = len(lambdas_ttf)
    states_record = np.zeros((n_components, n_Hr))

    # Precompute the inverses to optimize performance
    inv_lambdas_ttf = 1 / lambdas_ttf
    inv_lambdas_ttr = 1 / lambdas_ttr

    for comp in range(n_components):
        time = 0
        current_state = 1  # Start as operational

        while time < n_Hr:
            if current_state == 1:  # Currently operational
                ttf = np.random.exponential(inv_lambdas_ttf[comp])
                end_time = min(time + int(np.ceil(ttf)), n_Hr)
                states_record[comp, time:end_time] = 1
                time = end_time  # Move to the end of operational period
                current_state = 0  # Switch to failed state
            else:  # Currently failed
                ttr = np.random.exponential(inv_lambdas_ttr[comp])
                time = min(time + int(np.ceil(ttr)), n_Hr)  # Move to the end of repair period
                current_state = 1  # Switch back to operational state

    return states_record



def run_monte_carlo_simulation(iteration, all_indices, datetime_column, line_lengths):
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
    #n_ele = n_lines + n_oil + n_hydro + n_ror + n_geo + n_biomass + n_onwind + n_solar + n_OCGT + n_CCGT

    # Define failure rates (lambdas) for Time to Failure (TTF)
    lambdas_ttf = np.array([
        1/438000,  # Lines
        1/2190,    # OCGT
        1/2190,    # Biomass
        1/2190,    # CCGT
        1/2190,    # Oil
        1/2190,    # Geothermal
        148/87600000, # Onwind
        148/87600000, # Solar https://www.sciencedirect.com/science/article/pii/S0960148111000589
        1/4380,    # ROR
        1/4380     # Hydro
    ])

    # Define specific repair rates (lambdas) for Time to Repair (TTR) for each type
    lambdas_ttr = np.array([
        1/10,     # Lines
        49/2190,      # OCGT
        49/2190,      # Biomass
        49/2190,      # CCGT
        49/2190,      # Oil
        49/2190,      # Geothermal
        1/3.6,      # Onwind https://www.mdpi.com/1996-1073/10/11/1904
        1/11.2,      # Solar https://www.sciencedirect.com/science/article/pii/S0360544219313234
        33/1460,      # ROR 
        33/1460       # Hydro
    ])

    lambdas_ttf_adjusted = np.zeros(n_lines)
    mus_ttr_adjusted = np.zeros(n_lines)

    i = 0
    for i,row in line_lengths.iterrows():
        lambdas_ttf_adjusted[i] = row['Length'] * lambdas_ttf[0]
        mus_ttr_adjusted[i] = lambdas_ttr[0] 
        i += 1

    lambdas_ttf_expanded = np.concatenate([
        lambdas_ttf_adjusted,
        np.repeat(lambdas_ttf[1:], [n_OCGT, n_biomass, n_CCGT, n_oil, n_geo, n_solar, n_onwind, n_ror, n_hydro])
    ])
    mus_ttr_expanded = np.concatenate([
        mus_ttr_adjusted,
        np.repeat(lambdas_ttr[1:], [n_OCGT, n_biomass, n_CCGT, n_oil, n_geo, n_solar, n_onwind, n_ror, n_hydro])
    ])
  

    States_Raw = monte_carlo_simulation_multi_component(8760, lambdas_ttf_expanded, mus_ttr_expanded)
    states_df = pd.DataFrame(States_Raw)
    states_df_transposed = states_df.T

    states_df_transposed.insert(0, 'datetime', datetime_column) 

    df_lines = states_df_transposed.iloc[:, :n_lines + 1]

    start_generators = n_lines + 1
    end_generators = start_generators + n_oil + n_ror + n_geo + n_biomass + n_onwind + n_solar + n_OCGT + n_CCGT
    df_generators = states_df_transposed.iloc[:, np.r_[0, start_generators:end_generators]]

    start_storage_units = end_generators
    end_storage_units = start_storage_units + n_hydro
    df_storage_units = states_df_transposed.iloc[:, np.r_[0, start_storage_units:end_storage_units]]

    mapping = {i: name for i, name in enumerate(all_indices)}

    df_lines.rename(columns=mapping, inplace=True)
    df_generators.rename(columns=mapping, inplace=True)
    df_storage_units.rename(columns=mapping, inplace=True)

    # Overwriting matrix files
    # df_lines.to_csv('matrices/lines_matrix.csv', index=False)
    # df_generators.to_csv('matrices/generators_matrix.csv', index=False)
    # df_storage_units.to_csv('matrices/storage_units_matrix.csv', index=False)
    
    # # Saving matrix file for all iterations
    # df_lines.to_csv('matrices/lines_matrix_' + str(iteration) + '.csv', index=False)
    # df_generators.to_csv('matrices/generators_matrix_' + str(iteration) + '.csv', index=False)
    # df_storage_units.to_csv('matrices/storage_units_matrix_' + str(iteration) + '.csv', index=False)


def rename_results_file(iteration):
    current_location = 'results/networks/'
    old_filename = "elec_s_all_ec_lcopt_Co2L-1H.nc"
    new_filename = f"network_{iteration}.nc"
    new_location = 'network_check/'

    # Create the full paths for the old and new files
    old_file_path = os.path.join(current_location, old_filename)
    new_file_path = os.path.join(new_location, new_filename)

    # Rename the file
    os.rename(old_file_path, new_file_path)


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

def yearly_changes(n,year):
    # ------- EMISSIONS -------
    #n.global_constraints.constant = emission_limit[year]

    # ------- GENERATOR EXTENSTION -----
    solved_network = 'network_bnze_2040/BNZE_2040.nc'
    m = pypsa.Network(solved_network)
    additional_exp= m.generators.p_nom_opt - m.generators.p_nom
    # replace negative values with 0
    for index, value in additional_exp.items():
        if value < 0:
            additional_exp[index]=0
    # add expansion to previous network
    n.generators.p_nom = n.generators.p_nom.add(additional_exp, fill_value=0)
    n.generators.p_nom_min = n.generators.p_nom_min.add(additional_exp, fill_value=0)
    #display(n.generators.p_nom)

    # ------- STORES ----------
    additional_stores = m.stores.e_nom_opt - m.stores.e_nom
    additional_stores
    n.stores.e_nom = n.stores.e_nom.add(additional_stores, fill_value = 0)
    n.stores.e_nom_min = n.stores.e_nom_min.add(additional_stores, fill_value = 0)
    #display(n.stores.e_nom.sum())

    # ------- STORAGE UNITS -------
    addiional_storage = m.storage_units.p_nom_opt - m.storage_units.p_nom
    addiional_storage
    n.storage_units.p_nom = n.storage_units.p_nom.add(addiional_storage, fill_value = 0)
    n.storage_units.p_nom_min = n.storage_units.p_nom_min.add(addiional_storage, fill_value = 0)

    # ------- LINES -------
    additional_lines = m.lines.s_nom_opt - m.lines.s_nom
    additional_lines
    n.lines.s_nom = n.lines.s_nom.add(additional_lines, fill_value = 0)
    n.lines.s_nom_min = n.lines.s_nom_min.add(additional_lines, fill_value = 0)

    # ------- LINKS -------
    # additional_links = m.links.p_nom_opt - m.links.p_nom
    # additional_links
    # n.links.p_nom = n.links.p_nom.add(additional_links, fill_value = 0)
    # n.links.p_nom_min = n.links.p_nom_min.add(additional_links, fill_value = 0)

    n.lines.loc[n.lines.index,"s_nom_extendable"] = False
    n.generators.loc[n.generators.index,"p_nom_extendable"] = False
    n.stores.loc[n.stores.index,"e_nom_extendable"] = False
    n.links.loc[n.links.index,"p_nom_extendable"] = False

    # ------- SAVING ----------
    n.export_to_netcdf('networks/elec_s_all_ec_lcopt_Co2L-1H.nc')

n_simulations = 1

start_date = '2013-01-01'
datetime_column = pd.date_range(start='2013-01-01', periods=8760, freq='H')

n = pypsa.Network('network_bnze_2040/BNZE_2040.nc')
line_indices = list(n.lines.index)
generators = n.generators[~n.generators.carrier.str.contains('load')].carrier.unique()
generator_indices = []
for carrier in generators:
    generator_indices += list(n.generators.query(f"carrier == '{carrier}'").index)
storage_unit_indices = list(n.storage_units.index)
all_indices = line_indices + generator_indices + storage_unit_indices

line_lengths = []
for line in n.lines.index:
    line_lengths.append({'Line': line, 'Length': n.lines.loc[line, 'length']})
line_lengths_df = pd.DataFrame(line_lengths)


for iteration in range(n_simulations):
    n = pypsa.Network('network_bnze_2040/network_bnze_2040.nc')
    yearly_changes(n,2040)
    run_monte_carlo_simulation(iteration+1, all_indices, datetime_column, line_lengths_df)
    subprocess.run(['snakemake', '-j', '14', 'solve_all_networks'])
    rename_results_file(iteration+1)
