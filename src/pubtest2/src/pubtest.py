#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import ColorRGBA, Float32, Bool
import numpy as np
import collections
import time
import copy
import random as rand
import random as rand
import numpy as np
import pickle
import time
import glob
from GUI import experiment as getFeedback
from DemoNotification import show_experiment_notification


PRIMITIVES_CONFIGS = collections.OrderedDict() #Ordered dict with values as [amplitudes,frequency]


#no movement
PRIMITIVES_CONFIGS['no_action']=[0,0,0]

#oscillatory movement
PRIMITIVES_CONFIGS['oscillate_smallAmp_slow']=[50,0,.5]
PRIMITIVES_CONFIGS['oscillate_smallAmp_medium']=[100,0,1]
PRIMITIVES_CONFIGS['oscillate_smallAmp_fast']=[300,0,3]

PRIMITIVES_CONFIGS['oscillate_largeAmp_slow']=[50,0,.25]
PRIMITIVES_CONFIGS['oscillate_largeAmp_medium']=[100,0,.5]

#spinning movement
PRIMITIVES_CONFIGS['spin_forward_slow'] =[25,25,.25]
PRIMITIVES_CONFIGS['spin_forward_medium'] = [50,50,.5]
PRIMITIVES_CONFIGS['spin_forward_fast'] = [100,100,1]

PRIMITIVES_CONFIGS['spin_backward_slow']=[25,-25,25]
PRIMITIVES_CONFIGS['spin_backward_medium']=[50,-50,.5]
PRIMITIVES_CONFIGS['spin_backward_fast']=[100,-100,1]

N_PRIMITIVES =  len(PRIMITIVES_CONFIGS)

DURATION_PRIMITIVE = 3 #sec

# hyperparameters
INITIAL_POPULATION_SIZE = 20
STABLE_POPULATION_SIZE = 20
NUM_OFFSPRING = 10 # for each population for each generation
REPEAT_EVERY_N_GEN = 3 # repeat fitness evaluation
MUTATION_CHANCE = 0.1
NAME_PREFIX = '/home/manish/Awesomestuff/classes/HRI-F-2k17/projectws/src/pubtest2/src/ga_data_'

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

COMMON_LOG = 'common_log'
USER_LOG = 'user_log'
USER_LOG_FILE = open('/home/manish/Awesomestuff/classes/HRI-F-2k17/projectws/src/pubtest2/src/logs/usr_log.txt','a')
COMMON_LOG_FILE = open('/home/manish/Awesomestuff/classes/HRI-F-2k17/projectws/src/pubtest2/src/logs/common_log.txt','a')

rospy.init_node('cmdtest',anonymous=True)
pub_velocity = rospy.Publisher('cmd_vel',Twist,queue_size=10)

GLOBAL_RATE = 100.0
rate = rospy.Rate(GLOBAL_RATE)


def execute_primitive(primitive_index):
    """

    :param: primitive_index is the index of the primitive motion to execute. It is an integer, ranging between 0,N_PRIMITIVES
    :return: True when done. False when Failed.
    """
    #Integer Check
    try:
        b = primitive_index+1
    except TypeError:
        print("Passed a non-integer when requested primitive_index {}".format(primitive_index))
        return False

    if b<0 or b>N_PRIMITIVES:
        print("Seeking for a primitive by specifying index larger than the library size. {}".format(primitive_index))
        return False

    configs = PRIMITIVES_CONFIGS.items()
    amp_sin, amp_cos, freq = configs[primitive_index][1]
    name = configs[primitive_index][0]
    print('Executing {}'.format(name))

    iter = 0
    start_time = time.time()

    try:
        while not rospy.is_shutdown() and (time.time()-start_time)<DURATION_PRIMITIVE:

            msg1 = Twist()
            msg1.linear.x = amp_cos*np.sin(iter * freq * np.pi * 2 / GLOBAL_RATE)
            msg1.linear.y = amp_sin*np.cos(iter * freq * np.pi * 2 / GLOBAL_RATE)

            iter += 1
            msg1.linear.z = 0
            msg1.angular.z = 0
            msg1.angular.y = 0
            msg1.angular.x = 0  # Same as above


            pub_velocity.publish(msg1)
            rate.sleep()
        return True

    except:
        print("Primitive not executed properly index - {}, name - {}".format(primitive_index,name))
        return False

def execute_sequence(primitiveIndex_list):
    """

    :param primitiveIndex_list: List of primitive indices (integers)
    :return:
    """

    try:
        a = primitiveIndex_list+[1]
    except TypeError:
        raise Exception("Didn't receive a list in the execute sequence function")

    try:
        for ele in copy.deepcopy(primitiveIndex_list):
            ele+=1

    except TypeError:
        raise Exception("Non integers passed as a primitive indices in the execute sequence function {}".format(ele))

    for primitiveMotion_index in primitiveIndex_list:

        ret_value=execute_primitive(primitiveMotion_index)
        print("executed the primitve action {}".format(primitiveMotion_index))
        if ret_value==False:
            print("Couldn't execute the primitive action {}".format(primitiveMotion_index))

    return



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


def run_experiment(pattern):
    # TODO
    #print(pattern)
    #label = input("label: ")
    #value = input("value: ")
    #return int(label), int(value)
    to_pattern = list(pattern)

    command_file = open("/home/manish/Awesomestuff/classes/HRI-F-2k17/projectws/flag.txt",'w+')
    command_file.write(str(to_pattern))
    command_file.close()

    show_experiment_notification()

    label,value = getFeedback()
    command_file = open("flag.txt", 'w+')
    # command_file.write('')
    command_file.close()

    USER_LOG_FILE.write("{} for USER {} and pattern {} the observed label,value are {} {} \n".format(time.asctime(),USER_ID,to_pattern,label,value))

    #TODO: check that the file is being written and saved properly.

    return label,value


def choice_curr(ls,weights,n_items):
    indices = np.arange(len(ls))
    normalized_weights = np.copy(weights).astype('float')/np.sum(weights)
    # print(np.sum(normalized_weights))

    chosen_indices = np.random.choice(indices,n_items,False,normalized_weights)
    chosen_elements =[]
    for idx in chosen_indices:
        chosen_elements.append(ls[idx])
    return chosen_elements





generation = 0
fitness = {}
pop1 = set()
pop2 = set()
pop3 = set()
pops = [pop1,pop2,pop3]
exp_list = set()
exp_count = 0

USER_ID = input('Enter the user ID: \n')


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
USER_LOG_FILE.close()
COMMON_LOG_FILE.close()

