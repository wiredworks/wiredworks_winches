import mathutils
import math

class SFX_Simplyfy_fcurves():


    def SFX_fcurves_simplify(self, fcurve_sel, options, fcurves):
        # main vars
        mode = options[0]
        for fcurve_i, fcurve in enumerate(fcurves):
            # test if fcurve is long enough
            if len(fcurve) >= 3:
                # simplify spline according to mode
                if mode == 'DISTANCE':
                    newVerts = self.simplify_RDP(fcurve, options)
                if mode == 'CURVATURE':
                    newVerts = self.simplypoly(fcurve, options)
                # convert indices into vectors3D
                newPoints = []
                # this is different from the main() function for normal curves, different api...
                for v in newVerts:
                    newPoints.append(fcurve[v])
                # remove all points from curve first
                for i in range(len(fcurve) - 1, 0, -1):
                    fcurve_sel[fcurve_i].keyframe_points.remove(fcurve_sel[fcurve_i].keyframe_points[i])
                # put newPoints into fcurve
                for v in newPoints:
                    fcurve_sel[fcurve_i].keyframe_points.insert(frame=v[0], value=v[1])
        return

    def getDerivative(self,verts, t, nth):
        order = len(verts) - 1 - nth
        QVerts = []
        if nth:
            for i in range(nth):
                if QVerts:
                    verts = QVerts
                derivVerts = []
                for i in range(len(verts) - 1):
                    derivVerts.append(verts[i + 1] - verts[i])
                QVerts = derivVerts
        else:
            QVerts = verts
        if len(verts[0]) == 3:
            point = mathutils.Vector((0, 0, 0))
        if len(verts[0]) == 2:
            point = mathutils.Vector((0, 0))
        for i, vert in enumerate(QVerts):
            point += self.binom(order, i) * pow(t, i) * pow(1 - t, order - i) * vert
        deriv = point
        return deriv

    def binom(self, n, m):
        b = [0] * (n + 1)
        b[0] = 1
        for i in range(1, n + 1):
            b[i] = 1
            j = i - 1
            while j > 0:
                b[j] += b[j - 1]
                j -= 1
        return b[m]

    def getCurvature(self, deriv1, deriv2):
        if deriv1.length == 0:  # in case of points in straight line
            curvature = 0
            return curvature
        curvature = (deriv1.cross(deriv2)).length / pow(deriv1.length, 3)
        return curvature

    def altitude(self, point1, point2, pointn):
        edge1 = point2 - point1
        edge2 = pointn - point1
        if edge2.length == 0:
            altitude = 0
            return altitude
        if edge1.length == 0:
            altitude = edge2.length
            return altitude
        alpha = edge1.angle(edge2)
        altitude = math.sin(alpha) * edge2.length
        return altitude

    def simplypoly(self,splineVerts, options):
        # main vars
        newVerts = []           # list of vertindices to keep
        points = splineVerts    # list of 3dVectors
        pointCurva = []         # table with curvatures
        curvatures = []         # averaged curvatures per vert
        for p in points:
            pointCurva.append([])
        order = options[3]      # order of sliding beziercurves
        k_thresh = options[2]   # curvature threshold
        dis_error = options[6]  # additional distance error
        # get curvatures per vert
        for i, point in enumerate(points[: -(order - 1)]):
            BVerts = points[i: i + order]
            for b, BVert in enumerate(BVerts[1: -1]):
                deriv1 = self.getDerivative(BVerts, 1 / (order - 1), order - 1)
                deriv2 = self.getDerivative(BVerts, 1 / (order - 1), order - 2)
                curva  = self.getCurvature(deriv1, deriv2)
                pointCurva[i + b + 1].append(curva)
        # average the curvatures
        for i in range(len(points)):
            avgCurva = sum(pointCurva[i]) / (order - 1)
            curvatures.append(avgCurva)
        # get distancevalues per vert - same as Ramer-Douglas-Peucker
        # but for every vert
        distances = [0.0]  # first vert is always kept
        for i, point in enumerate(points[1: -1]):
            dist = self.altitude(points[i], points[i + 2], points[i + 1])
            distances.append(dist)
        distances.append(0.0)  # last vert is always kept
        # generate list of vert indices to keep
        # tested against averaged curvatures and distances of neighbour verts
        newVerts.append(0)  # first vert is always kept
        for i, curv in enumerate(curvatures):
            if (curv >= k_thresh * 0.01 or distances[i] >= dis_error * 0.1):
                newVerts.append(i)
        newVerts.append(len(curvatures) - 1)  # last vert is always kept
        return newVerts

    def simplify_RDP(self, splineVerts, options):
        # main vars
        error = options[4]
        # set first and last vert
        newVerts = [0, len(splineVerts) - 1]
        # iterate through the points
        new = 1
        while new is not False:
            new = self.iterate(splineVerts, newVerts, error)
            if new:
                newVerts += new
                newVerts.sort()
        return newVerts

    def iterate(self, points, newVerts, error):
        new = []
        for newIndex in range(len(newVerts) - 1):
            bigVert = 0
            alti_store = 0
            for i, point in enumerate(points[newVerts[newIndex] + 1: newVerts[newIndex + 1]]):
                alti = self.altitude(points[newVerts[newIndex]], points[newVerts[newIndex + 1]], point)
                if alti > alti_store:
                    alti_store = alti
                    if alti_store >= error:
                        bigVert = i + 1 + newVerts[newIndex]
            if bigVert:
                new.append(bigVert)
        if new == []:
            return False
        return new