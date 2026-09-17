## IMPORTS ##########################################
#####################################################
import numpy as np

## MAIN #############################################
#####################################################
if __name__ == "__main__":
    p = np.array([[(1/2), (1/2), 0, 0, 0, 0],
         [(1/3), 0, (1/3), 0, (1/3), 0],
         [0, 0, (1/4), (3/4), 0, 0],
         [0, 0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 1, 0]])
    
    p20 = np.linalg.matrix_power(p, 20)
    p21 = np.linalg.matrix_power(p, 21)
    
    # np.set_printoptions(formatter={'float_kind': '{: .4e}'.format})
    np.set_printoptions(suppress = True)
    print("\np20:")
    print(p20)
    print("\np21")
    print(p21)
    print(f"\n\n(p^20) at (1,5):{p20[0, 4]:.4f}")
    print(f"(p^20) at (1,6):{p20[0, 5]:.4f}")
    print(f"Sum: {p20[0, 4]+p20[0, 5]:.4f}")
    