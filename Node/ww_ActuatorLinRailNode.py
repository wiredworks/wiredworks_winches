import bpy
import time
import ctypes

from mathutils import Vector

from .. exchange_data.Share import Shared
from .. exchange_data.ww_actuator_basic_props import ww_Actuator_basic_props
from .. exchange_data.ww_Joystick_props import ww_Joystick_props
from .. sockets import ww_input_actuator_socket
from .. sockets import ww_output_actuator_socket
from .. operator import SFX_Exists

class ww_ActuatorLinRailNode(bpy.types.Node):
    '''ww Linear Rail Actuator'''
    bl_idname = 'ww_ActuatorLinRail'
    bl_label = 'Rail Actuator'
    bl_icon = 'ARROW_LEFTRIGHT'
    bl_width_min = 580 # 920 to draw ww_Actuator_Props properly
    bl_width_max = 5000

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'ww_NodeTree'

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
    ist_Vel : bpy.props.FloatProperty(name = "Ist Vel",
                                     description = "Ist Vel",
                                    default = 0.0)
    ist_Pos : bpy.props.FloatProperty(name = "Ist Pos",
                                    description = "Ist Pos",
                                    default = 0.0)
    ist_Force : bpy.props.FloatProperty(name = "Ist Force",
                                    description = "Ist Force",
                                    default = 0.0)

    Shared : bpy.props.PointerProperty(type = Shared,
                                        update = update_value)
    ww_Actuator_basic_props : bpy.props.PointerProperty(type = ww_Actuator_basic_props)

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
    actuator_registered_bit1 : bpy.props.BoolProperty(name = "Operator Started",
                                        description = "Operator Started",
                                        default = False)
    TickTime_prop: bpy.props.FloatProperty(name = "Tick Time",
                                        description ="Sanity Check message round trip Time",
                                        default=0.014,
                                        precision=3,
                                        update = update_value)
    expand_Actuator_basic_data : bpy.props.BoolProperty(name = "Expand Basic Data",
                                    description = "Expand Basic Data",
                                    default = False)

    def init(self, context):
        self.inputs.new('ww_actuator_input_set_vel', "Set Vel")
        self.inputs["Set Vel"].set_vel = 0.0

        self.inputs.new('ww_actuator_input_select', "select_Act")
        self.inputs["select_Act"].select = False

        self.inputs.new('ww_actuator_input_enable', "enable_Act")
        self.inputs["enable_Act"].enable = False

        self.outputs.new('ww_actuator_output_ist_vel',name= 'Ist Pos')
        self.outputs["Ist Pos"].default_value = 0.0
        
        self.outputs.new('ww_actuator_output_ist_pos',name= 'Ist Vel')
        self.outputs["Ist Vel"].default_value = 0.0
        
        self.outputs.new('ww_actuator_output_ist_force',name= 'Ist Force')
        self.outputs["Ist Force"].default_value = 0.0
        
        self.draw_model(context)

    def copy(self, node):
        print("copied node", node)

    def free(self):
        ID = (self.actuator_name+'_'+
              str(self.socket_ip)+'_'+
              str(self.rsocket_port)+'_'+
              str(self.ssocket_port))
        try:
            self.Shared.ww_data[ID]["Destroy"] = True
        except KeyError:
            #print('not yet registered')
            pass
        obj1 = bpy.data.collections[self.name].objects[self.name+'_extr']
        bpy.data.objects.remove(obj1, do_unlink=True)
        obj2 = bpy.data.collections[self.name].objects[self.name+'_In']
        bpy.data.objects.remove(obj2, do_unlink=True)
        obj3 = bpy.data.collections[self.name].objects[self.name+'_Out']
        bpy.data.objects.remove(obj3, do_unlink=True)
        obj4 = bpy.data.collections[self.name].objects[self.name+'_Path']
        bpy.data.objects.remove(obj4, do_unlink=True)
        obj5 = bpy.data.collections[self.name].objects[self.name+'_Connector']
        bpy.data.objects.remove(obj5, do_unlink=True)
        bpy.data.collections.remove(bpy.data.collections.get(self.name))
        print("Node removed", ID, self)

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
        if not(self.actuator_registered_bit1):
            row7.operator('ww.actuator_register',text ='Register')
        else:
            row7.operator('ww.actuator_already_registered',text ='Registered')    
        row8.prop(self, 'ssocket_port', text = '')
        row9.prop(self, 'rsocket_port', text = '')
        row10.prop(self, 'socket_ip', text = '')
        row11.prop(self, 'actuator_name', text = '')        

        row2 = layout.row(align=True)
        row2.prop(self, 'expand_Actuator_basic_data')

        if self.expand_Actuator_basic_data:
            self.ww_Actuator_basic_props.draw_ww_Actuator_basic_props(context, layout)

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
                        pass
            if inp2.is_linked:
                for i1 in inp2.links:
                    if i1.is_valid:
                        self.inputs["enable_Act"].enabel=i1.from_socket.node.outputs[i1.from_socket.name].ww_out
                        pass
            if inp3.is_linked:
                for i1 in inp3.links:
                    if i1.is_valid:
                        self.inputs["select_Act"].select=i1.from_socket.node.outputs[i1.from_socket.name].ww_out
                        pass
            if out1.is_linked:
                for o in out1.links:
                    if i1.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].default_value = self.ist_Vel
                        pass
            if out2.is_linked:
                for i1 in out2.links:
                    if i1.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].default_value = self.ist_Pos
                        pass
            if out3.is_linked:
                for i1 in out3.links:
                    if i1.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].default_value = self.ist_Force
                        pass

    def draw_model(self,context):

        #if 'ww SFX_Nodes' in bpy.context.scene.collection.children.keys():            
        ww_Actcollection = bpy.data.collections.new(self.name)
    #    bpy.data.collections.get("ww SFX_Nodes").children.link(ww_Actcollection)
        bpy.data.collections.get("Collection").children.link(ww_Actcollection)
        #Add Bevel Thingy
        coords_list = ([[0.01,0.02,0], [0.06,0.06,0],[0.02,0.01,0],[0.02,-0.01,0],
                        [0.06,-0.06,0], [0.01,-0.02,0],[-0.01,-0.02,0],[-0.06,-0.06,0],
                        [-0.02,-0.01,0], [-0.02,0.01,0],[-0.06,0.06,0],[-0.01,0.02,0],[0.01,0.02,0]])
        extr = bpy.data.curves.new('crv', 'CURVE')
        extr.dimensions = '3D'
        spline = extr.splines.new(type='POLY')
        spline.points.add(len(coords_list)-1) # theres already one point by default
        for p, new_co in zip(spline.points, coords_list):
            p.co = (new_co + [1.0]) # (add nurbs weight)
        Extr = bpy.data.objects.new(self.name+'_extr', extr)
        ww_Actcollection.objects.link(Extr)
        # Add Path
        coords_list = ([[0,0,0], [0,0,0]])
        path = bpy.data.curves.new(self.name+'_path', 'CURVE')
        path.dimensions = "3D"
        spline = path.splines.new(type='POLY')
        spline.points.add(len(coords_list)-1)
        for p, new_co in zip(spline.points, coords_list):
            p.co = (new_co + [1.0]) # (add nurbs weight)
        Path = bpy.data.objects.new(self.name+'_Path', path)
        ww_Actcollection.objects.link(Path)
        # Bevel Bevel Thingy
        Path.data.bevel_object = Extr
        # Add Empties as hooks
        # In hook 
        In = bpy.data.objects.new( self.name+"_In", None )
        In.empty_display_size = 0.5
        In.empty_display_type = 'ARROWS'
        ww_Actcollection.objects.link( In )
        # Out hook
        Out = bpy.data.objects.new( self.name+"_Out", None )
        Out.empty_display_size = 0.5
        Out.empty_display_type = 'ARROWS'
        ww_Actcollection.objects.link( Out )
        # hook modifier left
        hook_left = Path.modifiers.new(name= 'hook_left', type = 'HOOK')
        Path.modifiers['hook_left'].object = bpy.data.objects[self.name+'_In']
        Path.modifiers['hook_left'].vertex_indices_set([0])
        # hook modifier right 
        hook_right = Path.modifiers.new(name= 'hook_right', type = 'HOOK')
        Path.modifiers['hook_right'].object = bpy.data.objects[self.name+'_Out']
        Path.modifiers['hook_right'].vertex_indices_set([1])
        # Object Connect 
        Connector = bpy.data.objects.new( self.name+"_Connector", None )
        Connector.empty_display_size = 0.25
        Connector.empty_display_type = 'SPHERE'
        Connector.constraints.new(type = 'CLAMP_TO')
        Connector.constraints['Clamp To'].target = Path
        ww_Actcollection.objects.link( Connector )

        Out.location = (0,0,5)
        #else:
        #   bpy.ops.ww.sfxexists('INVOKE_DEFAULT')
        
    #OPTIONAL
    #we can use this function to dynamically define the label of
    #   the node, however defining the bl_label explicitly overrides it
    #def draw_label(self):
    #   return "this label is shown"

   