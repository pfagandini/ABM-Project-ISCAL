import mesa

class agent(mesa.Agent):
    
    def __init__(self, unique_id, model):

        super().__init__(unique_id, model)

        self.wealth = 1

    def step(self):

        print(f"Hi, I am an agent, you can call me {str(self.unique_id)}.")