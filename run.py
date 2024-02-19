from model import model
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

samples = 1
agents = 100
steps = 200

for j in range(samples):
    mymodel = model(agents)

    for _ in range(steps):
        mymodel.step()

####################
#   Get the data   #
####################

results_model = mymodel.datacollector.get_model_vars_dataframe()
results_model.to_csv('results_model.csv')

results_agents = mymodel.datacollector.get_agent_vars_dataframe()
results_agents.to_csv('results_agents.csv')