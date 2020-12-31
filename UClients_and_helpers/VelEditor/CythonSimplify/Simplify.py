#!python
##cython: boundscheck=False

import numpy as np
cimport numpy as np

class Simplify:
    def __init__(self):
        pass

    def main(self, Kurve, Ableitung, error):
        splineVerts = []
        for i in range(0, len(Kurve[0])):
            splineVerts.append(np.array([Kurve[0][i],Kurve[1][i]]))

        newVerts = self.Visvalingam(splineVerts, error)

        X_Values  = np.zeros(len(newVerts))
        Y_Values  = np.zeros(len(newVerts))
        k_Values  = np.zeros(len(newVerts))

        for i in range(0,len(newVerts)):
            X_Values[i]  = Kurve[0][newVerts[i]]
            Y_Values[i]  = Kurve[1][newVerts[i]]
            k_Values[i]  = Ableitung[1][newVerts[i]]
        return [X_Values, Y_Values, k_Values]

    def Visvalingam(self,splineVerts, error):
        return simplify_coords_idx(splineVerts, 0.01)
