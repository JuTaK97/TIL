import matplotlib.pyplot as plt
import numpy as np

def draw(start=1,end=4, linsp=3001, size=0.2) :

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
     
        plt.scatter([a]*len(final_states), final_states,
                    color='k', s=size/len(final_states))

    plt.show()

  
##Problem 1
draw()
