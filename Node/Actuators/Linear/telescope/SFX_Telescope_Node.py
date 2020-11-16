import bpy
import time
import ctypes

from mathutils import Vector

from .SFX_Telescope_Model import SFX_Telescope_Model

from ..... exchange_data.sfx import sfx
from .SFX_Telescope_Data import actuator_telescope

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

   