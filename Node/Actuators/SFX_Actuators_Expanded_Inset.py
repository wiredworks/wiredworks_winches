import bpy

import bpy
from bpy.types import UIList
from bpy_extras.io_utils import ImportHelper
import os

class SFX_Actuators_Expanded_Inset(bpy.types.PropertyGroup):
    '''Defines Physical Props of an Actuator'''
    bl_idname = "SFX_simple_Actuator_Inset"
    
    def update_conf(self,context):
        pass

    simple_actuator_HardMax_prop: bpy.props.FloatProperty(name = "Hard Max",
                                                                description ="Maximum Position set in the PLC",
                                                                default=5.0,
                                                                precision=3,
                                                                update = update_conf)
    simple_actuator_HardMin_prop: bpy.props.FloatProperty(name = "Hard Min",
                                                                description ="Minimum Position set in the PLC",
                                                                default=0.0,
                                                                precision=3,
                                                                update = update_conf)
    simple_actuator_VelMax_prop: bpy.props.FloatProperty(name = "Vel Max",
                                                                description ="Maximum Velocity set in Program",
                                                                default=5.0,
                                                                precision=3,
                                                                update = update_conf)
    simple_actuator_AccMax_prop: bpy.props.FloatProperty(name = "Acc Max",
                                                                description ="Maximum Acceleration",
                                                                default=5.0,
                                                                precision=3,
                                                                update = update_conf)

    # SFX_actions                 : bpy.props.CollectionProperty(type=SFX_ListProps)
    # SFX_actions_index           : bpy.props.IntProperty()

    # MotherNode_name : bpy.props.StringProperty(name = 'Mother Node Name',
    #                             description = 'Mother Node Name',
    #                             default = '')
    
    simple_actuator_confirm: bpy.props.BoolProperty(name = "Confirm Data",
                                    description = " Set to confirm Data",
                                    default = False)
    simple_actuator_confirmed: bpy.props.BoolProperty(name = "Confirmed Data",
                                    description = " Set if Data is confirmed",
                                    default = False)

    def update_confirm(self):
       #self.simple_actuator_confirm = False 
       self.simple_actuator_confirmed = False
       pass

    def drawActuatorSetup(self, context, layout):

        scn = bpy.context.scene

        boxA = layout.box()
        row = boxA.row()
        row.label(text='Action Setup') 
        box1 = boxA.split(factor = 0.8)
        col = box1.column(align = True)
        try:
            current_item = (scn.SFX[scn.SFX_index].name)
        except IndexError:
            current_item = ""
        col = col.split(factor = 0.95)
        rows = 4
        col.template_list("SFX_UL_List", "", scn, "SFX", scn, "SFX_index", rows=rows)
        #col.label(text = 'mist')
        col = col.column(align=True)
        col.operator("sfx.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("sfx.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = col.row()        
        col = boxA.column(align=True)
        rowsub = col.row(align=True)
        rowsub.operator("sfx.list_action", icon='ZOOM_IN', text="Add Action").action = 'ADD'
        rowsub.operator("sfx.list_action", icon='ZOOM_OUT', text="Remove Action").action = 'REMOVE'
        rowsub.operator("sfx.list_action", icon='FILE_TICK', text="Save Action").action = 'SAVE'
        row = col.row()
        col = row.column(align=True)
        col.operator("sfx.clear_list", icon="X")        
        # row = col.row(align = True)
        # row.label(text ="Active Action: {}".format(current_item))

        col1= box1.column()
        row = col1.row() 
        row.label(text = 'Min Pos')
        row.prop(self,'simple_actuator_HardMin_prop', text='')
        row = col1.row()
        row.label(text = 'Max Pos')
        row.prop(self,'simple_actuator_HardMax_prop', text='')
        row = col1.row()
        row.label(text = 'Max Vel')
        row.prop(self,'simple_actuator_VelMax_prop', text='')
        row= col1.row()
        row.label(text = 'Max Acc')
        row.prop(self,'simple_actuator_AccMax_prop', text='')
        row= col1.row()
        row = row.split(factor = 0.7)
        col= row.column()
        col.separator()
        col = row.column()
        col.prop(self,'simple_actuator_confirm', text='')
        col = row.column()
        col.prop(self,'simple_actuator_confirmed', text='')



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

        scn = context.scene
        idx = scn.SFX_index

        try:
            item = scn.SFX[idx]
        except IndexError:
            pass

        else:
            if self.action == 'DOWN' and idx < len(scn.SFX) - 1:
                item_next = scn.SFX[idx+1].name
                scn.SFX_index += 1
                info = 'Item %d selected' % (scn.SFX_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.SFX[idx-1].name
                scn.SFX_index -= 1
                info = 'Item %d selected' % (scn.SFX_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item %s removed from list' % (scn.SFX[scn.SFX_index].name)
                scn.SFX_index -= 1
                self.report({'INFO'}, info)
                scn.SFX.remove(idx)

        if self.action == 'ADD':
            bpy.ops.sfx.select_operator('INVOKE_DEFAULT')            
            scn.SFX_index = (len(scn.SFX)) # (len(scn.custom)-1)

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
        scn = context.scene
        
        # get the folder
        folder = (os.path.dirname(self.filepath))

        # iterate through the selected files
        for i in self.files:
            # generate full path to file
            path_to_file = (os.path.join(folder, i.name))   
            item = scn.SFX.add()
            item.id = len(scn.SFX)
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
        scn = context.scene
        lst = scn.SFX
        current_index = scn.SFX_index

        if len(lst) > 0:
             # reverse range to remove last item first
            for i in range(len(lst)-1,-1,-1):
                scn.SFX.remove(i)
            self.report({'INFO'}, "All items removed")

        else:
            self.report({'INFO'}, "Nothing to remove")   

        return{'FINISHED'}

class SFX_OT_print_List(bpy.types.Operator):
    bl_idname = "sfx.print_list"
    bl_label = "Print Name, ID and Path to Console"
    bl_description = "Print all items to the Console"

    def execute(self, context):
        scn = context.scene
        for i in scn.SFX:
            print ("Action-File:", i.name, "ID:", i.id, "Path:", i.path)
        
        return{'FINISHED'}

class SFX_OT_print_Item(bpy.types.Operator):
    bl_idname = "sfx.print_item"
    bl_label = "Print Active Item to Console"
    bl_description = "Print Active Selection"

    def execute(self, context):
        scn = context.scene
        print (scn.SFX[scn.SFX_index].name)
        
        return{'FINISHED'}







    
