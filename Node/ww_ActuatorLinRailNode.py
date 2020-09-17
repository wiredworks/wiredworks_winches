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

    def update_func(self,context):
        pass    

    Shared : bpy.props.PointerProperty(type = Shared,
                                        update = update_func)
    ww_Actuator_basic_props : bpy.props.PointerProperty(type = ww_Actuator_basic_props)


    actuator_connected_bit1 : bpy.props.BoolProperty(name = "Connected",
                                        description = " Actuator Connected ?",
                                        default = False,
                                        update = update_func)
    actuator_connected_bit2 : bpy.props.BoolProperty(name = "Connected",
                                        description = " Actuator Connected ?",
                                        default = False,
                                        update = update_func)
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
                                        precision=3)
    expand_Actuator_basic_data : bpy.props.BoolProperty(name = "Expand Basic Data",
                                    description = "Expand Basic Data",
                                    default = False)


    def init(self, context):
        self.inputs.new('ww_actuator_input_set_vel', "Set Vel")
        self.inputs["Set Vel"].default_value = 0.0

        self.inputs.new('ww_actuator_input_select', "enable")
        self.inputs["enable"].default_value = 0.0

        self.inputs.new('ww_actuator_input_enable', "select")
        self.inputs["select"].default_value = 0.0

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

    def draw_model(self,context):

        if 'ww SFX_Nodes' in bpy.context.scene.collection.children.keys():            
            Actcollection = bpy.data.collections.new(self.name)
            bpy.data.collections.get("ww SFX_Nodes").children.link(Actcollection)
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
            Actcollection.objects.link(Extr)
            # Add Path
            coords_list = ([[0,0,0], [0,0,0]])
            path = bpy.data.curves.new(self.name+'_path', 'CURVE')
            path.dimensions = "3D"
            spline = path.splines.new(type='POLY')
            spline.points.add(len(coords_list)-1)
            for p, new_co in zip(spline.points, coords_list):
                p.co = (new_co + [1.0]) # (add nurbs weight)
            Path = bpy.data.objects.new(self.name+'_Path', path)
            Actcollection.objects.link(Path)
            # Bevel Bevel Thingy
            Path.data.bevel_object = Extr
            # Add Empties as hooks
            # In hook 
            In = bpy.data.objects.new( self.name+"_In", None )
            In.empty_display_size = 2
            In.empty_display_type = 'ARROWS'
            Actcollection.objects.link( In )
            # Out hook
            Out = bpy.data.objects.new( self.name+"_Out", None )
            Out.empty_display_size = 2
            Out.empty_display_type = 'ARROWS'
            Actcollection.objects.link( Out )
            # hook modifier left
            hook_left = Path.modifiers.new(name= 'hook_left', type = 'HOOK')
            Path.modifiers['hook_left'].object = bpy.data.objects[self.name+'_In']
            Path.modifiers['hook_left'].vertex_indices_set([0])
            # hook modifier right 
            hook_right = Path.modifiers.new(name= 'hook_right', type = 'HOOK')
            Path.modifiers['hook_right'].object = bpy.data.objects[self.name+'_Out']
            Path.modifiers['hook_right'].vertex_indices_set([1])
        else:
            bpy.ops.ww.sfxexists('INVOKE_DEFAULT')
            pass
    #OPTIONAL
    #we can use this function to dynamically define the label of
    #   the node, however defining the bl_label explicitly overrides it
    #def draw_label(self):
    #   return "this label is shown"

   