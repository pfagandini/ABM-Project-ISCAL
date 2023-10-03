from model import model
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

samples = 100
agents = 100
steps = 50

wealth = []
political_view = []
moral_behavior = []
consumption = []
tax = []

av_wealth = []
av_polit = []

for j in range(samples):
    mymodel = model(agents)

    av_wealth_aux = []

    for a in mymodel.schedule.agents:
        wealth.append(a.wealth)
        political_view.append(a.political_view)
        moral_behavior.append(a.moral_behavior)
        consumption.append(a.consumed)
        
    for i in range(steps):
        print(f'run {j} step {i}')
        mymodel.step()

        for a in mymodel.schedule.agents:
            wealth.append(a.wealth)
            political_view.append(a.political_view)
            moral_behavior.append(a.moral_behavior)
            consumption.append(a.consumed)

        av_wealth_aux.append(mymodel.av_wealth)
    
    av_wealth.append(av_wealth_aux)

av_wealth = [sum(sub_list) / len(sub_list) for sub_list in zip(*av_wealth)]
    
#################
# Data Analysis #
#################

ax = plt.plot(av_wealth)
plt.xlabel('Period (t)')
plt.ylabel('Av. Wealth')
plt.show()