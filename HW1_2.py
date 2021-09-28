import matplotlib.pyplot as plt
import numpy as np

def draw(start=1,end=4, linsp=3001, dotsize=0.02, subplot=None) :

    bifur = 1024
    converge = 10000

    axis_a = np.linspace(start, end, linsp)

    for i, a in enumerate(axis_a) :
        
        x = np.random.rand(1)[0]
        for k in range(converge) :
            x = a*x*(1-x)

        final_states = []
        for k in range(bifur) :
            x = a * x * (1-x)
            if round(x,5) not in final_states :
                final_states.append(round(x,5))
            else :
                break

        subplot.scatter([a]*len(final_states), final_states,
                    color='k', s=dotsize/len(final_states))
    


##Problem 2
fig = plt.figure()

self0 = fig.add_subplot(2, 2, 1)
self0.axis([1, 4, 0, 1])

self1 = fig.add_subplot(2, 2, 2)
self1.axis([3, 3.678, 0.7287, 0.2722])

self2 = fig.add_subplot(2, 2, 3)
self2.axis([3.45122, 3.59383, 0.4105, 0.594])

self3 = fig.add_subplot(2, 2, 4)
self3.axis([3.54416, 3.57490, 0.5357, 0.4636])

draw(start=1, end=4, subplot=self0)
draw(start=3, end=3.678, dotsize=0.1, subplot=self1)
draw(start=3.45122, end=3.59383, dotsize=0.5, subplot=self2)
draw(start=3.54416, end=3.5749, dotsize=2.0, subplot=self3)
fig.show()
