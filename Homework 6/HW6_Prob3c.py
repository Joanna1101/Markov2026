## IMPORTS ################################################################
###########################################################################
import matplotlib.pyplot as plt
import numpy as np


## PLOT ###################################################################
###########################################################################
def plotstuff():
    N1 = 100
    K1 = int(N1/10)
    R0s = np.arange(0.5, 3, 0.01)
    rhojs1 = np.ones_like(R0s)
    sum1 = np.ones_like(R0s)
    
    for k in range(1, K1):
        rhojs1 = rhojs1*(N1/(R0s*(N1-k)))
        sum1 += rhojs1
    
    h1_1 = 1/sum1
    
    N2 = 1000
    K2 = int(N2/10)
    rhojs2 = np.ones_like(R0s)
    sum2 = np.ones_like(R0s)
    
    for k in range(1, K2):
        rhojs2 = rhojs2*(N2/(R0s*(N2-k)))
        sum2 += rhojs2
        
    h1_2 = 1/sum2
    
    fig, ax = plt.subplots(1, 2, figsize = (12, 5))
    ax[0].plot(R0s, 1-1/R0s, color = "lightskyblue", label = "1 - 1/R0")
    ax[0].plot(R0s, h1_1, '--', color = "royalblue", label = "Exact h1")
    ax[0].set_ylabel("h1 And Approximation")
    ax[0].set_xlabel("R0")
    ax[0].legend()
    ax[0].set_title("N = 100")
    ax[1].plot(R0s, 1-1/R0s, color = "palegreen", label = "1 - 1/R0")
    ax[1].plot(R0s, h1_2,'--',  color = "green", label = "Exact h1")
    ax[1].set_ylabel("h1 And Approximation")
    ax[1].set_xlabel("R0")
    ax[1].legend()
    ax[1].set_title("N = 1000")
    plt.savefig("HW6_P3c.png")
    
    

## MAIN ###################################################################
###########################################################################
if __name__ == "__main__":
    plotstuff()