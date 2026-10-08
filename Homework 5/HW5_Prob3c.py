## IMPORTS ################################################################
###########################################################################
import matplotlib.pyplot as plt
import numpy as np


## PLOT ###################################################################
###########################################################################
def plotrms(rms, T, pi):
    """
    plots stuff
    """
    rms = np.array(rms)
    ts = np.arange(0, T, 1)
    plt.loglog(ts, rms, color = "violet", label = "RMSE")
    
    # slope
    fit_ts = np.arange(10**2, 10**5)
    logts = np.log(fit_ts)
    logrms = np.log( rms[(ts >= 10**2)&(ts <= 10**5)])
    m, b = np.polyfit(logts, logrms, 1)
    fit = np.exp(b)*fit_ts**m
    
    plt.loglog(fit_ts, fit, '--', color = "seagreen", label = f"Fitted Slope: {b:.4f}")
    
    # pi_6 thing
    thing = np.sqrt(pi[6]*(1-pi[6])/(ts+1))
    plt.loglog(ts, thing, color = "darkorange", label = "sqrt(pi_6(1-pi_6)/T)")
    
    plt.xlabel('Steps T')
    plt.ylabel('RMSE')
    plt.legend()
    plt.tight_layout()
    plt.savefig("HW5_Prob3c_RMSE.png")
    plt.close()
    
def plotbar(est, pi, T):
    """
    bar chart thingie
    """
    pages = np.arange(1, 9, 1)
    plt.bar(pages, est, color = "plum", edgecolor = "blueviolet", label = "Surfer 1")
    plt.bar(pages, pi, color = "mediumaquamarine", width = 0.3, edgecolor = "seagreen", label = "pi")
    plt.xlabel("Page Number")
    plt.ylabel("Number of times visited ")
    plt.title("Surfer 1's distribution vs pi")
    plt.legend()
    plt.tight_layout()
    plt.savefig("HWt_Prob3c_Bar.png")
    

    
## SIMULATE ###############################################################
###########################################################################
def surf(R, T, G, pi):
    """
    Runs R surfers on G for T steps.
    Outputs: idk lol
    """
    # how much time each surfer spends on each page
    counts = np.zeros((R, 8))
    surfers = np.zeros(R, dtype = int)
    t = 0
    rmss = []
    
    while t < T:
        r = np.random.rand(R)
        cdf = np.cumsum(G[surfers], axis=1) # row = cdf for one surfer
        surfers = np.sum(r[:, None] > cdf, axis = 1)
        counts[np.arange(R), surfers] += 1
        
        hat_pi = counts/(t+1)
        errs = np.max(np.abs(hat_pi - pi), axis = 1)
        rms = np.sqrt(np.mean(errs**2))
        rmss.append(rms)
        t += 1
        
    hat_pi = counts/T
    
    return hat_pi, rmss
        
    
    
## RUN STUFF ##############################################################
###########################################################################
def runStuff():
    P = np.array([[0, 1/2, 1/2, 0, 0, 0, 0, 0],
                    [0, 0, 1/2, 1/2, 0, 0, 0, 0],
                    [1/2, 0, 0, 0, 1/2, 0, 0, 0],
                    [1/3, 0, 1/3, 0, 1/3, 0, 0, 0],
                    [0, 1/3, 0, 0, 0, 1/3, 1/3, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 1, 0]], dtype = float)
    d = 0.85
    G = d*P+((1-d)/(8))*np.ones((8,8))
    
    # Params of surfing
    R = 100
    T = 10**5
    
    # exact pi
    A = G.T - np.eye(8)
    A[-1, :] = 1
    bs = np.zeros(8)
    bs[-1] = 1
    pi = np.linalg.solve(A, bs)

    # surf wheeeeeeeee
    hat_pi, rms = surf(R, T, G, pi)
    print(f"hatpi = {hat_pi}")
    
    plotrms(rms, T, pi)
    plotbar(hat_pi[0], pi, T)
    
    
    
    
    
## MAIN ###################################################################
###########################################################################
if __name__ == "__main__":
    runStuff()