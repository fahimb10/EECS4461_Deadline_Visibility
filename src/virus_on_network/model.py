import mesa
import networkx as nx
from .agents import State, VirusAgent

def number_state(model, state):
    return sum(1 for a in model.agents if a.state is state)

def number_infected(model):
    return number_state(model, State.INFECTED)

def number_susceptible(model):
    return number_state(model, State.SUSCEPTIBLE)

def number_resistant(model):
    return number_state(model, State.RESISTANT)

class VirusOnNetwork(mesa.Model):
    def __init__(
        self,
        num_nodes=10,
        avg_node_degree=3,
        initial_outbreak_size=1,
        virus_spread_chance=0.4,
        virus_check_frequency=0.4,
        recovery_chance=0.3,
        gain_resistance_chance=0.5,
        seed=None,
    ):
        super().__init__(seed=seed)
        self.num_nodes = num_nodes
        prob = avg_node_degree / self.num_nodes
        self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
        self.grid = mesa.space.NetworkGrid(self.G)

        self.initial_outbreak_size = (
            initial_outbreak_size
            if initial_outbreak_size <= num_nodes
            else num_nodes
        )
        self.virus_spread_chance = virus_spread_chance
        self.virus_check_frequency = virus_check_frequency
        self.recovery_chance = recovery_chance
        self.gain_resistance_chance = gain_resistance_chance

        for node in self.G.nodes():
            agent = VirusAgent(
                self,
                State.SUSCEPTIBLE,
                self.virus_spread_chance,
                self.virus_check_frequency,
                self.recovery_chance,
                self.gain_resistance_chance,
            )
            self.grid.place_agent(agent, node)

        # infect initial outbreak
        infected_nodes = self.random.sample(list(self.G.nodes()), self.initial_outbreak_size)
        for a in self.grid.get_cell_list_contents(infected_nodes):
            a.state = State.INFECTED

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Infected": number_infected,
                "Susceptible": number_susceptible,
                "Resistant": number_resistant,
            }
        )
        self.datacollector.collect(self)

    def step(self):
        self.agents.do("step")
        self.datacollector.collect(self)
