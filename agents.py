import mesa

class agent(mesa.Agent):
    
    def __init__(self, unique_id, model):

        super().__init__(unique_id, model)

        self.wealth = 1

    def step(self):

        if self.wealth > 0:
            other_agent = self.random.choice(self.model.schedule.agents)
            if other_agent is not None:
                other_agent.wealth = other_agent.wealth + 1
                self.wealth = self.wealth - 1

        #print(f"Hi, I am an agent, you can call me {str(self.unique_id)}. My wealth is {self.wealth}.")