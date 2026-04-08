import sys

#Preferences this is just based off what was given from the animation file

men_pref = {
    'A': ['F', 'G', 'H', 'I', 'J'],
    'B': ['G', 'F', 'I', 'H', 'J'],
    'C': ['H', 'I', 'F', 'G', 'J'],
    'D': ['I', 'H', 'G', 'F', 'J'],
    'E': ['J', 'I', 'H', 'G', 'F']
    }

women_pref = {
    'F': ['A', 'B', 'C', 'D', 'E'],
    'G': ['B', 'A', 'D', 'C', 'E'],
    'H': ['C', 'D', 'A', 'B', 'E'],
    'I': ['D', 'C', 'B', 'A', 'E'],
    'J': ['E', 'D', 'C', 'B', 'A']
}

##The global state of the algorithm
free_men = ['A', 'B', 'C', 'D', 'E']
engaged = {} ##this will be woman -> man
proposals = {man: 0 for man in men_pref} ##this will track which woman each man will propose to next

def GaleShapely(graph):
    if not free_men:
        return graph, None
    man = free_men.pop(0)
    if proposals[man] >= len(men_pref[man]):
        return graph, None ##no more women to propose to
    
    woman = men_pref[man][proposals[man]]
    proposals[man] += 1

    if woman not in engaged:
        engaged[woman] = man
        new_edge = (man, woman)
    else:
        current_man = engaged[woman]
        if women_pref[woman].index(man) < women_pref[woman].index(current_man):
            engaged[woman] = man
            free_men.append(current_man)
            new_edge = (man, woman)

        else:
            free_men.append(man)
            new_edge = None ##no new edge, just rejected

##Build the new graph
    new_graph = {node: [] for node in "ABCDEFGHIJ"}
    for w, m in engaged.items():
        new_graph[m].append(w)
        new_graph[w].append(m)

    return new_graph, new_edge


##Example usage

##if __name__ == "__main__":
  ##  graph = {node: [] for node in "ABCDEFGHIJ"}
  ##  steps = 0
   ## while free_men and steps < 20: ##safety to prevent infinite loop
      ##  graph, new_edge = GaleShapely(graph)
      ##  steps += 1
      ##  print(f"Step {steps}: New edge added: {new_edge}, Current engagements: {engaged}")
    ##print("Final engagements:", engaged)
