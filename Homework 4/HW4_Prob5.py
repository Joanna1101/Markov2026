## IMPORTS ###################################################################
##############################################################################
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable 

## PLOTTING ##################################################################
##############################################################################
def plotHist(Tfold, Tagg, name):
    """
    plots normalized histograms of T wrt folded or aggregated runs
    Inputs:  Tfold....(list) avg times to absorb in F
             Tagg.....(list) avg times to absorb in A
             name.....(string) name of plot
    Outputs: plotsies
    """
    Q = np.array([[0, 1/2, 1/2],
                 [1/4, 0, 0],
                 [3/4, 0, 0]])
    R = np.array([[0, 0],
                 [1/2, 1/4],
                 [0, 1/4]])

    pfold = 5/8
    pagg = 3/8
    
    maxT = max(max(Tfold), max(Tagg))
    ns = range(1, maxT+1)
    
    # PMFS:
    pmfFold = []
    exactF = []
    pmfAgg = []
    exactA = []
    
    for n in ns:
        pmfFold.append(Tfold.count(n)/len(Tfold))
        pmfAgg.append(Tagg.count(n)/len(Tagg))
        
        if n%2 == 0:
            exactF.append(0)
            exactA.append(0)
        else:
            QR = np.linalg.matrix_power(Q, n-1)@R
            exactF.append(QR[1,0]/pfold)
            exactA.append(QR[1,1]/pagg)
            
    plt.bar(list(ns), pmfFold, color = "blue", label = "Simulated Fold PMF")
    plt.bar([n+0.35 for n in ns], pmfAgg, color = "green", label = "Simulated Agg PMF")
    plt.plot(list(ns), exactF, color = "darkblue", label = "Exact Fold PMF")
    plt.plot(list(ns), exactA, color = "darkgreen", label = "Exact Agg PMF")
    plt.xlabel("Time To Absorption")
    plt.ylabel("Conditional Prob")
    plt.title("Distribution of Tau, X0 = I")
    plt.legend()
    plt.savefig(f"{name}.png")

## SIMULATE NORMAL CHAIN #####################################################
##############################################################################    
def chain(start, mat, N):
    """
    simulates a chain until absorbies
    Inputs:  start....(int) starting state where 0=U, 1=I, 2=M, 3=F or A
             mat......(np array) transition matrix
             N........(float) number of iterations
    Outputs: hX.......(float) how many end at f
             gX.......(float) avg absorb time
    """
    steps = []
    folds = 0
    
    for n in range (N):
        Xn = start
        nsteps = 0
        
        while Xn != 3 and Xn != 4 and Xn != 5:
            # choose state according to where r falls in the transition probs
            r = np.random.rand()
            cumulative = np.cumsum(mat[Xn])
            Xn = np.searchsorted(cumulative, r)  
            nsteps += 1
            
        if Xn == 3: folds += 1
        steps.append(nsteps)
    
    hX = folds/N
    gX = np.mean(steps)
    
    return hX, gX

## SIMULATE CONDITION CHAIN ################################################## 
############################################################################## 
def chainCond(start, mat, N):
    """
    simulates a chain until absorbies BUt conditioned on where absorbies
    Inputs:  start....(int) starting state where 0=U, 1=I, 2=M, 3=F or A
             mat......(np array) transition matrix
             N........(float) number of iterations
    Outputs: taux.....(float) absorb time
    """
    steps = []
    
    for n in range (N):
        Xn = start
        nsteps = 0
        while Xn != 3:
            # choose state according to where r falls in the transition probs
            r = np.random.rand()
            cumulative = np.cumsum(mat[Xn])
            Xn = np.searchsorted(cumulative, r)  
            nsteps += 1
        steps.append(nsteps)
    
    tauX = np.mean(steps)
    
    return tauX, steps
    
## MAIN ######################################################################
############################################################################## 
if __name__ == "__main__":
    N = 10000
    
    P = np.array([[0, 1/2 , 1/2 , 0 , 0 , 0],
         [1/4 , 0 , 0 , 1/2 , 0 , 1/4],
         [3/4 , 0 , 0 , 0 , 0 , 1/4],
         [0 , 0 , 0 , 3/4 , 1/4 , 0],
         [0 , 0 , 0 , 1/2 , 1/2 , 0],
         [0 , 0 , 0 , 0 , 0 , 1]])
    
    hU, gU = chain(0, P, N)
    hI, gI = chain(1, P, N)
    hM, gM = chain(2, P, N)
    print("did normal ok")
    
    Fmat = np.array([[0, 5/8, 3/8, 0],
            [1/5, 0, 0, 4/5],
            [1, 0, 0, 0],
            [0, 0, 0, 1]])
    
    Amat = np.array([[0, 3/8, 5/8, 0],
            [1/3, 0, 0, 2/3],
            [3/5, 0, 0, 2/5],
            [0, 0, 0, 1]])
    
    tauUF, _ = chainCond(0, Fmat, N)
    tauIF, foldTs  = chainCond(1, Fmat, N)
    tauMF, _ = chainCond(2, Fmat, N)
    tauUA, _ = chainCond(0, Amat, N)
    tauIA, aggTs = chainCond(1, Amat, N)
    tauMA, _ = chainCond(2, Amat, N)
    print("pretty plz")
    plotHist(foldTs, aggTs, "StateI")
    
    table = PrettyTable()
    table.field_names = ["Start", "hx", "gx", "tauxF", "tauxA"]
    table.add_row(["U", f"{hU}", f"{gU}", f"{tauUF}", f"{tauUA}"])
    table.add_row(["I", f"{hI}", f"{gI}", f"{tauIF}", f"{tauIA}"])
    table.add_row(["M", f"{hM}", f"{gM}", f"{tauMF}", f"{tauMA}"])
    print(table)

    