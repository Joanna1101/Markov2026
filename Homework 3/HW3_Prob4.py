## IMPORTS ##########################################
#####################################################
import numpy as np
from scipy.special import erf
import matplotlib.pyplot as plt
from prettytable import PrettyTable

## PLOTTING #########################################
#####################################################
def plotstuff(times, S1t, S1erf, slope1, beta1, S2t = None, S1t2 = None):
    """
    Inputs:  times.....(np array) time steps array
             S1t.......(np array) simulated survival times
             S1erf.....(np array) error function estimate 
             slope1....(float) slope fit for 10^2 <=t <= 10^4
             beta1.....(float) exponent
             S2t.......() (optional so part b can use same function)
             S1t2......() (optional so part b can use same function)
    Outputs: HW3_P4.png
    """
    plt.loglog(times, S1erf, label = "Continuum Prediction", color = "darkgreen")
    plt.loglog(times, S1t, '--', label = "S_1(t)", color = "springgreen")
    plt.loglog(times, slope1, label = f"Power Law, beta = {beta1:.4f}", color = "paleturquoise")
    
    if S2t is not None:
        plt.loglog(times, S2t, label = "S_2(t)", color = "violet")
        plt.loglog(times, S1t2, label = "S_1(t)^2", color = "gold")
    
    plt.title(f"Fit window 10^2 <= t <= 10^4, beta = {beta1:.4f}")
    plt.xlabel(f"Timestep")
    plt.ylabel(f"Bugs alive (scaled)")
    plt.legend()
    plt.savefig("HW3_P4.png")
    
    
## PART C ###########################################
#####################################################
def partcSim(T, R):
    """
    Simulates 2x10^2 bugs with one frog, starting at (0, 10)
    Inputs:  T..........(int) max iterations
             R..........(int) number of bugs
    Outputs: deaths.....(np array) list of death times
    """
    time = 0
    allDead = 0
    
    deaths = np.zeros(R)
    buggies = np.zeros(R)
    froggies = np.full(R, 10)
    
    while time < T:
        bzz = np.random.choice([-1, 1], size = R)
        hop = np.random.choice([-1, 1], size = R)
        
        # don't move dead buggies
        alive = deaths == 0
        buggies[alive] += bzz[alive]
        froggies[alive] += hop[alive]
        
        died = (buggies == froggies) & alive
        deaths[died] = time + 1
        
        if np.all(deaths > 0):
            allDead = time + 1
            print("They all died! :( ;-;")
        time += 1
    
    return deaths
 
def partcAnalysis():
    T = 10**4
    R = 2*10**4
    
    deaths = partcSim(T, R)
    
    # estimated survival times
    times = np.arange(1, T+1)
    S1t = np.array([np.sum((deaths == 0)| (deaths > t))/R for t in times])
    
    # fitting slope
    mask = (times >= 100) & (times <= 10000) & (S1t > 0)
    m, b = np.polyfit(np.log(times[mask]), np.log(S1t[mask]), 1)
    slopeLine = np.exp(b)*times**m
    
    print("m1 = ", m)
    print("beta1 = ", -m)
    print("b1 = ", b)
    
    # error function
    S1erf = erf(10/(2*np.sqrt(times)))
    
    # plotstuff(times, S1t, S1erf, slopeLine, -m)
    return S1t, S1erf, slopeLine, -m
    
## PART D ###########################################
#####################################################
def partdSim(R, T):
    """
    Simulates 2x10^2 bugs with one frog, starting at (0, 10)
    Inputs:  T..........(int) max iterations
                R..........(int) number of bugs
    Outputs: deaths.....(np array) list of death times
                buggies....(np array) bug final positions
                froggy.....(np array) frog final position
                allDead....(int) when all bugs died, if that happens
            
    """
    time = 0
    allDead = 0
    
    deaths = np.zeros(R)
    buggies = np.zeros(R)
    froggies1 = np.full(R, 10)
    froggies2 = np.full(R, 10)
    
    while time < T:
        bzz = np.random.choice([-1, 1], size = R)
        hop1 = np.random.choice([-1, 1], size = R)
        hop2 = np.random.choice([-1, 1], size = R)
        
        # don't move dead buggies
        alive = deaths == 0
        buggies[alive] += bzz[alive]
        froggies1[alive] += hop1[alive]
        froggies2[alive] += hop2[alive]
        
        died = ((buggies == froggies1) | (buggies == froggies2)) & alive
        deaths[died] = time + 1
        
        if np.all(deaths > 0):
            allDead = time + 1
            print("They all died! :( ;-;")
        time += 1
    
    return deaths

def partdAnalysis():
    T = 10**4
    R = 2*10**4
    
    S1t, S1erf, slopeLine1, beta1 = partcAnalysis()
    
    deaths = partdSim(T, R)
    
    # estimated survival times
    times = np.arange(1, T+1)
    S2t = np.array([np.sum((deaths == 0)| (deaths > t))/R for t in times])
        
    # fitting slope
    mask = (times >= 100) & (times <= 10000) & (S2t > 0)
    m2, b2 = np.polyfit(np.log(times[mask]), np.log(S2t[mask]), 1)
    slopeLine2 = np.exp(b2)*times**m2
    
    print("m2 = ", m2)
    print("beta2 = ", -m2)
    print("b2 = ", b2)
    
    S1t2 = S1t**2
    
    plotstuff(times, S1t, S1erf, slopeLine1, beta1, S2t, S1t2)
    
    # Table Time!
    table = PrettyTable()
    table.field_names = ["t", "S_2(t)", "S_1(t)^2"]

    for t in [100, 1000, 10000]:
        i = t - 1
        table.add_row([f"10^{len(str(t))-1}" if t != 10000 else "10^4", f"{S2t[i]:.6f}", f"{S1t[i]**2:.6f}"])

    print(table)


## MAIN #############################################
#####################################################
if __name__ == "__main__":
    # partcAnalysis()
    partdAnalysis()
    