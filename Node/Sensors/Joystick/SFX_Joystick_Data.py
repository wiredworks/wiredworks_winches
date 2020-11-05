import bpy

from .. SFX_Sensors_Base_Data import sensor_base
from . SFX_Joystick_Inset import SFX_Joystick_Inset

class sensor_joystick(bpy.types.PropertyGroup,sensor_base):
    ''' Defines sfx_sensor'''
    bl_idname = "sfx_sensor"

    Joystick_props : bpy.props.PointerProperty(type = SFX_Joystick_Inset)

    actuator_connected_bit1 : bpy.props.BoolProperty(name = "Connected",
                                    description = " Actuator Connected ?",
                                    default = False)
    actuator_connected_bit2 : bpy.props.BoolProperty(name = "Connected",
                                    description = " Actuator Connected ?",
                                    default = False)

    sensor_name: bpy.props.StringProperty(name = "Actuator Name",
                                    description = "Name of Actuator",
                                    default = "Joystick")    
    socket_ip: bpy.props.StringProperty(name = "Socket ip",
                                    description = "IP of Actuator",
                                    default = "127.0.0.1")
    rsocket_port: bpy.props.StringProperty(name = "Receive Socket port",
                                    description = "Receive Port of Actuator",
                                    default = "15017")
    ssocket_port: bpy.props.StringProperty(name = "Send Socket port",
                                    description = "Send Port of Actuator",
                                    default = "15018")

    expand_Joystick_data : bpy.props.BoolProperty(name = "Joystick Data",
                                    description = "Show Joystick Data",
                                    default = False)
