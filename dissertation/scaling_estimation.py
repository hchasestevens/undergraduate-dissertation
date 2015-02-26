# Find least mean squares
import random


def mean_square_error(xs, ys):
    square_errors = (
        (x - y) ** 2
        for x, y in
        zip(xs, ys)
    )
    return sum(square_errors) / float(len(xs))


def hill_climbing(func, iterations=20000):
    current = random.random()
    cur_error = func(current)
    #print cur_error
    for __ in xrange(iterations):
        change = random.random() / 20.
        if random.choice((True, False)):
            change *= -1
        new = max(0, min(1, change + current))
        new_error = func(new)
        if new_error < cur_error:
            current, cur_error = new, new_error
            #print '%.5f' % cur_error
    return current


def make_task(experimental, model):
    def scale(s):
        return mean_square_error(model, [i * s for i in experimental])
    return scale


if __name__ == '__main__':
    experimental = [0.6, 0.5, 0.8, 0.5]
    models = {
        'Rejection': [0.032, 0.0268, 0.0316, 0.026],
        'Repair': [0.3352, 0.2388, 0.3184, 0.2184],
        'Baseline': [0.0564, 0.0448, 0.0624, 0.0524]
    }
    for model_name, model in models.iteritems():
        task = make_task(experimental, model)
        scale = hill_climbing(task)
        print
        print model_name
        print 'Scale: ', 1. / scale
        print 'Error: ', '%.6f' % task(scale)
        print 'Model: ', ['%.3f' % i for i in model]
        print 'Exper: ', ['%.3f' % i for i in experimental]
        print 'ScMod: ', ['%.3f' % ((1. / scale) * i) for i in model]

