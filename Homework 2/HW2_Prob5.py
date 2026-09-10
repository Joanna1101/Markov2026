## IMPORTS ##########################################
#####################################################
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable

## Part (b) #########################################
#####################################################
def part_b():
    N = int(10e5)
    
    count = 0
    hs = []
    while count < N:
        U = np.random.uniform()
        h = 1-np.sqrt(U)
        hs.append(h)
        count += 1
        
    mean = np.sum(hs)/N
    print(f"Sample Mean: {mean}")
    
## Part (c) #########################################
#####################################################
def plot_hist(Zs):
    """
    Plots normalized histogram with f(x) overlaid
    Inputs:  Zs....(list)
    Outputs: prob5.png
    """
    # Making f
    zs = np.linspace(0, 1,1000)
    f = lambda z: 2*(1-z) 
    
    plt.plot(zs, f(zs), color = "indigo", label = "h(z)")
    plt.hist(Zs, bins=50, density = True, color='thistle', edgecolor = 'purple', label = "Samples")
    plt.legend()
    plt.xlabel('Samples')
    plt.ylabel('Frequency')
    plt.title(f'Normalized Histogram vs h(z)')
    plt.savefig("prob5.png")
    plt.close()
    
def part_c():
    Cs = np.ones(1000)
    Us = np.ones(1000)
    
    for N in range(3, 9999):
        probs = Cs/N
        Us = np.random.uniform(size = 1000)
        Bs = Us < probs
        Cs = Cs + Bs
    
    Zs = Cs/10000
    plot_hist(Zs)
    
    emp_mean = np.mean(Zs)
    emp_var = np.var(Zs)
    CV = np.sqrt(emp_var)/emp_mean
    
    table = PrettyTable()
    table.field_names = ["Metric", "Empirical", "Theoretical", "Difference"]
    table.add_row(["Mean", round(emp_mean,8), round(1/3,8), f"{emp_mean-(1/3):.8f}"])
    table.add_row(["Variance", round(emp_var,8), round(1/18,8), f"{emp_var-(1/18):.8f}"])
    table.add_row(["CV", round(CV,8), round(1/np.sqrt(2),8), f"{CV-(1/np.sqrt(2)):.8f}"])
    print(table)
    
    print(f"Smallest Core: {np.min(Cs)}")
    print(f"Largest Core: {np.max(Cs)}")
    

## MAIN #############################################
#####################################################
if __name__ == "__main__":
    # part_b()
    part_c()