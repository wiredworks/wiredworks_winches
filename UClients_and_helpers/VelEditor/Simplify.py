from mathutils import Vector
from math import (sin, pow, sqrt,acos)

options = [
        self.mode,       # 0
        self.output,     # 1
        self.k_thresh,   # 2
        self.pointsNr,   # 3
        self.error,      # 4
        self.degreeOut,  # 5
        self.dis_error,  # 6
        self.keepShort   # 7
        ]

# ### Ramer-Douglas-Peucker algorithm ###

# get altitude of vert
def altitude(point1, point2, pointn):
    edge1 = [[],[]]
    edge2 = [[],[]]
    edge1[0] = point2[0] - point1[0]
    edge1[1] = point2[0] - point1[1]
    edge2[0] = pointn[0] - point1[0]
    edge2[1] = pointn[0] - point1[1]
    e2l = sqrt(edge2[0]*edge2[0]+edge2[1],edge2[1])
    e1l = sqrt(edge1[0]*edge1[0]+edge1[1],edge1[1])
    if e2l == 0:
        altitude = 0
        return altitude
    if e1l.length == 0:
        altitude = e2l
        return altitude
    alpha = acos(edge2[0]*edge1[0]+edge2[1]*edge1[1])/ (e2l*e1l)
    altitude = sin(alpha) * e2l
    return altitude


# iterate through verts
def iterate(points, newVerts, error):
    new = []
    for newIndex in range(len(newVerts) - 1):
        bigVert = 0
        alti_store = 0
        for i, point in enumerate(points[newVerts[newIndex] + 1: newVerts[newIndex + 1]]):
            alti = altitude(points[newVerts[newIndex]], points[newVerts[newIndex + 1]], point)
            if alti > alti_store:
                alti_store = alti
                if alti_store >= error:
                    bigVert = i + 1 + newVerts[newIndex]
        if bigVert:
            new.append(bigVert)
    if new == []:
        return False
    return new


# get SplineVertIndices to keep
def simplify_RDP(splineVerts, options):
    # main vars
    error = options[4]

    # set first and last vert
    newVerts = [0, len(splineVerts) - 1]

    # iterate through the points
    new = 1
    while new is not False:
        new = iterate(splineVerts, newVerts, error)
        if new:
            newVerts += new
            newVerts.sort()
    return newVerts


# ### CURVE GENERATION ###

# get array of new coords for new spline from vertindices
def vertsToPoints(newVerts, splineVerts, splineType):
    # main vars
    newPoints = []

    # array for BEZIER spline output
    if splineType == 'BEZIER':
        for v in newVerts:
            newPoints += splineVerts[v].to_tuple()

    # array for nonBEZIER output
    else:
        for v in newVerts:
            newPoints += (splineVerts[v].to_tuple())
            if splineType == 'NURBS':
                newPoints.append(1)  # for nurbs w = 1
            else:                    # for poly w = 0
                newPoints.append(0)
    return newPoints


# ### MAIN OPERATIONS ###

def main(Kurve, options):
    mode = options[0]
    output = options[1]
    degreeOut = options[5]
    keepShort = options[7]

    splineVerts = []

    for i in range(0, len(Kurve[0])):
        splineVerts.append([Kurve[0],Kurve[1]]) 

    newVerts = simplify_RDP(splineVerts, options)

    return

