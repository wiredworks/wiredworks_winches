import bpy
import time
import ctypes

from mathutils import Vector

from .SFX_LinRail_Model import SFX_LinRail_Model

from .... exchange_data.sfx import sfx
from .... exchange_data.sfx import actuator_linrail

class SFX_LinRail_Node(bpy.types.Node):
    '''simple Linear Rail Actuator'''
    bl_idname = 'SFX_LinRail_Node'
    bl_label = 'linrail'
    bl_icon = 'ARROW_LEFTRIGHT'
    bl_width_min = 580 # 920 to draw ww_Actuator_Props properly
    bl_width_max = 580

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SFX_NodeTree'

    sfx          : bpy.props.PointerProperty(type = sfx)
    sfx_actuator : bpy.props.PointerProperty(type = actuator_linrail)

    def init(self, context):
        self.init_sfxData()

        self.inputs.new('SFX_act_in_set_Vel', "Set Vel")
        self.inputs["Set Vel"].set_vel = 0.0

        self.inputs.new('SFX_Act_in_select', "select_Act")
        self.inputs["select_Act"].select = False

        self.inputs.new('SFX_Act_in_enable', "enable_Act")
        self.inputs["enable_Act"].enable = False

        self.outputs.new('SFX_act_out_ist_Pos',name= 'Ist Pos')
        self.outputs["Ist Pos"].default_value = 0.0
        
        self.outputs.new('SFX_act_out_ist_Vel',name= 'Ist Vel')
        self.outputs["Ist Vel"].default_value = 0.0
        
        self.outputs.new('SFX_act_out_ist_Force',name= 'Ist Force')
        self.outputs["Ist Force"].default_value = 0.0

        sfx.actuators[self.name].Actuator_basic_props.DigTwin_basic_props.Mother_name = self.name

        self.SFX_drawLinRail = SFX_LinRail_Model(self.name)
        self.draw_model(self.name)

    def copy(self, node):
        print("copied node", node)

    def free(self):
        sfx.actuators[self.name].operator_opened = False
        sfx.actuators.pop(self.name)
        bpy.data.objects.remove(bpy.data.objects[self.name+'_extr'], do_unlink=True)
        bpy.data.objects.remove(bpy.data.objects[self.name+'_In'],   do_unlink=True)
        bpy.data.objects.remove(bpy.data.objects[self.name+'_Out'],  do_unlink=True)
        bpy.data.objects.remove(bpy.data.objects[self.name+'_Path'], do_unlink=True)
        bpy.data.objects.remove(bpy.data.objects[self.name+'_Connector'], do_unlink=True)
        bpy.data.collections.remove(bpy.data.collections.get(self.name))
        print("Node removed",self)

    def draw_buttons(self, context, layout):       
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
            inp2 = self.inputs['enable_Act']
            inp3 = self.inputs['select_Act']
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if inp1.is_linked:
                for i1 in inp1.links:
                    if i1.is_valid:
                        self.inputs["Set Vel"].set_vel=i1.from_socket.node.outputs[i1.from_socket.name].ww_out_value
                        sfx.actuators[self.name].Actuator_basic_props.soll_Vel = \
                           (self.inputs["Set Vel"].set_vel * sfx.actuators[self.name].Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop)/100.0
                        pass
            if inp2.is_linked:
                for i1 in inp2.links:
                    if i1.is_valid:
                        self.inputs["enable_Act"].enable=i1.from_socket.node.outputs[i1.from_socket.name].ww_out
                        sfx.actuators[self.name].Actuator_basic_props.enable_Actuator = i1.from_socket.node.outputs[i1.from_socket.name].ww_out
                        pass
            if inp3.is_linked:
                for i1 in inp3.links:
                    if i1.is_valid:
                        self.inputs["select_Act"].select=i1.from_socket.node.outputs[i1.from_socket.name].ww_out
                        sfx.actuators[self.name].Actuator_basic_props.select_Actuator = i1.from_socket.node.outputs[i1.from_socket.name].ww_out
                        pass
            if out1.is_linked:
                for o in out1.links:
                    if o.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].default_value_set = sfx.actuators[self.name].Actuator_basic_props.ist_Vel
                        pass
            if out2.is_linked:
                for o in out2.links:
                    if o.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].default_value_set = sfx.actuators[self.name].Actuator_basic_props.ist_Pos
                        pass
            if out3.is_linked:
                for o in out3.links:
                    if o.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].default_value_set = sfx.actuators[self.name].Actuator_basic_props.ist_Force
                        pass

    def draw_model(self,name):
        self.SFX_drawLinRail.draw_model(name)

   