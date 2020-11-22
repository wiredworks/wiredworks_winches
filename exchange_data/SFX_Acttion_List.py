import bpy

import bpy
from bpy.types import UIList
from bpy_extras.io_utils import ImportHelper
import os

from .sfx import sfx

class SFX_OT_list_actions(bpy.types.Operator):
    bl_idname = "sfx.list_action"
    bl_label = "List Action"

    action : bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", ""),
            ('SAVE', "Save", "")
        )
    )
    def invoke(self, context, event):
        MotherNode = context.active_node
        sfx_actions   = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions

        try:
            item = sfx_actions[sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index]
        except IndexError:
            pass
        else:
            if (self.action == 'DOWN' and \
                sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index < len(sfx_actions)):
                item_next = sfx_actions[sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index+1].name
                sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index +=1
                info = 'Item %d selected' % (sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index + 1)
                self.report({'INFO'}, info)

            elif (self.action == 'UP' and \
                sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index>= 1):
                item_prev = sfx_actions[sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index-1].name
                sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index -= 1
                info = 'Item %d selected' % (sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                sfx_actions.remove(sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index)
                info = 'Item %s removed from list' % (sfx_actions[sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index].name)
                sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index -= 1
                self.report({'INFO'}, info)

        if self.action == 'ADD':
            bpy.ops.sfx.select_operator('INVOKE_DEFAULT')            
            sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index = (len(sfx_actions))

        if self.action == 'SAVE':
            bpy.ops.sfx.save_list('INVOKE_DEFAULT')          

        return {"FINISHED"}

class SFX_OT_save_List(bpy.types.Operator):
    bl_idname = "sfx.save_list"
    bl_label = "Save Action"
    bl_description = "Save Action"

    def execute(self, context):
        print('Not yet implemented')
        
        return{'FINISHED'}


class SFX_OT_SelectOperator(bpy.types.Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "sfx.select_operator"
    bl_label = "Action Selector"
    bl_options = {'PRESET', 'UNDO'}

    # ImportHelper mixin class uses this
    filename_ext = ".sfxact"

    filter_glob : bpy.props.StringProperty(
            default="*.sfxact",
            options={'HIDDEN'},
            )

    # Selected files
    files : bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)

    def execute(self, context):
        MotherNode = context.active_node
        sfx_actions       = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions
        
        # get the folder
        folder = (os.path.dirname(self.filepath))

        # iterate through the selected files
        for i in self.files:
            # generate full path to file
            path_to_file = (os.path.join(folder, i.name))   
            item = sfx_actions.add()
            item.id = len(sfx_actions)
            item.name = i.name # assign name of selected object
            item.path = path_to_file
        
        self.report({'INFO'}, "Files Added")
        return {'FINISHED'}
    
# -------------------------------------------------------------------
# draw
# -------------------------------------------------------------------

# custom list
class SFX_UL_List(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor = 0.7)
        split.prop(item, "name", text="", emboss=False, translate=False, icon='FILE_BLEND')
        split.label(text="Index: %d" % (index))

    def invoke(self, context, event):
        pass

class SFX_OT_clear_List(bpy.types.Operator):
    bl_idname = "sfx.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items in the list"

    def execute(self, context):
        MotherNode = context.active_node
        sfx_actions       = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions

        if len(sfx_actions) > 0:
             # reverse range to remove last item first
            for i in range(len(sfx_actions)-1,-1,-1):
                sfx_actions.remove(i)
            self.report({'INFO'}, "All items removed")

        else:
            self.report({'INFO'}, "Nothing to remove")   

        return{'FINISHED'}

class SFX_OT_print_List(bpy.types.Operator):
    bl_idname = "sfx.print_list"
    bl_label = "Print Name, ID and Path to Console"
    bl_description = "Print all items to the Console"

    def execute(self, context):
        MotherNode = context.active_node
        sfx_actions       = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions

        for i in sfx_actions:
            print ("Action-File:", i.name, "ID:", i.id, "Path:", i.path)
        
        return{'FINISHED'}

class SFX_OT_print_Item(bpy.types.Operator):
    bl_idname = "sfx.print_item"
    bl_label = "Print Active Item to Console"
    bl_description = "Print Active Selection"

    def execute(self, context):
        MotherNode = context.active_node
        sfx_actions       = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions
        sfx_actions_index = sfx.actuators[MotherNode.name].Actuator_basic_props.Actuator_props.SFX_actions_index

        print (sfx_actions[sfx_actions_index].name)
        
        return{'FINISHED'}