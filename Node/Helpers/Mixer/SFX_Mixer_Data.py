import bpy

from ....exchange_data.sfx import SFX_Actuators_Basic_Inset

from ..SFX_Helpers_Base_Data import helper_base

class helper_mixer(bpy.types.PropertyGroup,helper_base):
    ''' Defines sfx_mixer'''
    bl_idname = "sfx_mixer"

    Actuator_basic_props : bpy.props.PointerProperty(type =SFX_Actuators_Basic_Inset)

    expand_Actuator_basic_data : bpy.props.BoolProperty(name = "Expand Basic Data",
                                    description = "Expand Basic Data",
                                    default = False)

    factor : bpy.props.FloatProperty(name='Factor',
                                      description='Factor',
                                      default = 50.0,
                                      soft_max = 100.0,
                                      soft_min = 0.0)