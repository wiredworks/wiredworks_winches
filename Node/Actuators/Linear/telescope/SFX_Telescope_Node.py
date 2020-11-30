import bpy
import time
import ctypes
import math
import json
import numpy as np
from scipy.integrate import simps
from scipy.integrate import quad

from mathutils import Vector

from .SFX_Telescope_Model import SFX_Telescope_Model

from ..... exchange_data.sfx import sfx
from .SFX_Telescope_Data import actuator_telescope

from ..... SFX_Helpers.SFX_Calc_Default_Move import SFX_Calc_Default_Move

class SFX_LinRail_Node(bpy.types.Node):
    '''Telescope Actuator'''
    bl_idname = 'SFX_Telescope_Node'
    bl_label = 'telescope'
    bl_icon = 'ARROW_LEFTRIGHT'
    bl_width_min = 580 # 920 to draw ww_Actuator_Props properly
    bl_width_max = 580

    sfx_type     = 'Actuator'
    sfx_sub_type = 'Linear'
    sfx_id       = 'telescope'

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SFX_NodeTree'

    sfx          : bpy.props.PointerProperty(type = sfx)
    sfx_actuator : bpy.props.PointerProperty(type = actuator_telescope)

    def init(self, context):
        self.init_sfxData()

        self.inputs.new('SFX_Socket_Float', "Set Vel")
        self.inputs["Set Vel"].float = 0.0

        self.inputs.new('SFX_Socket_Bool', "select")
        self.inputs["select"].bool = False

        self.inputs.new('SFX_Socket_Bool', "enable")
        self.inputs["enable"].bool = False

        self.outputs.new('SFX_Socket_Float',name= 'Ist Pos')
        self.outputs["Ist Pos"].float = 0.0
        
        self.outputs.new('SFX_Socket_Float',name= 'Ist Vel')
        self.outputs["Ist Vel"].float = 0.0
        
        self.outputs.new('SFX_Socket_Float',name= 'Ist Force')
        self.outputs["Ist Force"].float = 0.0

        sfx.actuators[self.name].Actuator_basic_props.DigTwin_basic_props.Mother_name         = self.name
        sfx.actuators[self.name].Actuator_basic_props.DigTwin_basic_props.Mother_sfx_type     = self.sfx_type
        sfx.actuators[self.name].Actuator_basic_props.DigTwin_basic_props.Mother_sfx_sub_type = self.sfx_sub_type
        sfx.actuators[self.name].Actuator_basic_props.DigTwin_basic_props.Mother_sfx_id       = self.sfx_id

        self.SFX_drawTelescope = SFX_Telescope_Model(self.name)
        self.draw_model(self.name)

        action0 = sfx.actuators[self.name].Actuator_basic_props.Actuator_props.SFX_actions.add()
        action0.id = 0
        action0.name = self.name+'_default.sfxact'

        self.default_action(context, self.name, action0)        

        bpy.ops.sfx.save_action('INVOKE_DEFAULT')

    def copy(self, node):
        print("copied node", node)

    def free(self):
        sfx.actuators[self.name].operator_opened = False
        sfx.actuators.pop(self.name)
        bpy.data.meshes.remove(bpy.data.meshes[self.name], do_unlink = True)
        bpy.data.objects.remove(bpy.data.objects[self.name+'_In'],   do_unlink=True)
        bpy.data.objects.remove(bpy.data.objects[self.name+'_Out'],  do_unlink=True)
        bpy.data.objects.remove(bpy.data.objects[self.name+'_Connector'], do_unlink=True)      
        bpy.data.collections.remove(bpy.data.collections.get(self.name))

    def draw_buttons(self, context, layout):
        try:
            sfx.sensors[self.name]
        except KeyError:
            self.init_sfxData()       
        box = layout.box()
        col   = box.column(align = True)
        row4  = col.split(factor=0.85)         # Tick Time
        row5  = row4.split(factor=0.978)       # conn bit1
        row6  = row5.split(factor=0.978)       # conn bit2
        row7  = row6.split(factor=0.978)       # started
        row8  = row7.split(factor=0.978)       # running modal
        row9  = row8.split(factor=0.85)        # label
        row10  = row9.split(factor=0.85)        # ssocket
        row11 = row10.split(factor=0.83)       # rsocket 
        row12 = row11.split(factor=0.5)       # IP
        row13 = row12.split(factor=1)         # Name
        row4.prop(sfx.actuators[self.name], 'TickTime_prop', text = '')
        row5.prop(sfx.actuators[self.name], 'actuator_connected_bit2', text = '')
        row6.prop(sfx.actuators[self.name], 'actuator_connected_bit1', text = '')
        row7.prop(sfx.actuators[self.name], 'operator_running_modal', text = '')
        row8.prop(sfx.actuators[self.name], 'operator_started', text = '')
        if not(sfx.actuators[self.name].operator_started):
            row9.label(text ='Closed')
        else:
           row9.label(text ='Opened')
        row10.prop(sfx.actuators[self.name], 'ssocket_port', text = '')
        row11.prop(sfx.actuators[self.name], 'rsocket_port', text = '')
        row12.prop(sfx.actuators[self.name], 'socket_ip', text = '')
        row13.prop(sfx.actuators[self.name], 'actuator_name', text = '')      

        box = layout.box()
        col = box.column()
        row = col.split(factor= 0.8)
        row1= row.split(factor=0.7)
        row2= row1.split(factor=0.5)
        row3= row2.split(factor=1)
        row3.prop(sfx.actuators[self.name].Actuator_basic_props,'online_Actuator')
        row2.prop(sfx.actuators[self.name].Actuator_basic_props,'enable_Actuator')
        row1.prop(sfx.actuators[self.name].Actuator_basic_props,'select_Actuator')
        row.prop(sfx.actuators[self.name].Actuator_basic_props.Actuator_props,'simple_actuator_confirmed')

        row2 = layout.row(align=True)
        row2.prop(sfx.actuators[self.name], 'expand_Actuator_basic_data')

        if sfx.actuators[self.name].expand_Actuator_basic_data:
            sfx.actuators[self.name].Actuator_basic_props.draw_Actuator_basic_props(context, layout)

    def draw_buttons_ext(self, context, layout):
        pass

    def init_sfxData(self):
        sfx.actuators.update({self.name :self.sfx_actuator})
        pass

    def sfx_update(self):
        if sfx.actuators[self.name].operator_running_modal:
            self.color = (0,0.4,0.1)
            self.use_custom_color = True
        else:
            self.use_custom_color = False
        try:
            out1 = self.outputs["Ist Pos"]
            out2 = self.outputs["Ist Vel"]
            out3 = self.outputs["Ist Force"]
            inp1 = self.inputs['Set Vel']
            inp2 = self.inputs['enable']
            inp3 = self.inputs['select']
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if inp1.is_linked:
                for i1 in inp1.links:
                    if i1.is_valid:
                        self.inputs["Set Vel"].float=i1.from_socket.node.outputs[i1.from_socket.name].float
                        sfx.actuators[self.name].Actuator_basic_props.soll_Vel = \
                           (self.inputs["Set Vel"].float * sfx.actuators[self.name].Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop)/100.0
                        pass
            if inp2.is_linked:
                for i1 in inp2.links:
                    if i1.is_valid:
                        self.inputs["enable"].bool=i1.from_socket.node.outputs[i1.from_socket.name].bool
                        sfx.actuators[self.name].Actuator_basic_props.enable_Actuator = i1.from_socket.node.outputs[i1.from_socket.name].bool
                        pass
            if inp3.is_linked:
                for i1 in inp3.links:
                    if i1.is_valid:
                        self.inputs["select"].bool=i1.from_socket.node.outputs[i1.from_socket.name].bool
                        sfx.actuators[self.name].Actuator_basic_props.select_Actuator = i1.from_socket.node.outputs[i1.from_socket.name].bool
                        pass
            if out1.is_linked:
                for o in out1.links:
                    if o.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].float = sfx.actuators[self.name].Actuator_basic_props.ist_Pos
                        pass
            if out2.is_linked:
                for o in out2.links:
                    if o.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].float = sfx.actuators[self.name].Actuator_basic_props.ist_Vel
                        pass
            if out3.is_linked:
                for o in out3.links:
                    if o.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].float = sfx.actuators[self.name].Actuator_basic_props.ist_Force
                        pass

    def draw_model(self,name):
        self.SFX_drawTelescope.draw_model(name)

    def default_action(self, context, name, action0):

        Dataobject = bpy.data.objects[name+'_Connector']
        action0.minPos = sfx.actuators[name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop
        action0.maxPos = sfx.actuators[name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop
        action0.length = action0.maxPos - action0.minPos
        action0.maxAcc = sfx.actuators[name].Actuator_basic_props.Actuator_props.simple_actuator_AccMax_prop
        action0.maxVel = sfx.actuators[name].Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop

        self.DefaultMove = SFX_Calc_Default_Move(Dataobject, action0.length, action0.maxAcc, action0.maxVel )

        Jrk_Data =[]
        for i in range(0,len(bpy.data.objects['telescope_Connector'].animation_data.drivers[0].keyframe_points)):
            Jrk_Data.append((bpy.data.objects['telescope_Connector'].animation_data.drivers[0].keyframe_points[i].co[0],
            bpy.data.objects['telescope_Connector'].animation_data.drivers[0].keyframe_points[i].co[1]))
        Acc_Data =[]
        for i in range(0,len(bpy.data.objects['telescope_Connector'].animation_data.drivers[1].keyframe_points)):
            Acc_Data.append((bpy.data.objects['telescope_Connector'].animation_data.drivers[1].keyframe_points[i].co[0],
            bpy.data.objects['telescope_Connector'].animation_data.drivers[1].keyframe_points[i].co[1]))
        Vel_Data =[]
        for i in range(0,len(bpy.data.objects['telescope_Connector'].animation_data.drivers[2].keyframe_points)):
            Vel_Data.append((bpy.data.objects['telescope_Connector'].animation_data.drivers[2].keyframe_points[i].co[0],
            bpy.data.objects['telescope_Connector'].animation_data.drivers[2].keyframe_points[i].co[1]))
        Pos_Data =[]
        for i in range(0,len(bpy.data.objects['telescope_Connector'].animation_data.drivers[3].keyframe_points)):
            Pos_Data.append((bpy.data.objects['telescope_Connector'].animation_data.drivers[3].keyframe_points[i].co[0],
            bpy.data.objects['telescope_Connector'].animation_data.drivers[3].keyframe_points[i].co[1]))

        action0.Jrk = json.dumps(Jrk_Data)
        action0.Acc = json.dumps(Acc_Data)
        action0.Vel = json.dumps(Vel_Data)
        action0.Pos = json.dumps(Pos_Data)

        # self.fcurves_simplify(context, fcurves_sel, options, fcurves)

    def fcurves_simplify(self, context, fcurve_sel, options, fcurves):
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
            point = Vector((0, 0, 0))
        if len(verts[0]) == 2:
            point = Vector((0, 0))
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




   