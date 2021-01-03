import bpy
import json

from .. Node.SFX_Action_Props import SFX_Action_Props

from .. exchange_data.sfx import sfx


def write_some_data(context, filepath, action, description):
    f = open(filepath, 'w', encoding='utf-8')
    Data = (str(action.id)       +';'+     # 0
           action.name           +';'+     # 1
           str(action.saved)     +';'+     # 2
           action.path           +';'+     # 3
           description           +';'+     # 4
           str(action.signed)    +';'+     # 5
           str(action.maxAcc)    +';'+     # 6
           str(action.maxVel)    +';'+     # 7
           str(action.minPos)    +';'+     # 8
           str(action.maxPos)    +';'+     # 9                                                  
           str(action.length)    +';'+     # 10
           str(action.duration)  +';'+     # 11
           action.Pos_SM         +';'+     # 12
           action.Jrk            +';'+     # 13
           action.Acc            +';'+     # 14
           action.Vel            +';'+     # 15
           action.Pos            +';'+     # 16
           action.VP             +';')     # 17
  
    f.write(json.dumps(Data))
    f.close()

    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper

from bpy.types import Operator


class SFX_Save_Action(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "sfx.save_action"
    bl_label = "Export Some Data"

    # ExportHelper mixin class uses this
    filename_ext = ".sfxact"

    filter_glob: bpy.props.StringProperty(
        default="*.sfxact",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    #action_index: bpy.props.IntProperty(name = 'Action Index',
    #                                        description = 'Action Index',
    #                                        default = 0)

    description : bpy.props.StringProperty(name = 'Description',
                                            description = 'Describe the Charactristics of that Action',
                                            default = 'Default Description')

    #sfx_action : bpy.props.PointerProperty(type = SFX_Action_Props)

    def execute(self, context):
        MotherNode = context.active_node
        if MotherNode.sfx_type == 'Actuator':
            index = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index
            action = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions[index]
            #self.description = action.name
        elif MotherNode.sfx_type == 'Cue':
            index = sfx.cues[MotherNode.name].Actuator_props.SFX_actions_index
            action = sfx.cues[MotherNode.name].Actuator_props.SFX_actions[index] 
        action.saved = True
        action.description = self.description
        return write_some_data(context, self.filepath, action, self.description)

