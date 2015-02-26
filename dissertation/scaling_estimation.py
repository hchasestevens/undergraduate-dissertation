# Find least mean squares
import random


def mean_square_error(xs, ys):
    square_errors = (
        (x - y) ** 2
        for x, y in
        zip(xs, ys)
    )
    return sum(square_errors) / float(len(xs))


def hill_climbing(func, iterations=10000):
    current = random.random()
    cur_error = func(current)
    print cur_error
    for __ in xrange(iterations):
        change = random.random() / 20.
        if random.choice((True, False)):
            change *= -1
        new = max(0, min(1, change + current))
        new_error = func(new)
        if new_error < cur_error:
            current, cur_error = new, new_error
            print '%.5f' % cur_error
    return current


def make_task(experimental, model):
    def scale(s):
        return mean_square_error(model, [i * s for i in experimental])
    return scale


if __name__ == '__main__':
    experimental = [2, 4, 6, 8]
    model = [1, 2, 3, 4]
    task = make_task(experimental, model)
    scale = hill_climbing(task)
    print
    print scale
    print 'Model: ', ['%.3f' % i for i in model]
    print 'ScExp: ', ['%.3f' % (scale * i) for i in experimental]

