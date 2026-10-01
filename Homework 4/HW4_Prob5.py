## IMPORTS ###################################################################
##############################################################################
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable 

## PLOTTING ##################################################################
##############################################################################
def plotHist(params, PMF, name, Fold = False, Agg = False):
    """
    plots normalized histograms of T wrt folded or aggregated runs
    Inputs:  params
    Outputs: plotsies
    """
    print("lol idk")

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
        
        while Xn != 3 and Xn != 4:
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
             P........(np array) transition matrix
             N........(float) number of iterations
    Outputs: taux.....(float) absorb time
    """
    steps = []
    
    for n in range (N):
        Xn = start
        nsteps = 0
        while Xn != 3 and Xn != 4:
            # choose state according to where r falls in the transition probs
            r = np.random.rand()
            cumulative = np.cumsum(P[Xn])
            Xn = np.searchsorted(cumulative, r)  
            nsteps += 1
        steps.append(nsteps)
    
    tauX = np.mean(steps)
    
    return tauX
    
## MAIN ######################################################################
############################################################################## 
if __name__ == "__main__":
    N = 10000
    
    P = [[0, 1/2 , 1/2 , 0 , 0 , 0],
         [1/4 , 0 , 0 , 1/2 , 0 , 1/4],
         [3/4 , 0 , 0 , 0 , 0 , 1/4],
         [0 , 0 , 0 , 3/4 , 1/4 , 0],
         [0 , 0 , 0 , 1/2 , 1/2 , 0],
         [0 , 0 , 0 , 0 , 0 , 1]]
    
    hU, gU = chain(0, P, N)
    hI, gI = chain(1, P, N)
    hM, gM = chain(2, P, N)
    
    Fmat = [[0, 5/8, 3/8, 0],
            [1/5, 0, 0, 4/5],
            [1, 0, 0, 0],
            [0, 0, 0, 1]]
    
    Amat = [[0, 3/8, 5/8, 0],
            [1/3, 0, 0, 2/3],
            [3/5, 0, 0, 2/5],
            [0, 0, 0, 1]]
    
    tauUF = chainCond(0, Fmat, N)
    tauIF = chainCond(1, Fmat, N)
    tauMF = chainCond(2, Fmat, N)
    tauUA = chainCond(0, Amat, N)
    tauIA = chainCond(1, Amat, N)
    tauMA = chainCond(2, Amat, N)
    
    table = PrettyTable()
    table.field_names["Start", "hx", "gx", "tauxF", "tauxA"]
    table.add_row(["U", f"{hU}", f"{gU}", f"{tauUF}", f"{tauUA}"])
    table.add_row(["I", f"{hI}", f"{gI}", f"{tauIF}", f"{tauIA}"])
    table.add_row(["M", f"{hM}", f"{gM}", f"{tauMF}", f"{tauMA}"])

    