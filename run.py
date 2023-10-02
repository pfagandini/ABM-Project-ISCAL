from model import model
import matplotlib.pyplot as plt
import seaborn as sns

all_wealth = []

for j in range(100):

    mymodel = model(200)

    for i in range(10):
        mymodel.step()

    for agent in mymodel.schedule.agents:
        all_wealth.append(agent.wealth)

g = sns.histplot(all_wealth, discrete = True)
g.set(title = "Wealth distribution", xlabel = "Wealth", ylabel = "Number of agents")
g.get_figure().savefig('Plots/wealth_distribution.png')