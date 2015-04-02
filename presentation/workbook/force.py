from pylab import *
import numpy as np

r = np.array([ 0.5,  1. ,  1.5,  2. ,  2.5,  3. ,  3.5,  4. ,  4.5,  5. ,  5.5,
        6. ,  6.5,  7. ,  7.5,  8. ,  8.5,  9. ,  9.5])
gbest_force = 1.
pbest_force = 1.
gbest = np.array([4, 5])
pbest = np.array([8, 2])
coords = [[gbest_force * (gbest - np.array([x, y])) + pbest_force * (pbest - np.array([x, y])) for x in r] for y in r]
xs = np.array([[x for x, y in ar] for ar in coords])
ys = np.array([[y for x, y in ar] for ar in coords])
q = quiver(xs, ys)
scatter([gbest[0] * 1.9], [gbest[1] * 1.9], s=500, c='r', marker='*')
scatter([pbest[0] * 1.9], [pbest[1] * 1.9], s=500, c='b', marker='*')
ylim([0, 18])
xlim([0, 18])
xticks([])
yticks([])
show()
