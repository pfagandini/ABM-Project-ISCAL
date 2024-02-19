from model import model
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

samples = 1
agents = 10
steps = 5

for j in range(samples):
    mymodel = model(agents)

    for _ in range(steps):
        mymodel.step()

####################
#   Get the data   #
####################

results = mymodel.datacollector.get_model_vars_dataframe()

results.to_csv('results.csv')