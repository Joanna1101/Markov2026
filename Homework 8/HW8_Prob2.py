## IMPORTS ####################################################################
###############################################################################
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable



## SIMULATION 1 ###############################################################
###############################################################################
def sim1(time):
    """
    Emit star and sky photons and then keep each with probability 0.4
    Inputs:  time.........(int) how many seconds the simulation should run 
    Outputs: starcount....(int) total accepted star photons
             startimes....(np array) times of accepted star photons
             skycount.....(int) total accepted sky photons
             skytimes.....(np array) times of accepted sky photons
    """
    nstars = np.random.poisson(3*time)
    nskys = np.random.poisson(2*time)
    
    startimes = np.sort(np.random.uniform(0, time, nstars))
    skytimes = np.sort(np.random.uniform(0, time, nskys))
    
    starkeeps = np.random.rand(nstars) < 0.4
    skykeeps = np.random.rand(nskys) < 0.4
    
    startimes = startimes[starkeeps]
    skytimes = skytimes[skykeeps]
    
    starcount = len(startimes)
    skycount = len(skytimes)

    return starcount, startimes, skycount, skytimes
    
    


## SIMULATION 2 ###############################################################
###############################################################################
def sim2(time):
    """
    Generate the two detected processes directly at rates 1.2 and 0.8
    Inputs:  time.........(int) how many seconds the simulation should run 
    Outputs: starcount....(int) total accepted star photons
             startimes....(np array) times of accepted star photons
             skycount.....(int) total accepted sky photons
             skytimes.....(np array) times of accepted sky photons
    """
    startimes = []
    skytimes = []
    
    # Stars
    t = 0
    while t < time:
        t += np.random.exponential(1/1.2)
        if t > time: break
        startimes.append(t)
    
    # Sky
    t = 0
    while t < time:
        t += np.random.exponential(1/0.8)
        if t > time: break
        skytimes.append(t)   
    
    starcount = len(startimes)
    skycount = len(skytimes)
    
    return starcount, startimes, skycount, skytimes


## RESULTS ####################################################################
###############################################################################
def results():
    # simulate 2e5 windows of 5 seconds
    starcounts1 = []
    skycounts1 = []
    starcounts2 = []
    skycounts2 = []
    
    # Keep track of windows with exactly 10 detections
    windows_10 = []
    
    # Need firsts
    firsts1 = []
    firsts2 = []
    firstwhom1 = []
    firstwhom2 = []
    starfirst1 = []
    skyfirst1 = []
    starfirst2 = []
    skyfirst2 = []
    
    # Need time till first detection
    M1 = []
    M2 = []
    
    for w in range(int(2e5)):
        starcount1, startimes1, skycount1, skytimes1 = sim1(5)
        starcount2, startimes2, skycount2, skytimes2 = sim2(5)
        
        starcounts1.append(starcount1)
        skycounts1.append(skycount1)
        starcounts2.append(starcount2)
        skycounts2.append(skycount2)
        
        firststar1 = startimes1[0] if len(startimes1) else np.inf
        firstsky1 = skytimes1[0] if len(skytimes1) else np.inf
        firststar2 = startimes2[0] if len(startimes2) else np.inf
        firstsky2 = skytimes2[0] if len(skytimes2) else np.inf
        
        # Ms
        if len(startimes1) > 0 and len(skytimes1) > 0:
            M1.append(max(firststar1, firstsky1))
        if len(startimes2) > 0 and len(skytimes2) > 0:
            M2.append(max(firststar2, firstsky2))
        
        # Firsts
        if firststar1 < firstsky1:
            starfirst1.append(firststar1) 
            firsts1.append(firststar1)
            firstwhom1.append(1)
        else:
            skyfirst1.append(firstsky1)
            firsts1.append(firstsky1)
            firstwhom1.append(0)
                
        if firststar2 < firstsky2:
            if len(startimes2) > 0:
                starfirst2.append(firststar2) 
                firsts2.append(firststar2)
                firstwhom2.append(1)
        else:
            if len(skytimes2) > 0:
                skyfirst2.append(firstsky2)
                firsts2.append(firstsky2)
                firstwhom2.append(0)
        
        # Windows of length 10
        if starcount1+skycount1 == 10:
            windows_10.append((starcount1, skycount1))
        if starcount2 + skycount2 == 10:
            windows_10.append((starcount2, skycount2))
        
    # Means and Variances of counts
    meanstar1 = np.mean(starcounts1)
    varstar1 = np.var(starcounts1)
    meansky1 = np.mean(skycounts1)
    varsky1 = np.var(skycounts1)
    meantot1 = np.mean(np.array(starcounts1)+np.array(skycounts1))
    vartot1 = np.var(np.array(starcounts1)+np.array(skycounts1))
    meanstar2 = np.mean(starcounts2)
    varstar2 = np.var(starcounts2)
    meansky2 = np.mean(skycounts2)
    varsky2 = np.var(skycounts2)      
    meantot2 = np.mean(np.array(starcounts2)+np.array(skycounts2))
    vartot2 = np.var(np.array(starcounts2)+np.array(skycounts2))
    
    # Comparison with Poisson(10) for total counts
    table = PrettyTable()
    table.field_names = ("Stat", "Method 1", "Method 2", "Poisson(10)")
    table.add_row(["Mean Star Count", f"{meanstar1:.5f}", f"{meanstar2:.5f}", "--"])
    table.add_row(["Variance Star Count", f"{varstar1:.5f}", f"{varstar2:.5f}", "--"])
    table.add_row(["Mean Sky Count", f"{meansky1:.5f}", f"{meansky2:.5f}", "--"])
    table.add_row(["Variance Sky Count", f"{varsky1:.5f}", f"{varsky2:.5f}", "--"])
    table.add_row(["Mean Total Count", f"{meantot1:.5f}", f"{meantot2:.5f}", "10"])
    table.add_row(["Variance Total Count", f"{vartot1:.5f}", f"{vartot2:.5f}", "10"])
    print(table)
    
    # Among windows with 10 detections estimate P(exactly 6 stars)
    windows_10 = np.array(windows_10)
    six_stars = 0
    for w in windows_10:
        if w[0] == 6:
            six_stars +=1
    total_wins = windows_10.shape[0]
    print(f"Probability of Exactly 6 stars out of 10: {(six_stars/total_wins):.5f}%")
    
    # P(star first) = how many times star was first / total runs
    pstar1 = len(starfirst1)/(2e5)
    pstar2 = len(starfirst2)/(2e5)
     
    # P(star first and within 1 s)
    yeppers = 0
    peppers = 0
    # Number of times star was first and within 1 s
    yeppers = sum(t <= 1 for t in starfirst1)
    peppers = sum(t <= 1 for t in starfirst2)
    pstar1sec1 = yeppers/2e5
    pstar1sec2 = peppers/2e5
    
    # E[M]
    em1 = np.mean(M1)
    em2 = np.mean(M2)
    
    # Correlation between the time of the first detection and its type.
    mask1 = np.isfinite(firsts1)
    corr1 = np.corrcoef(np.array(firsts1)[mask1], np.array(firstwhom1)[mask1])[0,1]
    
    mask2 = np.isfinite(firsts2)
    corr2 = np.corrcoef(np.array(firsts2)[mask2], np.array(firstwhom2)[mask2])[0,1]
    
    table1 = PrettyTable()
    table1.field_names = ("Statistic", "Method 1", "Method 2", "Theoretical")
    table1.add_row(["P(star first)", f"{pstar1:.5f}", f"{pstar2:.5f}", "0.6"])
    table1.add_row(["P(star first, within 1 s)", f"{pstar1sec1:.5f}", f"{pstar1sec2:.5f}", f"{0.6*(1-np.e**(-2)):.5f}"])
    table1.add_row(["E[M]", f"{em1:.5f}", f"{em2:.5f}", "1.5833"])
    table1.add_row(["Correlation", f"{corr1:.5f}", f"{corr2:.5f}", "0"])
    print(table1)
    
## MAIN #######################################################################
###############################################################################
if __name__ == "__main__":
    results()

