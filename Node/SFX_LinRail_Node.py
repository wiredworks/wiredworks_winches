import bpy
import time
import ctypes

from mathutils import Vector

from .. exchange_data.SFX_actuator_basic_Inset import SFX_actuator_basic_Inset
from .. exchange_data.SFX_Joystick_Inset import SFX_Joystick_Inset
from ..models.SFX_draw_LinRail import SFX_drawLinRail

class SFX_LinRailNode(bpy.types.Node):
    '''simple Linear Rail Actuator'''
    bl_idname = 'SFX_LinRailNode'
    bl_label = 'Simple Rail Actuator'
    bl_icon = 'ARROW_LEFTRIGHT'
    bl_width_min = 580 # 920 to draw ww_Actuator_Props properly
    bl_width_max = 5000

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SFX_NodeTree'

    def update_value(self,context):
        self.update()
        pass

    set_Vel : bpy.props.IntProperty(name = "Set Vel",
                                        description = "Set Vel",
                                        default = 0)
    enable_Act : bpy.props.BoolProperty(name='enable',
                                    description = 'Enable Actuator',
                                    default = False)
    selected_Act : bpy.props.BoolProperty(name='selected',
                                    description = 'Select Actuator',
                                    default = False)

    Actuator_basic_props : bpy.props.PointerProperty(type =SFX_actuator_basic_Inset)

    actuator_connected_bit1 : bpy.props.BoolProperty(name = "Connected",
                                        description = " Actuator Connected ?",
                                        default = False)
    actuator_connected_bit2 : bpy.props.BoolProperty(name = "Connected",
                                        description = " Actuator Connected ?",
                                        default = False)
    actuator_name: bpy.props.StringProperty(name = "Actuator Name",
                                        description = "Name of Actuator",
                                        default = "Anton")    
    socket_ip: bpy.props.StringProperty(name = "Socket ip",
                                        description = "IP of Actuator",
                                        default = "127.0.0.1")
    rsocket_port: bpy.props.StringProperty(name = "Receive Socket port",
                                        description = "Receive Port of Actuator",
                                        default = "15021")
    ssocket_port: bpy.props.StringProperty(name = "Send Socket port",
                                        description = "Send Port of Actuator",
                                        default = "15022")
    operator_started_bit1 : bpy.props.BoolProperty(name = "Operator Started",
                                        description = "Operator Started",
                                        default = False)
    TickTime_prop: bpy.props.FloatProperty(name = "Tick Time",
                                        description ="Sanity Check message round trip Time",
                                        default=0.014,
                                        precision=1,
                                        update = update_value)
    expand_Actuator_basic_data : bpy.props.BoolProperty(name = "Expand Basic Data",
                                    description = "Expand Basic Data",
                                    default = False)


    def init(self, context):

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

        self.Actuator_basic_props.DigTwin_basic_props.Mother_name = self.name

        self.SFX_drawLinRail = SFX_drawLinRail(self.name)
        #self.draw_model(context)
        self.draw_model(self.name)

    def copy(self, node):
        print("copied node", node)

    def free(self):
        self.operator_started_bit1 = False
        bpy.data.objects.remove(bpy.data.objects[self.name+'_extr'], do_unlink=True)
        bpy.data.objects.remove(bpy.data.objects[self.name+'_In'],   do_unlink=True)
        bpy.data.objects.remove(bpy.data.objects[self.name+'_Out'],  do_unlink=True)
        bpy.data.objects.remove(bpy.data.objects[self.name+'_Path'], do_unlink=True)
        bpy.data.objects.remove(bpy.data.objects[self.name+'_Connector'], do_unlink=True)
        bpy.data.collections.remove(bpy.data.collections.get(self.name))
        print("Node removed",self)

    def draw_buttons(self, context, layout):
       
        box = layout.box()
        col = box.column(align = True)
        row4 = col.split(factor=0.91)         # Tick Time
        row5 = row4.split(factor=0.978)       # conn bit1
        row6 = row5.split(factor=0.978)       # conn bit2
        row7 = row6.split(factor=0.85)        # register
        row8 = row7.split(factor=0.85)        # ssocket
        row9 = row8.split(factor=0.85)        # rsocket 
        row10 = row9.split(factor=0.5)        # IP
        row11 = row10.split(factor=1)         # Name
        row4.prop( self, 'TickTime_prop', text = '')
        row5.prop(self, 'actuator_connected_bit2', text = '')
        row6.prop(self, 'actuator_connected_bit1', text = '')
        if not(self.operator_started_bit1):
            row7.operator('sfx.commactop',text ='Register')
        else:
            row7.operator('sfx.commstarteddiag',text ='Registered')    
        row8.prop(self, 'ssocket_port', text = '')
        row9.prop(self, 'rsocket_port', text = '')
        row10.prop(self, 'socket_ip', text = '')
        row11.prop(self, 'actuator_name', text = '')        

        row2 = layout.row(align=True)
        row2.prop(self, 'expand_Actuator_basic_data')

        if self.expand_Actuator_basic_data:
            self.Actuator_basic_props.draw_Actuator_basic_props(context, layout)

    def draw_buttons_ext(self, context, layout):
        layout.label(text='Adress')
        layout.prop(self, 'socket_ip', text = 'IP')
        layout.prop(self, 'rsocket_port', text = 'Rec Port')
        layout.prop(self, 'ssocket_port', text = 'Send Port')

    def update(self):
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
                        self.Actuator_basic_props.soll_Vel = \
                           (self.inputs["Set Vel"].set_vel * self.Actuator_basic_props.Actuator_props.simple_actuator_VelMax_prop)/100.0
                        pass
            if inp2.is_linked:
                for i1 in inp2.links:
                    if i1.is_valid:
                        self.inputs["enable_Act"].enable=i1.from_socket.node.outputs[i1.from_socket.name].ww_out
                        self.Actuator_basic_props.enable_Actuator = i1.from_socket.node.outputs[i1.from_socket.name].ww_out
                        pass
            if inp3.is_linked:
                for i1 in inp3.links:
                    if i1.is_valid:
                        self.inputs["select_Act"].select=i1.from_socket.node.outputs[i1.from_socket.name].ww_out
                        self.Actuator_basic_props.select_Actuator = i1.from_socket.node.outputs[i1.from_socket.name].ww_out
                        pass
            if out1.is_linked:
                for o in out1.links:
                    if o.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].default_value_set = self.Actuator_basic_props.ist_Vel
                        pass
            if out2.is_linked:
                for o in out2.links:
                    if o.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].default_value_set = self.Actuator_basic_props.ist_Pos
                        pass
            if out3.is_linked:
                for o in out3.links:
                    if o.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].default_value_set = self.Actuator_basic_props.ist_Force
                        pass

    def draw_model(self,name):
        self.SFX_drawLinRail.draw_model(name)

    #OPTIONAL
    #we can use this function to dynamically define the label of
    #   the node, however defining the bl_label explicitly overrides it
    #def draw_label(self):
    #   return "this label is shown"

   