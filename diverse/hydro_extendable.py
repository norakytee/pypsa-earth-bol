import pypsa
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess

def extend_hydro(n):
    # ALREADY EXISTING HYDRO
    
    n.add("Generator",
        '2', # name of the new unit
        bus = '40',
        carrier = 'ror',
        p_nom = 55,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 55
        )
    
    n.add("Generator",
        '3', # name of the new unit
        bus = '40',
        carrier = 'ror',
        p_nom = 69,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 69
        )
    
    n.add("Generator",
        '6', # name of the new unit
        bus = '30',
        carrier = 'ror',
        p_nom = 6.81,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 6.81
        )
    
    n.add("Generator",
        '7', # name of the new unit
        bus = '58',
        carrier = 'ror',
        p_nom = 22.97,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 22.97
        )
    
    n.add("Generator",
        '9', # name of the new unit
        bus = '58',
        carrier = 'ror',
        p_nom = 10.69,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 10.69
        )
    
    n.add("Generator",
        '10', # name of the new unit
        bus = '58',
        carrier = 'ror',
        p_nom = 10.5,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 10.5
        )
    
    n.add("Generator",
        '11', # name of the new unit
        bus = '58',
        carrier = 'ror',
        p_nom = 25.39,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 25.39
        )
    
    n.add("Generator",
        '12', # name of the new unit
        bus = '58',
        carrier = 'ror',
        p_nom = 25.85,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 25.85
        )
    
    n.add("Generator",
        '13', # name of the new unit
        bus = '58',
        carrier = 'ror',
        p_nom = 28.02,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 28.02
        )
    
    n.add("Generator",
        '14', # name of the new unit
        bus = '58',
        carrier = 'ror',
        p_nom = 30.15,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 30.15
        )
    
    n.add("Generator",
        '20', # name of the new unit
        bus = '94',
        carrier = 'ror',
        p_nom = 50.79,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 50.79
        )
    
    n.add("Generator",
        '21', # name of the new unit
        bus = '50',
        carrier = 'ror',
        p_nom = 7.54,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 7.54
        )
    
    n.add("Generator",
        '22', # name of the new unit
        bus = '13',
        carrier = 'ror',
        p_nom = 11.49,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 11.49
        )
    
    n.add("Generator",
        '23', # name of the new unit
        bus = '13',
        carrier = 'ror',
        p_nom = 5.15,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 5.15
        )
    
    n.add("Generator",
        '24', # name of the new unit
        bus = '13',
        carrier = 'ror',
        p_nom = 2.4,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 2.4
        )
    
    n.add("Generator",
        '25', # name of the new unit
        bus = '83',
        carrier = 'ror',
        p_nom = 1.97,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 1.97
        )
    
    #PLANNED HYDRO
    n.add("Generator",
        '83-6 hydro', # name of the new unit
        bus = '83',
        carrier = 'ror',
        p_nom = 0,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 85
        )
 
    n.add("Generator",
        '83-7 hydro', # name of the new unit
        bus = '83',
        carrier = 'ror',
        p_nom = 0,
        marginal_cost = 0.0103746318,
        capital_cost = 270940.715282615,
        efficiency = 0.9,
        p_nom_extendable = True,
        p_nom_max = 118
        )
 
    n.add("StorageUnit",
        '37 hydro', # name of the new storage unit
        bus = '37',
        carrier = 'hydro',
        p_nom = 0,
        marginal_cost = 0.0106120929,
        capital_cost = 270940.715282615,
        efficiency_dispatch = 0.9,
        p_nom_extendable = True,
        p_nom_max = 290.2,
        max_hours = 6,
        p_min_pu = 0.0,
        efficiency_store = 0,
        cyclic_state_of_charge = True
        )