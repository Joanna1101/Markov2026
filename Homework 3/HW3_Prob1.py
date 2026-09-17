## IMPORTS ##########################################
#####################################################
import numpy as np

## MAIN #############################################
#####################################################
if __name__ == "__main__":
    p = [[(9/10), (1/10), 0],[0, (3/4), (1/4)],[(1/2), 0, (1/2)]]
    p50 = np.linalg.matrix_power(p, 50)
    print("\np^50 via numpy matrix_power:")
    print(p50)
    
    f = p50[0]
    print("\nLong run fraction (fW, fC, fS):")
    print(f)
    
    dwell = [i*16 for i in f]
    print("\nDwell times = f*16 ms")
    print(f"{dwell}\n")