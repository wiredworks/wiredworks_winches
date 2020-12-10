import bpy
import mathutils
import math
import time
import json

from ..exchange_data.sfx import sfx

class SFX_OT_Simplyfy(bpy.types.Operator):
    bl_idname = "sfx.simplify"
    bl_label = "Simplyify"
    # Properties

    opModes = [
        ('DISTANCE', 'Distance', 'Distance-based simplification (Poly)'),
            ('CURVATURE', 'Curvature', 'Curvature-based simplification (RDP)')]
    mode: bpy.props.EnumProperty(
        name="Mode",
            description="Choose algorithm to use",
            items=opModes
    )
    k_thresh: bpy.props.FloatProperty(
        name="k",
            min=0, soft_min=0,
            default=0, precision=5,
            description="Threshold"
    )
    pointsNr: bpy.props.IntProperty(
        name="n",
            min=5, soft_min=5,
            max=16, soft_max=9,
            default=5,
            description="Degree of curve to get averaged curvatures"
    )
    error: bpy.props.FloatProperty(
        name="Error",
            description="Maximum allowed distance error",
            min=0.0, soft_min=0.0,
            default=0.1, precision=5,
            step = 0.1
    )
    degreeOut: bpy.props.IntProperty(
        name="Degree",
            min=3, soft_min=3,
            max=7, soft_max=7,
            default=5,
            description="Degree of new curve"
    )
    dis_error: bpy.props.FloatProperty(
        name="Distance error",
            description="Maximum allowed distance error in Blender Units",
            min=0, soft_min=0,
            default=0.02, precision=5
    )
    fcurves = []

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        col.label(text="Distance Error:")
        col.prop(self, "error", expand=True)

    def execute(self, context):
        options = [ self.mode,       # 0
                    self.mode,       # 1
                    self.k_thresh,   # 2
                    self.pointsNr,   # 3
                    self.error,      # 4
                    self.degreeOut,  # 6
                    self.dis_error ] # 7
        
        options = ('DISTANCE', 0, 1, 3, 0.015, 0, 0.52)
        self.fcurves_simplify(self.fcurve_sel, options, self.fcurves)

        for i in range(0,len(self.VPcurve.keyframe_points)):
            self.VPcurve.keyframe_points[i].interpolation = 'BEZIER'

        try:
            self.VPcurve.keyframe_points[-1].handle_right = (self.VPcurve.keyframe_points[-1].co[0],-5)
            self.VPcurve.keyframe_points[-1].handle_left  = (self.VPcurve.keyframe_points[-1].co[0],self.VPcurve.keyframe_points[-2].co[1]/3.0)
            self.VPcurve.keyframe_points[0].handle_right = (self.VPcurve.keyframe_points[0].co[0],self.VPcurve.keyframe_points[1].co[1]/2.0)
            self.VPcurve.keyframe_points[0].handle_left  = (self.VPcurve.keyframe_points[0].co[0],-5)
        except IndexError:
            pass      
        
        self.Save_Simplified_Curve()

        self.tag_redraw(context, space_type = 'GRAPH_EDITOR', region_type ='WINDOW')

    def Save_Simplified_Curve(self):
        if self.type == 'Actuator': 
            index      = sfx.actuators[self.mothernode.name].Actuator_basic_props.Actuator_props.SFX_actions_index
            action0    = sfx.actuators[self.mothernode.name].Actuator_basic_props.Actuator_props.SFX_actions[index]
            action0.id = index

            Jrk_Data =[[],[]]
            for i in range(0,len(bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[0].keyframe_points)):
                Jrk_Data[0].append(bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[0].keyframe_points[i].co[0])
                Jrk_Data[1].append(bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[0].keyframe_points[i].co[1])
            Acc_Data =[[],[]]
            for i in range(0,len(bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[1].keyframe_points)):
                Acc_Data[0].append(bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[1].keyframe_points[i].co[0])
                Acc_Data[1].append(bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[1].keyframe_points[i].co[1])
            Vel_Data =[[],[]]
            for i in range(0,len(bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[2].keyframe_points)):
                Vel_Data[0].append(bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[2].keyframe_points[i].co[0])
                Vel_Data[1].append(bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[2].keyframe_points[i].co[1])
            Pos_Data =[[],[]]
            for i in range(0,len(bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[3].keyframe_points)):
                Pos_Data[0].append(bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[3].keyframe_points[i].co[0])
                Pos_Data[1].append(bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[3].keyframe_points[i].co[1])
            Vel_Pos_Data =[[],[]]
            for i in range(0,len(bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[4].keyframe_points)):
                Vel_Pos_Data[0].append(bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[4].keyframe_points[i].co[0])
                Vel_Pos_Data[1].append(bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[4].keyframe_points[i].co[1])
        elif self.type =='Cue':
            index      = sfx.cues[self.mothernode.name].Actuator_props.SFX_actions_index
            action0    = sfx.cues[self.mothernode.name].Actuator_props.SFX_actions[index]
            action0.id = index

            Jrk_Data =[[],[]]
            for i in range(0,len(bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[0].keyframe_points)):
                Jrk_Data[0].append(bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[0].keyframe_points[i].co[0])
                Jrk_Data[1].append(bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[0].keyframe_points[i].co[1])
            Acc_Data =[[],[]]
            for i in range(0,len(bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[1].keyframe_points)):
                Acc_Data[0].append(bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[1].keyframe_points[i].co[0])
                Acc_Data[1].append(bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[1].keyframe_points[i].co[1])
            Vel_Data =[[],[]]
            for i in range(0,len(bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[2].keyframe_points)):
                Vel_Data[0].append(bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[2].keyframe_points[i].co[0])
                Vel_Data[1].append(bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[2].keyframe_points[i].co[1])
            Pos_Data =[[],[]]
            for i in range(0,len(bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[3].keyframe_points)):
                Pos_Data[0].append(bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[3].keyframe_points[i].co[0])
                Pos_Data[1].append(bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[3].keyframe_points[i].co[1])
            Vel_Pos_Data =[[],[]]
            for i in range(0,len(bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[4].keyframe_points)):
                Vel_Pos_Data[0].append(bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[4].keyframe_points[i].co[0])
                Vel_Pos_Data[1].append(bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[4].keyframe_points[i].co[1])            

        action0.Jrk = json.dumps(Jrk_Data)
        action0.Acc = json.dumps(Acc_Data)
        action0.Vel = json.dumps(Vel_Data)
        action0.Pos = json.dumps(Pos_Data)
        action0.VP  = json.dumps(Vel_Pos_Data) 

        #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)


        return {'FINISHED'}

    def tag_redraw(self, context, space_type="PROPERTIES", region_type="WINDOW"):
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.spaces[0].type == space_type:
                        for region in area.regions:
                            if region.type == region_type:
                                region.tag_redraw()

    def invoke(self, context, event):
        self.mothernode = bpy.context.active_node
        self.type =  self.mothernode.sfx_type
        if self.type == 'Actuator':
            self.Jrkcurve = bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[0]
            self.Acccurve = bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[1]
            self.Velcurve = bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[2]
            self.Poscurve = bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[3]
            self.VPcurve  = bpy.data.objects[self.mothernode.name+'_Connector'].animation_data.drivers[4]
            self.fcurve_sel = [self.Jrkcurve, self.Acccurve, self.Velcurve, self.Poscurve, self.VPcurve]
        elif self.type =='Cue':
            self.Jrkcurve = bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[0]
            self.Acccurve = bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[1]
            self.Velcurve = bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[2]
            self.Poscurve = bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[3]
            self.VPcurve  = bpy.data.objects[self.mothernode.name+'_Data'].animation_data.action.fcurves[4]
            self.fcurve_sel = [self.Jrkcurve, self.Acccurve, self.Velcurve, self.Poscurve, self.VPcurve]

        self.fcurves=[]
        for i in range(0,len(self.fcurve_sel)):
            points = []
            for j in range(0, len(self.fcurve_sel[i].keyframe_points)):
                x = self.fcurve_sel[i].keyframe_points[j].co.x
                y = self.fcurve_sel[i].keyframe_points[j].co.y
                points.append(mathutils.Vector((x, y)))
            self.fcurves.append(points)
        self.execute(context)

        return {"FINISHED"}

    def fcurves_simplify(self, fcurve_sel, options, fcurves):
        # main vars
        mode = options[0]
        #for fcurve_i, fcurve in enumerate(fcurves):
        for i in range(0, len(fcurves)):
            # test if fcurve is long enough
            if len(fcurves[i]) >= 3:
                # simplify spline according to mode
                if mode == 'DISTANCE':
                    newVerts = self.simplify_RDP(fcurves[i], options)
                if mode == 'CURVATURE':
                    newVerts = self.simplypoly(fcurves[i], options)
                # convert indices into vectors3D
                newPoints = []
                # this is different from the main() function for normal curves, different api...
                for v in newVerts:
                    newPoints.append(fcurves[i][v])
                # remove all points from curve first
                for j in range(len(fcurves[i]) - 1, 0, -1):
                    fcurve_sel[i].keyframe_points.remove(fcurve_sel[i].keyframe_points[j])
                # put newPoints into fcurve
                for v in newPoints:
                    fcurve_sel[i].keyframe_points.insert(frame=v[0], value=v[1])
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

 