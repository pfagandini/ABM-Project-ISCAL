from model import model
import matplotlib.pyplot as plt
import xlsxwriter

workbook = xlsxwriter.Workbook('Data.xlsx')
worksheet_wealth = workbook.add_worksheet('wealth')
worksheet_political = workbook.add_worksheet('political')
worksheet_moral = workbook.add_worksheet('moral')
worksheet_consumption = workbook.add_worksheet('consumption')

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
        
###############
# Data Export #
###############

def trans(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]

wealth_list = trans(wealth_list)

ag = []
for i in range(0, agents):
    ag.append(str(f"Agent {i+1}"))
print(ag)

pe = []
for i in range(0, steps):
    pe.append(str(f"Period {i+1}"))
print(pe)

head = ['periods \ agents'] + ag

# Write the data.
worksheet_wealth.write_row(0 , 0 , head)
worksheet_wealth.write_row(1 , 0 , pe)

for i in range(0, len(ag)):
    print(i)
    worksheet_wealth.write_row(1 , i + 1 , wealth_list[i])

workbook.close()