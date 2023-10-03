from model import model
import matplotlib.pyplot as plt
import seaborn as sns

for j in range(100):
    mymodel = model(100)

    for i in range(10):
        print(f'run {j} step {i}')
        mymodel.step()