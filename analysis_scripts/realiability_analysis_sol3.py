import pypsa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import logging
import datetime
from collections import defaultdict, Counter

n_simulations = 100
path = '/mnt/beegfs/users/noraky/pypsa-earth-3/pypsa-earth/monte_carlo_networks_emissions/network_'
teal3 = '#527D77'
price_LL = 22000

# Helper functions

def get_snapshot_generation(network, first_date, second_date, carrier):
    if carrier == 'hydro':
        generation = network.storage_units_t.p_dispatch[first_date:second_date].groupby(network.storage_units.carrier, axis=1).sum()[carrier]
    elif carrier == 'battery' or carrier == 'H2':
        generation = network.stores_t.p.loc[first_date:second_date].groupby(network.stores.carrier, axis=1).sum()[carrier]
    else:
        generation = network.generators_t.p.loc[first_date:second_date].groupby(network.generators.carrier, axis=1).sum()[carrier]
    return generation

def get_snapshot_demand(network, first_date, second_date):
    demand = network.loads_t.p_set.loc[first_date:second_date].sum(axis=1)
    return demand

def calculate_lost_load(network, first_date="2013-01-01", second_date="2013-12-31"):
    CCGT = get_snapshot_generation(network, first_date, second_date, 'CCGT')
    OCGT = get_snapshot_generation(network, first_date, second_date, 'OCGT')
    Oil = get_snapshot_generation(network, first_date, second_date, 'oil')
    Geothermal = get_snapshot_generation(network, first_date, second_date, 'geothermal')
    Hydro = get_snapshot_generation(network, first_date, second_date, 'ror') + get_snapshot_generation(network, first_date, second_date, 'hydro')
    Wind = get_snapshot_generation(network, first_date, second_date, 'onwind')
    Solar = get_snapshot_generation(network, first_date, second_date, 'solar')
    Biomass = get_snapshot_generation(network, first_date, second_date, 'biomass')
    Battery = get_snapshot_generation(network, first_date, second_date, 'battery')
    demand = get_snapshot_demand(network, first_date, second_date)

    nbattery = [(i*-1) if i < 0 else 0 for i in Battery]
    pbattery = [i if i > 0 else 0 for i in Battery]

    nbattery_9 = [float(n) / 0.9 for n in nbattery]
    pbattery_9 = [float(n) * 0.9 for n in pbattery]

    LL = (demand.values + nbattery_9) - (CCGT + OCGT + Oil + Wind + Solar + Biomass + Hydro + pbattery_9 + Geothermal)
    return LL

def load_matrices(iteration):

    df_lines = pd.read_csv(f'/mnt/beegfs/users/noraky/pypsa-earth-3/pypsa-earth/matrices/lines_matrix_{iteration}.csv')
    df_generators = pd.read_csv(f'/mnt/beegfs/users/noraky/pypsa-earth-3/pypsa-earth/matrices/generators_matrix_{iteration}.csv')
    df_storage_units = pd.read_csv(f'/mnt/beegfs/users/noraky/pypsa-earth-3/pypsa-earth/matrices/storage_units_matrix_{iteration}.csv')
    
    # Assuming the datetime column is named 'datetime' and is the first column
    datetime_column = df_generators['datetime']

    # Drop the datetime column for concatenation
    df_generators = df_generators.drop(columns=['datetime'])
    df_lines = df_lines.drop(columns=['datetime'])
    df_storage_units = df_storage_units.drop(columns=['datetime'])
    
    # Concatenate the dataframes horizontally
    states_df = pd.concat([df_lines, df_generators, df_storage_units], axis=1)
    
    # Reinsert the datetime column at the beginning
    states_df.insert(0, 'datetime', datetime_column)
    
    return states_df

def get_top_lost_load_hours(all_LL_values, top_n_hours=100):
    all_LL_df = pd.DataFrame(all_LL_values, columns=['Lost_Load', 'Simulation', 'Hour', 'Datetime'])
    top_hours_df = all_LL_df.nlargest(top_n_hours, 'Lost_Load').reset_index(drop=True)
    return top_hours_df

def analyze_top_hours(top_hours_df):
    results = []
    for idx, row in top_hours_df.iterrows():
        iteration = int(row['Simulation'])
        hour = int(row['Hour'])
        datetime_value = row['Datetime']
        lost_load = row['Lost_Load']
        rank = idx + 1  # One-based ranking

        # Load the state matrices for the specific iteration
        states_df = load_matrices(iteration)
        states_at_hour = states_df.iloc[hour, 1:]  # Skip datetime column
        failed_components = states_at_hour[states_at_hour == 0].index.tolist()
        results.append([rank, iteration, datetime_value, lost_load, failed_components])

    return results

def analyze_lost_loads(all_LL_values, state_matrices, n_simulations):
    component_caused_ll = defaultdict(list)
    multiple_components_caused_ll = defaultdict(list)
    yearly_component_lost_load = defaultdict(list)
    yearly_combination_lost_load = defaultdict(list)

    for iteration in range(1, n_simulations + 1):
        yearly_lost_load = defaultdict(float)
        yearly_combination_load = defaultdict(float)
        for ll, iter_num, hour, datetime_value in all_LL_values:
            if iter_num != iteration:
                continue
            if ll > 0:
                states_df = state_matrices[iteration]
                states_at_hour = states_df.iloc[hour, 1:]  # Skip datetime column
                failed_components = states_at_hour[states_at_hour == 0].index.tolist()

                if len(failed_components) == 1:
                    component = failed_components[0]
                    component_caused_ll[component].append(ll)
                    yearly_lost_load[component] += ll
                else:
                    multiple_components_caused_ll[tuple(failed_components)].append(ll)
                    yearly_combination_load[tuple(failed_components)] += ll

        for component, lost_load in yearly_lost_load.items():
            yearly_component_lost_load[component].append(lost_load)

        for combination, lost_load in yearly_combination_load.items():
            yearly_combination_lost_load[combination].append(lost_load)

        tot_component_caused_ll = {component: np.sum(lost_loads) for component, lost_loads in yearly_component_lost_load.items()}
        tot_multiple_components_caused_ll = {components: np.sum(lost_loads) for components, lost_loads in yearly_combination_lost_load.items()}

    return component_caused_ll, multiple_components_caused_ll, tot_component_caused_ll, tot_multiple_components_caused_ll


def calculate_LL_occurence(LL):
    time_LL = 0
    for i in LL:
        if i > 1:
            time_LL += 1
    return time_LL

def get_indices():
    n = pypsa.Network('/mnt/beegfs/users/noraky/pypsa-earth-3/pypsa-earth/network_bnze_2040/BNZE_2040.nc')
    line_indices = list(n.lines.index)
    generators = n.generators[~n.generators.carrier.str.contains('load')].carrier.unique()
    generator_indices = []
    for carrier in generators:
        generator_indices += list(n.generators.query(f"carrier == '{carrier}'").index)
    storage_unit_indices = list(n.storage_units.index)
    all_indices = line_indices + generator_indices + storage_unit_indices
    return all_indices

def total_ll_node(network,loads):
    LL = network.generators_t.p[loads].sum()
    return LL / 1e3 # MWh

def time_ll_node(network, loads):
    LL = network.generators_t.p[loads] / 1e3  # Convert to MWh
    time_LL = pd.DataFrame(0, index=loads, columns=['Times Load Loss'])
    for load in loads:
        time_LL.loc[load, 'Times Load Loss'] = calculate_LL_occurence(LL[load])
    return time_LL

total_LL = 0
time_LL = 0
LL_values = []
LL_ranges = {}
n_Hr = 8760
all_LL_values = []
first_date = datetime.datetime(2013, 1, 1)
loads_indices = pypsa.Network(path + '1.nc').generators.query('carrier == "load"').index
total_nodal_LL = pd.DataFrame(0, index=loads_indices, columns=['Total Load Loss'])
times_nodal_LL = pd.DataFrame(0, index=loads_indices, columns=['Times Load Loss'])

for iteration in range(1,n_simulations+1):
    network = pypsa.Network(path + str(iteration) + '.nc')
    LL = calculate_lost_load(network)

    for hour in range(n_Hr):
        datetime_value = first_date + datetime.timedelta(hours=hour)
        all_LL_values.append([max(0,LL[hour]/1e3), iteration, hour, datetime_value])

    time_LL += calculate_LL_occurence(LL)

    current_LL = 0
    for i in LL:
        current_LL += max(0, i)
    print('LL ' + str(iteration) + ': ', current_LL/1e3)
    LL_values.append(current_LL/1e3)

    #LL per node
    nodal_LL = total_ll_node(network,loads_indices)
    total_nodal_LL['Total Load Loss'] += nodal_LL
    nodal_times_LL = time_ll_node(network, loads_indices)
    times_nodal_LL['Times Load Loss'] += nodal_times_LL['Times Load Loss']

    state_matrices = {}

for iteration in range(1, n_simulations + 1):
    state_matrices[iteration] = load_matrices(iteration)

component_caused_ll, multiple_components_caused_ll, tot_component_lost_load, tot_combination_lost_load = analyze_lost_loads(all_LL_values, state_matrices, n_simulations)
tot_component_caused_ll_df = pd.DataFrame(list(tot_component_lost_load.items()), columns=['Component', 'Lost Load'])
tot_multiple_components_caused_ll_df = pd.DataFrame([(components, avg_loss) for components, avg_loss in tot_combination_lost_load.items()], columns=['Components', 'Lost Load'])
component_caused_ll_df = pd.DataFrame(list(component_caused_ll.items()), columns=['Component', 'Lost Load'])

time_LL_df = pd.DataFrame([time_LL], columns=['Time LL'])
time_LL_df.to_csv('/mnt/beegfs/users/noraky/pypsa-earth-3/pypsa-earth/csa_results/time_LL_em.csv', index=False)

LL_df = pd.DataFrame(LL_values, columns=["LL Values"])
LL_df.to_csv('/mnt/beegfs/users/noraky/pypsa-earth-3/pypsa-earth/csa_results/LL_values_em.csv', index=False)

# Save the results to CSV files
tot_component_caused_ll_df.to_csv('/mnt/beegfs/users/noraky/pypsa-earth-3/pypsa-earth/csa_results/avg_component_caused_ll_em.csv', index=False)
tot_multiple_components_caused_ll_df.to_csv('/mnt/beegfs/users/noraky/pypsa-earth-3/pypsa-earth/csa_results/avg_multiple_components_caused_ll_em.csv', index=False)
total_nodal_LL.to_csv('/mnt/beegfs/users/noraky/pypsa-earth-3/pypsa-earth/csa_results/total_nodal_LL_em.csv')
times_nodal_LL.to_csv('/mnt/beegfs/users/noraky/pypsa-earth-3/pypsa-earth/csa_results/times_nodal_LL_em.csv')
component_caused_ll_df.to_csv('/mnt/beegfs/users/noraky/pypsa-earth-3/pypsa-earth/csa_results/component_caused_ll_em.csv', index=False)

print("Results saved to csv files")