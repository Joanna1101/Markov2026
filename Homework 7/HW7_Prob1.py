## IMPORTS ###################################################################
##############################################################################
import numpy as np
from scipy.stats import multivariate_normal as gaussies
import scipy.stats as stats
import emcee
import matplotlib.pyplot as plt
from prettytable import PrettyTable




## THE CHAIN #################################################################
##############################################################################
def log_g(alpha, b):
    """
    From part (b). Need to take log for numerical stability.
    gy/gz = exp(log gy - log gz) 
    """
    beta = np.exp(b)
    xs = np.array([-1.77, 2.47, 1.34, 2.18, 13.05, 1.60, 1.50, -1.97, 0.79, 1.50, 2.00, 2.63, 1.19, -2.31, 0.87])
    norm = 2*np.log(np.abs(xs - alpha))
    additallup = np.sum(np.logaddexp(2*b, norm))
        
    logg = 15*b - additallup
    
    return logg
        
def chain(start, T, s):
    """
    Runs the MC forward 
    Inputs:  start......((alpha, beta)) starting position
             T..........(int) number of steps to take
             s..........(float) step size
    Outputs: accept.....(float) acceptance rate
             samples....(list of (alpha, log beta)) accepted samples
             allphas....(list) all alphas
    """
    mu = [0.0,0.0]
    cov = [[1.0, 0.0], [0.0, 1.0]]
    accepted = 0
    samples = []
    allphas = []
    z = start
    
    for t in range(0, T):
        y = z + s*gaussies.rvs(mu, cov) # need a ~saample~ from the gaussies
        
        rando = np.random.uniform(0,1) 
        gy = log_g(y[0], y[1])
        gz = log_g(z[0], z[1])
        prob = min(1, np.exp(gy-gz))
        
        if rando < prob:
            z = y
            accepted += 1
        
        allphas.append(y[0])
        samples.append((z[0], z[1]))
        
    accept = accepted/T
        
    return accept, samples, allphas
    


## PART C ####################################################################
##############################################################################
def plot400(alphas, ss):
    """
    Plots first 400 values of alpha for all ss
    """
    colors = ["palegreen", "royalblue", "deeppink"]
    for i, s in enumerate(ss):
        plt.plot(range(400), alphas[i], lw = 1, color = colors[i], label = f"s = {s}")
        
    plt.xlabel("Iteration")
    plt.ylabel("alpha")
    plt.title(f"First 400 Alphas")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"HW7_P1c_all.png")
    plt.close()  
    
def con(data):
    """
    90% confidence interval helper for plotSamples
    """
    df = len(data) -1
    sample_mean = np.mean(data)
    conint = stats.t.interval(.90, df, sample_mean)
    return conint
    
def plotSamples(samples, s):
    """
    Plots samples over contours of exact posterior
    """
    samples = samples[5000:, :]
    
    # Funny Buisiness
    agrid = np.linspace(-1, 3.5, 500)
    bgrid = np.linspace(-2.5, 1.5, 500)
    alphas, bs = np.meshgrid(agrid, bgrid)
    log_post = np.empty_like(alphas)
    for i in range(bs.shape[0]):
        for j in range(alphas.shape[1]):
            log_post[i,j] = log_g(alphas[i,j], bs[i,j]) # the actual sampling
    # sir please do not blow up on me
    weights = np.exp(log_post - np.max(log_post))
    # levels = [0.01, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8]

    plt.scatter(samples[:, 0], samples[:, 1], marker ='o', s = 1, color = "thistle", label = "Samples")
    contours = plt.contour(alphas, bs, weights, levels = 12, alpha = 0.8, cmap = "rainbow")
    plt.colorbar(contours, label="Posterior Density")
    plt.title(f"Samples Over Contours, s = {s}")
    plt.xlabel("Alpha")
    plt.ylabel("b = log(beta)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("HW7_Prob1c_best.png")
    plt.close()
    
    # Stats 
    weights = weights/np.sum(weights)
    weights = weights.ravel()
    idxs = np.random.choice(len(weights), size = 100000, replace = True, p = weights)
    ameang = np.mean(alphas.ravel()[idxs])
    bmeang = np.mean(np.exp(bs.ravel()[idxs]))
    a90g = np.quantile(alphas.ravel()[idxs], [0.05, 0.95])
    b90g = np.quantile(bs.ravel()[idxs], [0.05, 0.95])
    ameanc = np.mean(samples[:, 0])
    bmeanc = np.mean(samples[:, 1])
    a90c = np.quantile(samples[:, 0], [0.05, 0.95])
    b90c = np.quantile(np.exp(samples[:, 1]), [0.05, 0.95])
    
    # Makit pretttyyyyyy
    table1 = PrettyTable()
    table1.field_names = ["Method", "Posterior Mean, alpha", "Posterior Mean, beta", "90% Interval, alpha", "90% Interval, beta"]
    table1.add_row(["Grid", ameang, bmeang, a90g, b90g])
    table1.add_row(["Chain", ameanc, bmeanc, a90c, b90c])
    print(table1)
    
    
def partc():
    start = (0,0)
    T = int(50000)
    ss = [0.02, 0.5, 5]
    all_alphas = []
    bests = 0
    bests_auto = 1000000
    bests_samples = []
    
    table0 = PrettyTable()
    table0.field_names = ["s", "acceptance rate", "autocorellation"]
    
    for s in ss:
        print(f"Running s = {s}")
        accept, samples, alphas = chain(start, T, s)
        samples = np.array(samples)
        
        try: auto = emcee.autocorr.integrated_time(samples[:, 0])
        except emcee.autocorr.AutocorrError as e:
            auto = e.tau[0]
            print(f"Warning: Emcee Cranky bc Chain Not Long Enough: {auto:.2f}")
            
        table0.add_row([f"{s}", accept, auto])
        all_alphas.append(alphas[:400])
        
        if auto < bests_auto:
            bests = s
            bests_auto = auto
            bests_samples = samples
            
    plot400(all_alphas[::-1], ss[::-1])
    plotSamples(bests_samples, bests)
    print(table0)
    
    xs = np.array([-1.77, 2.47, 1.34, 2.18, 13.05, 1.60, 1.50, -1.97, 0.79, 1.50, 2.00, 2.63, 1.19, -2.31, 0.87])
    print(f"Sample mean: {np.mean(xs)}")
    print(f"Sample median: {np.median(xs)}")
    
    
    
        
## PART D ####################################################################
##############################################################################  
def partd():
    ns = [10, 100, 1000]
    
    # set up empty slots for 2000 samples per n
    means = {n: [] for n in ns}
    medians = {n: [] for n in ns}
    
    for n in ns:
        for i in range(2000):
            samples = 1.5 + 0.8*np.random.standard_cauchy(n)
            means[n].append(np.mean(samples))
            medians[n].append(np.median(samples))
        
        means[n] = np.array(means[n])
        medians[n] = np.array(medians[n])
    
    # Separate by n
    means10 = means[10]
    medians10 = medians[10]
    means100 = means[100]
    medians100 = medians[100]
    means1000 = means[1000]
    medians1000 = medians[1000]
    
    # Scatter = (25th-75th)/1.349
    meanscatter10 = (np.percentile(means10, 75) - np.percentile(means10, 25))/1.349
    meanscatter100 = (np.percentile(means100, 75) - np.percentile(means100, 25))/1.349
    meanscatter1000 = (np.percentile(means1000, 75) - np.percentile(means1000, 25))/1.349
    medianscatter10 = (np.percentile(medians10, 75) - np.percentile(medians10, 25))/1.349
    medianscatter100 = (np.percentile(medians100, 75) - np.percentile(medians100, 25))/1.349
    medianscatter1000 = (np.percentile(medians1000, 75) - np.percentile(medians1000, 25))/1.349
    
    # Report
    table2 = PrettyTable()
    table2.field_names = ["n", "mean scatter", "median scatter"]
    table2.add_row([10, f"{meanscatter10 :.5f}", f"{medianscatter10 :.5f}"])
    table2.add_row([100, f"{meanscatter100 :.5f}", f"{medianscatter100 :.5f}"])
    table2.add_row([1000, f"{meanscatter1000 :.5f}", f"{medianscatter1000 :.5f}"])
    print(table2)

## MAIN ######################################################################
##############################################################################
if __name__ == "__main__":
    # partc()
    partd()