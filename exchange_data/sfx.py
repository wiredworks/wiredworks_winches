import bpy

class sfx_sensor(bpy.types.PropertyGroup):
    ''' Defines sfx_sensor'''
    bl_idname = "sfx_sensor"

    X_Achse : bpy.props.FloatProperty(name = "X-Achse",
                                    description = "X-Achse",
                                    precision = 3,
                                    default = 0.001)

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

class sfx_helper(bpy.types.PropertyGroup):
    ''' Defines sfx_helper'''
    bl_idname = "sfx_helper"

    X_Achse : bpy.props.FloatProperty(name = "X-Achse",
                                    description = "X-Achse",
                                    precision = 3,
                                    default = 0.001)

class sfx_actuator(bpy.types.PropertyGroup):
    ''' Defines sfx_actuator'''
    bl_idname = "sfx_actuator"

    X_Achse : bpy.props.FloatProperty(name = "X-Achse",
                                    description = "X-Achse",
                                    precision = 3,
                                    default = 0.001)

class sfx_clock(bpy.types.PropertyGroup):
    ''' Defines sfx_clock'''
    bl_idname = "sfx_clock"

    # def update_value(self,context):
    #     self.update()
    #     pass

    operator_started : bpy.props.BoolProperty(name = "Operator Started",
                                    description = "Operator Started",
                                    default = False)
    operator_running_modal: bpy.props.BoolProperty(name = "Operator Running Modal",
                                    description = "Operator Running Modal",
                                    default = False)
    operator_restart : bpy.props.BoolProperty(name = "Operator Started",
                                    description = "Operator Started",
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

