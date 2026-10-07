## IMPORTS ################################################################
###########################################################################
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom

## PLOT ###################################################################
###########################################################################
def plotstuffb(qn2, qn4, avgs):
    """
    plots stuff for part b :)
    """
    
    ns = np.arange(0, 61)
    plt.plot(ns, qn2, 'o-', markersize = 5, color = 'violet', label = "q_n(2)")
    plt.plot(ns, qn4, 'o-', markersize = 5, color = "darkorange", label = "q_n(4)")
    plt.plot(ns, avgs, 'o-', markersize = 5, color = "blueviolet", label = "Running Avg")
    plt.xlabel("n = 0, ... , 60")
    plt.ylabel("q_n(i) And Average")
    plt.title("Distribution At Time n")
    plt.legend()
    plt.savefig("HW5_P1b.png")
    plt.close()
    
def plotstuffc(qn2, pi, qn2_old, avgs):
    """
    plots stuff for part c :)
    """
    ns = np.arange(0, 61)
    pi2 = np.full(61, pi[2])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    ax1.plot(ns, qn2, 'o-', markersize = 5, color = 'turquoise', label = "q_n(2)")
    ax1.plot(ns, pi2, '--', color = 'seagreen', label = "pi(2)")
    ax1.set_xlabel("n = 0, ... , 60")
    ax1.set_ylabel("Distribution At Time n")
    ax1.legend()
    ax1.set_title("a = 0.3, b = 0.1")
    
    ax2.plot(ns, qn2_old, 'o-', markersize = 5, color = 'violet', label = "q_n(2)")
    ax2.plot(ns, avgs, 'o-', markersize = 5, color = 'blueviolet', label = "Running Avg")
    ax2.set_xlabel("n = 0, ... , 60")
    ax2.set_ylabel("Distribution At Time n")
    ax2.legend(loc = 'upper right')
    ax2.set_title("a = b = 1")
    
    plt.tight_layout()
    plt.savefig("HW5_P1c.png")
    plt.close() 
    

## COMPUTE ################################################################
###########################################################################
def makeP(K, a, b):
    """
    Makes tridiagonal P following given rules
    Theoretically, should work for any K, a, b
    """
    p = np.zeros((K+1, K+1))
   
    for k in range(K+1):
        if k < K:
            p[k][k+1] = a*(4-k)/(4)
            
        if k > 0:
            p[k][k-1] = b*(k/4)
        
        p[k][k] = 1 - np.sum(p[k])

    print("p = ")
    print(p)
    return p

def computeQn():
    """
    Computes Qn for n=1, ... 60
    Outputs: q50.....(list) 50th 
             q51.....(list) 51st
             plot....(figures) qn2, qn4 on same plot. running avg separate. 
    """
    a = b = 1
    q0 = [1, 0, 0, 0, 0]
    p = makeP(4, a, b)
    q50 = []
    q51 = []
    qn2 = []
    qn4 = []
    avgs = []
    
    
    for n in range(61):
        qn = q0@np.linalg.matrix_power(p, n)
        qn2.append(qn[2])
        qn4.append(qn[4])
        
        # qn2 will only contain k <= n
        avg = 1/(n+1)*np.sum(qn2)
        avgs.append(avg)
        
        if n == 50: q50 = qn
        elif n == 51: q51 = qn
    
    plotstuffb(qn2, qn4, avgs)
    print("\n q_50 = ")
    print(q50)
    print("\n q_51 = ")
    print(q51)
        

def computePi():
    """
    Computes stationary distribution
    Recomputes qn
    """
    a = 0.3
    b = 0.1
    K = 4
    q0 = [1, 0, 0, 0, 0]
    qn2 = []
    qn2_old = []
    avgs = []
    
    p1 = makeP(4, 1, 1)
    P = makeP(4, a, b)
    I = np.eye(K)
    
    # deal with redundancy
    A = P.T - np.eye(K+1)
    A[-1, :] = 1
    
    bs = np.zeros(K+1)
    bs[-1] = 1
    
    pi = np.linalg.solve(A, bs)
    print(f"\npi:\n {pi}")
    
    theta = a/(a+b)
    pi_exact = binom.pmf(np.arange(5), 4, theta)
    print(f"\npi (a):\n {pi_exact}")
    
    print("\nsum ||pi - pi_exact||:")
    diff_pi = np.linalg.norm(pi-pi_exact)
    print(np.sum(diff_pi))
    
    # Plot qns against each other
    for n in range(61):
        qn_old = q0@np.linalg.matrix_power(p1, n)
        qn2_old.append(qn_old[2])
        
        qn = q0@np.linalg.matrix_power(P, n)
        qn2.append(qn[2])
        
        avg = 1/(n+1)*np.sum(qn2_old)
        avgs.append(avg)
        
    plotstuffc(qn2, pi, qn2_old, avgs)
    
    # Find the smallest n
    qn2s_again = []
    diffs = []
    for n in range(1000):
        qn = q0@np.linalg.matrix_power(P, n)
        diff = np.linalg.norm(qn-pi)
        qn2s_again.append(qn[2])
        diffs.append(diff)
        
        if np.max(diff) < 1e-6:
            print(f"\nSmallest n: {n}")
            print(f"\nqn = {qn}")
            break
        
    # eigs
    eigs = np.linalg.eigvals(P)
    print(f"\nEigenvalues: {np.abs(eigs)}")
    
    sorted_eigs = np.sort(np.abs(eigs))[::-1] # reverse order large --> smol
    second = sorted_eigs[1]
    print(f"\n Second Largest: {second}")
    
    ns = np.arange(137)
    geom = lambda n: (0.9)**n
    plt.semilogy(ns, diffs, color = 'seagreen', label = "Error")
    plt.semilogy(ns, geom(ns), '--', color = 'turquoise', label = '(0.9)^n')
    plt.xlabel("n = 0, ... , 136")
    plt.ylabel("||qn - pi||")
    plt.title("Convergence of q_n to pi")
    plt.legend()
    plt.tight_layout()
    plt.savefig("HW5_P1c2.png")
    plt.close()

            
    
    
## MAIN ###################################################################
###########################################################################
if __name__ == "__main__":
    # computeQn()
    computePi()