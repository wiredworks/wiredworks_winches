import bpy

from .... exchange_data.sfx import sfx
from .... exchange_data.sfx import SFX_Actuators_Basic_Inset
from .. SFX_Helpers_Base_Data import helper_base

class helper_adder(bpy.types.PropertyGroup,helper_base):
    ''' Defines sfx_adder'''
    bl_idname = "sfx_adder"

    Actuator_basic_props : bpy.props.PointerProperty(type =SFX_Actuators_Basic_Inset)

    expand_Actuator_basic_data : bpy.props.BoolProperty(name = "Expand Basic Data",
                                    description = "Expand Basic Data",
                                    default = False)