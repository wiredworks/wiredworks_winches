import bpy

from .. Node.Actuators.SFX_Actuators_Basic_Inset import SFX_Actuators_Basic_Inset
from .. Node.Actuators.SFX_Actuators_Expanded_Inset import SFX_Actuators_Expanded_Inset
from .. Node.Actuators.SFX_Digtwin_Basic_Inset import SFX_Digtwin_Basic_Inset
from .. Node.Actuators.SFX_Digtwin_Expanded_Inset import SFX_Digtwin_Expanded_Inset

from .. Node.Sensors.Joystick.SFX_Joystick_Inset import SFX_Joystick_Inset 

class sfx(bpy.types.PropertyGroup):
    ''' Defines sfx '''
    bl_idname = "SFX"

    clocks     ={}
    sensors    ={}
    cues       ={}
    kinematics ={}
    helpers    ={}
    actuators  ={}

