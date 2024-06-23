
import pypsa
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess
import math


# # # Define paths
# home = "C:/Users/noraky/Documents/Masteroppgave/pypsa-earth/"
# master = "C:/Users/noraky/Documents/Masteroppgave/pypsa-earth/custom_files/"


# p_network = pypsa.Network(home + "networks/base.nc")

# # Load the Excel file with line capacity data
# lines_cap_df = pd.read_excel(master + "lines_capacity.xlsx")

# lines_cap_df.set_index(["Line"], inplace=True)

# power_factor = 0.9

# for idx, row in lines_cap_df.iterrows():
#     print(idx)
#     print(row["capacity"])
#     print(p_network.lines.loc[idx, 's_nom'])
#     if math.isfinite(row["capacity"]):
#         p_network.lines.at[idx, 's_nom'] = row['capacity'] * power_factor
#         p_network.lines.at[idx, 's_nom_min'] = p_network.lines.at[idx, 's_nom']

# p_network.export_to_netcdf(home + "networks/base_changed_lines.nc") 


# subprocess.run(['snakemake', '-j', '14', 'solve_all_networks', '--unlock'])
# subprocess.run(['snakemake', '-j', '14', 'solve_all_networks'])

# network = 'networks/elec_s_30_ec_lcopt_Co2L-1H.nc'
# n = pypsa.Network(network)
# n.export_to_netcdf('networks/elec_s_30_ec_lcopt_Co2L-1H-changed_lines.nc')

# network = 'networks/elec_s_30_ec_lcopt_Co2L-1H-changed_lines.nc'
# n = pypsa.Network(network)
# n.export_to_netcdf('networks/elec_s_30_ec_lcopt_Co2L-1H.nc')

# # Load the Excel file with line capacity data
# lines_cap = pd.read_excel("custom_files/lines_capacity.xlsx")

# lines_cap.set_index(["Line"], inplace=True)

# power_factor = 0.9

# for idx, row in lines_cap.iterrows():
#     if math.isfinite(row["capacity"]):
#         n.lines.at[idx, 's_nom'] = row['capacity'] * power_factor
#         n.lines.at[idx, 's_nom_min'] = n.lines.at[idx, 's_nom']

# n.export_to_netcdf('networks/base.nc')

network = 'networks/elec_s_30_ec_lcopt_Co2L-1H-changed_lines.nc'
n = pypsa.Network(network)
n.export_to_netcdf('networks/elec_s_30_ec_lcopt_Co2L-1H.nc')


scale_demand_period_ends = {
    2029: 1.199126092,
    2034: 1.192236139,
    2039: 1.225922909,
    'back':0.569269673, # scaling factor for scaling from 2035 to 2021
    'direct' : 1.7566367 # scaling factor from 2021 to 2035
}

scale_cost_sudden = {
    ('OCGT', 2025): 1.0,
    ('OCGT', 2026): 1.0,
    ('OCGT', 2027): 0.20,
    ('OCGT', 2028): 1.0,
    ('OCGT', 2029): 1.0,
    ('OCGT', 2030): 1.0,
    ('OCGT', 2031): 1.0,
    ('OCGT', 2032): 1.0,
    ('OCGT', 2033): 1.0,
    ('OCGT', 2034): 1.0,
    ('OCGT', 2035): 1.0,
    ('OCGT', 2036): 1.0,
    ('OCGT', 2037): 1.0,
    ('OCGT', 2038): 1.0,
    ('OCGT', 2039): 1.0,
    ('OCGT', 2040): 1.0,

    ('CCGT', 2025): 1.0,
    ('CCGT', 2026): 1.0,
    ('CCGT', 2027): 0.22,
    ('CCGT', 2028): 1.0,
    ('CCGT', 2029): 1.0,
    ('CCGT', 2030): 1.0,
    ('CCGT', 2031): 1.0,
    ('CCGT', 2032): 1.0,
    ('CCGT', 2033): 1.0,
    ('CCGT', 2034): 1.0,
    ('CCGT', 2035): 1.0,
    ('CCGT', 2036): 1.0,
    ('CCGT', 2037): 1.0,
    ('CCGT', 2038): 1.0,
    ('CCGT', 2039): 1.0,
    ('CCGT', 2040): 1.0,

    ('oil', 2025): 1.0,
    ('oil', 2026): 1.0,
    ('oil', 2027): 0.29,
    ('oil', 2028): 1.0,
    ('oil', 2029): 1.0,
    ('oil', 2030): 1.0,
    ('oil', 2031): 1.0,
    ('oil', 2032): 1.0,
    ('oil', 2033): 1.0,
    ('oil', 2034): 1.0,
    ('oil', 2035): 1.0,
    ('oil', 2036): 1.0,
    ('oil', 2037): 1.0,
    ('oil', 2038): 1.0,
    ('oil', 2039): 1.0,
    ('oil', 2040): 1.0,
}

scale_cost_gradual = {
    ('OCGT', 2025): 0.81,
    ('OCGT', 2026): 0.84,
    ('OCGT', 2027): 0.86,
    ('OCGT', 2028): 0.88,
    ('OCGT', 2029): 0.89,
    ('OCGT', 2030): 0.90,
    ('OCGT', 2031): 0.91,
    ('OCGT', 2032): 0.92,
    ('OCGT', 2033): 0.92,
    ('OCGT', 2034): 0.93,
    ('OCGT', 2035): 0.93,
    ('OCGT', 2036): 0.94,
    ('OCGT', 2037): 0.94,
    ('OCGT', 2038): 0.95,
    ('OCGT', 2039): 1,
    ('OCGT', 2040): 1,

    ('CCGT', 2025): 0.83,
    ('CCGT', 2026): 0.85,
    ('CCGT', 2027): 0.87,
    ('CCGT', 2028): 0.89,
    ('CCGT', 2029): 0.90,
    ('CCGT', 2030): 0.91,
    ('CCGT', 2031): 0.92,
    ('CCGT', 2032): 0.92,
    ('CCGT', 2033): 0.93,
    ('CCGT', 2034): 0.93,
    ('CCGT', 2035): 0.94,
    ('CCGT', 2036): 0.94,
    ('CCGT', 2037): 0.94,
    ('CCGT', 2038): 0.95,
    ('CCGT', 2039): 1,
    ('CCGT', 2040): 1,

    ('oil', 2025): 0.858,
    ('oil', 2026): 0.876,
    ('oil', 2027): 0.890,
    ('oil', 2028): 0.901,
    ('oil', 2029): 0.910,
    ('oil', 2030): 0.917,
    ('oil', 2031): 0.923,
    ('oil', 2032): 0.929,
    ('oil', 2033): 0.934,
    ('oil', 2034): 0.938,
    ('oil', 2035): 0.941,
    ('oil', 2036): 0.945,
    ('oil', 2037): 0.948,
    ('oil', 2038): 0.950,
    ('oil', 2039): 1,
    ('oil', 2040): 1,
}

decom = {
    2029: {'BO0 1 OCGT' : 16.84 + 15.99 + 57.14 + 55.97, 'BO0 5 OCGT': 49.76 + 51.37},
    2034: {'BO0 1 OCGT' : 18.1, 'BO0 5 OCGT' : 42.41 + 41.15, 'BO0 10 oil' : 1.1 + 1.12 + 1.12},
    2039: {'BO0 10 oil' : 1.1, 'BO0 28 oil' : 1.1, 'BO0 2 solar' : 5, 'BO0 11 onwind' : 14.4, 'BO0 1 onwind' : 39.6, 'BO0 19 onwind' : 50.4, 'BO0 11 biomass' : 21, 'BO0 25 ror' : 11.49, 'BO0 27 ror' : 6.81, 'BO0 1 OCGT' : 57 + 18.79, 'BO0 6 OCGT' : 1.49 + 1.49 + 1.6 + 1.55 + 1.51 + 1.6},
}
 
decom_storage = {
2029: {},
2034: {'BO0 18 hydro' : 2.55},
2039: {'BO0 18 hydro' : 6.2 + 6.23},
}


start_year = 2024
start_value = 2740892 #2784650 #2533122 #2728743
end_year = 2050
end_value = 0

years = range(start_year, end_year + 1)
emissions = []

decrease_per_year = (start_value - end_value) / (end_year - start_year)

for i in years:
    emission = max(start_value - decrease_per_year * (i - start_year), end_value)
    emissions.append(emission)

# Make into dict
index = np.arange(2024,2051)
emission_limit = dict(zip(index, emissions))
emission_limit


def read_network_file():
    network = 'networks/elec_s_30_ec_lcopt_Co2L-1H.nc'
    n = pypsa.Network(network)
    return n
   

# Function that implements 4 yearly changes

    
def yearly_changes_b(n,year,scen_folder,scen):
    print(year)
    # ------- DEMAND ---------
    upscaling_factor = scale_demand_period_ends[year]
    n.loads_t.p_set = n.loads_t.p_set * upscaling_factor    
    # ------- EMISSIONS -------
    #n.global_constraints.constant = emission_limit[year]
    # display(n.global_constraints.constant)

    #-------- COSTS ---------
    # indexes = {}
    # for car in ['OCGT', 'CCGT', 'oil']:
    #     mask = n.generators['carrier'] == car
    #     indexes[car] = n.generators.index[mask].tolist()
    # for car in indexes:
    #     n.generators.loc[indexes[car], 'marginal_cost'] = n.generators.loc[indexes[car], 'marginal_cost'] / scale_cost_sudden[(car, year)]

    # ------- GENERATOR EXTENSTION -----
    solved_network = f'{scen_folder}/{scen}_{year-5}.nc'
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
    additional_links = m.links.p_nom_opt - m.links.p_nom
    additional_links
    n.links.p_nom = n.links.p_nom.add(additional_links, fill_value = 0)
    n.links.p_nom_min = n.links.p_nom_min.add(additional_links, fill_value = 0)

    # ------- DECOM ---------
    for index,value in decom[year].items():
        n.generators.loc[index, 'p_nom'] = n.generators.loc[index].p_nom - value
        n.generators.loc[index, 'p_nom_min'] = n.generators.loc[index].p_nom_min - value

    # ------- HYDRO-DECOM-------- # is done seperately, because the  code is different
    for index,value in decom_storage[year].items():
        n.storage_units.loc[index,'p_nom'] = n.storage_units.loc[index].p_nom - value

    # ------- SAVING ----------
    n.export_to_netcdf('networks/elec_s_30_ec_lcopt_Co2L-1H.nc')

def extend_hydro_old(n):
    n.add("Generator",
        '83-6 hydro', # name of the new storage unit --> REAL NAME: UMA
        bus = 'BO0 18',
        carrier = 'ror',
        p_nom = 0,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 85
        )
 
    n.add("Generator",
        '83-7 hydro', # name of the new storage unit --> REAL NAME: PLD
        bus = 'BO0 18',
        carrier = 'ror',
        p_nom = 0,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 118
        )
   
    n.add("Generator",
        '37-1 hydro', # name of the new storage unit --> REAL NAME: JUN
        bus = 'BO0 5',
        carrier = 'ror',
        p_nom = 0,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 89.73
        )
 
    
def save_network_file(n):
    n.export_to_netcdf('networks/elec_s_30_ec_lcopt_Co2L-1H.nc')

# Function that renames the results file and moves it to the scenario folder

def rename_results_file(year, scen, scen_folder):
    current_location = 'results/networks/'
    old_filename = "elec_s_30_ec_lcopt_Co2L-1H.nc"
    new_filename = f"{scen}_{year}.nc"
    new_location = f'{scen_folder}/'

    # Create the full paths for the old and new files
    old_file_path = os.path.join(current_location, old_filename)
    new_file_path = os.path.join(new_location, new_filename)

    # Rename the file
    os.rename(old_file_path, new_file_path)



scen_folder = 'base_period_ends'
scen = 'B_wo_hydroex'

# run for loop over 4 years
for year in [2024, 2029, 2034, 2039]:
    n = read_network_file()
    if year == 2024:
        #extend_hydro_old(n)
        save_network_file(n)
        subprocess.run(['snakemake', '-j', '14', 'solve_all_networks', '--unlock'])
        subprocess.run(['snakemake', '-j', '14', 'solve_all_networks'])
        rename_results_file(year, scen, scen_folder)
    else:
        yearly_changes_b(n, year, scen_folder,scen)
        subprocess.run(['snakemake', '-j', '14', 'solve_all_networks'])
        rename_results_file(year, scen, scen_folder)

# def run_all_scen():
#     scenarios = ["base", "base_nze", "gc", "gc_nze", "sc", "sc_nze"]

#     for scen in scenarios:
#         network = 'networks/elec_s_30_ec_lcopt_Co2L-1H-changed_lines.nc'
#         n = pypsa.Network(network)
#         n.export_to_netcdf('networks/elec_s_30_ec_lcopt_Co2L-1H.nc')
#         if scen == "base":
#             scen_folder = 'base_004'
#             scen = 'B'
#             for year in range(2024, 2041):
#                 n = read_network_file()
#                 if year == 2024:
#                     extend_hydro_old(n)
#                     save_network_file(n)
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks', '--unlock'])
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks'])
#                     rename_results_file(year, scen, scen_folder)
#                 else:
#                     yearly_changes_base(n, year, scen_folder, scen)
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks'])
#                     rename_results_file(year, scen, scen_folder)
#         if scen == "base_nze":
#             scen_folder = 'base_nze_004'
#             scen = 'BNZE_'
#             for year in range(2024, 2041):
#                 n = read_network_file()
#                 if year == 2024:
#                     extend_hydro_old(n)
#                     save_network_file(n)
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks', '--unlock'])
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks'])
#                     rename_results_file(year, scen, scen_folder)
#                 else:
#                     yearly_changes_bnze(n, year, scen_folder, scen)
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks'])
#                     rename_results_file(year, scen, scen_folder)
#         if scen == "gc":
#             scen_folder = 'gc_004'
#             scen = 'GC'
#             for year in range(2024, 2041):
#                 n = read_network_file()
#                 if year == 2024:
#                     extend_hydro_old(n)
#                     save_network_file(n)
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks', '--unlock'])
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks'])
#                     rename_results_file(year, scen, scen_folder)
#                 else:
#                     yearly_changes_gc(n, year, scen_folder, scen)
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks'])
#                     rename_results_file(year, scen, scen_folder)
#         if scen == "gc_nze":
#             scen_folder = 'gc_nze_004'
#             scen = 'GCNZE'
#             for year in range(2024, 2041):
#                 n = read_network_file()
#                 if year == 2024:
#                     extend_hydro_old(n)
#                     save_network_file(n)
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks', '--unlock'])
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks'])
#                     rename_results_file(year, scen, scen_folder)
#                 else:
#                     yearly_changes_gcnze(n, year, scen_folder, scen)
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks'])
#                     rename_results_file(year, scen, scen_folder)
#         if scen == "sc":
#             scen_folder = 'sc_004'
#             scen = 'SC'
#             for year in range(2024, 2041):
#                 n = read_network_file()
#                 if year == 2024:
#                     extend_hydro_old(n)
#                     save_network_file(n)
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks', '--unlock'])
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks'])
#                     rename_results_file(year, scen, scen_folder)
#                 else:
#                     yearly_changes_sc(n, year, scen_folder, scen)
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks'])
#                     rename_results_file(year, scen, scen_folder)
#         if scen == "sc_nze":
#             scen_folder = 'sc_nze_004'
#             scen = 'SCNZE'
#             for year in range(2024, 2041):
#                 n = read_network_file()
#                 if year == 2024:
#                     extend_hydro_old(n)
#                     save_network_file(n)
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks', '--unlock'])
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks'])
#                     rename_results_file(year, scen, scen_folder)
#                 else:
#                     yearly_changes_scnze(n, year, scen_folder, scen)
#                     subprocess.run(['snakemake', '-j', '14', 'solve_all_networks'])
#                     rename_results_file(year, scen, scen_folder)
        

# run_all_scen()