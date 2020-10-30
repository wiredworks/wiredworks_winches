import bpy

from .. exchange_data.SFX_Joystick_Inset import SFX_Joystick_Inset

class sfx_sensor(bpy.types.PropertyGroup):
    ''' Defines sfx_sensor'''
    bl_idname = "sfx_sensor"

    ww_Joystick_props : bpy.props.PointerProperty(type = SFX_Joystick_Inset)

    actuator_connected_bit1 : bpy.props.BoolProperty(name = "Connected",
                                    description = " Actuator Connected ?",
                                    default = False)
    actuator_connected_bit2 : bpy.props.BoolProperty(name = "Connected",
                                    description = " Actuator Connected ?",
                                    default = False)
    actuator_name: bpy.props.StringProperty(name = "Actuator Name",
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
    operator_registered : bpy.props.BoolProperty(name = "Operator Started",
                                    description = "Operator Started",
                                    default = False)
    TickTime_prop: bpy.props.FloatProperty(name = "Tick Time",
                                    description ="Sanity Check message round trip Time",
                                    default=0.1,
                                    precision=1)
    expand_Joystick_data : bpy.props.BoolProperty(name = "Joystick Data",
                                    description = "Show Joystick Data",
                                    default = False)

class sfx_cue(bpy.types.PropertyGroup):
    ''' Defines sfx_cue'''
    bl_idname = "sfx_cue"

    X_Achse : bpy.props.FloatProperty(name = "X-Achse",
                                    description = "X-Achse",
                                    precision = 3,
                                    default = 0.001)

class sfx_kinematic(bpy.types.PropertyGroup):
    ''' Defines sfx_kinematic'''
    bl_idname = "sfx_kinematic"

    X_Achse : bpy.props.FloatProperty(name = "X-Achse",
                                    description = "X-Achse",
                                    precision = 3,
                                    default = 0.001)

class helper_demux(bpy.types.PropertyGroup):
    ''' Defines sfx_helper'''
    bl_idname = "sfx_helper"

    operator_started : bpy.props.BoolProperty(name = "Demux Operator Started",
                                    description = "Demux Operator Started",
                                    default = False)
    operator_running_modal: bpy.props.BoolProperty(name = "Demux Operator Running Modal",
                                    description = "Demux Operator Running Modal",
                                    default = False)
        
    TickTime_prop : bpy.props.FloatProperty(default=0.0)

class sfx_actuator(bpy.types.PropertyGroup):
    ''' Defines sfx_actuator'''
    bl_idname = "sfx_actuator"

    X_Achse : bpy.props.FloatProperty(name = "X-Achse",
                                    description = "X-Achse",
                                    precision = 3,
                                    default = 0.001)

class clock(bpy.types.PropertyGroup):
    ''' Defines sfx_clock'''
    bl_idname = "sfx_clock"

    operator_started : bpy.props.BoolProperty(name = "Operator Started",
                                    description = "Operator Started",
                                    default = False)
    operator_running_modal: bpy.props.BoolProperty(name = "Operator Running Modal",
                                    description = "Operator Running Modal",
                                    default = False)
    date :bpy.props.StringProperty(name='Date',
                                description='Date',
                                default = 'Sun Jun 20 23:21:05 1993')

    TickTime_prop: bpy.props.FloatProperty(name = "Tick Time",
                                    description ="Sanity Check message round trip Time",
                                    default=0.1,
                                    precision=2)

class sfx(bpy.types.PropertyGroup):
    ''' Defines sfx '''
    bl_idname = "SFX"

    clocks     ={}
    sensors    ={}
    cues       ={}
    kinematics ={}
    helpers    ={}
    actuators  ={}

