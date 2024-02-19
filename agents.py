import mesa
import numpy as np
import random
from scipy.stats import pareto, truncnorm

class agent(mesa.Agent):
    
    def __init__(self, unique_id, model):

        super().__init__(unique_id, model)

        ###################
        ### Parameters ###
        ###################

        # Wealth distribution parameter: The higher, the higher the inequality
        inequality_wealth = 2 
 
        # Skills distribution parameter: The higher, the higher the inequality
        inequality_skills = 2 
        weight_gen_skills = 0.5 # theta in the paper

        # Qualities and varieties parameters
        self.qualities = 10 # Q in the paper
        varieties = 10 # J in the paper

        # Own good pricing parameters
        a = 1 # a in the paper
        alpha = 1 # alpha in the paper

        # Connectivity limits, parameters
        self.min_connectivity = 2 # This is the N^0 of the paper
        self.max_connectivity = self.model.num_agents - 1 # This is the \tilde{N} of the paper.

        #################
        ### Vars Init ###
        #################
 
        self.wealth = pareto.rvs(inequality_wealth)

        self.gen_skills = (self.wealth * (1 - weight_gen_skills) + pareto.rvs(inequality_skills) * weight_gen_skills)

        self.sp_skills = np.round(np.random.default_rng().uniform(0.5 , varieties + 0.5) , 0)

        self.pref_low = np.round(np.random.default_rng().uniform(0.5 , varieties + 0.5) , 0)

        self.pref_high = np.round(np.random.default_rng().uniform(0.5 + self.pref_low , varieties + 0.5) , 0)

        # Connectivity will be updated later, once everyone has already gotten their wealth
        self.connectivity = -1

        self.animal_spirits = truncnorm.rvs(-1,1)

        self.moral_behavior = truncnorm.rvs(-1,1)

        self.political_view = truncnorm.rvs(-1,1)

        self.price = a * self.gen_skills ** alpha

        ######################
        ### Auxiliary Vars ###
        ######################

        self.past_wealth = 0

        self.max_consumption = 0
        self.consumed = 0

        self.revenue = 0

        self.my_friends = [] # list of contacts

    def get_friends(self):
        
        aux_agents = [a for a in self.model.schedule.agents]
        aux_agents.remove(self)
        random.shuffle(aux_agents)

        return aux_agents[0 : min(int(self.connectivity), self.max_connectivity)]
    
    def propensity_to_consume(self):
        c_l = 0.1 # paper's c_l
        c_h = 0.9 # paper's c_h

        a = 0.5 # a in the paper

        return 0.5*((c_h + c_l)+(c_h - c_l)*(np.arctan(a/2*self.animal_spirits))/(np.arctan(a/2)))

    def update_connectivity(self):
        w = 0.5 # w in the paper
        b = 0.5 # b in the paper

        self.connectivity = self.connectivity + np.round((w * (self.wealth - self.past_wealth) + b * self.moral_behavior ) * self.connectivity)
        if self.connectivity > self.model.num_agents:
            self.connectivity = self.max_connectivity

        elif self.connectivity < 1:
            self.connectivity = self.min_connectivity

        if np.isnan(self.connectivity):
            self.connectivity = self.min_connectivity

    def update_animal_spirits(self, friends):

        def gamma(x):
            ga = 0.5 # gamma constant in the paper
            if x < 0:
                return -ga * (1+x)
            elif x == 0 :
                return 0
            else:
                return ga * (1-x)
        
        g = 0.5 # g constant in the paper

        Am_temp = []

        for a in friends:
            Am_temp.append(a.animal_spirits)

        Am = np.mean(Am_temp)

        self.animal_spirits = self.animal_spirits + g * (Am - self.animal_spirits) + gamma(self.animal_spirits)

    def update_moral_behavior(self, friends):

        z = 0.5 # constant z in the paper
        
        def zeta(x):
            zet = 0.5 # constant greez zeta in the paper

            if x < 0 :
                return -zet * (1+x)
            elif x == 0:
                return 0
            else:
                return zet * (1-x)

        Bm = np.mean([a.moral_behavior for a in friends])

        self.moral_behavior = self.moral_behavior + z * (Bm - self.moral_behavior) + zeta(self.moral_behavior)

    def update_political_view(self, friends):

        x = 0.5 # constant x in the paper

        def omega(x):
            ome = 0.5
            if x == 0:
                return 0
            if x < 0:
                return - ome * (1+x)
            else:
                return ome * (1-x)

        Xm_temp = []

        for a in friends:
            Xm_temp.append(a.political_view)

        Xm = np.mean(Xm_temp)

        self.political_view = self.political_view + x*(Xm-self.political_view) + omega(self.political_view)

        return 0

    def update_wealth(self):  
        new_wealth = self.revenue + self.wealth * (1 + self.model.interest_rate) - self.consumed
        self.past_wealth = self.wealth
        self.wealth = new_wealth
    
########################################################################
    ##### Actually the move of the agents, crucial for the order ####   
########################################################################

    def step(self):

        self.my_friends = self.get_friends()

        self.my_friends.sort(key = lambda x: x.connectivity, reverse = True)

        self.max_consumption = self.propensity_to_consume() * self.wealth
        self.consumed = 0
        self.revenue = 0

        for a in self.my_friends:
            if (self.max_consumption - self.consumed > a.price) and (a.sp_skills >= self.pref_low) and (a.sp_skills <= self.pref_high):
                self.consumed += a.price
                a.revenue += a.price