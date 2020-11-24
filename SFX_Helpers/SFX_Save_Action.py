import bpy

from .. Node.SFX_Action_Props import SFX_Action_Props

from .. exchange_data.sfx import sfx


def write_some_data(context, filepath, use_some_setting):
    print("running write_some_data...")
    f = open(filepath, 'w', encoding='utf-8')
    f.write("Hello World")
    f.close()

    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class SFX_Save_Action(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "sfx.save_action"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Some Data"

    # ExportHelper mixin class uses this
    filename_ext = ".sfxact"

    filter_glob: StringProperty(
        default="*.sfxact",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    sfx_action : bpy.props.PointerProperty(type = SFX_Action_Props)

    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )

    type: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ('OPT_A', "First Option", "Description one"),
            ('OPT_B', "Second Option", "Description two"),
        ),
        default='OPT_A',
    )

    def execute(self, context):
        MotherNode = context.active_node
        action = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions
        return write_some_data(context, self.filepath, action)

