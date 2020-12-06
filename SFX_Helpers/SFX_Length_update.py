import bpy
import json

from ..exchange_data.sfx import sfx

class SFX_OT_Length_update(bpy.types.Operator):
    bl_idname = "sfx.length_update"
    bl_label = "Update Max Pos based on Length"

    def invoke(self, context, event):
        if (abs((sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop - \
            sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop) - \
            sfx.actuators[context.active_node.name].Actuator_basic_props.DigTwin_basic_props.length) > 0.001):

            sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMax_prop = \
            sfx.actuators[context.active_node.name].Actuator_basic_props.Actuator_props.simple_actuator_HardMin_prop + \
            sfx.actuators[context.active_node.name].Actuator_basic_props.DigTwin_basic_props.length    
        return {"FINISHED"}