## IMPORTS  #####################################################################################
#################################################################################################
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson

## PLOTTING #####################################################################################
#################################################################################################
def plothist(Ns_exp, Ns_poiss):
    """
    Compares histograms of N(1) and Poisson(4)
    """
    kmax = max(Ns_exp.max(), Ns_poiss.max())
    k = np.arange(kmax + 1)
    pmf = poisson.pmf(k, 4)
    
    fig, ax = plt.subplots(1, 2, figsize = (12, 5))
    ax[0].hist(Ns_exp, bins = np.arange(kmax+2)-0.5, density = True, alpha = 0.8, color = "paleturquoise", edgecolor = "teal", label = "Exponential Sim")
    ax[0].plot(k, pmf, color = "darkorchid", label = "Poisson(4) pmf")
    ax[0].set_title("Exponential Gaps")
    ax[0].legend()
    ax[1].hist(Ns_poiss, bins = np.arange(kmax + 2)-0.5, density = True, alpha = 0.8, color = "palegreen", edgecolor = "seagreen", label = "Poisson Sim")
    ax[1].plot(k, pmf, color = "darkorchid", label = "Poisson(4) pmf")
    ax[1].set_title("Poisson and Uniform")
    ax[1].legend()
    plt.tight_layout()
    plt.savefig("Histogrammys.png")
    plt.close()
    
def plotraster(meteors, name):
    """
    Plots realization as raster 
    """
    for j, arrivals in enumerate(meteors):
        plt.vlines(arrivals, j+0.5, j+1.5)
    plt.xlabel("time")
    plt.ylabel("realization")
    plt.title(f"Realization using {name} method")
    plt.savefig(f"HW7_P3_{name}.png")
    plt.close()
    
def gammaplot(T3):
    t = np.linspace(0, T3.max(), 500)
    f = 32*t**2*np.exp(-4*t)
    
    plt.hist(T3, bins = 100, density = True, alpha = 0.8, color = "lemonchiffon", edgecolor = "gold", label = "Simulation")
    plt.plot(t, f, color = "tomato", label = "Gamma density")
    plt.xlabel("T3")
    plt.ylabel("Density")
    plt.title("T3 Histogram vs Gamma(3,4)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("T3Gamma.png")
    plt.close()    
    
## SIMULATIONS ##################################################################################
#################################################################################################
def simexp(T, lam):
    """
    Simulates meteors via exponential gaps
    Inputs: T......(int) number of hours
            lam....(int) rate meteors/hour
    """
    Ns = np.zeros(T, dtype = int)
    rasters = []
    t = 0.0
    
    while t < T:
        # exponential waiting time
        t += np.random.exponential(1/lam)
        if t>= T: break
        
        hour = int(t)
        Ns[hour] += 1
        
        if hour < 10:
            rasters.append(t)
    return Ns, rasters
    
def simpoiss(T, lam):
    """
    Simulates meteors via poisson count + uniform points
    Inputs: T......(int) number of hours
            lam....(int) rate meteors/hour
    """
    Ns = np.random.poisson(lam, T)
    rasters = []
    
    for hour in range(min(10, T)):
        n = Ns[hour]
        arrivals = hour + np.random.uniform(0, 1, n) # as in part c
        rasters.extend(arrivals)
        
    return Ns, rasters
        


## MAIN #########################################################################################
#################################################################################################
if __name__ == "__main__":
    T = int(2*1e5)
    lam = 4
    
    Ns_exp, meteors_exp = simexp(T, lam)
    Ns_poiss, meteors_poiss = simpoiss(T, lam)
    
    # histograms of N(1) with Poisson(4) pmf
    plothist(Ns_exp, Ns_poiss)
    
    # mean, variance of N(1)
    print("Exp Method:")
    print(f"Mean = {Ns_exp.mean()}")
    print(f"Variance = {Ns_exp.var()}")
    
    print("Poisson Method:")
    print(f"Mean = {Ns_poiss.mean()}")
    print(f"Variance = {Ns_poiss.var()}")
    
    # plot 10 realizations of each as rasters
    plotraster(meteors_exp, "Exponential")
    plotraster(meteors_poiss, "Poisson")
    
    # compare histogram of T3 with gamma density
    sims = 200000
    X1 = np.random.exponential(scale = 1/4, size = sims)
    X2 = np.random.exponential(scale = 1/4, size = sims)
    X3 = np.random.exponential(scale = 1/4, size = sims)
    T3 = X1 + X2 + X3
    
    gammaplot(T3)
    
    # among hours with N(1) = 3, estimate P(N(1/2) = 0, E[T_1]), and correlation btwn counts in first and second half hour over all hours
    # Compute total variation dist btwn Binomial(t/delta t, lambda delta t) and poisson(lambda t) for t=1 and deltat = 1/10,...1/2000 and fit itsslope against delta t on log log