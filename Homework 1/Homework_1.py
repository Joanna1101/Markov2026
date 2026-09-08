## IMPORTS ##########################################
#####################################################
import numpy as np
import matplotlib.pyplot as plt

## Monte Carlo #####################################
####################################################
def monte_carlo(X, Y, Z):
    """
    does things frfr
    Inputs:  X, Y, Z....(ints) sampled from U ~(0,1)
    Outputs: 1 if point accepted, 0 else.
    """
    bound1 = X**2+Y**2
    bound2 = X*Y
    
    if bound1 < Z and bound2 < Z**2:
        return 1
    else: 
        return 0
   
   
## Main ############################################
####################################################
if __name__ == "__main__":
    N = 100
    count = 0
    estimates = []
    
    for i in range(1, N+1):
        X, Y, Z = np.random.rand(3)
        count += monte_carlo(X,Y,Z)
        estimates.append(count/i)
        i += 1
          
    plt.axhline(y=(23*np.pi)/192, color = "teal", label = "23 pi / 192")
    plt.plot(range(1, N+1), estimates, color = "lightseagreen", linewidth = 1, label = "MC Estimates")
    plt.xscale("log")
    plt.xlabel("N")
    plt.ylabel("Monte Carlo Estimate")
    plt.title(f"Convergence of Monte Carlo Estimate, N={N}")
    plt.legend()
    plt.savefig(f"HW1_Monte Carlo_{N}.png")
        
    