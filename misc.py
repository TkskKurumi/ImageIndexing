import random
rnd=random.random
def random_interval(mingap=0.1):
    tmp=1-mingap
    a,b=sorted([rnd()*tmp,rnd()*tmp])
    b+=mingap
    return a,b
