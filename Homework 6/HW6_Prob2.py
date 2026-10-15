## IMPORTS ################################################################
###########################################################################
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

## OTHER STUFF ############################################################
###########################################################################
def barchart(r, teams, name):
    """
    makes bar chart of r, saves fig wrt prior
    """
    ordered = np.argsort(-r)
    teams_sorted = [teams[i] for i in ordered]
    rsorted = r[ordered]
    
    plt.figure(figsize = (10,6))
    plt.bar(range(len(rsorted)), rsorted, color = "palegreen", edgecolor = "forestgreen")
    plt.xticks(range(len(rsorted)), teams_sorted, rotation=45, ha="right")
    plt.xlabel("Team")
    plt.ylabel("Ranking")
    plt.title(f"Rankings for Prior = {name}")
    plt.tight_layout()
    plt.savefig(f"Bar_r_{name}")

def h(x):
    return 0.5 + 0.5*np.sign(x-0.5)*np.sqrt(np.abs(2*x-1))

def oct1011(data, teamsidx, r):
    future = data[(data["date"] >= "2026-10-10") & (data["date"] <= "2026-10-11")]
    nice = 0
    for g, game in future.iterrows():
        h = game["home"]
        a = game["away"]
        i = teamsidx[h]
        j = teamsidx[a]
        S = game["home_pts"]
        T = game["away_pts"]
        
        if r[i] > r[j]:
            win = h
        else:
            win = a
            
        if S>T: 
            win_frfr = h
        elif T > S:
            win_frfr = a
        else:
            win_frfr = "Tie"
            
        print(f"{a} vs {h}")
        print(f"Winner = {win}")    
        print(f"Actual winner = {win_frfr}")
        if win == win_frfr:
            nice += 1
        
    print(f"Total Correct Predictions: {nice}")
        

def predict(prior, name, A, num_games, teams):
    m = len(A[0])
    for i in range(m):
        for j in range(m):
            if i != j:
                A[i,j] += prior[i, j]
        A[i,:] = A[i,:]/(num_games[i] + m-1)
    
    # power it!
    r = np.ones(m)/m
    for i in range(100):
        r = A@r
        r = r/np.sum(r)
    
    ordered = np.argsort(-r)
    
    lams = np.linalg.eigvals(A)
    
    idxs = np.argsort(-np.abs(lams))
    lams = lams[idxs]
    lamstar = lams[0]
 
    # Result
    print(f"lambda * = {np.abs(lamstar)}")
    print(f"lambda2/lambda * = {(np.abs(lams[1]))/(np.abs(lamstar))}")
    barchart(r, teams, name)
    
    # Oct 10-11 Big 12 games
    return ordered
    
## DRIVER THING ###########################################################
###########################################################################
def run():
    data = pd.read_csv("big12.csv")
    games2025 = data[data["season"] == 2025]
    games2026 = data[(data["season"] == 2026) & (data["completed"] == 1)] # well if you dont completed you get nans. ask me how i know.
    
    # need to index teams and be able to retrieve their names later (dict)
    teams = sorted(set(data["home"]).union(set(data["away"])))
    teamsidx = {team: i for i,team in enumerate(teams)} 
    m = len(teams)
    
    # Flat Prior
    pi_flat = np.full((m,m), 0.5)
    for i in range(m): pi_flat[i, i] = 0
     
    # silly made up strength metric
    strengths = {team: 0.0 for team in teams}
    
    # Last Season, si/(si+sj)
    last = {}
    poll = {}
    for g, game in games2025.iterrows():
        # variables 
        i = game["home"]
        j = game["away"]
        S = game["home_pts"]
        T = game["away_pts"]
        
        # make de h
        hij = h((S+1)/(S+T+2))
        last.setdefault((i,j), []).append(hij) # if ij isnt already there append the thing
        poll.setdefault((i, j), []).append(0)
        # make de strengths
        strengths[i] += game["home_pts"]
        strengths[j] += game["away_pts"]
        
    # Fill up the pis
    pi_last = np.full((m,m), 0.5)
    for (teami, teamj), vals in last.items():
        i = teamsidx[teami]
        j = teamsidx[teamj]
        
        pi_last[i,j] = np.mean(vals)
        pi_last[j, i] = 1- pi_last[i, j]
        
    pi_avg = np.full((m,m), 0.5)
    for (teami, teamj), vals in poll.items():
        i = teamsidx[teami]
        j = teamsidx[teamj]
        if i == j: continue
        
        si = strengths[teami]
        sj = strengths[teamj]
        
        pi_avg[i,j] = si/(si+sj)
        pi_avg[j, i] = 1- pi_avg[i, j]
          
# Matrix A from 2026 games
    A = np.zeros((m,m))
    num_games = np.zeros(m)
    for g, game  in games2026.iterrows():
        # get proper data
        teami = game["home"]
        teamj = game["away"]
        i = teamsidx[teami]
        j = teamsidx[teamj]
        S = game["home_pts"]
        T = game["away_pts"]
        
        # make A
        hij = h((S+1)/(S+T+2))
        hji = h((T+1)/(S+T+2))
        A[i,j] += hij
        A[j, i] += hji
        
        # iterate
        num_games[i] += 1
        num_games[j] += 1
        
    print("\n\nFlat Prior:")
    rflat = predict(pi_flat, "Flat", A.copy(), num_games, teams)  
    oct1011(data, teamsidx, rflat)
    
    print("\n\nLast Season Prior:")
    rlast = predict(pi_last, "Last", A.copy(), num_games, teams)
    oct1011(data, teamsidx, rlast)

    print("\n\nStrengths Prior:")
    rstronk = predict(pi_avg, "Strengths", A.copy(), num_games, teams)
    oct1011(data, teamsidx, rstronk)
    
    

        
    
## MAIN ###################################################################
###########################################################################
if __name__ == "__main__":
    run()
