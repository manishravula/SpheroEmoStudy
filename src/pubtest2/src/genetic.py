import random as rand
import numpy as np
import pickle
import time
import glob

# hyperparameters
INITIAL_POPULATION_SIZE = 20
STABLE_POPULATION_SIZE = 20
NUM_OFFSPRING = 10 # for each population for each generation
REPEAT_EVERY_N_GEN = 3 # repeat fitness evaluation
MUTATION_CHANCE = 0.1
NAME_PREFIX = 'ga_data/state_ga_'

# 12 different behaviors possible for each action
alleles = ['rest',
            'osc_small_slow','osc_small_fast',
            'jitter',
            'osc_large_slow','osc_large_fast',
            'spin_dir1_slow','spin_dir1_med','spin_dir1_fast',
            'spin_dir2_slow','spin_dir2_med','spin_dir2_fast']
NUM_ACTIONS = 3 # Number of actions for each pattern

# generator
# returns a uniformly distributed population
def generate_initial(num):
    pop = set()
    while len(pop) < num:
        pop.add(cyclepick(tuple([rand.randrange(len(alleles)) for i in range(NUM_ACTIONS)])))
    return pop

# chooses minimum element from equivalence class for rotation invariance
def cyclepick(pattern):
    minpat = pattern
    for n in range(NUM_ACTIONS-1):
        pattern = rotate(pattern)
        minpat = min(minpat,pattern)
    return minpat

def rotate(tup):
    return tup[1:]+(tup[0],)

def load():
    # TODO
    # return generation, pop1, pop2, pop3, fitness
    return get_latest_state()

def save(generation, pop1, pop2, pop3, fitness):
    # TODO
    obj = [generation,pop1,pop2,pop3,fitness]
    save_state(obj)
    return

def run_experiment(pattern):
    # TODO
    #print(pattern)
    #label = input("label: ")
    #value = input("value: ")
    #return int(label), int(value)
    return pattern[0]%3, sum(list(pattern))

def choice_curr(ls,weights,n_items):
    indices = np.arange(len(ls))
    normalized_weights = np.copy(weights).astype('float')/np.sum(weights)
    # print(np.sum(normalized_weights))

    chosen_indices = np.random.choice(indices,n_items,False,normalized_weights)
    chosen_elements =[]
    for idx in chosen_indices:
        chosen_elements.append(ls[idx])
    return chosen_elements

def get_latest_state():
    all_state_names = glob.glob(NAME_PREFIX+'*')
    all_state_names.sort()
    if len(all_state_names):
        latest_stateName = all_state_names[0]
        latest_state = pickle.load(open(latest_stateName,'r'))
        return latest_state
    else:
        return [1,set(),set(),set(),{}]


def save_state(obj):
    curr_timeStr = time.strftime("%Y%b%a:%d:%Y:%H:%M:%S")
    state_name = NAME_PREFIX+curr_timeStr
    pickle.dump(obj,open(state_name,'w+'))
    return




generation = 0
fitness = {}
pop1 = set()
pop2 = set()
pop3 = set()
pops = [pop1,pop2,pop3]
exp_list = set()
exp_count = 0



# main loop
while True:
    try:
        #What to load in the first time?
        generation, pop1, pop2, pop3, fitness = get_latest_state() #load() #TODO: Add back in when load is implemented
    except ValueError:
        print("Unpacking went wrong check the get_latest_function")
        break

    pops=[pop1,pop2,pop3]


    if len(pop1)*len(pop2)*len(pop3) is 0:
        # first iteration; must generate random populations
        for i in generate_initial(INITIAL_POPULATION_SIZE):
            fitness[i] = (0, 0, 0, 0)
            pop1.add(i)
            pop2.add(i)
            pop3.add(i)
    # check to see which experiments still need to be performed
    if len(exp_list) is 0:
        min_seen = generation // REPEAT_EVERY_N_GEN + 2
        # If an individual hasn't been seen the min number of times,
        # then add it to the exp_list
        for pop in pops:
            for i in pop:
                if fitness[i][3] < min_seen:
                    exp_list.add(i)
        # If exp_list is still empty, we are ready to replace
        if len(exp_list) is 0:
            generation += 1
            # first reduce all populations to STABLE_POPULATION_SIZE
            for pop in pops:
                label = pops.index(pop)
                ranked = sorted(pop, key=lambda i: -fitness[i][label])
                for i in ranked[STABLE_POPULATION_SIZE:]:
                    pop.remove(i)
            # now create offspring until at least NUM_OFFSPRING have been created
            for pop in pops:
                label = pops.index(pop)
                ranked = sorted(pop, key=lambda i: fitness[i][label])
                while len(pop) < STABLE_POPULATION_SIZE+NUM_OFFSPRING:
                    parents = choice_curr(ranked, range(len(ranked)), 2)
                    swapindex = rand.randrange(1,NUM_ACTIONS)
                    child1 = parents[0][:swapindex]+parents[1][swapindex:]
                    child2 = parents[1][:swapindex]+parents[0][swapindex:]
                    if rand.random() < MUTATION_CHANCE:
                        index = rand.randrange(NUM_ACTIONS)
                        if rand.random() < 0.5:
                            templist = list(child1)
                            templist[index] = rand.randrange(NUM_ACTIONS)
                            child2 = tuple(templist)
                        else:
                            templist = list(child2)
                            templist[index] = rand.randrange(NUM_ACTIONS)
                            child2 = tuple(templist)
                    for child in [child1,child2]:
                        child = cyclepick(child)
                        pop.add(child)
                        if child not in fitness:
                            fitness[child] = (0, 0, 0, 0)
    # pick an individual from exp_list and run the experiment
    else:
        current_exp = rand.sample(exp_list,1)[0]
        # labels: 0:happy, 1:sad, 2:confused
        label, value = run_experiment(current_exp)
        exp_count += 1
        fit0, fit1, fit2, n_seen = fitness[current_exp]
        fitness[current_exp] = ((n_seen*fit0 + value*(label==0))/(n_seen+1),
                                (n_seen*fit1 + value*(label==1))/(n_seen+1),
                                (n_seen*fit2 + value*(label==2))/(n_seen+1),
                                n_seen+1)
        if fitness[current_exp][3] >= generation // REPEAT_EVERY_N_GEN + 2:
            exp_list.remove(current_exp)
    # save(...) TODO
    save(generation,pop1,pop2,pop3,fitness)
    if generation == 100:
        break
for pop in pops:
    index = pops.index(pop)
    print(index,len(pop))
    for i in pop:
        print(fitness[i][index], i, fitness[i][3])
print(exp_count)
