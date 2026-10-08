## IMPORTS ################################################################
###########################################################################
import matplotlib.pyplot as plt
import numpy as np

## PART A #################################################################
###########################################################################
def parta():
    """
    Computes q100, q101
    """
    P = np.array([[0, 1/2, 1/2, 0, 0, 0, 0, 0],
                  [0, 0, 1/2, 1/2, 0, 0, 0, 0],
                  [1/2, 0, 0, 0, 1/2, 0, 0, 0],
                  [1/2, 0, 0, 0, 1/2, 0, 0, 0],
                  [0, 1/3, 0, 0, 0, 1/3, 1/3, 0],
                  [0, 0, 0, 0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1],
                  [0, 0, 0, 0, 0, 0, 1, 0]])
    
    q0 = np.ones(8)/8
    q100 = q0@np.linalg.matrix_power(P, 100)
    q101 = q0@np.linalg.matrix_power(P, 101)
    
    print(f"\nq_100: {q100}")
    print(f"\nq_101: {q101}")

## PART B #################################################################
###########################################################################
def partb():
    """
    Computes G, finds stationary distribution
    Compares power iteration and linear solve for pi
    """
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
    print(f"G = \n{G}")
        
    # Power iteration
    print("Power Iteration")
    q0 = np.ones(8)/8
    q1 = q0@G
    qns = [q0, q1]
    n = 1
    
    while np.linalg.norm(qns[n-1] - qns[n], 1) >= 1e-10:
        n += 1
        qnew = qns[n-1]@G
        qns.append(qnew)
        
    print(f"\nFinal n = {n}")
    print(f"\nFinal q: {qns[-1]}")
    
    # Linear solve
    print("\nLinear Solve")
    A = G.T - np.eye(8)
    A[-1, :] = 1
    
    bs = np.zeros(8)
    bs[-1] = 1
    
    pi = np.linalg.solve(A, bs)
    print(f"\npi = {pi}")
    
    print(f"\n|q_{n} - pi| = {np.abs(qns[-1]-pi)}")
    
    # Ranking
    print("sure is smth frfr")
   

## MAIN ###################################################################
###########################################################################
if __name__ == "__main__":
    # parta()
    partb()
