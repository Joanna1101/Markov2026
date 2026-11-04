## IMPORTS ########################################################################
###################################################################################
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

## PLOTTING #######################################################################
###################################################################################
def plotmeans(Means):
    """
    Plots number of arrivals per hour averaged over 30 days against lambda(t)
    Inputs:  Means....(np array) list of means
    Outputs: plot
    """
    ts = np.arange(0.5, 24.5, 1) # center
    ts_fine = np.linspace(0, 23, 1440)
    lam = lambda t: 12+8*np.cos(np.pi*(t-16)/12)
    plt.plot(ts, Means, 'o', color = 'coral', label = "Averages")
    plt.plot(ts_fine, lam(ts_fine), color = "firebrick", label = "lambda(t)")
    plt.xlabel("Time")
    plt.ylabel("Number of Arrivals")
    plt.title("Averages vs lambda(t)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("meanies.png")
    plt.close()


    
    
## SIMULATION #####################################################################
###################################################################################
def one_day():
    """
    Simulates arrivals over one day by thinning
    Inputs:  none
    Outputs: times......(np array) list of accepted times
             arrives....(np array) num arrivals in each hour
    """
    times = []
    t = 0
    totalprops = 0
    lam = lambda t: 12+8*np.cos(np.pi*(t-16)/12)

    while t <= 24:
        wait = np.random.exponential(1/20)
        t_new = t + wait
        if t_new > 24: break
        totalprops += 1
        
        # accept/reject
        u = np.random.uniform(0,1)
        if u < lam(t_new)/20:
            times.append(t_new)
        
        # scoot forward
        t = t_new
    
    arrives, _ = np.histogram(times, bins=np.arange(25))
    return times, arrives, totalprops



## RESULTS ########################################################################
###################################################################################
def results():
    # simulate 30 days (720 hours) of arrivals by thinning
    Times = []
    Arrivals = np.zeros((30,24))
    totals = []
    
    for day in range(30):
        times, arrives, total = one_day()
        Times.extend(np.array(times)+24*day) # creating unique times
        Arrivals[day] = arrives
        totals.append(total)
    Times = np.array(Times)
    
    # Fraction accepted
    frac = np.sum(Arrivals)/np.sum(totals)
    print(f"Fraction Accepted: {frac:.5f}\n")
    
    # Plot mean arrivals against lambda(t)
    Means = np.mean(Arrivals, axis = 0) # should be over cols
    plotmeans(Means)
    
    # Mean/var of num arrivals from 3-4 am
    mean_34 = np.mean(Arrivals[:,3])
    var_34 = np.var(Arrivals[:,3])
    print("_________________________________________")
    print("From 3 to 4 am over 30 days:")
    print("_________________________________________")
    print(f"Mean number of arrivals: {mean_34:.5f}")
    print(f"Variance of number of arrivals: {var_34:.5f}")
    print("According to Poisson(4.091):")
    print(f"Mean = Variance = {4.091}")
    print("________________________________________")
    print(Arrivals[:,3])
    print(np.var(Arrivals[:,3], ddof=1))
    # Inference
    lam = lambda t, a, b, phi: a+b*np.cos(np.pi*(t-phi)/12)
    def negloglike(params, Times):
        a, b, phi = params
        return -(np.sum(np.log(lam(Times%24, a, b, phi))) - 720*a)
    
    # Maximize loglike to fit lam
    start = [10, 5, 14]
    res = minimize(negloglike, start, args=(Times,), bounds = [(0.01, None), (0, None), (0, 24)])
    print(f"True: [12, 8, 16]")
    print(f"Estimated: {res.x}\n")
    
    # Constant rate
    r = len(Times)/720
    const = len(Times)*np.log(r)-r*720
    
    print(f"Log Likelihood Fitted: {-res.fun}")
    print(f"Log Likelihood Constant lambda: {const}")
    


## MAIN ###########################################################################
###################################################################################
if __name__ == "__main__":
    results()