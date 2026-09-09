## IMPORTS ##########################################
#####################################################
import time
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable


## Plotting #########################################
#####################################################
def plothist(accepted, lam, name):
    """
    Plots normalized histogram with f(x) overlaid
    Inputs:  accepted....(list) accepted samples
             lam.........(float) lambda for naming
             name........(string) desired plot name
    Outputs: name.png
    """
    # Making f
    xs = np.arange(0, max(accepted), 0.01)
    f = lambda x: x*np.exp(-x) 
    
    plt.plot(xs, f(xs), color = "indigo", label = "f(x)")
    plt.hist(accepted, bins=50, density = True, color='thistle', edgecolor = 'purple', label = "Accepted Samples")
    plt.legend()
    plt.xlabel('Accepted Samples')
    plt.ylabel('Frequency')
    plt.title(f'Normalized Histogram vs f(x), \u03BB = {lam}')
    plt.savefig(f"{name}.png")
    plt.close()
    

## Acceptance-Rejection Method ######################
#####################################################
def accept_reject(N, lam, c):
    """
    A_R for f(x) = xe^(-x), g(x) = lam e^(-lam x)
    Inputs:  N...........(int) number of accepted samples
             lam.........(float) exponential parameter
             c...........(float) envelope constant
    Outputs: accepted....(list) accepted samples
             times.......(list) time btwn accepteds
             total.......(int) total number of samples
    """
    total = 0
    accepted = []
    start = time.perf_counter()
    
    while(len(accepted) < N):
        U1 = np.random.uniform(0,1)
        U2 = np.random.uniform(0,1)
        X = -(1/lam)*np.log(U1)
        
        if (U2 <= (1/(lam*c))*X*np.exp((lam-1)*X)):
            accepted.append(X)
        total +=1 
        
    end = time.perf_counter()
    elapsed = end-start
    
    return accepted, elapsed, total
    

## MAIN #############################################
#####################################################
if __name__ == "__main__":
    N = 10e4
    lambda1 = 0.5
    lambda2 = 0.2
    c1 = 4/np.exp(1)
    c2 = 1/(0.16*np.exp(1))
    
    accepted1, elapsed1, total1 = accept_reject(N, lambda1, c1)
    accepted2, elapsed2, total2 = accept_reject(N, lambda2, c2)
    
    plothist(accepted1, 0.5, "lambda=0.5")
    plothist(accepted2, 0.2, "lambda=0.2")
    
    # Empirical acceptance fraction
    fraction1 = len(accepted1)/total1
    fraction2 = len(accepted2)/total2
    
    # Mean Time
    mean1 = elapsed1/N
    mean2 = elapsed2/N

    # A Pretty Table :)
    table = PrettyTable()
    table.field_names = ["\u03BB", "Empirical Fraction", "1/c", "Mean Time"]
    table.add_row([lambda1, round(fraction1,4), round(1/c1,4), f"{mean1:.4e}"])
    table.add_row([lambda2, round(fraction2,4), round(1/c2,4), f"{mean2:.4e}"])
    print(table)
