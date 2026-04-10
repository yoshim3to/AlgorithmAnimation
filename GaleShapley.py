import sys
import random

def gale_shapley_generator(men_pref, women_pref):
    free_men = list(men_pref.keys())
    engaged = {}  # woman -> man
    proposals = {man: 0 for man in men_pref}

    while free_men:
        man = free_men.pop(0)
        if proposals[man] >= len(men_pref[man]):
            continue
            
        woman = men_pref[man][proposals[man]]
        proposals[man] += 1
        
        accepted = False
        rejected_man = None

        if woman not in engaged:
            engaged[woman] = man
            accepted = True
        else:
            current_man = engaged[woman]
            if women_pref[woman].index(man) < women_pref[woman].index(current_man):
                engaged[woman] = man
                free_men.append(current_man)
                accepted = True
                rejected_man = current_man
            else:
                free_men.append(man)
                accepted = False
                rejected_man = man

        yield {
            "proposer": man,
            "proposee": woman,
            "accepted": accepted,
            "rejected_man": rejected_man,
            "engaged": dict(engaged),
            "done": False
        }

    yield {
        "engaged": dict(engaged),
        "done": True
    }

class GaleShapley:
    def __init__(self, women_pref, men_pref, free_men, engaged, proposals):
        self.women_pref = women_pref
        self.men_pref = men_pref
        self.free_men = free_men
        self.engaged = engaged
        self.proposals = proposals
    def step(self, graph):
        if not self.free_men:
            return graph, None, None
        man = self.free_men.pop(0)
        if self.proposals[man] >= len(self.men_pref[man]):
            return graph, None, None ##no more women to propose to
        
        woman = self.men_pref[man][self.proposals[man]]
        self.proposals[man] += 1

        if woman not in self.engaged:
            self.engaged[woman] = man
            removed_edge = None
            new_edge = (man, woman)
        else:
            current_man = self.engaged[woman]
            if self.women_pref[woman].index(man) < self.women_pref[woman].index(current_man):
                self.engaged[woman] = man
                self.free_men.append(current_man)
                removed_edge = (current_man, woman) # for deleting edge in animation
                new_edge = (man, woman)

            else:
                self.free_men.append(man)
                removed_edge = None
                new_edge = None ##no new edge, just rejected

    ##Build the new graph
        new_graph = {node: [] for node in list(graph.keys())}
        for w, m in self.engaged.items():
            new_graph[m].append(w)
            new_graph[w].append(m)

        return new_graph, removed_edge, new_edge

##The global state of the algorithm

# men_pref = {
#     'A': random.sample(['F', 'G', 'H', 'I', 'J'], 5),
#     'B': random.sample(['G', 'F', 'I', 'H', 'J'], 5),
#     'C': random.sample(['H', 'I', 'F', 'G', 'J'], 5),
#     'D': random.sample(['I', 'H', 'G', 'F', 'J'], 5),
#     'E': random.sample(['J', 'I', 'H', 'G', 'F'], 5)
#     }

# women_pref = {
#     'F': random.sample(['A', 'B', 'C', 'D', 'E'], 5),
#     'G': random.sample(['B', 'A', 'D', 'C', 'E'], 5),
#     'H': random.sample(['C', 'D', 'A', 'B', 'E'], 5),
#     'I': random.sample(['D', 'C', 'B', 'A', 'E'], 5),
#     'J': random.sample(['E', 'D', 'C', 'B', 'A'], 5)
# }
# free_men = ['A', 'B', 'C', 'D', 'E']
# engaged = {} ##this will be woman -> man
# proposals = {man: 0 for man in men_pref} ##this will track which woman each man will propose to next

##Example usage

# if __name__ == "__main__":
# graph = {node: [] for node in "ABCDEFGHIJ"}
# big_steppa = GaleShapley(women_pref, men_pref, free_men, engaged, proposals)
# steps = 0
# while free_men and steps < 20: ##safety to prevent infinite loop
#     graph, removed_edge, new_edge = big_steppa.step(graph)
#     steps += 1
#     print(f"Step {steps}: New edge added: {new_edge}, Current engagements: {engaged}")
# print("Final engagements:", big_steppa.engaged)
