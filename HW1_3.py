import matplotlib.pyplot as plt
import numpy as np

def Feigenbaum(num) :
    bifur = 2**(num+1)
    converge = 100000
    linsp = 300001

    axis_a = np.linspace(1, 4, linsp)
    F_points = []
    prev_len=1
    prev_a=1
    x0 = np.random.rand(1)[0]
    
    for i, a in enumerate(axis_a) :
        if(i%((linsp-1)/100)==0) :
            print('Process: {0}%'.format(100*i/(linsp-1)))

        x = x0
        for k in range(converge) :
            x = a*x*(1-x)

        final_states = set()
        for k in range(bifur) :
            x = a*x*(1-x)
            if round(x, 6) not in final_states :
                final_states.add(round(x, 6))
            else :
                break

        if len(final_states)==(2*prev_len) :
            F_points.append(round(prev_a,6))
            prev_len = len(final_states)
            if len(F_points) == num :
                break
        prev_a = a

    return F_points


#Problem 3
F_points = Feigenbaum(8)
for i, f in enumerate(F_points) :
    print('{0}th Feigenbaum point is {1}'.format(i+1, f))

for i, f in enumerate(F_points) :
    delta = (F_points[i+1]-F_points[i])/(F_points[i+2]-F_points[i+1])
    print('Feigenbaum constant = {0}'.format(delta))
    if i==len(F_points)-3 :
        break
