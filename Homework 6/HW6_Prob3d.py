## IMPORTS ################################################################
###########################################################################
import matplotlib.pyplot as plt
import numpy as np

## MAIN ###################################################################
###########################################################################
def solvesystem():
    N=100
    K=10
    gamma=1
    delt = 0.005
    R0s = [0.5, 0.8, 1.5, 3]
    EDT = 0 # i promise i use this later

    for R0 in R0s:    
        print(f"\n\nR0 = {R0}")
        beta = R0*gamma/N
        A = np.zeros((K-1, K-1))
        b = np.ones(K-1)
        
        for n in range(1, K):
            p = beta*n*(N-n)*delt
            q = gamma*n*delt 
            A[n-1, n-1] = p+q
            
            if n>1:
                A[n-1, n-2] = -q
                
            if n < K-1:
                A[n-1, n] = -p
                
        e = np.linalg.solve(A, b)
        print(f"e = {e}")
        print(f"e1 Delta t = {e[0]*delt:.5f}")
        
        if R0 == 1.5: EDT = e[0]*delt
        
    return EDT
    
## SIMULATION #############################################################
###########################################################################
def sim():
    N=100
    K=10
    gamma=1
    delt = 0.005
    R0 = 1.5
    beta = R0*gamma/N
    
    nsims = 10000
    Ts = []
    
    for i in range(nsims):
        # one infected person
        n = 1
        T = 0
        
        while 0 < n < K:
            p = beta*n*(N-n)*delt
            q = gamma*n*delt 
            u = np.random.rand()
            
            if u < p:
                n += 1
            elif u < p + q:
                n -= 1
            T += 1
        
        Ts.append(T)
    ET = np.mean(Ts)
    print(f"Estimated e1 delta t: {ET*delt}")
    return ET*delt
    

## MAIN ###################################################################
###########################################################################
if __name__ == "__main__":
    ETexact = solvesystem()
    ETsim = sim()
    
    print(f"Difference = {np.abs(ETexact-ETsim)}")