import pypsa

n = pypsa.Network("C:/Users/noraky/Documents/Masteroppgave/pypsa-earth/networks/elec_s_all_ec_lcopt_Co2L_1H.nc")

n.add("Generator",
      '28 hydro',
      bus = '87', 
      carrier = 'ror',
      p_nom = 0, 
      marginal_cost = n.generators.loc['30'].marginal_cost,
      capital_cost = n.generators.loc['30'].capital_cost,
      efficiency = 0.9,
      p_num_extendable = True,
      p_max_pu = 0.5,
      p_nom_max = 85
      )

n.add("Generator",
      '29 hydro',
      bus = '87', 
      carrier = 'ror',
      p_nom = 0, 
      marginal_cost = n.generators.loc['30'].marginal_cost,
      capital_cost = n.generators.loc['30'].capital_cost,
      efficiency = 0.9,
      p_num_extendable = True,
      p_max_pu = 0.5,
      p_nom_max = 118
      )

n.add("StorageUnit",
      '30 hydro',
      bus = '37', 
      carrier = 'hydro',
      p_nom = 0, 
      marginal_cost = n.storage_units.loc['30'].marginal_cost,
      capital_cost = n.generators.loc['30'].capital_cost,
      efficiency = 0.9,
      p_num_extendable = True,
      p_max_pu = 0.5,
      p_nom_max = 290.2
      )