## IMPORTS ###########################################
######################################################
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
from scipy.optimize import fsolve


## MAIN ##############################################
######################################################
if __name__ == "__main__":
    Q = np.array([[-2, 2, 0, 0], [1, -3, 2, 0], [0, 2, -4, 2], [0, 0, 3, -3]])
    x0 = np.array([1,0,0,0])
    pi = np.array([3/19, 6/19, 6/19, 4/19])
    eigs, vecs = np.linalg.eig(Q)
    eigs = np.sort(np.real(eigs))
    lam1 = eigs[-2]
    
    print(f"Eigenvalues: {eigs}")
    print(f"Lambda 1 = {lam1}")
    
    time = np.linspace(0,5,500)
    X = np.array([x0@expm(t*Q) for t in time])
    TV = 0.5*np.sum(np.abs(X-pi), axis = 1)
    
    guess = fsolve(lambda t: 0.5*np.sum(np.abs(x0 @ expm(t[0]*Q)-pi)) - 0.01, x0 = 0)
    print(f"TV = 0.01 at t = {guess}")
    print(f"ln(100)/|lambda 2| = {np.log(100)/np.abs(lam1)}")
    
    plt.figure(figsize = (8,5))
    colors = ["darkgreen", "seagreen", "mediumseagreen", "springgreen"]
    for i in range(4):
        plt.semilogy(time, X[:, i]+1e-12, color = colors[i], label = f"x{i}")
        
    plt.semilogy(time, TV, color = "royalblue", label = "TV")
    
    line = TV[50]/np.exp(lam1*time[50])
    plt.semilogy(time, line*np.exp(lam1*time), "--", color = "fuchsia", label = "slope lambda 2")
    plt.xlabel("Time")
    plt.ylabel("xi(t) or TV(t)")
    plt.title("xi(t) and TV(t) for 4 states")
    plt.legend()
    plt.tight_layout()
    plt.savefig("3c.png")