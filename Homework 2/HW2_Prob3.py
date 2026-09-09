## IMPORTS ##########################################
#####################################################
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable


## Plotting #########################################
#####################################################
def plothist(accepted, name):
    """
    Plots normalized histogram with f(x) overlaid
    Inputs:  accepted....(list) accepted samples
             name........(string) desired plot name
    Outputs: name.png
    """
    f = lambda x: x*np.exp(-x)
    # TODO
    plt.plot(accepted)
    plt.savefig(f"{name}.png")
    # Pinks I Thinks tee hee
    

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
    prev_accepted = 0
    accepted = []
    times = []
    while(len(accepted) < N):
        U1 = np.random.uniform()
        U2 = np.random.uniform()
        X = -(1/lam)*np.ln(U1)
        
        if (U2 <= (1/lam*c)*X*np.exp((lam-1)*X)):
            accepted.append(X)
            times.append(total-prev_accepted)
            prev_accepted = total
        total +=1 
        
    return accepted, times, total
    

## MAIN #############################################
#####################################################
if __name__ == "__main__":
    N = 10e4
    lambda1 = 0.5
    lambda2 = 0.2
    c1 = 4/np.e
    c2 = 1/(0.16*np.e)
    
    accepted1, times1, total1 = accept_reject(N, lambda1, c1)
    accepted2, times2, total2 = accept_reject(N, lambda2, c2)
    
    plothist(accepted1, r"$\lambda$ = 0.5")
    plothist(accepted2, r"$\lambda$ = 0.2")
    
    # empirical acceptance fraction
    fraction1 = len(accepted1)/len(total1)
    fraction2 = len(accepted2)/len(total2)
    
    # mean time per accepted sample
    mean1 = np.average(times1)
    mean2 = np.average(times2)
    
    # TODO: round numbers so dey look nice
    table = PrettyTable()
    table.fieldnames = [r"$\lambda$", "Empirical Fraction", "1/c", "Mean Time"]
    table.addrow([lambda1, fraction1, 1/c1, mean1])
    table.addrow([lambda2, fraction2, 1/c2, mean2])
    print(table)
