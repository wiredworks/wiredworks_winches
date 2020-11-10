import bpy

from ....exchange_data.sfx import sfx
from ....exchange_data.sfx import SFX_Actuators_Expanded_Inset

from .. SFX_Cues_Base_Data import cue_base

class cue_simple(bpy.types.PropertyGroup,cue_base):
    ''' Defines sfx_cue'''
    bl_idname = "sfx_cue"

    play_state_items = (('Play','Play','Play','PLAY',1),
                        ('Pause','Pause','Pause','PAUSE',2),
                        ('SpeedUp','Speed Up','Speeding Up to Play Speed','FF',3),
                        ('Slowing','Slowing','Slowing Down from Play Speed','REW',4),
                        ('Reverse','Reverse','Playing Reverse','PLAY_REVERSE',5),
                        ('GoTo1','Go To 1','Going To Start Position','FRAME_PREV',6))
        
    max_Vel : bpy.props.FloatProperty(name='Max Vel',
                                      description='Max Vel of Cue',
                                      default = 0.0)
    max_Acc : bpy.props.FloatProperty(name='Max Acc',
                                      description='Max Acc of Cue',
                                      default = 0.0)
    duration : bpy.props.FloatProperty(name='Duration',
                                      description='Duration of Cue',
                                      default = 0.0)
    play_head_percent : bpy.props.FloatProperty(name='Play Head',
                                      description='Play Head',
                                      default = 0.0,
                                      soft_max = 100.0,
                                      soft_min = -100.0)
    play_head : bpy.props.FloatProperty(name='Play Head',
                                      description='Play Head',
                                      default = 0.0)
    play_state : bpy.props.EnumProperty(name='Play State',
                                       description = 'Play State of Cue',
                                       items = play_state_items,
                                       default = 'Pause')
    cue_min_pos: bpy.props.FloatProperty(name='Cue Min Pos',
                                      description='Cue Min Pos',
                                      default = 0.0) 
    cue_max_pos: bpy.props.FloatProperty(name='Cue Max Pos',
                                      description='Cue Max Pos',
                                      default = 0.0)
    cue_set_pos: bpy.props.FloatProperty(name='Cue Set Pos',
                                      description='Cue Set Pos',
                                      default = 0.0)
    cue_act_pos: bpy.props.FloatProperty(name='Cue Actual Pos',
                                      description='Cue Actual Pos',
                                      default = 0.0)
    cue_act_speed: bpy.props.FloatProperty(name='Cue Actual Speed',
                                      description='Cue Actual Speed',
                                      default = 0.0)
    cue_target_speed: bpy.props.FloatProperty(name='Cue Target Speed',
                                      description='Cue Target Speed',
                                      default = 0.0)                                                                           
    cue_diff_pos: bpy.props.FloatProperty(name='Cue Dif Pos',
                                      description='Difference Set Act Pos',
                                      default = 0.0)
    cue_diff_speed: bpy.props.FloatProperty(name='Cue Dif Speed',
                                      description='Difference Target Act Speed',
                                      default = 0.0) 
    confirm : bpy.props.BoolProperty(name = "Confirm Cue",
                                    description = "Confirm Cue",
                                    default = False)
    confirmed: bpy.props.BoolProperty(name = "Confiremd Cue",
                                    description = "The Confirmed Cue can be executed",
                                    default = False)
    ActConfirm: bpy.props.BoolProperty(name = "Actuator Confiremd",
                                    description = "The connected Actuator has confirmed properties",
                                    default = False)
    ActConfirmed: bpy.props.BoolProperty(name = "Actuator Confiremd",
                                    description = "The connected Actuator has confirmed properties",
                                    default = False)
    toTime : bpy.props.BoolProperty(name = "To Vel/Time",
                                    description = "To Vel over Time",
                                    default = False)                                            
    toTime_executed : bpy.props.BoolProperty(name = "To Vel/Time",
                                    description = "To Vel over Time",
                                    default = False)
    operator_edit : bpy.props.BoolProperty(name = "Operator Edit",
                                    description = "Operator Edit",
                                    default = False)
    operator_editing : bpy.props.BoolProperty(name = "Operator Edit",
                                    description = "Operator Edit",
                                    default = False)
    expand_Actuator_props : bpy.props.BoolProperty(name = "Expand Basic Data",
                                    description = "Expand Basic Data",
                                    default = False)
    length : bpy.props.FloatProperty(name = 'Length',
                                     description = 'Length of Actuator',
                                     default = 0)

    Actuator_props : bpy.props.PointerProperty(type = SFX_Actuators_Expanded_Inset)


class sfx_kinematic(bpy.types.PropertyGroup):
    ''' Defines sfx_kinematic'''
    bl_idname = "sfx_kinematic"

    X_Achse : bpy.props.FloatProperty(name = "X-Achse",
                                    description = "X-Achse",
                                    precision = 3,
                                    default = 0.001)