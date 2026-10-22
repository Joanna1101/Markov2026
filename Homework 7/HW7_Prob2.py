## IMPORTS ######################################################################################
#################################################################################################
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from itertools import combinations

## PLOTTING #####################################################################################
#################################################################################################
def plothist(Ms, rates):
    """
    Plots histogram of total time against theoretical density
    """
    def density(t, rates):
        total = 0
        # product rule yay
        for i, lam  in enumerate(rates):
            dfdt = lam*np.exp(-lam*t)
            prod = 1
            
            for j, lam2 in enumerate(rates):
                if j != i:
                    prod *= (1 - np.exp(-lam2*t))
            total += dfdt*prod
        return total
    
    ts = np.linspace(0, max(Ms), 500)  
    plt.hist(Ms, bins = 50, density = True, alpha = 0.5, color = "pink", edgecolor = "palevioletred")
    plt.plot(ts, [density(t, rates) for t in ts], color = "forestgreen", label = "Exact Density")
    plt.title("M Against Exact Density")
    plt.xlabel("Total Time Taken")
    plt.ylabel("Frequency")
    plt.legend()
    plt.savefig("HW7_P2d_M_hist.png")
    plt.tight_layout()
    plt.close()
    
## EM CALCULATION ###############################################################################    
#################################################################################################    
def EM(rates):
    n = len(rates)
    EM = 0

    for k in range(1, n+1):
        sign = (-1)**(k+1)
        for subset in combinations(range(n), k):
            summed = sum(rates[i] for i in subset)
            EM += sign/summed
    
    return EM
    
    
## RECURSIVE THINGIE ############################################################################
#################################################################################################    
def next_finish(survivors):
    lams = np.array([rate for student, rate in survivors])
    student_probs = lams/np.sum(lams)
    whomst = np.random.choice(len(lams), p=student_probs)
    whence = np.random.exponential(1/np.sum(lams))
    return whomst, whence    
    
## SIMULATION DRIVERS ###########################################################################
#################################################################################################
def simulation():
    """
    Simulates 2x10^5 exams
    Compares probability that each student finishes last across all exams 
    Plots histogram of actual ta bedtimes compared to theoretical density
    """
    rates = [3, 2, 1.5, 1.2, 1, 0.75]
    orders = []
    times = []
    firsts = [[] for student in range(6)]
    
    for exam in range(int(2*1e5)):
        survivors = list(enumerate(rates))
        finish_order = []
        total_time = 0
        Em = 1/np.sum(rates)
        first_student = None
        first_time = None
        
        while len(survivors) != 0:
           remove, time = next_finish(survivors)
           student, length = survivors.pop(remove)
           finish_order.append(student)
           total_time += time
           
           if first_student is None:
               first_student = student
               first_time = time
        
        orders.append(finish_order)
        times.append(total_time)
        firsts[first_student].append(first_time)
           
    plothist(times, rates)
    
    finish_probs = []
    for student in range(len(rates)):
        lasts = 0
        for o in orders:
            if o[-1] == student:
                lasts += 1
        prob = lasts/(2*1e5)
        finish_probs.append(prob)
            
    table0 = PrettyTable()
    table0.field_names = ["1", "2", "3", "4", "5", "6"]
    table0.add_row([f"{finish_probs[0]:.5f}", f"{finish_probs[1]:.5f}", f"{finish_probs[2]:.5f}", f"{finish_probs[3]:.5f}", f"{finish_probs[4]:.5f}", f"{finish_probs[5]:.5f}"])
    
    print("\nProbability that student i finishes last averaged across 2x10^5 exams:")
    print(table0)
    print(f"\nMCMC E[M] Estimate: {np.mean(times):.5f}")
    print(f"Alt Formula E[M]: {EM(rates)}")
    
    print("\nFinishing Time of First Student:")
    for i in range(6): print(f"Student {i+1}: {np.mean(firsts[i]) :.5f}")
    
def simulation2():
    ks = np.arange(1, 13)
    EMs = []
    for k in ks:
        lams = [i  for i in range(1, k+1)]
        EMs.append(EM(lams))
        
    plt.plot(ks, EMs, marker = 'o', color = "palevioletred")
    plt.xlabel("k")
    plt.ylabel("E[M]")
    plt.title("E[M] where lambda_i = i")
    plt.savefig("HW7_P2d_E[M]k.png")
    plt.close()
    
    # for fun
    EMs = np.array(EMs)
    plt.plot(ks, np.abs(EMs - 2*np.log(2)), marker = 'o', color = "mediumpurple")
    plt.xlabel("k")
    plt.ylabel("E[M] - 2ln(2)")
    plt.title("Error in E[M]")
    plt.savefig("HW7_P2d_E[M]err.png")
    plt.close()
    
    
## MAIN #########################################################################################
#################################################################################################
if __name__ == "__main__":
    # simulation()
    simulation2()