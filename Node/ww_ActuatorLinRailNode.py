import bpy
import time
import ctypes

from .. exchange_data.Share import Shared
from .. exchange_data.ww_actuator_basic_props import ww_Actuator_basic_props

class ww_ActuatorLinRailNode(bpy.types.Node):
    '''ww Linear Rail Actuator'''
    bl_idname = 'ww_ActuatorLinRail'
    bl_label = 'Rail Actuator'
    bl_icon = 'ARROW_LEFTRIGHT'
    bl_width_min = 600 # 920 to draw ww_Actuator_Props properly
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
        pass

    def copy(self, node):
        print("copied node", node)

    def free(self):
        ID = (self.actuator_name+'_'+
              str(self.socket_ip)+'_'+
              str(self.rsocket_port)+'_'+
              str(self.ssocket_port))
        self.Shared.ww_data[ID]["Destroy"] = True
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

    #OPTIONAL
    #we can use this function to dynamically define the label of
    #   the node, however defining the bl_label explicitly overrides it
    #def draw_label(self):
    #   return "this label is shown"

   