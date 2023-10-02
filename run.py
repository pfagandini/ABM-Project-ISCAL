from model import model
import matplotlib.pyplot as plt

starter_model = model(10)

for i in range(10):
    starter_model.step()
    