## THIS ONES SIMPLE ##############################
##################################################
import numpy as np

if __name__ == "__main__":
    Q = np.array([[-2, 2, 0, 0], [1, -3, 2, 0], [0, 2, -4, 2], [0, 0, 3, -3]])
    eigs, vecs = np.linalg.eig(Q)
    print(f"Eigenvalues: {eigs}")
    print(f"Sum: {np.sum(eigs)}")