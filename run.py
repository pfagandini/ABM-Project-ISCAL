from model import model
import matplotlib.pyplot as plt
import seaborn as sns

samples = 100
agents = 100
steps = 10

wealth = []
politlca_view = []
moral_behavior = []
consumption = []
tax = []

for j in range(samples):
    mymodel = model(agents)

    for i in range(steps):
        print(f'run {j} step {i}')
        mymodel.step()