import random
rnd = random.random


def random_interval(mingap=0.07, scale=1, integer=True):
    tmp = scale-mingap
    a, b = sorted([rnd()*tmp, rnd()*tmp])
    b += mingap
    if(integer):
        a, b = int(a), int(b)
    return a, b
