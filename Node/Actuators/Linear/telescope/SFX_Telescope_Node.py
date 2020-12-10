import bpy
import time
import ctypes
import json

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

        self.inputs.new('SFX_Socket_Float', "Joy In")
        self.inputs["Joy In"].float = 0.0

        self.inputs.new('SFX_Socket_Float', "Cue In")
        self.inputs["Cue In"].float = 0.0

        self.inputs.new('SFX_Socket_Int', "Action Select")
        self.inputs["Action Select"].int = 0

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

        self.Init_Driver_Curves()
        action = self.Calc_Default_Action()
        self.Plot_Driver_Curves(action)        

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

        self.inputs["Action Select"].int= sfx.actuators[self.name].Actuator_basic_props.Actuator_props.SFX_actions_index

        if sfx.actuators[self.name].operator_running_modal:
            self.color = (0,0.4,0.1)
            self.use_custom_color = True
        else:
            self.use_custom_color = False
        try:
            out1  = self.outputs["Ist Pos"]
            out2  = self.outputs["Ist Vel"]
            out3  = self.outputs["Ist Force"]
            JoyIn = self.inputs['Joy In']
            CueIn = self.inputs['Cue In']
            ASel  = self.inputs['Action Select']
            enab  = self.inputs['enable']
            sele  = self.inputs['select']
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if JoyIn.is_linked:
                for i1 in JoyIn.links:
                    if i1.is_valid:
                        self.inputs["Joy In"].float=i1.from_socket.node.outputs[i1.from_socket.name].float
            if CueIn.is_linked:
                for i1 in CueIn.links:
                    if i1.is_valid:
                        self.inputs["Cue In"].float=i1.from_socket.node.outputs[i1.from_socket.name].float

            if  JoyIn.is_linked or CueIn.is_linked :
                self.Calc_soll_Vel()           

            if ASel.is_linked:
                for i1 in ASel.links:
                    if i1.is_valid:
                        sfx.actuators[self.name].Actuator_basic_props.Actuator_props.SFX_actions_index=i1.from_socket.node.outputs[i1.from_socket.name].int
                        pass
            if enab.is_linked:
                for i1 in enab.links:
                    if i1.is_valid:
                        self.inputs["enable"].bool=i1.from_socket.node.outputs[i1.from_socket.name].bool
                        sfx.actuators[self.name].Actuator_basic_props.enable_Actuator = i1.from_socket.node.outputs[i1.from_socket.name].bool
                        pass
            if sele.is_linked:
                for i1 in sele.links:
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

    def Calc_Default_Action(self):
        action0 = sfx.actuators[self.name].Actuator_basic_props.Actuator_props.SFX_actions.add()
        action0.id = 0
        action0.name = self.name+'_default.sfxact'
        action0.minPos = sfx.actuators[self.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop
        action0.maxPos = sfx.actuators[self.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop
        action0.length = action0.maxPos - action0.minPos
        action0.maxAcc = sfx.actuators[self.name].Actuator_basic_props.Actuator_props.simple_actuator_AccMax_prop
        action0.maxVel = sfx.actuators[self.name].Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop

        A = SFX_Calc_Default_Move(action0.length, action0.maxAcc, action0.maxVel )
        Jrk_Data,Acc_Data,Vel_Data,Pos_Data,Vel_Pos_Data = SFX_Calc_Default_Move.out(A)

        action0.Jrk = json.dumps(Jrk_Data)
        action0.Acc = json.dumps(Acc_Data)
        action0.Vel = json.dumps(Vel_Data)
        action0.Pos = json.dumps(Pos_Data)
        action0.VP  = json.dumps(Vel_Pos_Data)

        return action0

        # self.maxJrk = max(abs(self.JrkC))
        # self.maxAcc = max(abs(self.AccC))
        # self.maxVel = max((self.VelC))
        # self.maxPos = max(abs(self.PosC))
        # self.maxTime = self.X[-1]

    def Init_Driver_Curves(self):               
        bpy.data.objects[self.name+'_Connector']['Pos'] = 0
        bpy.data.objects[self.name+'_Connector']['Vel'] = 0
        bpy.data.objects[self.name+'_Connector']['Acc'] = 0
        bpy.data.objects[self.name+'_Connector']['Jrk'] = 0 
        bpy.data.objects[self.name+'_Connector']['Vel-Time'] = 0
        try:
            bpy.data.objects[self.name+'_Connector'].driver_remove('["Jrk"]')
            bpy.data.objects[self.name+'_Connector'].driver_remove('["Acc"]')
            bpy.data.objects[self.name+'_Connector'].driver_remove('["Vel"]')
            bpy.data.objects[self.name+'_Connector'].driver_remove('["Pos"]')
            bpy.data.objects[self.name+'_Connector'].driver_remove('["Vel-Time"]')
        except:
             pass
        self.Jrkcurve = bpy.data.objects[self.name+'_Connector'].driver_add('["Jrk"]')
        # THX to Philipp Oeser (lichtwerk)
        # to edit the driver fcurve with keyframes, you'll have to remove the fmodifier
        try:
            self.Jrkcurve.modifiers.remove(self.Jrkcurve.modifiers[0])
        except IndexError:
            pass
        self.Acccurve = bpy.data.objects[self.name+'_Connector'].driver_add('["Acc"]')
        try:
            self.Acccurve.modifiers.remove(self.Acccurve.modifiers[0])
        except IndexError:
            pass
        self.Velcurve = bpy.data.objects[self.name+'_Connector'].driver_add('["Vel"]')
        try:
            self.Velcurve.modifiers.remove(self.Velcurve.modifiers[0])
        except IndexError:
            pass
        self.Poscurve = bpy.data.objects[self.name+'_Connector'].driver_add('["Pos"]')
        try:
            self.Poscurve.modifiers.remove(self.Poscurve.modifiers[0])
        except IndexError:
            pass
        self.VPcurve = bpy.data.objects[self.name+'_Connector'].driver_add('["Vel-Time"]')
        try:
            self.VPcurve.modifiers.remove(self.VPcurve.modifiers[0])
        except IndexError:
            pass

    def Plot_Driver_Curves(self, action):
        Jrk = json.loads(action.Jrk)
        Acc = json.loads(action.Acc)
        Vel = json.loads(action.Vel)
        Pos = json.loads(action.Pos)
        VP  = json.loads(action.VP)
        self.Jrkcurve.keyframe_points.insert(0,0) 
        for i in range(0,len(Jrk[0])):
            if Jrk[0][i]>0.01:
                A=self.Jrkcurve.keyframe_points.insert(Jrk[0][i],Jrk[1][i], options =  {'FAST'}) 
                A.interpolation = 'LINEAR'
        self.Acccurve.keyframe_points.insert(0,0)
        for i in range(0,len(Acc[0])):
            if Acc[0][i]>0.01:
                A=self.Acccurve.keyframe_points.insert(Acc[0][i],Acc[1][i], options =  {'FAST'}) 
                A.interpolation = 'LINEAR'
        self.Velcurve.keyframe_points.insert(0,0)
        for i in range(0,len(Vel[0])):
            if Vel[0][i]>0.01:
                A=self.Velcurve.keyframe_points.insert(Vel[0][i],Vel[1][i], options =  {'FAST'}) 
                A.interpolation = 'LINEAR'
        self.Poscurve.keyframe_points.insert(0,0)
        for i in range(0,len(Pos[0])):
            if Pos[0][i]>0.01:
                A=self.Poscurve.keyframe_points.insert(Pos[0][i],Pos[1][i], options =  {'FAST'}) 
                A.interpolation = 'LINEAR'
        self.VPcurve.keyframe_points.insert(0,0)         
        for i in range(0,len(VP[0])):
            if VP[0][i]>0.01:
                A=self.VPcurve.keyframe_points.insert(VP[0][i],VP[1][i], options =  {'FAST'}) 
                A.interpolation = 'LINEAR'        

    def Calc_soll_Vel(self):
        J = self.inputs["Joy In"].float
        C = (self.inputs["Cue In"].float)
        Vel_Pos_Limit =bpy.data.objects[self.name+'_Connector'].animation_data.drivers[4]
        VIn    = max(min(J+C,100),-100)
        IstPos = sfx.actuators[self.name].Actuator_basic_props.ist_Pos
        MinPos = sfx.actuators[self.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop
        MaxPos = sfx.actuators[self.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop
        MaxVel = sfx.actuators[self.name].Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop

        LimitVel = Vel_Pos_Limit.evaluate(sfx.actuators[self.name].Actuator_basic_props.ist_Pos -\
                sfx.actuators[self.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop)

        if IstPos < MinPos and VIn > 0 and IstPos < MaxPos:
            #print('Moving from minus into Valid Intervall')
            LimitVel = MaxVel / 3.0
        elif MinPos <= IstPos  and VIn > 0 and LimitVel < 0.01 and IstPos <= MaxPos :                   
            LimitVel = 0.01
        elif MinPos <= IstPos and VIn < 0 and LimitVel < 0.01 and IstPos <= MaxPos :
            LimitVel = 0.01
        elif IstPos > MaxPos and VIn < 0 and IstPos > MinPos:
            #print('Moving from plus into Valid Intervall')
            LimitVel = MaxVel / 3.0
        else:
            LimitVel = Vel_Pos_Limit.evaluate(sfx.actuators[self.name].Actuator_basic_props.ist_Pos -\
                sfx.actuators[self.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop)

        sfx.actuators[self.name].Actuator_basic_props.soll_Vel = VIn * LimitVel/100.0