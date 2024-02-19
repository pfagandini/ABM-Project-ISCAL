from model import model
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

samples = 1
agents = 10
steps = 5

wealth_list = []
political_view_list = []
moral_behavior_list = []
consumption_list = []

wealth = []
political_view = []
moral_behavior = []
consumption = []

for j in range(samples):
    mymodel = model(agents)

    for a in mymodel.schedule.agents:
        wealth.append(a.wealth)
        political_view.append(a.political_view)
        moral_behavior.append(a.moral_behavior)
        consumption.append(a.consumed)
        
    wealth_list.append(wealth)
    political_view_list.append(political_view)
    moral_behavior_list.append(moral_behavior)
    consumption_list.append(consumption)    
        
    wealth = []
    political_view = []
    moral_behavior = []
    consumption = []

    for i in range(steps):
        print(f'run {j} step {i}')
        mymodel.step()

        wealth = []
        political_view = []
        moral_behavior = []
        consumption = []

        for a in mymodel.schedule.agents:
            wealth.append(a.wealth)
            political_view.append(a.political_view)
            moral_behavior.append(a.moral_behavior)
            consumption.append(a.consumed)

        wealth_list.append(wealth)
        political_view_list.append(political_view)
        moral_behavior_list.append(moral_behavior)
        consumption_list.append(consumption)

####################
#   Get the data   #
####################

results = mymodel.datacollector.get_model_vars_dataframe()