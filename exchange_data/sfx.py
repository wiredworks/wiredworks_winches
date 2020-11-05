import bpy

from .. Node.Sensors.Joystick.SFX_Joystick_Inset import SFX_Joystick_Inset


from .. Node.Clock.SFX_Clock_Data import clock

from .. Node.Actuators.SFX_Actuators_Base_Data import actuator_base
from .. Node.Actuators.SFX_Actuators_Basic_Inset import SFX_Actuators_Basic_Inset
from .. Node.Actuators.SFX_Actuators_Expanded_Inset import SFX_Actuators_Expanded_Inset
from .. Node.Actuators.SFX_Digtwin_Basic_Inset import SFX_Digtwin_Basic_Inset
from .. Node.Actuators.SFX_Digtwin_Expanded_Inset import SFX_Digtwin_Expanded_Inset

from .. Node.Cues.SFX_Cues_Base_Data import cue_base

from .. Node.Helpers.SFX_Helpers_Base_Data import helper_base

from .. Node.Kinematics.SFX_Kinematics_Base_Data import kinematic_base

from .. Node.Sensors.SFX_Sensors_Base_Data import sensor_base
from .. Node.Sensors.Joystick.SFX_Joystick_Data import sensor_joystick
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

