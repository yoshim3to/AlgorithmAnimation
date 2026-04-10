import sys

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

