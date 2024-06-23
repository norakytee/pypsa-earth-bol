import pandas as pd

n_sims = 100
n_hours = 8760  # total hours in a year

# Initialize a dictionary to hold the sum of failures for each line across all simulations
failures_per_line = {}

# Read and process each simulation
for i in range(1, n_sims + 1):
    line_matrix = pd.read_csv(f'matrices/lines_matrix_{i}.csv')
    
    # Process each line in the matrix
    for line in line_matrix.columns[1:]:  # Skip the datetime column
        if line not in failures_per_line:
            failures_per_line[line] = 0  # Initialize if not already present
        # Count the number of failures (where the state is 0)
        failures_this_sim = line_matrix[line].value_counts().get(0, 0)
        failures_per_line[line] += failures_this_sim

# Calculate average failures per line over all simulations and output
for line in failures_per_line:
    average_failures = failures_per_line[line] / n_sims
    print(f"{line}: Average Failures = {average_failures}")


failures_per_generator = {}

for i in range(1,n_sims+1):
    generator_matrix = pd.read_csv('matrices/generators_matrix_' + str(i) + '.csv')

    for generator in generator_matrix.columns[1:]:
        if generator not in failures_per_generator:
            failures_per_generator[generator] = 0
        failure_this_sim_gen = generator_matrix[generator].value_counts().get(0,0)
        failures_per_generator[generator] += failure_this_sim_gen

for generator in failures_per_generator:
    average_failures = failures_per_generator[generator] / n_sims
    print(f"{generator}: Average Failures = {average_failures}")


failures_per_storage_unit = {}

for i in range(1,n_sims+1):
    storage_unit_matrix = pd.read_csv('matrices/storage_units_matrix_' + str(i) + '.csv')

    for storage_unit in storage_unit_matrix.columns[1:]:
        if storage_unit not in failures_per_storage_unit:
            failures_per_storage_unit[storage_unit] = 0
        failure_this_sim_storage = storage_unit_matrix[storage_unit].value_counts().get(0,0)
        failures_per_storage_unit[storage_unit] += failure_this_sim_storage

for storage_unit in failures_per_storage_unit:
    average_failures = failures_per_storage_unit[storage_unit] / n_sims
    print(f"{storage_unit}: Average Failures = {average_failures}")

