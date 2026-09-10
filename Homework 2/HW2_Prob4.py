## IMPORTS ##########################################
#####################################################
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable

## PLOTTING #########################################
#####################################################
def plot_hist(data, a, lambdaf, lambdas):
    """
    Plots normalized histogram with f(x) overlaid
    Inputs:  data...................(list) 
             a, lambdaf, lambdas....(ints) parameters of f
    Outputs: prob4.png
    """
    # Making f
    xs = np.arange(0, max(data), 0.01)
    f = lambda x: a*lambdaf*np.exp(-lambdaf*x)+(1-a)*lambdas*np.exp(-lambdas*x)
    
    plt.plot(xs, f(xs), color = "indigo", label = "f(t)")
    plt.hist(data, bins=50, density = True, color='thistle', edgecolor = 'purple', label = "Times")
    plt.legend()
    plt.xlabel('Times')
    plt.ylabel('Frequency')
    plt.yscale("log")
    plt.title(f'Normalized Histogram vs f(t)')
    plt.savefig("prob4.png")
    plt.close()

## COMPOSITION ######################################
#####################################################
def composition(a, lambdaf, lambdas, N):
    """
    Generates samples from f by composition.
    Inputs:  a..........(float) P(choose first exponential)
             lambdaf....(float) parameter for first exponential
             lambdas....(float) parameter for second exponential
             N..........(int) number of samples
    Outputs: Ts.........(list) samples from f
    """
    nsamples = 0
    Ts = []
    while nsamples < N:
        U1 = np.random.uniform()
        if U1 < a:
            B=1
        else:
            B=0
        
        U2 = np.random.uniform()
        if B == 1:
            T = -(np.log(1-U2))/(lambdaf)
            Ts.append(T)
        else:
            T = -(np.log(1-U2))/(lambdas)
            Ts.append(T)
        
        nsamples +=1
    
    return Ts


## MAIN #############################################
#####################################################
if __name__ == "__main__":
    a = 0.9
    lambdaf = 1000
    lambdas = 10
    N = int(10e5)
    
    Ts = composition(a, lambdaf, lambdas, N)
    plot_hist(Ts, a, lambdaf, lambdas)
    
    theory_mean = a/lambdaf + (1-a)/lambdas
    emp_mean = np.sum(Ts)/N
    diff_mean = theory_mean - emp_mean
    
    theory_prob = a*np.exp(-lambdaf*50)+(1-a)*np.exp(-lambdas*50)
    emp_prob = np.mean(np.array(Ts)>50)
    diff_prob = theory_prob - emp_prob
    
    table = PrettyTable()
    table.field_names = ["Metric", "Theoretical", "Empirical", "Difference"]
    table.add_row(["Mean", round(theory_mean,8), round(emp_mean,8), f"{diff_mean:.8e}"])
    table.add_row(["P(T>50)", round(theory_prob,8), round(emp_prob,8), f"{diff_prob:.8e}"])
    print(table)
        