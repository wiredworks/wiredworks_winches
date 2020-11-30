import bpy

from .. Node.SFX_Action_Props import SFX_Action_Props

from .. exchange_data.sfx import sfx


def write_some_data(context, filepath, action):
    print("running write_some_data...")
    f = open(filepath, 'w', encoding='utf-8')
    Data = (str(action.id)+';'+
           action.name+';'+
           str(action.minPos)+';'+
           str(action.maxPos)+';'+
           str(action.maxAcc)+';'+
           str(action.maxVel)+';'+
           str(action.length)+';'+
           action.Jrk+';'+
           action.Acc+';'+
           action.Vel+';'+
           action.Pos)   
    f.write(Data)
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

    action_index: bpy.props.IntProperty(name = 'Action Index',
                                            description = 'Action Index',
                                            default = 0)

    sfx_action : bpy.props.PointerProperty(type = SFX_Action_Props)



    def execute(self, context):
        MotherNode = context.active_node
        action = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions[self.action_index]
        return write_some_data(context, self.filepath, action)

