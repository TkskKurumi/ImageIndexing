import random

rnd = random.random


def rate_diff(a, b):
    return max(a/b, b/a)


def random_interval(mingap=0.07, scale=1, integer=True):
    tmp = scale-mingap
    a, b = sorted([rnd()*tmp, rnd()*tmp])
    b += mingap
    if(integer):
        a, b = int(a), int(b)
    return a, b


def random_crop_box(w, h, max_aspect_ratio=2, min_size_ratio=0.05):
    min_size = min(w, h)*min_size_ratio
    le, ri = random_interval(mingap=min_size, scale=w)
    _w = ri-le
    up, lo = random_interval(mingap=min_size, scale=w)
    _h = lo-up
    while(rate_diff(_w, _h) > max_aspect_ratio):
        # crop box shouldn't be too slim
        le, ri = random_interval(mingap=min_size, scale=w)
        _w = ri-le
        up, lo = random_interval(mingap=min_size, scale=w)
        _h = lo-up
    return le, ri, up, lo
