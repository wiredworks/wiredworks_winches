import bpy

from ...SFX_Actuators_Base_Data import actuator_base
from ...SFX_Actuators_Basic_Inset import SFX_Actuators_Basic_Inset


class actuator_simplelin(bpy.types.PropertyGroup,actuator_base):
    ''' Defines sfx_actuator'''
    bl_idname = "sfx_actuator"

    set_Vel : bpy.props.IntProperty(name = "Set Vel",
                                        description = "Set Vel",
                                        default = 0)
    enable_Act : bpy.props.BoolProperty(name='enable',
                                    description = 'Enable Actuator',
                                    default = False)
    selected_Act : bpy.props.BoolProperty(name='selected',
                                    description = 'Select Actuator',
                                    default = False)

    Actuator_basic_props : bpy.props.PointerProperty(type =SFX_Actuators_Basic_Inset)

    actuator_connected_bit1 : bpy.props.BoolProperty(name = "Connected",
                                        description = " Actuator Connected ?",
                                        default = False)
    actuator_connected_bit2 : bpy.props.BoolProperty(name = "Connected",
                                        description = " Actuator Connected ?",
                                        default = False)
    actuator_name: bpy.props.StringProperty(name = "Actuator Name",
                                        description = "Name of Actuator",
                                        default = "Cecil")    
    socket_ip: bpy.props.StringProperty(name = "Socket ip",
                                        description = "IP of Actuator",
                                        default = "127.0.0.1")
    rsocket_port: bpy.props.StringProperty(name = "Receive Socket port",
                                        description = "Receive Port of Actuator",
                                        default = "15025")
    ssocket_port: bpy.props.StringProperty(name = "Send Socket port",
                                        description = "Send Port of Actuator",
                                        default = "15026")

    expand_Actuator_basic_data : bpy.props.BoolProperty(name = "Expand Basic Data",
                                    description = "Expand Basic Data",
                                    default = False)